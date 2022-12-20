from django.urls import path
from . import views
from orders.views import *

urlpatterns = [
    path('', views.home, name='home'),

    path('profile/',views.UserSettings, name='settings'),
    path('editprofile/',views.EditProfile, name='editprofile'),
    path('updateprofile/<int:id>',views.UpdateProfile, name='updateprofile'),

    path('products/', views.store, name='products'),
    path('products/<slug:category_slug>/', views.by_category, name='by_category'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.productDetail, name= 'productDetail'),
    path('search', views.Search, name='search'),

    path('wishlist', views.wishlist, name='wishlist'),
    path('add-to-wishlist', views.AddtoWishlist, name='add-to-wishlist'),
    path('wishlist/<int:id>', views.RemoveWhishlist, name='removewishlist'),

    path('cart/', views.cart, name='cart'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('add_quantity/<int:id>', views.add_quantity, name='add_quantity'),
    path('remove_quantity/<int:id>', views.remove_quantity, name='remove_quantity'),
    path('delete_cartitem/<int:id>/', views.delete_cartitem, name='delete_cartitem'),

    path('addresses/',views.MyAddresses, name='addresses'),
    path('addaddress/', views.AddnewAddress, name='addaddress'),
    path('editaddress/<int:id>', views.EditAddress, name='editaddress'),
    path('updateaddress/<int:id>', views.UpdateAddress, name='updateaddress'),
    path('deleteaddress/<int:id>', views.deleteAddress, name='deleteaddress'),

    path('checkout/', views.checkout , name='checkout'),
    path('Orderaddress/', views.AddOrderAddress, name='Orderaddress'),
    path('seladd/<int:id>',views.SelectedAddress, name='seladd'),
    path('selcpn/<int:id>',views.SelectedCoupon, name='selcpn'),
    path('proceed-to-pay', views.razorpaycheck),
    path('placeorder', placeOrder, name='placeorder'),
    path('orderconfirmed', views.OrderConfirmed, name='orderconfirmed'),

    path('myorders/', MyOrders, name='myorders'),
    path('myorders/<int:id>', OrderView, name='vieworder'),
    path('ordersuccess/', success_order, name='ordersuccess'),
    path('cancel/<int:id>', CancelOrder, name='cancelorder'), 
    path('return/<int:id>', ReturnOrder, name='returnorder'),

    path('products/&<slug:brand_slug>/', views.by_brand, name='by_brand'),
    path('products/color=<slug:color_slug>/', views.by_color, name='by_color'),
    path('products/memory=<slug:ram_slug>/', views.by_ram, name='by_ram'),
    
    # path('review/<int:product_id>', views.ReviewSubmit, name='addreview'),
]