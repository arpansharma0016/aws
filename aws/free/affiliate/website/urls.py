from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.dynamic, name="dynamic"),
    path('<str:username>-<str:pro_id>/<str:product_slug>', views.product, name="product"),
] 

