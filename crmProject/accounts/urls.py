from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name='customer'),
    path('registerPage', views.registerPage, name='register'),
    path('loginPage', views.loginPage, name='loginPage'), 
    path('user', views.UserPage, name='user'),
    path('logoutView', views.logoutView, name='logout'),  
    path('create_order/<str:pk>/', views.createOrder, name='createorder'),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

]