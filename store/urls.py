from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('settings/',views.UserSettings, name='settings'),
    path('products/', views.store, name='products'),
    path('products/<slug:category_slug>/', views.by_category, name='by_category'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.productDetail, name= 'productDetail'),
    path('search', views.Search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>', views.remove_cart, name='remove_cart'),
    path('delete_item/<int:product_id>/<int:cart_item_id>', views.delete_cart_item, name='delete_item'),
    path('checkout/', views.demo , name='checkout')
]