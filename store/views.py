from Brand.models import Brand
from category.models import Category
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.contrib import messages
from products.models import *
from orders.models import *
from orders.forms import *
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from Brand.models import *
from accounts.forms import *
from django.core.paginator import Paginator 
from datetime import date
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.

#----------------Home Page--------------#

@never_cache
def home(request):
    ctgy = Category.objects.filter(is_active=True)
    prdts = ProductAttribute.objects.filter(is_active = True, category_name__is_active=True).order_by('-id')[:4]
    context = {
        "ctgy":ctgy,
        "prdts": prdts
    }
    return render(request, 'home.html',context)

 
#-----------------------Product Page--------------------------#

@never_cache 
def store(request):
    ctgy = Category.objects.filter(is_active=True)
    prdts = ProductAttribute.objects.filter(is_active = True,category_name__is_active=True, productrelate__is_available=True).distinct()
    clr = Products.objects.distinct().values('color__color','color__id','color__color_code','color__slug')
    ram = Products.objects.distinct().values('ram__ram','ram__id','ram__slug')
    brnd = Brand.objects.filter(is_available=True)
    paginator = Paginator(prdts, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        "prdts": paged_products,
        "ctgy":ctgy,
        "clr":clr,
        "ram":ram,
        "brnd":brnd,
    }
    return render(request, 'store/shop.html', context)

@never_cache
def by_category(request,category_slug):
    categories = Category.objects.get(slug=category_slug)
    ctgy = Category.objects.filter(is_active=True)
    brnd = Brand.objects.filter(is_available=True)
    prdts = ProductAttribute.objects.filter(category_name = categories, is_active = True, productrelate__is_available=True).distinct()
    clr = Products.objects.distinct().values('color__color','color__id','color__color_code','color__slug').distinct()
    ram = Products.objects.distinct().values('ram__ram','ram__id','ram__slug').distinct()
    paginator = Paginator(prdts, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productCount = prdts.count()
    context = {
        "prdts": paged_products,
        "productCount": productCount,
        "clr":clr,
        "ram":ram,
        "brnd":brnd,
        "ctgy":ctgy,
    }
    return render(request, 'store/shop.html', context)


def productDetail(request,category_slug, product_slug):
    prdts = ProductAttribute.objects.get(slug=product_slug)
    relprdts = ProductAttribute.objects.filter(category_name=prdts.category_name).exclude(product_name=prdts)[:4]
    ram = Products.objects.filter(product_name=prdts, is_available=True).values('id','ram__id','ram__ram','color__id','price','stock').distinct()
    colors = Products.objects.filter(product_name=prdts, is_available=True).values('color__id','color__color','color__color_code').distinct()
    context = {
         'prdts':prdts,
         'ram':ram, 
         'colors':colors,
         'relprdts':relprdts,
    }
    return render(request, 'store/Productview.html', context)
    

#----------------------------Cart-------------------------------#

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        print('session created')
    return cart

def add_to_cart(request):
    current_user=request.user
    product = Products.objects.get(id=request.GET['id'])
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id =_cart_id(request))
        cart.save()
    print(product.stock)
    if current_user.is_authenticated:
        if product.stock == 0:
            return JsonResponse({'status':"Out of stock"})
        else:
            if CartItem.objects.filter(user=request.user,cart_product=product): 
                return JsonResponse({'status':"Don't Add"})
            else:
                is_cart_item_exists = CartItem.objects.filter(cart_product__price=product.price, user=current_user).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.get(cart_product=product, user=current_user)
                    cart_item.quantity += int(request.GET['qty'])
                    cart_item.save()
                else:
                    cart_item = CartItem.objects.create(
                        cart_product = product,
                        quantity = request.GET['qty'],
                        user = current_user,
                    )
    else:
        if product.stock != 0:
            if CartItem.objects.filter(cart=cart,cart_product=product): 
                return JsonResponse({'status':"Don't Add"})
            else: 
                is_cart_item_exists = CartItem.objects.filter(cart_product__price=product.price, cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.get(cart_product=product.id, cart=cart.id)
                    cart_item.quantity += int(request.GET['qty'])
                    cart_item.save()
                    print(cart_item.quantity)
                else:
                    cart_item = CartItem.objects.create(
                        cart_product=product,
                        quantity = request.GET['qty'],
                        cart = cart,
                    )
                    cart_item.save()
        else:
            return JsonResponse({'status':"Out of stock"})
    print('last')
    return JsonResponse({'single_product':'success'})

def add_quantity(request,id):
    current_user=request.user
    product = Products.objects.get(id=id)
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id =_cart_id(request))
        cart.save()
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(cart_product__price=product.price, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(cart_product=product, user=current_user)
            cart_item.quantity += 1
            cart_item.save()
    else:
        is_cart_item_exists = CartItem.objects.filter(cart_product__price=product.price, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(cart_product=product.id, cart=cart.id)
            cart_item.quantity += 1 
            cart_item.save()
    return redirect('cart')

def cart(request):
    current_user=request.user
    context={}
    try:
        if current_user.is_authenticated:
            cart_items = CartItem.objects.filter(user=current_user, cart_product__is_available=True, is_active=True).order_by('-id')
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, cart_product__is_available=True, is_active=True).order_by('-id')
        total_amount = 0
        for cart_item in cart_items:
            poff_price = round(cart_item.cart_product.price - cart_item.cart_product.price * cart_item.cart_product.product_name.product_offer /100)
            coff_price = round(cart_item.cart_product.price - cart_item.cart_product.price * cart_item.cart_product.product_name.category_name.category_offer /100)
            if poff_price <= coff_price:
                total_amount += (poff_price * cart_item.quantity)
            elif poff_price >= coff_price:
                total_amount += (coff_price * cart_item.quantity)
        tax = round((6 * float(total_amount))/100)
        grand_total = total_amount + tax
        context = {
            'cart_items':cart_items,
            'total_amount':total_amount,
            'tax':tax,
            'grand_total':grand_total,
        }
    except:
        pass
    return render(request, 'Orders/Cart.html', context)

def delete_cartitem(request, id):
    current_user=request.user 
    product = Products.objects.get(id=id)
    if current_user.is_authenticated:
        cart_item=CartItem.objects.filter(user=current_user, cart_product=product)
    else:
        cart = Cart.objects.get(cart_id=request.session.session_key)
        cart_item = CartItem.objects.get(cart_product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

def remove_quantity(request,id):
    current_user=request.user
    product = Products.objects.get(id=id)
    try:
        if current_user.is_authenticated:
            cart_item = CartItem.objects.get(cart_product=product, user=current_user)
        else:
            print('session')
            cart = Cart.objects.get(cart_id =_cart_id(request))
            print(cart,'cart kaynn')
            cart_item = CartItem.objects.get(cart_product=product, cart=cart)
            print(cart_item, 'cart_item kaynn')

        print('if lek vanne')
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            print('quantity kurach')
            cart_item.save()
            print('saved')
        else:
            print('else is working')
            cart_item.delete()
            print('delete')
    except:
        pass
    return redirect('cart')

#---------------------Order--------------------------#

@never_cache
@login_required(login_url='login')
def checkout(request):
    cart_count = 0
    cart_count = CartItem.objects.all().filter(user=request.user, cart_product__is_available=True).count()
    if cart_count: 
        if request.method == "POST":
            code = request.POST.get('code')
            try:
                today = date.today()
                value = Coupon.objects.get(code = code)
                if not value.valid_at >= today:
                    return JsonResponse({"Status" : "Coupon is not valid currently"})
                try:
                    test = Couponuser.objects.filter(user = request.user).exists()
                    if test:
                        current1 = Couponuser.objects.get(user = request.user)
                        if current1.coupon_code != code:
                            current1.coupon_code = code
                            current1.coupon_value = value.offer_value
                            current1.coupon_model = value
                            current1.save()
                            return JsonResponse({"Status" : "Coupon changed"})
                        return JsonResponse({"Status" : "Coupon already Entered"})
                    Couponuser.objects.create(
                            user = request.user,
                            coupon_model = value,
                            coupon_code = code,
                            coupon_value = value.offer_value   
                        )
                except Exception as e:
                    pass
                return JsonResponse({"Status" : "Coupon Activated"})
            except:
                return JsonResponse({"Status" : "Invalid coupon"})
        cpns = Coupon.objects.filter(active=True)
        mycart = CartItem.objects.filter(user=request.user,  cart_product__is_available=True)
        ads = useraddress.objects.filter(user_id = request.user)
        account = Account.objects.filter(email = request.user)
        total_amount = 0
        for cart_item in mycart:
            poff_price = round(cart_item.cart_product.price - cart_item.cart_product.price * cart_item.cart_product.product_name.product_offer /100)
            coff_price = round(cart_item.cart_product.price - cart_item.cart_product.price * cart_item.cart_product.product_name.category_name.category_offer /100)
            if poff_price <= coff_price:
                total_amount += (poff_price * cart_item.quantity)
            elif poff_price >= coff_price:
                total_amount += (coff_price * cart_item.quantity)
        tax = round((2 * float(total_amount))/100)
        grand_total = total_amount + tax
        coup_perc = 0
        try: 
            coup_value = Couponuser.objects.get(user = request.user, used=False)
            coupon_status = True
            coup_perc = coup_value.coupon_value
            coupon_codes = coup_value.coupon_code
        except Exception as e:
            coupon_codes = None
            coupon_status = False
            coup_perc = 0

        final_total = total_amount + tax

        grand_total  = int(grand_total - grand_total * int(coup_perc)/100)
        coup_red = final_total - grand_total

        context = {
            'ads':ads,
            'account':account,
            'mycart':mycart,
            'total_amount':total_amount,
            'tax':tax,
            'grand_total':grand_total,
            'coupon_status' : coupon_status,
            'coupon_codes' : coupon_codes,
            'coup_perc' : coup_perc,
            'coup_red':coup_red,
            'cpns':cpns
        }
        return render(request, 'Orders/checkout.html', context)
    else:
        return redirect('home')

def AddOrderAddress(request):
    if request.method == "POST":
        form = AddAddressform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('checkout')
        else:
            print(form.errors.as_data())
            messages.error(request,"you are a FAILURE!!")
    data = Account.objects.filter(email = request.user)
    context = {
        'data' : data
    }
    return render(request, 'Orders/OrderAddress.html', context)

@never_cache
def SelectedAddress(request, id):
    cadd = useraddress.objects.get(id=id)
    context = {
        'cadd': cadd
    }
    return render(request, 'Orders/checkout2.html', context)

@never_cache
def SelectedCoupon(request, id):
    cpn = Coupon.objects.get(id=id)
    context = {
        'cpn': cpn
    }
    return render(request, 'Orders/cpn.html', context)



@login_required(login_url='login')
def razorpaycheck(request):
    mycart = CartItem.objects.filter(user=request.user,  cart_product__is_available=True)
    total_amount = 0
    for cart_item in mycart:
        total_amount += (cart_item.cart_product.price * cart_item.quantity)
    tax = round((2 * float(total_amount))/100)
    grand_total = total_amount + tax
    context = {
        'grand_total':grand_total,
    }
    return JsonResponse(context)

@never_cache
def OrderConfirmed(request):
    return render(request, 'Orders/confirmed.html')

#------------------------Filter-----------------#



#--------------------------Search View-----------------------------#

def Search(request):
    ctgy = Category.objects.filter(is_active=True)
    clr = Products.objects.distinct().values('color__color','color__id','color__color_code','color__slug')
    ram = Products.objects.distinct().values('ram__ram','ram__id','ram__slug')
    brnd = Brand.objects.filter(is_available=True)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            prdts = ProductAttribute.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword)
                |Q(brand_name__brand_name__icontains=keyword)|Q(category_name__category_name__icontains=keyword)|Q(productrelate__ram__ram__icontains=keyword)
                |Q(productrelate__color__color__icontains=keyword)).distinct()
        else:
            return redirect('products')
    context={
        'prdts':prdts,
        'ctgy':ctgy,
        'clr':clr,
        'ram':ram,
        'brnd':brnd,
    }
    return render(request,'store/shop.html', context)


@never_cache
@login_required(login_url=('login'))
def UserSettings(request):
    return render(request, 'store/settings.html')

@never_cache
@login_required(login_url=('login'))
def EditProfile(request):
    user = Account.objects.get(id=request.user.id)
    context={
        'user':user
    }
    return render(request, 'store/EditProfile.html', context)

@never_cache
@login_required(login_url=('login'))
def UpdateProfile(request,id):
    user = Account.objects.get(id=id)
    form = EditAccountForm(request.POST, instance = user)
    if form.is_valid():
        form.save()
        return redirect('settings')
    else:
         messages.error(request, 'Invalid Entry')
    context = {
        'user': user
    } 
    return render(request,'store/EditProfile.html', context)

@never_cache
@login_required(login_url=('login'))
def MyAddresses(request):
    ads = useraddress.objects.filter(user_id = request.user)
    account = Account.objects.get(email = request.user)
    context = {
        'ads':ads,
        'account':account,
    }
    return render(request, 'store/Address.html', context)


@never_cache
@login_required(login_url=('login'))
def AddnewAddress(request):
    if request.method == "POST":
        form = AddAddressform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addresses')
        else:
            print(form.errors.as_data())
            messages.error(request,"you are a FAILURE!!")
    data = Account.objects.filter(email = request.user)
    context = {
        'data' : data
    }
    return render(request, 'store/AddAddress.html', context)

@never_cache
@login_required(login_url='login')
def EditAddress(request, id):
    usid = useraddress.objects.get(id=id)
    context = {
        'usid':usid
    }
    return render(request, 'store/UpdateAddress.html', context)

@never_cache
@login_required(login_url='login')
def UpdateAddress(request, id):
    usid = useraddress.objects.get(id=id)
    form = UpdateAddressForm(request.POST, instance=usid)
    if form.is_valid():
        form.save()
        messages.success(request, 'Updated Successfully')
        return redirect('addresses')
    context = {
        'form':form
    }
    return render(request, 'store/UpdateAddress.html', context)

@never_cache
@login_required(login_url='login')
def deleteAddress(request, id):
    usid = useraddress.objects.get(id=id)
    usid.delete()
    return redirect('addresses')

def by_brand(request, brand_slug):
    brand = Brand.objects.get(slug=brand_slug)
    ctgy = Category.objects.filter(is_active=True)
    brnd = Brand.objects.filter(is_available=True)
    prdts = ProductAttribute.objects.filter(brand_name = brand, is_active = True, productrelate__is_available=True).distinct()
    clr = Products.objects.distinct().values('color__color','color__id','color__color_code','color__slug')
    ram = Products.objects.distinct().values('ram__ram','ram__id','ram__slug')
    paginator = Paginator(prdts, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productCount = prdts.count()
    context = {
        "prdts": paged_products,
        "productCount": productCount,
        "clr":clr,
        "ram":ram,
        "brnd":brnd,
        "ctgy":ctgy,
    }
    return render(request, 'store/shop.html', context)

def by_color(request, color_slug):
    color = Color.objects.get(slug=color_slug)
    ctgy = Category.objects.filter(is_active=True)
    brnd = Brand.objects.filter(is_available=True)
    prdts = ProductAttribute.objects.filter(productrelate__color = color, is_active = True, productrelate__is_available=True).distinct()
    clr = Products.objects.distinct().values('color__color','color__id','color__color_code','color__slug').distinct()
    ram = Products.objects.distinct().values('ram__ram','ram__id','ram__slug').distinct()
    paginator = Paginator(prdts, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productCount = prdts.count()
    for i in prdts:
        print(i.product_name)
    context = {
        "prdts": paged_products,
        "productCount": productCount,
        "clr":clr,
        "ram":ram,
        "brnd":brnd,
        "ctgy":ctgy,
    }
    return render(request, 'store/shop.html', context)

def by_ram(request, ram_slug):
    ram = Ram.objects.get(slug=ram_slug)
    ctgy = Category.objects.filter(is_active=True)
    brnd = Brand.objects.filter(is_available=True)
    prdts = ProductAttribute.objects.filter(productrelate__ram = ram, is_active = True, productrelate__is_available=True).distinct()
    clr = Products.objects.distinct().values('color__color','color__id','color__color_code','color__slug').distinct()
    ram = Products.objects.distinct().values('ram__ram','ram__id','ram__slug').distinct()
    paginator = Paginator(prdts, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productCount = prdts.count()
    for i in prdts:
        print(i.product_name)
    context = {
        "prdts": paged_products,
        "productCount": productCount,
        "clr":clr,
        "ram":ram,
        "brnd":brnd,
        "ctgy":ctgy,
    }
    return render(request, 'store/shop.html', context)

@never_cache
@login_required(login_url='login')
def wishlist(request):
    witem = Wishlist.objects.filter(user=request.user,product__is_available=True)
    wcount = witem.count()
    context = {
        'witem':witem,
        'wcount':wcount,
    }
    return render(request, 'store/wishlist.html', context)

def AddtoWishlist(request):
    if request.user.is_authenticated:
        product = Products.objects.get(id=request.GET['id'])
        if product:
            if Wishlist.objects.filter(user=request.user,product=product):
                return JsonResponse({'status':"Not"})
            else:
                Wishlist.objects.create(user=request.user,product=product)
                return JsonResponse({'status':"Add"})
        else:
            return JsonResponse({'status':"No Such Product Found"})
    else:
        return redirect('login')

def RemoveWhishlist(request,id):
    witem = Wishlist.objects.get(user=request.user,id=id)
    witem.delete()
    return redirect('wishlist')

# def ReviewSubmit(request, product_id):
#     url = request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
#             form = ReviewForm(request.POST, instance=reviews)
#             form.save()
#             return redirect(url)
#         except ReviewRating.DoesNotExist:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 data = ReviewRating()
#                 data.subject = form.cleaned_data['subject']
#                 data.rating = form.cleaned_data['rating']
#                 data.review = form.cleaned_data['review']
#                 data.ip = request.META.get('REMOTE_ADDR')
#                 data.product = product_id
#                 data.user = request.user.id
#                 data.save()

# def filterdata(request):
#     colors = request.GET.getlist('color[]')
#     print('ki')
#     print(colors)
#     rams = request.GET.getlist('ram[]')
#     brands = request.GET.getlist('brand[]')
#     categories = request.GET.getlist('category[]')
#     prdts = ProductAttribute.objects.all().order_by('-id')
    
#     if len(colors)>0:
#         prdts = prdts.filter(productrelate__color__id__in=colors).distinct()
#     if len(rams)>0:
#         prdts = prdts.filter(productrelate__ram__id__in=rams).distinct()
#     if len(brands)>0:
#         prdts = prdts.filter(brand_name__id__in=brands).distinct()
#     if len(categories)>0:
#         prdts = prdts.filter(category_name__id__in=categories).distinct()
    
    # t=render_to_string('store/filterlist.html',{'prdts':prdts})
    # return render(request, 'shop.html',{'prdts':'prdts'})
    # return JsonResponse({'data':'prdts'})
