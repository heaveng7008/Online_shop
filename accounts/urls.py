from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'accounts'
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='homepage'),

    path('products/', views.products, name='products'),
    path('create_product/', views.createProduct, name='create_product'),
    path('create_product/<int:pk>', views.updateProduct, name='update_product'),
    path('delete_product/<int:pk>', views.deleteProduct, name='delete_product'),

    path('customer/<int:pk>', views.customer, name='customer'),

    path('update_order/<int:pk>', views.updateOrder, name='update_order'),
    path('delete_order/<int:pk>', views.deleteOrder, name='delete_order'),

    path('user/', views.userHomePage, name='user_home_page'),
    path('user_orders/', views.userOrdersPage, name='user_orders_page'),
    path('user_cart/', views.userCartPage, name='user_cart_page'),
    path('user_remove_cart/<str:pk>', views.deletecartitem, name='user_cart_remove'),
    path('settings/', views.userAccountSettings, name='user_account_settings'),
]
