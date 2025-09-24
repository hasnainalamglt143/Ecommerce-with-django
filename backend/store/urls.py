from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
      path('register/',views.user_register,name='register'),
      path('login/',views.user_login,name='login'),
      path('logout',views.user_logout,name='logout'),
      path('update_user/',views.update_user,name='update-user'),
      path('update_user_info/',views.update_user_info,name='update-user-info'),
      path('change-password/', views.change_password, name='change-password'),
     
     
     
      path('product/<int:pk>/', views.product_detail, name='product-detail'),
      path('category/<str:category>/', views.category_products, name='product-category'),
      path('search/', views.search_products, name='search-products'),

]