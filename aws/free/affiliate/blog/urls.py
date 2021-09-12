from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:id>/', views.blogg, name='blogg'),
    path('add_comment-<int:id>/', views.add_comment, name='add_comment'),
    path('<int:id>/<str:name>/', views.blog_detail, name='blog_detail'),
]