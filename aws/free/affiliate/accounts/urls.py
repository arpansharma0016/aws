from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('confirm_email/<str:uname>', views.confirm_email, name='confirm_email'),
    path('resend_code/<str:uname>', views.resend_code, name='resend_code'),
    path('enter_otp/<str:uname>', views.enter_otp, name='enter_otp'),
    path('enter_otp/', views.forgot_password, name='forgot_password'),
    path('new_password/<str:uname>', views.new_password, name='new_password'),
    path('resend_pass_code/<str:uname>', views.resend_pass_code, name='resend_pass_code'),
    path('logout', views.logout, name='logout'),
    path('info', views.info, name='info'),
    path('add_products', views.add_products, name='add_products'),
    path('add_banner', views.banner, name='banner'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('search', views.search, name='search'),
    path('delete/<int:pro_id>', views.delete, name='delete'),
    path('delete_pro/<int:pro_id>', views.delete_pro, name='delete_pro'),
    path('delete_banner/<int:ban_id>', views.delete_banner, name='delete_banner'),
    path('delete_widget/<int:wid_id>', views.delete_widget, name='delete_widget'),
    path('edit_product/<int:pro_id>', views.edit_product, name='edit_product'),
    path('edit_products', views.edit, name='edit'),
]
