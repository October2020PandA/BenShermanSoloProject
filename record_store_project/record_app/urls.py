from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns =[
    path('', views.index),
    path('equipment', views.equipment),
    path('records', views.records),
    path('item/<int:product_id>', views.item),
    path('item/<int:product_id>/add_to_cart', views.add_to_cart),
    path('login_page', views.login_page),
    path('register_page', views.register_page),
    path('login', views.login),
    path('register', views.register),
    path('confirmation', views.confirmation),
    path('add', views.add_product),
    path('checkout', views.checkout),
    path('orders', views.orders),
    path('products', views.products),
    path('checkout/<int:orderitem_id>/delete', views.delete),
    path('logout', views.logout),
    path('logout_page', views.logout_page),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)