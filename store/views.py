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
from django.core.paginator import Paginator 
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

#----------------Home Page--------------#

@never_cache
def home(request):
    ctgy = Category.objects.filter(is_active=True)
    prdts = ProductAttribute.objects.filter(is_active = True, category_name__is_active=True)
    context = {
        "ctgy":ctgy,
        "prdts": prdts
    }
    return render(request, 'home.html',context)


#-----------------------Product Page--------------------------#

@never_cache 
def store(request):
    ctgy = Category.objects.filter(is_active=True)
    prdts = ProductAttribute.objects.filter(is_active = True,category_name__is_active=True)
    paginator = Paginator(prdts, 15)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        "prdts": paged_products,
        "ctgy":ctgy,
    }
    return render(request, 'store/shop.html', context)

@never_cache
def by_category(request,category_slug):
    categories = Category.objects.get(slug=category_slug)
    prdts = ProductAttribute.objects.filter(category_name = categories, is_active = True)
    paginator = Paginator(prdts, 15)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productCount = prdts.count()
    context = {
        "prdts": paged_products,
        "productCount": productCount
    }
    return render(request, 'store/shop.html', context)

def productDetail(request,category_slug, product_slug):
    prdts = ProductAttribute.objects.get(slug=product_slug)
    ram = Products.objects.filter(product_name=prdts).values('id','ram__id','ram__ram','color__id','price','stock').distinct()
    colors = Products.objects.filter(product_name=prdts).values('color__id','color__color','color__color_code').distinct()
    images = ProductImage.objects.filter(product__product_name=prdts)
    context = {
         'prdts':prdts,
         'ram':ram,
         'colors':colors,
         'images':images
    }
    return render(request, 'store/ProductView.html', context)
    

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
        print('first try')
        cart = Cart.objects.get(cart_id= _cart_id(request))
        print('first try end')
    except Cart.DoesNotExist:
        print('first except')
        cart = Cart.objects.create(cart_id =_cart_id(request))
        cart.save()
        print('first except end')
    if current_user.is_authenticated:
        print('User Authenticated')
        is_cart_item_exists = CartItem.objects.filter(cart_product__price=product.price, user=current_user).exists()
        if is_cart_item_exists:
            print('cart item exists')
            cart_item = CartItem.objects.get(cart_product=product, user=current_user)
            cart_item.quantity += int(request.GET['qty'])
            cart_item.save()
            print('indayath sett aayi')
        else:
            print('cart illa mwone')
            cart_item = CartItem.objects.create(
                cart_product = product,
                quantity = request.GET['qty'],
                user = current_user,
            )
            print('ippam cartil add aaki')
    else:
        print('Session vech keri')
        is_cart_item_exists = CartItem.objects.filter(cart_product__price=product.price, cart=cart).exists()
        if is_cart_item_exists:
            print('session cartil already ind')
            cart_item = CartItem.objects.get(cart_product=product.id, cart=cart.id)
            cart_item.quantity += int(request.GET['qty'])
            cart_item.save()
            print(cart_item.quantity)
            print('session cartil athinte quantity kooti')
        else:
            print('session cartil  sadhanam  illa')
            cart_item = CartItem.objects.create(
                cart_product=product,
                quantity = request.GET['qty'],
                cart = cart,
            )
            cart_item.save()
            print('sambavam sesssion carttil addd aakitund')
    print('add to cart success aayi mwonee')
    return JsonResponse({'single_product':'success'})

def cart(request):
    current_user=request.user
    context={}
    try:
        if current_user.is_authenticated:
            cart_items = CartItem.objects.filter(user=current_user, is_active=True).order_by('-id')
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True).order_by('-id')
        total_amount = 0
        for cart_item in cart_items:
            total_amount += (cart_item.cart_product.price * cart_item.quantity)
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

def cart_update(request):
    current_user=request.user
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    product = Products.objects.get(id=p_id)
    if current_user.is_authenticated:
        cart_item=CartItem.objects.get(user=current_user, cart_product=product)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart_product=product, cart=cart)
    cart_item.quantity = p_qty
    cart_item.save()
    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    total_amount = 0
    for cart_item in cart_items:
        total_amount += (cart_item.cart_product.price * cart_item.quantity)
        tax = round((8 * float(total_amount))/100)
        sub_total = total_amount + tax
        context = {
            'total_amount':total_amount,
            'tax':tax,
            'sub_total':sub_total,
            'cart_items':cart_items,
        }
    t = render_to_string('Orders/cart-list.html', context)
    return JsonResponse({'data':t})

#---------------------Order--------------------------#

@login_required(login_url='login')
def checkout(request):
    mycart = CartItem.objects.filter(user=request.user)
    ads = useraddress.objects.filter(user_id = request.user)
    account = Account.objects.filter(email = request.user)
    total_amount = 0
    for cart_item in mycart:
        total_amount += (cart_item.cart_product.price * cart_item.quantity)
    tax = round((6 * float(total_amount))/100)
    grand_total = total_amount + tax
    context = {
        'ads':ads,
        'account':account,
        'mycart':mycart,
        'total_amount':total_amount,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request, 'Orders/checkout.html', context)

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

@login_required(login_url='login')
def razorpaycheck(request):
    mycart = CartItem.objects.filter(user=request.user)
    total_amount = 0
    for cart_item in mycart:
        total_amount += (cart_item.cart_product.price * cart_item.quantity)
    tax = round((6 * float(total_amount))/100)
    grand_total = total_amount + tax
    context = {
        'grand_total':grand_total,
    }
    return JsonResponse(context)

@never_cache
def OrderConfirmed(request):
    return render(request, 'Orders/confirmed.html')

#--------------------------Search View-----------------------------#

def Search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            prdts = ProductAttribute.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
        else:
            return redirect('products')
    context={
        'prdts':prdts,
    }
    return render(request,'store/shop.html', context)


@never_cache
@login_required(login_url=('login'))
def UserSettings(request):
    return render(request, 'store/settings.html')

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





