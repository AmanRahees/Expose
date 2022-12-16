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
from accounts.models import Account
from .models import *
from django.core.paginator import Paginator
from store.models import *
from django.db.models import Q
from Brand.models import *
from django.contrib.auth.decorators import login_required
import random

# Create your views here.

@login_required(login_url='login')
def placeOrder(request):
    if request.method == 'POST':
        current_user = Account.objects.filter(id=request.user.id)

        neworder = Order()
        neworder.name = request.POST.get('name')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.address_2 = request.POST.get('address_2')
        neworder.state = request.POST.get('state')
        neworder.district = request.POST.get('district')
        neworder.city = request.POST.get('city')
        neworder.pincode = request.POST.get('pincode')
        neworder.user = request.user
        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')
        mycart = CartItem.objects.filter(user=request.user, cart_product__is_available=True)
        total_amount = 0
        tax = 0
        for cart_item in mycart:
            poff_price = round(cart_item.cart_product.price - cart_item.cart_product.price * cart_item.cart_product.product_name.product_offer /100)
            coff_price = round(cart_item.cart_product.price - cart_item.cart_product.price * cart_item.cart_product.product_name.category_name.category_offer /100)
            if poff_price <= coff_price:
                total_amount += (poff_price * cart_item.quantity)
            elif poff_price >= coff_price:
                total_amount += (coff_price * cart_item.quantity)
            tax = round((2 * float(total_amount))/100)
        grand_total = total_amount + tax

        try:
            coup_value = Couponuser.objects.get(user = request.user)
            coupon_status = True
            coup_perc = coup_value.coupon_value
            coupon_codes = coup_value.coupon_code
            coup_value.used = True
            coup_value.save()
        except Exception as e:
            coupon_codes = None
            coupon_status = False
            coup_perc = 0
        grand_total  = int(grand_total - grand_total * int(coup_perc)/100)
        neworder.total_price = grand_total

        trackno = 'EI' + str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no = trackno) is None:
            trackno = 'EI' + str(random.randint(1111111,9999999))
        neworder.tracking_no = trackno
        neworder.save()
        neworderItems = CartItem.objects.filter(user=request.user, cart_product__is_available=True)
        for item in neworderItems:
            OrderItem.objects.create(
                order = neworder,
                product = item.cart_product,
                price = grand_total,
                quantity = item.quantity
            )
            orderproduct = Products.objects.filter(id=item.cart_product.id).first()
            orderproduct.stock = orderproduct.stock - item.quantity
            orderproduct.save()

        successordermod.objects.create(
            order_id = neworder.tracking_no
        )
        CartItem.objects.filter(user=request.user, cart_product__is_available=True).delete()
        Couponuser.objects.filter(user = request.user).delete()
        payMode =  request.POST.get('payment_mode')
        if (payMode == "Cash on Delivery"):
            return JsonResponse({'status':"Your order has been placed Successfully", 'tracking_no':trackno})
        if (payMode == "Paid by Razorpay"):
            return JsonResponse({'status':"Your order has been placed Successfully", 'tracking_no':trackno})
        elif (payMode == "Paid by PayPal"):
            return JsonResponse({'status':"Your order has been placed Successfully", 'tracking_no':trackno})
        return redirect('home')
    else:
        return redirect('checkout')
    
def success_order(request):
    order_number = request.GET.get('order_number')
    test =  successordermod.objects.get(order_id = order_number)
    try:
        test =  successordermod.objects.get(order_id = order_number, status = False)
        test.status = True
        test.save()
        order = Order.objects.get(tracking_no = order_number)
        items = OrderItem.objects.filter(order_id = order.id)
        context = {
            'obj' : order,
            'items' : items
        }
        return render(request, 'Orders/OrderSuccess.html', context)
    except Exception as e: 
        print(e)
        return redirect('home') 

def MyOrders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'orders':paged_products,
    }
    return render(request, 'Orders/OrderHistory.html', context)

def OrderView(request, id):
    orders = Order.objects.get(id=id)
    obj = OrderItem.objects.filter(order=orders)
    total_amount=0
    for order_item in obj: 
        poff_price = round(order_item.product.price - order_item.product.price * order_item.product.product_name.product_offer /100)
        coff_price = round(order_item.product.price - order_item.product.price * order_item.product.product_name.category_name.category_offer /100)
        if poff_price <= coff_price:
            total_amount += (poff_price * order_item.quantity)
        elif poff_price >= coff_price:
            total_amount += (coff_price * order_item.quantity)
    print(total_amount)
    tax = round((6 * float(total_amount))/100)
    context = {
        "orders":orders,
        "total_amount":total_amount,
        "tax":tax,
    }
    return render(request, 'Orders/Orderview.html', context)


def CancelOrder(request, id):
    corder = Order.objects.get(id=id)
    if corder.status != ("Order cancelled" or "Returned" or "Out for Delivery"):
        corder.status = "Order cancelled"
        corder.save()
    return redirect('myorders')

def ReturnOrder(request, id):
    rorder = Order.objects.get(id=id)
    returnform = Return()
    if request.method == "POST":
        returnform.Order = rorder
        returnform.reason = request.POST['reason']
        returnform.comment = request.POST['comment']
        returnform.item_img = request.FILES.get('item_img') 
        returnform.save()
        if rorder.status == ("Completed") or rorder.status == ("Out for Delivery"):
            rorder.status = "Returned"
            rorder.save()
    return redirect('myorders')
    
