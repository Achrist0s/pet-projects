from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('create/', views.article_create, name='article_create'),
]
