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
        mycart = CartItem.objects.filter(user=request.user)
        total_amount = 0
        tax = 0
        for cart_item in mycart:
            total_amount += (cart_item.cart_product.price * cart_item.quantity)
            tax = round((6 * float(total_amount))/100)
        grand_total = total_amount + tax
        neworder.total_price = grand_total

        trackno = 'EI' + str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no = trackno) is None:
            trackno = 'EI' + str(random.randint(1,100))
        
        neworder.tracking_no = trackno
        neworder.save()

        neworderItems = CartItem.objects.filter(user=request.user)
        for item in neworderItems:
            OrderItem.objects.create(
                order = neworder,
                product = item.cart_product,
                price = grand_total,
                quantity = item.quantity
            )
            # orderproduct = Products.objects.filter(id=item.cart_product.id).first()
            # orderproduct.quantity = orderproduct.quantity - item.quantity
            # orderproduct.save()
        
        CartItem.objects.filter(user=request.user).delete()
        payMode =  request.POST.get('payment_mode')
        if (payMode == "Cash on Delivery"):
            return JsonResponse({'status':"Your order has been placed Successfully"})
        if (payMode == "Paid by Razorpay"):
            return JsonResponse({'status':"Your order has been placed Successfully"})
        elif (payMode == "Paid by PayPal"):
            return JsonResponse({'status':"Your order has been placed Successfully"})
        return redirect('home')
    else:
        return redirect('checkout')

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
        total_amount += (order_item.product.price * order_item.quantity)
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
        if rorder.status == ("Completed"):
            rorder.status = "Returned"
            rorder.save()
    return redirect('myorders')
    
