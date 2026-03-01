from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.product_add, name='product_add'),
    path('edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.order_add, name='order_add'),
    path('orders/edit/<int:pk>/', views.order_edit, name='order_edit'),
    path('orders/delete/<int:pk>/', views.order_delete, name='order_delete'),
]