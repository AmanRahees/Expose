from Brand.models import Brand
from category.models import Category
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from products.models import Products, Variation, SubCategory
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

#----------------Home Page--------------#

@never_cache
def home(request):
    ctgy = Category.objects.filter(is_active=True)
    prdts = Products.objects.filter(is_available = True, product_category__is_active=True,product_brand__is_available=True).order_by('-created_date')[:5]
    context = {
        "ctgy":ctgy,
        "prdts": prdts
    }
    return render(request, 'home.html',context)


#-----------------------Product Page--------------------------#

@never_cache
def store(request):
    ctgy = Category.objects.filter(is_active=True)
    prdts = Products.objects.filter(is_available = True, product_category__is_active=True)
    subprdts = Variation.objects.all()
    paginator = Paginator(prdts, 5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        "prdts": paged_products,
        "ctgy":ctgy,
        "subprdts":subprdts
    }
    return render(request, 'store/shop.html', context)

@never_cache
def by_category(request,category_slug):
    categories = Category.objects.get(slug=category_slug)
    prdts = Products.objects.filter(product_category = categories ,is_available = True)
    paginator = Paginator(prdts, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    productCount = prdts.count()
    context = {
        "prdts": paged_products,
        "productCount": productCount
    }
    return render(request, 'store/shop.html', context)

def productDetail(request,category_slug, product_slug):
    try:
        prdts = Products.objects.get(slug=product_slug, product_category__slug=category_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), cart_product=prdts).exists
    except Exception as e:
        return e
    context={
        'prdts':prdts,
        'in_cart':in_cart,
    }
    return render(request, 'store/ProductView.html', context)
    

#----------------------------Cart-------------------------------#


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    prdts = Products.objects.get(id=product_id)
    if request.user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variations = Variation.objects.get(product_name=prdts, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variations)
                except:
                    pass

        is_cart_item_exists=CartItem.objects.filter(cart_product=prdts, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(cart_product=prdts, user=current_user)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(cart_product=prdts, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(cart_product=prdts, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else: 
            cart_item = CartItem.objects.create(
                    cart_product = prdts,
                    quantity = 1,
                    user = current_user,
                )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variations = Variation.objects.get(product_name=prdts, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variations)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id= _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists=CartItem.objects.filter(cart_product=prdts, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(cart_product=prdts, cart=cart)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(cart_product=prdts, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(cart_product=prdts, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else: 
            cart_item = CartItem.objects.create(
                    cart_product = prdts,
                    quantity = 1,
                    cart = cart,
                )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart') 

def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    prdts = Products.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(cart_product=prdts, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass 
    return redirect('cart')

@never_cache
def cart(request, total=0, quantity=0, cart_item=0):
    try:
        cart_items=0
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id =_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.cart_product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (8*total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request, 'store/cart.html', context)

def delete_cart_item(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    prdts = Products.objects.get(id=product_id)
    cart_item = CartItem.objects.get(cart_product=prdts, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


#--------------------------Search View-----------------------------#

def Search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            prdts = Products.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
    context={
        'prdts':prdts,
    }
    return render(request,'store/shop.html', context)

@login_required(login_url='login')
def demo(request):
    return render(request, 'store/checkout.html')
