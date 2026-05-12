from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    
    # Объявления
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ad/create/', views.ad_create, name='ad_create'),
    path('ad/<int:pk>/edit/', views.ad_edit, name='ad_edit'),
    path('ad/<int:pk>/delete/', views.ad_delete, name='ad_delete'),
    path('ad/<int:pk>/toggle/', views.ad_toggle_status, name='ad_toggle_status'),
    
    # Мои объявления
    path('my-ads/', views.my_ads, name='my_ads'),
    
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='ads/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
