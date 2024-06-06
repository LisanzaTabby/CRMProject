from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),
    path('createorder/', views.createOrder, name='createorder'),
    path('creatcustomer/', views.createCustomer, name='createcustomer'),

]