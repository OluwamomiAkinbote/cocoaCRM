from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('', views.index, name='index'),
    path('add_order/', views.add_order, name='add_order'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('product/', views.product_list, name='product_list'),
    path('product-entries/', views.product_entries, name='product_entries'),
    path('add_entry/', views.add_entry, name='add_entry'),
    path('add_product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('states/', views.states, name='states'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('restore_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('schedule_order/<int:order_id>/', views.schedule_order, name='schedule_order'),
    path('deliver_order/<int:order_id>/', views.deliver_order, name='deliver_order'),

]
