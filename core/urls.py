from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('Users/', views.UserManagement, name='Users'),
    path('user_status/<int:id>/<str:status>/', views.user_status, name='user_status'),
    path('deleteUser/<int:id>', views.deleteUser, name='deleteUser'),

    path('Orders/', views.OrderManagement, name='Orders'),

    path('category/', views.categoryList, name='category' ),
    path('addcategory/',views.AddCategory, name='addcategory'),
    path('editcategory/<int:id>', views.EditCategory ,name='editcategory'),
    path('updatecategory/<int:id>', views.UpdateCategory ,name='updatecategory'),
    path('deletecategory/<int:id>', views.DeleteCategory, name='deletecategory'),
    path('enable_category/<int:id>/<str:status>', views.enable_category, name='enable_category'),

    path('subcategory/', views.SubCategoryList, name='subcategory' ),
    path('addsubcategory/',views.AddSubCategory, name='addsubcategory'),
    path('editsubcategory/<int:id>', views.EditSubCategory ,name='editsubcategory'),
    path('updatesubcategory/<int:id>', views.UpdateSubCategory ,name='updatesubcategory'),
    path('enable_subcategory/<int:id>/<str:status>', views.enable_subcategory, name='enable_subcategory'),
    path('deletesubcategory/<int:id>', views.DeleteSubCategory, name='deletesubcategory'),

    path('brand/', views.brandList, name='brand'),
    path('addbrand/', views.AddBrand, name='addbrand'),
    path('editbrand/<int:id>/', views.EditBrand ,name='editbrand'),
    path('updatebrand/<int:id>/', views.UpdateBrand ,name='updatebrand'),
    path('deletebrand/<int:id>/', views.DeleteBrand, name='deletebrand'),
    path('enable_brand/<int:id>/<str:status>/', views.enable_brand, name='enable_brand'),

    path('product/', views.productList, name='product'),
    path('addproduct/', views.AddProduct, name='addproduct'),
    path('editproduct/<int:id>/', views.EditProduct ,name='editproduct'),
    path('updateproduct/<int:id>/', views.UpdateProduct ,name='updateproduct'),
    path('deleteproduct/<int:id>/', views.deleteProduct, name='deleteproduct'),
    path('enable_product/<int:id>/<str:status>/', views.enable_product, name='enable_product'),

    path('subproduct/', views.SubProductList, name='subproduct'),
    path('addsubproduct/', views.AddVariation, name='addsubproduct'),
    path('editsubproduct/<int:id>/', views.EditSubProduct ,name='editsubproduct'),
    path('updatesubproduct/<int:id>/', views.UpdateSubProduct ,name='updatesubproduct'),
    path('enable_subproduct/<int:id>/<str:status>/', views.enable_subproduct, name='enable_subproduct'),
    path('deletesubproduct/<int:id>/', views.deleteSubProduct, name='deletesubproduct'),


    path('login/', views.AdminLogin, name='adminlogin'),
    path('logoutAdmin/', views.logout_admin, name='logoutAdmin'),
]