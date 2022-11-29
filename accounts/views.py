from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import Account
from accounts.otp import *
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from store.models import  *
from store.views import _cart_id


# Create your views here.
@never_cache
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if Account.objects.filter(email=email).exists():
                messages.info(request,'You are already registered. Please log in.')
                return redirect('signup')
            elif Account.objects.filter(phone_number=phone_number).exists():
                messages.info(request, 'You are already registered. Please log in.')
                return redirect('signup')
            else:
                user = Account.objects.create_user(first_name=first_name,last_name=last_name,phone_number=phone_number, email=email, password=password)
                send_otp(user.phone_number)
                request.session['phone_number']=user.phone_number
                return redirect('verification')
        else:
             messages.info(request, 'Invalid Entry')
             return redirect('signup')
    return render(request, 'accounts/signup.html')

@never_cache
def otpVerification(request):
    if request.method=='POST':
        phone_number=request.session['phone_number']
        user= Account.objects.get(phone_number=phone_number)
        checkotp = request.POST.get('otp')
        check = verify_otp(phone_number, checkotp)

        if check:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid OTP')
            return redirect('verification')

    return render(request, 'accounts/otp.html')

@never_cache
def Userlogin(request):
    if request.user.is_authenticated:
            return redirect('home')
    else:
        if request.method == 'POST':
                email = request.POST.get('email')
                password = request.POST['password']

                user = authenticate(request, email=email, password=password)
                
                if user is not None:
                    try:
                        cart = Cart.objects.get(cart_id=_cart_id(request))
                        is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                        if is_cart_item_exists:
                            cart_item = CartItem.objects.filter(cart=cart)


                            for item in cart_item:
                                item.user = user
                                item.save()
                    except:
                        pass
                    login(request, user)
                    return redirect('home')
                else:
                    if Account.objects.filter(is_active = False):
                        messages.info(request, 'Your Account has been Suspended')
                        return redirect('login')
                    else:
                        messages.error(request, 'Invalid Username or Password')
                        return redirect('login')
        else:
            return render(request, 'accounts/login.html')

def otplogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')

            user = Account.objects.get(phone_number=phone_number)

            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()
                except:
                      pass
                request.session['phone_number'] = phone_number
                send_otp(user.phone_number)
                return redirect('verification')
            else:
                messages.info(request, 'Not Found')
                return redirect('otplogin')
        else:
            return render(request, 'accounts/OtpLogin.html')

@never_cache
@login_required(login_url='login')
def ChangePassword(request):
    if request.method == 'POST':
        current_password =  request.POST['current_password']
        password = request.POST['password']
        password2 = request.POST['password2']

        user = Account.objects.get(email__exact=request.user.email)

        if password == password2:
            success = user.check_password(current_password)
            if success:
                user.set_password(password)
                user.save()
                messages.success(request, 'Password updated Successfully')
                return redirect('login')
            else:
                messages.error(request, 'Please Enter Valid Password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not Match')
            return redirect('change_password')
    return render(request, 'store/Changepswd.html')


@never_cache
def User_logout(request):
    logout(request)
    return redirect('home')




