from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin_/', admin.site.urls),
    path('',include('store.urls')),
    path('accounts/',include('accounts.urls')),
    path('admin/',include('core.urls')),
    path('cart/', include('orders.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
