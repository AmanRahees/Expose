from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import Account
from category.models import Category
from Brand.models import Brand
from products.forms import AddProductForm, EditProductForm, AddVariationForm, EditVariationForm, AddSubCategoryForm, EditSubCategoryForm
from category.forms import AddCategoryForm, EditCategoryForm
from Brand.forms import AddBrandForm
from products.models import Products, Variation, SubCategory
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
                    return render(request, 'adminLogin.html')
            else:
                messages.info(request, 'Invalid Username or Password')
                return render(request, 'adminLogin.html')
        else:        
            return render(request, 'adminLogin.html')



@never_cache
@login_required(login_url='/admin_panel/login')
def logout_admin(request):
    logout(request)
    return redirect('/admin_panel/login')

#---------------------Dahsboard View--------------------#

@never_cache
@login_required(login_url='/admin_panel/login')
def dashboard(request):
    users = Account.objects.filter(is_superadmin = False)
    context={
        'users':users
    }
    return render(request, 'Dashboard.html', context)


#----------------------Dashboard End------------------#

#----------------------UserManagement View------------------#

@never_cache
@login_required(login_url='/admin_panel/login')
def UserManagement(request):
    users = Account.objects.filter(is_superadmin = False)
    context={
        'users':users
    }
    return render(request, 'accounts/UserManage.html', context)

def user_status(request,id,status):
    users = Account.objects.get(id=id)
    if status == 'true':  
        users.is_active = True
    elif status == 'false':
        users.is_active = False
    users.save()
    return redirect('Users')

def deleteUser(request,id):
    users = Account.objects.get(id=id)
    users.delete()
    return redirect('Users')

#----------------------Usermanagement End------------------#

#----------------------OrderManagement View------------------#

@never_cache
@login_required(login_url='/admin_panel/login')
def OrderManagement(request):
    return render(request, 'OrderManage.html')

#----------------------OrderManagement End------------------#

#---------------------Category View-----------------#

@never_cache
@login_required(login_url='/admin_panel/login')
def categoryList(request):
    ctgy = Category.objects.all().order_by('-id')
    context = {
        "ctgy":ctgy,
    }
    return render(request, 'backend/category.html', context)

@never_cache
@login_required(login_url='/admin_panel/login')
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
@login_required(login_url='/admin_panel/login')
def EditCategory(request,id):
    ctgy = Category.objects.get(id=id)
    return render(request,'backend/EditCategory.html', {'ctgy':ctgy}) 

@never_cache
@login_required(login_url='/admin_panel/login')
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
@login_required(login_url='/admin_panel/login')
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
@login_required(login_url='/admin_panel/login')
def DeleteCategory(request, id):
    ctgy = Category.objects.filter(id=id)
    ctgy.delete()
    return redirect('category')

#------------------Category End----------------------#

#------------------SubCategory View------------------#

@never_cache
@login_required(login_url='/admin_panel/login')
def SubCategoryList(request):
    subctgy = SubCategory.objects.all().order_by('-id')
    context = {
        "subctgy" : subctgy
    }
    return render(request, 'backend/Subcategory.html', context)

@never_cache
@login_required(login_url='/admin_panel/login')
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
@login_required(login_url='/admin_panel/login')
def EditSubCategory(request,id):
    subctgy = SubCategory.objects.get(id=id)
    context = {
        'subctgy':subctgy
    }
    return render(request,'backend/EditSubCategory.html', context) 

@never_cache
@login_required(login_url='/admin_panel/login')
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
@login_required(login_url='/admin_panel/login')
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
@login_required(login_url='/admin_panel/login')
def DeleteSubCategory(request, id):
    subctgy = SubCategory.objects.filter(id=id)
    subctgy.delete()
    return redirect('subcategory')

#------------------SubCategory End------------------#

#-----------------Brand View-------------------------#

@never_cache
@login_required(login_url='/admin_panel/login')
def brandList(request):
    brnd = Brand.objects.all().order_by('-id')
    context = {
        "brnd" : brnd
    }
    return render(request, 'backend/Brands.html', context)

@never_cache
@login_required(login_url='/admin_panel/login')
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
@login_required(login_url='/admin_panel/login')
def EditBrand(request, id):  
    brnd = Brand.objects.get(id=id)  
    context={
        'brnd':brnd
    }
    return render(request,'backend/EditBrand.html', context)

@never_cache
@login_required(login_url='/admin_panel/login')
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
@login_required(login_url='/admin_panel/login')
def DeleteBrand(request, id):
    brnd = Brand.objects.filter(id=id)
    brnd.delete()
    return redirect('brand')

@never_cache
@login_required(login_url='/admin_panel/login')
def enable_brand(request,id,status):
    brnd = Brand.objects.get(id=id)
    if status == 'true':  
        brnd.is_available = True
    elif status == 'false':
        brnd.is_available = False
    brnd.save()
    return redirect('brand') 

#------------------Brand End------------------------#

#-------------------Product Views---------------#

@never_cache
@login_required(login_url='/admin_panel/login')
def productList(request):
    prdts = Products.objects.all().order_by('-id')
    subprdts = Variation.objects.all().order_by('-id')
    context = {
        "prdts": prdts,
        "subprdts":subprdts
    }
    return render(request, 'products.html', context)

@never_cache
@login_required(login_url='/admin_panel/login')
def AddProduct(request):
    if request.method == "POST":
        form = AddProductForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')
        else:
            messages.info(request, 'Product already Added')
            return redirect('addproduct')
    else:
        form = AddProductForm()
    context = {
        'form': form,
        }
    return render(request, 'AddProduct.html', context)

@never_cache
@login_required(login_url='/admin_panel/login')
def deleteProduct(request, id):
    prdts = Products.objects.filter(id=id)
    prdts.delete()
    return redirect('product')

@never_cache
@login_required(login_url='/admin_panel/login')
def EditProduct(request, id):  
    prdts = Products.objects.get(id=id)  
    context = {
        'prdts':prdts
    }
    return render(request,'EditProduct.html', context) 

@never_cache
@login_required(login_url='/admin_panel/login')
def UpdateProduct(request, id):
    prdts = Products.objects.get(id=id)  
    form = EditProductForm(request.POST, instance = prdts)
    if form.is_valid():  
        form.save()  
        return redirect("product")  
    context = {
        'prdts': prdts
    }  
    return render(request, 'EditProduct.html', context) 

@never_cache
@login_required(login_url='/admin_panel/login')
def enable_product(request,id,status):
    prdts = Products.objects.get(id=id)
    if status == 'true':  
        prdts.is_available = True
    elif status == 'false':
        prdts.is_available = False
    prdts.save()
    return redirect('product') 

#---------------------Variation View-----------------#

@never_cache
@login_required(login_url='/admin_panel/login')
def SubProductList(request):
    subprdts = Variation.objects.all().order_by('-id')
    context = {
        "subprdts":subprdts
    }
    return render(request, 'backend/Variation.html', context)

@never_cache
@login_required(login_url='/admin_panel/login')
def AddVariation(request):
    if request.method == "POST":
        form = AddVariationForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subproduct')
        else:
            messages.info(request, 'Already Added')
            return redirect('addsubproduct')
    else:
        form = AddVariationForm()
    context = {
        'form': form,
        }
    return render(request, 'backend/AddVariation.html', context)

@never_cache
@login_required(login_url='/admin_panel/login')
def EditSubProduct(request, id):  
    subprdts = Variation.objects.get(id=id)  
    context = {
        'subprdts':subprdts
    }
    return render(request,'backend/EditVariation.html', context) 

@never_cache
@login_required(login_url='/admin_panel/login')
def UpdateSubProduct(request, id):
    subprdts = Variation.objects.get(id=id)  
    form = EditVariationForm(request.POST, instance = subprdts)
    if form.is_valid():  
        form.save()  
        return redirect("subproduct")  
    context = {
        'subprdts': subprdts
    }  
    return render(request, 'backend/EditVariation.html', context)


@never_cache
@login_required(login_url='/admin_panel/login')
def enable_subproduct(request,id,status):
    subprdts = Variation.objects.get(id=id)
    if status == 'true':  
        subprdts.is_acitve = True
    elif status == 'false':
        subprdts.is_acitve = False
    subprdts.save()
    return redirect('subproduct') 

@never_cache
@login_required(login_url='/admin_panel/login')
def deleteSubProduct(request, id):
    subprdts = Variation.objects.filter(id=id)
    subprdts.delete()
    return redirect('subproduct')

#---------------------Variation End-----------------#


