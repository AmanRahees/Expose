from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import Account
from category.models import Category
from Brand.models import Brand
from products.forms import *
from category.forms import *
from Brand.forms import *
from products.models import *
from orders.models import *
from orders.forms import OrderStatus
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from datetime import datetime,timedelta,date
from django.db.models import Sum, Q
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def AdminLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.is_superadmin:
                login(request, user)
                return redirect('/admin_panel')
            else:
                messages.info(request, 'You have Permission')
                return render(request, 'accounts/adminLogin.html')
        else:
            messages.info(request, 'Invalid Username or Password')
            return render(request, 'accounts/adminLogin.html')
    else:        
        return render(request, 'accounts/adminLogin.html')


def logout_admin(request):
    logout(request)
    return redirect('/admin_panel/login')

#---------------------Dahsboard View--------------------#

@never_cache
@staff_member_required(login_url='adminlogin')
def dashboard(request):
    users = Account.objects.filter(is_superadmin = False)
    orders = Order.objects.all().exclude(status='Completed'or 'Returned' or'Order cancelled')
    mostpopular = Products.objects.annotate(test = Count('orderproduct')).order_by('-test')[:4]
    count = []
    name = []
    for mo in mostpopular:
        x = mo.test
        count.append(x)
        y = mo.product_name
        name.append(y)
    count1 = count[0]
    count2 = count[1]
    count3 = count[2]
    count4 = count[3]
    name1 = name[0]
    name2 = name[1]
    name3 = name[2]
    name4 = name[3]
    cod = Order.objects.filter(payment_mode = "Cash on Delivery").count()
    razor = Order.objects.filter(payment_mode = "Paid by Razorpay").count()
    paypal = Order.objects.filter(payment_mode = "Paid by PayPal").count()
    total_products = ProductAttribute.objects.all().count()
    revenue = Order.objects.all().aggregate(Sum('total_price'))
    total_revenue = revenue['total_price__sum']
    today = datetime.today()
    today_date = today.strftime("%Y-%m-%d")
    f = date(2022,9,6)
    month = today.month
    year = today.strftime("%Y")
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month).count() 
    order_count_in_day =Order.objects.filter(created_at__contains = today).count()
    order_count_in_week = Order.objects.filter(created_at__gte = one_week).count()
    today_sale = Order.objects.filter(created_at__date = today_date).count()
    today = today.strftime("%A")
    new_date = datetime.today() - timedelta(days = 1)
    yester_day_sale =   Order.objects.filter(created_at__date = new_date).count()
    yesterday = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_2 = Order.objects.filter(created_at__date = new_date).count()
    day_2_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_3 = Order.objects.filter(created_at__date = new_date).count()
    day_3_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_4 = Order.objects.filter(created_at__date = new_date).count()
    day_4_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_5 = Order.objects.filter(created_at__date = new_date).count()
    day_5_name = new_date.strftime("%A")
    confirmed = Order.objects.filter(status = 'Completed').count()
    canc_return = Order.objects.filter(Q(status = "Order cancelled") | Q(status = "Returned")).count()
    context={
        'users':users,
        'orders':orders,
        "name1" : name1,
        "name2" : name2,
        "name3" : name3,
        "name4" : name4,
        "count1" : count1,
        "count2" : count2,
        "count3" : count3,
        "count4" : count4,
        "cod" : cod,
        "razor" : razor,
        "paypal" : paypal,
        "order_count_in_month" : order_count_in_month,
        "order_count_in_day" : order_count_in_day,
        "order_count_in_week" : order_count_in_week,
        "confirmed" : confirmed,
        "canc_return" : canc_return,
        "today_sale" : today_sale,
        "yester_day_sale" : yester_day_sale,
        "day_2": day_2,
        "day_3": day_3,
        "day_4": day_4,
        "today" : today,
        "yesterday" : yesterday,
        "day_2_name" : day_2_name,
        "day_3_name" : day_3_name,
        "day_4_name" : day_4_name,
        "total_revenue":total_revenue,
        "total_products":total_products,
    }
    return render(request, 'Dashboard.html', context)


#----------------------Dashboard End------------------#

#----------------------UserManagement View------------------#

@never_cache
@staff_member_required(login_url='adminlogin')
def UserManagement(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            users = Account.objects.filter(email__icontains = key, is_superadmin = False)
        else:
            return redirect('Users')
    else:
        users = Account.objects.filter(is_superadmin = False).order_by('-id')
    usercount = users.count()
    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context={
        'users':paged_products,
        'usercount':usercount,
    }
    return render(request, 'accounts/UserManage.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def user_status(request,id,status):
    users = Account.objects.get(id=id)
    if status == 'true':  
        users.is_active = True
    elif status == 'false':
        users.is_active = False
    users.save()
    return redirect('Users')

@never_cache
@staff_member_required(login_url='adminlogin')
def deleteUser(request,id):
    users = Account.objects.get(id=id)
    users.delete()
    return redirect('Users')

#----------------------Usermanagement End------------------#

#----------------------OrderManagement View------------------#

@never_cache
@staff_member_required(login_url='adminlogin')
def OrderManagement(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            orders = Order.objects.filter(tracking_no__icontains = key).order_by('-created_at')
        else:
            return redirect('Orders')
    else:
        orders = Order.objects.all().order_by('-id')
    ordercount = orders.count()
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    form = OrderStatus()
    context = {
        'orders':paged_products,
        'ordercount':ordercount,
        'form':form,
    }
    return render(request, 'OrderManage.html', context)

def Update_Order(request, id):
    if request.method == 'POST':
        Ustatus = get_object_or_404(Order, id=id)
        status = request.POST.get('status')
        Ustatus.status = status
        Ustatus.save()
        return redirect('Orders')

#----------------------OrderManagement End------------------#

#---------------------Category View-----------------#

@never_cache
@staff_member_required(login_url='adminlogin')
def categoryList(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            ctgy = Category.objects.filter(category_name__icontains = key).order_by('-id')
        else:
            return redirect('category')
    else:
        ctgy = Category.objects.all().order_by('-id')
    ctgycount = ctgy.count()
    paginator = Paginator(ctgy, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        "ctgy":paged_products,
        "ctgycount":ctgycount,
    }
    return render(request, 'backend/category.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def AddCategory(request):
    if request.method == "POST":
        form = AddCategoryForm(request.POST , request.FILES)
        if form.is_valid():
            form.errors.as_data()
            form.save()
            return redirect('category')
        else:
            return redirect('addcategory')
    else:
        form = AddCategoryForm()
    context={
        "form":form 
    }
    return render(request, 'backend/AddCategory.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def EditCategory(request,id):
    ctgy = Category.objects.get(id=id)
    return render(request,'backend/EditCategory.html', {'ctgy':ctgy}) 

@never_cache
@staff_member_required(login_url='adminlogin')
def UpdateCategory(request,id):
    ctgy = Category.objects.get(id=id)
    form = EditCategoryForm(request.POST, instance = ctgy)
    if form.is_valid():  
        form.save()  
        return redirect("category")
    else:
         print(form.errors.as_data()) 
    context = {
        'ctgy': ctgy
    }  
    return render(request, 'backend/EditCategory.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def enable_category(request,id,status):
    ctgy = Category.objects.get(id=id)
    if status == 'true':  
        print('true')
        ctgy.is_active = True
    elif status == 'false':
        print('fal')
        ctgy.is_active = False
    ctgy.save()
    return redirect('category') 

@never_cache
@staff_member_required(login_url='adminlogin')
def DeleteCategory(request, id):
    ctgy = Category.objects.filter(id=id)
    ctgy.delete()
    return redirect('category')

#------------------Category End----------------------#

#------------------SubCategory View------------------#

@never_cache
@staff_member_required(login_url='adminlogin')
def SubCategoryList(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            subctgy = SubCategory.objects.filter(subcategory_name__icontains = key).order_by('-id')
        else:
            return redirect('subcategory')
    else:
        subctgy = SubCategory.objects.all().order_by('-id')
    subctcnt = subctgy.count()
    paginator = Paginator(subctgy, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        "subctgy" : paged_products,
        "subctcnt":subctcnt
    }
    return render(request, 'backend/Subcategory.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def AddSubCategory(request):
    if request.method == "POST":
        form = AddSubCategoryForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subcategory')
        else:
            print('error')
            return redirect('addsubcategory')
    else:
        form = AddSubCategoryForm()
    context={
        "form":form
    }
    return render(request, 'backend/AddSubCategory.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def EditSubCategory(request,id):
    subctgy = SubCategory.objects.get(id=id)
    context = {
        'subctgy':subctgy
    }
    return render(request,'backend/EditSubCategory.html', context) 

@never_cache
@staff_member_required(login_url='adminlogin')
def UpdateSubCategory(request,id):
    subctgy = SubCategory.objects.get(id=id)
    form = EditSubCategoryForm(request.POST, instance = subctgy)
    if form.is_valid():  
        form.save()  
        return redirect("subcategory")
    else:
         print(form.errors.as_data()) 
    context = {
        'subctgy': subctgy
    }  
    return render(request, 'backend/EditSubCategory.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def enable_subcategory(request,id,status):
    subctgy = SubCategory.objects.get(id=id)
    if status == 'true':  
        print('true')
        subctgy.is_acitve = True
    elif status == 'false':
        print('fal')
        subctgy.is_acitve = False
    subctgy.save()
    return redirect('subcategory')

@never_cache
@staff_member_required(login_url='adminlogin')
def DeleteSubCategory(request, id):
    subctgy = SubCategory.objects.filter(id=id)
    subctgy.delete()
    return redirect('subcategory')

#------------------SubCategory End------------------#

#-----------------Brand View-------------------------#

@never_cache
@staff_member_required(login_url='adminlogin')
def brandList(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            brnd = Brand.objects.filter(brand_name__icontains = key).order_by('-id')
        else:
            return redirect('brand')
    else:
        brnd = Brand.objects.all().order_by('-id')
    brndcount = brnd.count()
    paginator = Paginator(brnd, 7)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        "brnd" : paged_products,
        "brndcount":brndcount,
    }
    return render(request, 'backend/Brands.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def AddBrand(request):
    if request.method == "POST":
        form = AddBrandForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('brand')
        else:
            return redirect('addbrand')
    else:
        form = AddBrandForm()
    return render(request, 'backend/AddBrand.html', {'form': form})

@never_cache
@staff_member_required(login_url='adminlogin')
def EditBrand(request, id):  
    brnd = Brand.objects.get(id=id)  
    context={
        'brnd':brnd
    }
    return render(request,'backend/EditBrand.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def UpdateBrand(request, id):
    brnd = Brand.objects.get(id=id)  
    form = AddBrandForm(request.POST, instance = brnd)
    if form.is_valid():  
        form.save()  
        return redirect("brand") 
    context = {
        'brnd': brnd
    }  
    return render(request, 'backend/EditBrand.html', context) 

@never_cache
@staff_member_required(login_url='adminlogin')
def DeleteBrand(request, id):
    brnd = Brand.objects.filter(id=id)
    brnd.delete()
    return redirect('brand')

@never_cache
@staff_member_required(login_url='adminlogin')
def enable_brand(request,id,status):
    brnd = Brand.objects.get(id=id)
    if status == 'true':  
        brnd.is_available = True
    elif status == 'false':
        brnd.is_available = False
    brnd.save()
    return redirect('brand') 

#------------------Brand End------------------------#

#-------------------ProductAttribute Views---------------#


@never_cache
@staff_member_required(login_url='adminlogin')
def ProductAttributeList(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            prdts = ProductAttribute.objects.filter(product_name__icontains = key).order_by('-id')
        else:
            return redirect('product')
    else:
        prdts = ProductAttribute.objects.all().order_by('-id')
    itcount = prdts.count()
    paginator = Paginator(prdts, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'prdts':paged_products,
        'itcount':itcount
    }
    return render(request, 'Product/products.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def AddProductAttribute(request):
    if request.method == "POST":
        form = AddProductAttributeForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')
        else:
            messages.info(request, 'Product already Added')
            return redirect('addproduct')
    else:
        form = AddProductAttributeForm()
    context = {
        'form': form,
        }
    return render(request, 'Product/AddProduct.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def deleteProduct(request, id):
    prdts = ProductAttribute.objects.filter(id=id)
    prdts.delete()
    return redirect('product')

@never_cache
@staff_member_required(login_url='adminlogin')
def EditProductAttribute(request, id):  
    prdts = ProductAttribute.objects.get(id=id)  
    context = {
        'prdts':prdts
    }
    return render(request,'Product/EditProduct.html', context) 

@never_cache
@staff_member_required(login_url='adminlogin')
def UpdateProductAttribute(request, id):
    prdts = ProductAttribute.objects.get(id=id)  
    form = EditProductAttributeForm(request.POST, instance = prdts)
    if form.is_valid():  
        form.save()
        return redirect("product")  
    context = {
        'prdts': prdts
    }  
    return render(request, 'Product/EditProduct.html', context) 

@never_cache
@staff_member_required(login_url='adminlogin')
def enable_productAttribute(request,id,status):
    prdts = ProductAttribute.objects.get(id=id)
    if status == 'true':  
        prdts.is_active = True
    elif status == 'false':
        prdts.is_active = False
    prdts.save()
    return redirect('product') 

#---------------------SubProduct View-----------------#

@never_cache
@staff_member_required(login_url='adminlogin')
def SubProductList(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            subprdts = Products.objects.filter(product_name__product_name__icontains = key).order_by('-id')
        else:
            return redirect('subproduct')
    else:
        subprdts = Products.objects.all().order_by('-id')
    spdt = subprdts.count()
    paginator = Paginator(subprdts, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'subprdts':paged_products,
        'spdt':spdt,
    }
    return render(request, 'Product/SubProduct.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def AddSubProduct(request):
    if request.method == "POST":
        form = AddProductForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subproduct')
        else:
            messages.info(request, 'Product already Added')
            return redirect('addsubproduct')
    else:
        form = AddProductForm()
    context = {
        'form': form,
        }
    return render(request, 'Product/AddSubProduct.html', context)

@never_cache
@staff_member_required(login_url='adminlogin')
def EditSubProduct(request, id):  
    subprdts = Products.objects.get(id=id)  
    context = {
        'subprdts':subprdts
    }
    return render(request,'Product/EditSubProduct.html', context) 

@never_cache
@staff_member_required(login_url='adminlogin')
def UpdateSubProduct(request, id):
    subprdts = Products.objects.get(id=id)
    form = EditProductForm(request.POST, instance = subprdts)
    if form.is_valid():  
        form.save()  
        return redirect("subproduct")
    else:
         print(form.errors.as_data()) 
    context = {
        'subprdts': subprdts
    }  
    return render(request, 'Product/EditSubProduct.html', context)


@never_cache
@staff_member_required(login_url='adminlogin')
def enable_subproduct(request,id,status):
    subprdts = Products.objects.get(id=id)
    if status == 'true':  
        subprdts.is_available = True
    elif status == 'false':
        subprdts.is_available = False
    subprdts.save()
    return redirect('subproduct')

@never_cache
@staff_member_required(login_url='adminlogin')
def deleteSubProduct(request, id):
    subprdts = Products.objects.filter(id=id)
    subprdts.delete()
    return redirect('subproduct')

#---------------------SubPRoduct End-----------------#

#--------------------Variation View------------------#

@never_cache
@staff_member_required(login_url='adminlogin')
def VariationList(request):
    ram = Ram.objects.all().order_by('-id')
    color = Color.objects.all().order_by('-id')
    clrcnt = color.count()
    paginator = Paginator(color, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'ram':ram,
        'color':paged_products,
        'clrcnt':clrcnt
    }
    return render(request, 'Product/variations.html',context)

@never_cache
@staff_member_required(login_url='adminlogin')
def AddRam(request):
    if request.method == "POST":
        form = AddRamForm(request.POST , request.FILES)
        if form.is_valid():
            form.errors.as_data()
            form.save()
            return redirect('variations')
        else:
            print(form.errors.as_data())
            messages.info(request, 'Ram already Added')
            return redirect('addram')
    else:
        form = AddRamForm()
    context = {
        'form': form,
        }
    return render(request, 'Product/AddVariation.html', context)


@never_cache
@staff_member_required(login_url='adminlogin')
def enable_ram(request,id,status):
    ram = Ram.objects.get(id=id)
    if status == 'true':  
        ram.is_acitve = True
    elif status == 'false':
        ram.is_acitve = False
    ram.save()
    return redirect('variations')

@never_cache
@staff_member_required(login_url='adminlogin')
def deleteRam(request,id):
    ram = Ram.objects.filter(id=id)
    ram.delete()
    return redirect('variations')



def AddColor(request):
    if request.method == "POST":
        form = AddColorForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('variations')
        else:
            messages.info(request, 'Ram already Added')
            return redirect('addcolor')
    else:
        form = AddColorForm()
    context = {
        'form': form,
        }
    return render(request, 'Product/AddVariation.html', context)


def enable_color(request,id,status):
    color = Color.objects.get(id=id)
    if status == 'true':  
        color.is_acitve = True
    elif status == 'false':
        color.is_acitve = False
    color.save()
    return redirect('variations')


def deleteColor(request,id):
    color = Color.objects.filter(id=id)
    color.delete()
    return redirect('variations')

#--------------------Variation End-----------------#


#---------------------Offer Management-------------#


def OfferManage(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            ctgyoff = Category.objects.filter(Q(category_name__icontains = key)|Q(category_offer__icontains = key)).order_by('-id')
        else:
            return redirect('coupon')
    else:
        ctgyoff = Category.objects.all()
    paginator = Paginator(ctgyoff, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'ctgyoff':paged_products
    }
    return render(request, 'Product/OfferManage.html', context)

def addCategoryOffer(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')
        category_offer = request.POST.get('category_offer')
        if int(category_offer) >= 1 and int(category_offer) <= 80:
            ctgyoff = Category.objects.get(category_name = category_name)
            ctgyoff.category_offer =  category_offer
            ctgyoff.save()
        else:
            messages.error(request, 'Offer must between 1% - 80%')
    return redirect('offer_manage')

def deleteCategoryoffer(request, id):
    ctgyoff = Category.objects.get(id=id)
    ctgyoff.category_offer = 0
    ctgyoff.save()
    messages.success(request, 'Deleted Category offer Successfully')
    return redirect('offer_manage')


def ProductOffer(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            pdtoff = ProductAttribute.objects.filter(Q(product_name__icontains = key)|Q(product_offer__icontains=key)).order_by('-product_offer')
        else:
            return redirect('prdt_offer')
    else:
        pdtoff = ProductAttribute.objects.all().order_by('-product_offer')
    paginator = Paginator(pdtoff, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'pdtoff':paged_products
    }
    return render(request, 'Product/ProductOffer.html', context)

def addPrdtOffer(request):
    if request.method == "POST":
        id = request.POST.get('id')
        product_offer = request.POST.get('product_offer')
        if int(product_offer) >= 1 and int(product_offer) <= 80:
            pdtoff = ProductAttribute.objects.get(id=id)
            pdtoff.product_offer =  product_offer
            pdtoff.save()
        else:
            messages.error(request, 'Offer must between 1% - 80%')
    return redirect('prdt_offer')

def deletePdtoffer(request, id):
    pdtoff = ProductAttribute.objects.get(id=id)
    pdtoff.product_offer = 0
    pdtoff.save()
    messages.success(request, 'Product offer Deleted Successfully')
    return redirect('prdt_offer')


def CpnLIst(request):
    if 'key' in request.GET:
        key = request.GET.get('key')
        if key:
            cpn = Coupon.objects.filter(Q(code__icontains = key)|Q(offer_value__icontains = key)).order_by('-id')
        else:
            return redirect('coupon')
    else:
        cpn = Coupon.objects.all().order_by('-id')
    if request.method == 'POST':
        form = CouponForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('coupon')
        else:
            messages.info(request, 'Invalid Entry')
            return redirect('coupon')
    else:
        form = CouponForm()
    paginator = Paginator(cpn, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context={
        'form':form,
        'cpn':paged_products,
    }
    return render(request, 'Product/Coupon.html', context)

def EditCoupon(request):
    if request.method == "POST":
        code = request.POST.get('code')
        offer_value = request.POST.get('offer_value')
        valid_at = request.POST.get('valid_at')
        cpnetz = Coupon.objects.get(code = code)
        cpnetz.offer_value =  offer_value
        cpnetz.valid_at =  valid_at
        if int(cpnetz.offer_value) <= 20 and int(cpnetz.offer_value) >= 1:
            cpnetz.save()
        else:
            messages.info(request, 'Offer must be 20% or below')
    return redirect('coupon')
 
def StatusCoupon(request,id,status):
    cpn = Coupon.objects.get(id=id)
    if status == 'true':  
        cpn.active = True
    elif status == 'false':
        cpn.active = False
    cpn.save()
    return redirect('coupon')

def deleteCpn(request,id):
    cpn = Coupon.objects.filter(id=id)
    cpn.delete()
    return redirect('coupon')


#---------------------Offer Management End-------------#

#---------------------Sales Report--------------------#


def sales_report(request):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    years = []
    today_date=str(date.today())
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        val = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = val+timedelta(days=1)
        orders = Order.objects.filter(Q(created_at__lt=end_date),Q(created_at__gte=start_date)).values('orderelate__product__product_name__product_name','orderelate__product__ram__ram','orderelate__product__color__color','orderelate__product__stock',
        total = Sum('total_price'),).annotate(dcount=Sum('orderelate__quantity')).order_by()
    else:
        orders = Order.objects.filter(created_at__year=year,created_at__month=month,orderelate__product__is_available=True).values('orderelate__product__product_name__product_name','orderelate__product__ram__ram','orderelate__product__color__color','orderelate__product__stock',
        total = Sum('total_price'),).annotate(dcount=Sum('orderelate__quantity')).order_by()
        for i in range (10):
            val = year-i
            years.append(val)
    context={
        'orders':orders,
        'today_date':today_date,
        'years':years,
    }
    return render(request,'Report/SalesReport.html', context)  

def monthly_sales_report(request, id):
    orders = Order.objects.filter(created_at__month = id).values('orderelate__product__product_name__product_name','orderelate__product__ram__ram','orderelate__product__color__color','orderelate__product__stock',
    total = Sum('total_price'),).annotate(dcount=Sum('orderelate__quantity')).order_by()
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    return render(request,'Report/SalesReport-table.html',context)

def yearly_sales_report(request, id):
    orders = Order.objects.filter(created_at__year = id).values('orderelate__product__product_name__product_name','orderelate__product__ram__ram','orderelate__product__color__color','orderelate__product__stock',
    total = Sum('total_price'),).annotate(dcount=Sum('orderelate__quantity')).order_by()
    today_date=str(date.today())
    context = {
        'orders':orders,
        'today_date':today_date
    }
    return render(request,'Report/SalesReport-table.html',context)






