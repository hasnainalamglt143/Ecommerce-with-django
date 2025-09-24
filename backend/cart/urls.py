from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.cart_summary,name='cart_summary'),
    path('add/',views.cart_add,name='cart-add'),
    path('delete/',views.cart_remove,name='cart-remove'),
    path('update/',views.cart_update,name='cart-update'),
    

    

   

]