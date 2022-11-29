from django.urls import path
from . import views
from orders.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('settings/',views.UserSettings, name='settings'),
    path('products/', views.store, name='products'),
    path('products/<slug:category_slug>/', views.by_category, name='by_category'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.productDetail, name= 'productDetail'),
    path('search', views.Search, name='search'),

    path('cart/', views.cart, name='cart'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('delete_cartitem/<int:id>/', views.delete_cartitem, name='delete_cartitem'),
    path('cart_update', views.cart_update, name='cart_update'),

    path('addresses/',views.MyAddresses, name='addresses'),
    path('addaddress/', views.AddnewAddress, name='addaddress'),
    path('editaddress/<int:id>', views.EditAddress, name='editaddress'),
    path('updateaddress/<int:id>', views.UpdateAddress, name='updateaddress'),
    path('deleteaddress/<int:id>', views.deleteAddress, name='deleteaddress'),

    path('checkout/', views.checkout , name='checkout'),
    path('Orderaddress/', views.AddOrderAddress, name='Orderaddress'),
    path('seladd/<int:id>',views.SelectedAddress, name='seladd'),
    path('proceed-to-pay', views.razorpaycheck),
    path('placeorder', placeOrder, name='placeorder'),
    path('orderconfirmed', views.OrderConfirmed, name='orderconfirmed'),

    path('myorders/', MyOrders, name='myorders'),
    path('myorders/<int:id>', OrderView, name='vieworder'),
    path('cancel/<int:id>', CancelOrder, name='cancelorder'),
    path('return/<int:id>', ReturnOrder, name='returnorder'),
]