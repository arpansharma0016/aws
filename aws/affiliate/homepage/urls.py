from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newsletter', views.newsletter, name='newsletter'),
    path('<str:username>/', include('website.urls')),
]