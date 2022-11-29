from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import Account
from category.models import Category
from Brand.models import Brand
from products.forms import *
from category.forms import *
from Brand.forms import AddBrandForm
from products.models import *
from orders.models import *
from orders.forms import OrderStatus
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
# Create your views here.

@never_cache
def AdminLogin(request):
    if request.user.is_authenticated:
        return redirect('/admin_panel')
    else:
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



@never_cache
@login_required(login_url='adminlogin')
def logout_admin(request):
    logout(request)
    return redirect('/admin_panel/login')

#---------------------Dahsboard View--------------------#

@never_cache
@login_required(login_url='adminlogin')
def dashboard(request):
    users = Account.objects.filter(is_superadmin = False)
    orders = Order.objects.all().exclude(status='Completed')
    context={
        'users':users,
        'orders':orders,
    }
    return render(request, 'Dashboard.html', context)


#----------------------Dashboard End------------------#

#----------------------UserManagement View------------------#

@never_cache
@login_required(login_url='adminlogin')
def UserManagement(request):
    users = Account.objects.filter(is_superadmin = False)
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
@login_required(login_url='adminlogin')
def user_status(request,id,status):
    users = Account.objects.get(id=id)
    if status == 'true':  
        users.is_active = True
    elif status == 'false':
        users.is_active = False
    users.save()
    return redirect('Users')

@never_cache
@login_required(login_url='adminlogin')
def deleteUser(request,id):
    users = Account.objects.get(id=id)
    users.delete()
    return redirect('Users')

#----------------------Usermanagement End------------------#

#----------------------OrderManagement View------------------#

@never_cache
@login_required(login_url='adminlogin')
def OrderManagement(request):
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
@login_required(login_url='adminlogin')
def categoryList(request):
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
@login_required(login_url='adminlogin')
def AddCategory(request):
    if request.method == "POST":
        form = AddCategoryForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category')
        else:
            print('error')
            return redirect('addcategory')
    else:
        form = AddCategoryForm()
    context={
        "form":form
    }
    return render(request, 'backend/AddCategory.html', context)

@never_cache
@login_required(login_url='adminlogin')
def EditCategory(request,id):
    ctgy = Category.objects.get(id=id)
    return render(request,'backend/EditCategory.html', {'ctgy':ctgy}) 

@never_cache
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def DeleteCategory(request, id):
    ctgy = Category.objects.filter(id=id)
    ctgy.delete()
    return redirect('category')

#------------------Category End----------------------#

#------------------SubCategory View------------------#

@never_cache
@login_required(login_url='adminlogin')
def SubCategoryList(request):
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
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def EditSubCategory(request,id):
    subctgy = SubCategory.objects.get(id=id)
    context = {
        'subctgy':subctgy
    }
    return render(request,'backend/EditSubCategory.html', context) 

@never_cache
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def DeleteSubCategory(request, id):
    subctgy = SubCategory.objects.filter(id=id)
    subctgy.delete()
    return redirect('subcategory')

#------------------SubCategory End------------------#

#-----------------Brand View-------------------------#

@never_cache
@login_required(login_url='adminlogin')
def brandList(request):
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
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def EditBrand(request, id):  
    brnd = Brand.objects.get(id=id)  
    context={
        'brnd':brnd
    }
    return render(request,'backend/EditBrand.html', context)

@never_cache
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def DeleteBrand(request, id):
    brnd = Brand.objects.filter(id=id)
    brnd.delete()
    return redirect('brand')

@never_cache
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def ProductAttributeList(request):
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
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def deleteProduct(request, id):
    prdts = ProductAttribute.objects.filter(id=id)
    prdts.delete()
    return redirect('product')

@never_cache
@login_required(login_url='adminlogin')
def EditProductAttribute(request, id):  
    prdts = ProductAttribute.objects.get(id=id)  
    context = {
        'prdts':prdts
    }
    return render(request,'Product/EditProduct.html', context) 

@never_cache
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def SubProductList(request):
    subprdts = Products.objects.all().order_by('-id')
    paginator = Paginator(subprdts, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'subprdts':paged_products,
    }
    return render(request, 'Product/SubProduct.html', context)

@never_cache
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def EditSubProduct(request, id):  
    subprdts = Products.objects.get(id=id)  
    context = {
        'subprdts':subprdts
    }
    return render(request,'Product/EditSubProduct.html', context) 

@never_cache
@login_required(login_url='adminlogin')
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
@login_required(login_url='adminlogin')
def enable_subproduct(request,id,status):
    subprdts = Products.objects.get(id=id)
    if status == 'true':  
        subprdts.is_available = True
    elif status == 'false':
        subprdts.is_available = False
    subprdts.save()
    return redirect('subproduct')

@never_cache
@login_required(login_url='adminlogin')
def deleteSubProduct(request, id):
    subprdts = Products.objects.filter(id=id)
    subprdts.delete()
    return redirect('subproduct')

#---------------------SubPRoduct End-----------------#

#--------------------Variation View------------------#

@never_cache
@login_required(login_url='adminlogin')
def VariationList(request):
    ram = Ram.objects.all().order_by('-id')
    size = Size.objects.all().order_by('-id')
    color = Color.objects.all().order_by('-id')
    clrcnt = color.count()
    paginator = Paginator(color, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'ram':ram,
        'size':size,
        'color':paged_products,
        'clrcnt':clrcnt
    }
    return render(request, 'Product/variations.html',context)

@never_cache
@login_required(login_url='adminlogin')
def AddRam(request):
    if request.method == "POST":
        form = AddRamForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('variations')
        else:
            messages.info(request, 'Ram already Added')
            return redirect('addram')
    else:
        form = AddRamForm()
    context = {
        'form': form,
        }
    return render(request, 'Product/AddVariation.html', context)


@never_cache
@login_required(login_url='adminlogin')
def enable_ram(request,id,status):
    ram = Ram.objects.get(id=id)
    if status == 'true':  
        ram.is_acitve = True
    elif status == 'false':
        ram.is_acitve = False
    ram.save()
    return redirect('variations')

@never_cache
@login_required(login_url='adminlogin')
def deleteRam(request,id):
    ram = Ram.objects.filter(id=id)
    ram.delete()
    return redirect('variations')


@never_cache
@login_required(login_url='adminlogin')
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

@never_cache
@login_required(login_url='adminlogin')
def enable_color(request,id,status):
    color = Color.objects.get(id=id)
    if status == 'true':  
        color.is_acitve = True
    elif status == 'false':
        color.is_acitve = False
    color.save()
    return redirect('variations')

@never_cache
@login_required(login_url='adminlogin')
def deleteColor(request,id):
    color = Color.objects.filter(id=id)
    color.delete()
    return redirect('variations')


@never_cache
@login_required(login_url='adminlogin')
def AddSize(request):
    if request.method == "POST":
        form = AddSizeForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('variations')
        else:
            messages.info(request, 'Ram already Added')
            return redirect('addsize')
    else:
        form = AddSizeForm()
    context = {
        'form': form,
        }
    return render(request, 'Product/AddVariation.html', context)

@never_cache
@login_required(login_url='adminlogin')
def enable_size(request,id,status):
    size = Size.objects.get(id=id)
    if status == 'true':  
        size.is_acitve = True
    elif status == 'false':
        size.is_acitve = False
    size.save()
    return redirect('variations')

@never_cache
@login_required(login_url='adminlogin')
def deleteSize(request,id):
    size = Size.objects.filter(id=id)
    size.delete()
    return redirect('variations')


#--------------------Variation End-----------------#




