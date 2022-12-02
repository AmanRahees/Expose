from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.AdminLogin, name='adminlogin'),
    path('logoutAdmin/', views.logout_admin, name='logoutAdmin'),

    path('Users/', views.UserManagement, name='Users'),
    path('user_status/<int:id>/<str:status>/', views.user_status, name='user_status'),
    path('deleteUser/<int:id>', views.deleteUser, name='deleteUser'),

    path('Orders/', views.OrderManagement, name='Orders'),
    path('Update_Order/<int:id>', views.Update_Order, name='Update_Order'),


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




    path('product/', views.ProductAttributeList, name='product'),
    path('addproduct/', views.AddProductAttribute, name='addproduct'),
    path('editproduct/<int:id>/', views.EditProductAttribute ,name='editproduct'),
    path('updateproduct/<int:id>/', views.UpdateProductAttribute ,name='updateproduct'),
    path('deleteproduct/<int:id>/', views.deleteProduct, name='deleteproduct'),
    path('enable_product/<int:id>/<str:status>/', views.enable_productAttribute, name='enable_product'),

    path('subproduct/', views.SubProductList, name='subproduct'),
    path('addsubproduct/', views.AddSubProduct, name='addsubproduct'),
    path('editsubproduct/<int:id>/', views.EditSubProduct ,name='editsubproduct'),
    path('updatesubproduct/<int:id>/', views.UpdateSubProduct ,name='updatesubproduct'),
    path('enable_subproduct/<int:id>/<str:status>/', views.enable_subproduct, name='enable_subproduct'),
    path('deletesubproduct/<int:id>/', views.deleteSubProduct, name='deletesubproduct'),

    path('variations/', views.VariationList, name='variations'),
    path('addram', views.AddRam, name='addram'),
    path('enable_ram/<int:id>/<str:status>', views.enable_ram, name='enable_ram'),
    path('deleteram/<int:id>/', views.deleteRam, name='deleteram'),

    path('addcolor', views.AddColor, name='addcolor'),
    path('enable_color/<int:id>/<str:status>', views.enable_color, name='enable_color'),
    path('deletecolor/<int:id>/', views.deleteColor, name='deletecolor'),

    path('addsize', views.AddSize, name='addsize'),
    path('enable_size/<int:id>/<str:status>', views.enable_size, name='enable_size'),
    path('deletesize/<int:id>/', views.deleteSize, name='deletesize'),


    path('OfferManage/', views.OfferManage, name='offer_manage'),
    path('addbrand_offer', views.addBrandOffer, name='add_boffer'),
    path('brndoff/<int:id>', views.deletebrandoffer, name='brndoff_del'),

    path('product_offer/', views.ProductOffer, name='prdt_offer'),
    path('addprdt_offer', views.addPrdtOffer, name='add_pdtoffer'),
    path('pdtoff/<int:id>', views.deletePdtoffer, name='pdtoff_del'),

    path('coupon/', views.CpnLIst, name='coupon'),
    path('editcoupon/', views.EditCoupon, name='editcoupon'),
    path('statuscpn/<int:id>/<str:status>/', views.StatusCoupon, name='statuscpn'),
    path('deletecpn/<int:id>/', views.deleteCpn, name='deletecpn'),
]