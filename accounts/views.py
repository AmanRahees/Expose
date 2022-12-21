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

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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
    phone_number=request.session['phone_number']
    print(phone_number)
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
            messages.error(request, 'Invalid OTP')
            return redirect('verification')
    context={
        'phone_number':phone_number
    }
    return render(request, 'accounts/otp.html',context)

@never_cache
def resendotp(request):
    phone_number=request.session['phone_number']
    send_otp(phone_number)
    return redirect('verification')

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
                            products = []
                            qty = []
                            for item in cart_item:
                                product = item.cart_product
                                products.append(product)
                                qty.append(item.quantity)
                            cart_item = CartItem.objects.filter(user=user)
                            print(user.id)
                            ex_product_list = []
                            id = []
                            for item in cart_item:
                                existing_product = item.cart_product
                                ex_product_list.append(existing_product)
                                id.append(item.id)
                            for pr in products:
                                index = products.index(pr)
                                item_qty = qty[index]
                                if pr in ex_product_list:
                                    index = ex_product_list.index(pr)
                                    item_id = id[index]
                                    item = CartItem.objects.get(id=item_id)
                                    item.quantity += item_qty
                                    item.user = user
                                    item.save()
                                else:
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
                        products = []
                        qty = []
                        for item in cart_item:
                            product = item.cart_product
                            products.append(product)
                            qty.append(item.quantity)
                        cart_item = CartItem.objects.filter(user=user)
                        print(user.id)
                        ex_product_list = []
                        id = []
                        for item in cart_item:
                            existing_product = item.cart_product
                            ex_product_list.append(existing_product)
                            id.append(item.id)
                        for pr in products:
                            index = products.index(pr)
                            item_qty = qty[index]
                            if pr in ex_product_list:
                                index = ex_product_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += item_qty
                                item.user = user
                                item.save()
                            else:
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

def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            messaage = render_to_string('accounts/password-reset.html',{
                'user': user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_mail = email
            print(email)
            send_male = EmailMessage(mail_subject, messaage, to=[to_mail])
            print('last chathi')
            send_male.send()
            
            messages.success(request, "Password reset email has been sent to your email. Please reset your account")
            return redirect('forgot_password')
        else:
            messages.error(request, 'Account does not exists')
            return redirect('forgot_password')
    return render(request, 'accounts/forgotPassword.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')

    else:
        messages.error(request, 'This link has been expired!')
        return redirect('forgot_password')
    
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful ')
            return redirect('signin')

        else:
            messages.error(request, 'Password does not match!')
            return redirect('resetPassword')
    return render(request, 'accounts/reset_password.html')



