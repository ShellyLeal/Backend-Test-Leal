"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from application import views

urlpatterns = [
    path('', views.main_page, name='mainPage'),
    #path('admin/', admin.site.urls),
    path('new-menu/', views.create_menu, name='newMenu'),
    path('appoint-meal/', views.request_lunch, name='appointMeal'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('show-menu/', views.list_menu, name='list'),
    path('edit-menu/<id>', views.edit_menu, name='edit'),
    path('delete-menu/<id>', views.delete_menu, name='delete'),
    path('delete-orders/<id>', views.delete_orders, name='deleteOrder'),
    path('requests/', views.list_requests, name='requests'),
    path('details/<id>', views.check_details, name='details'),
    path('menu/<uuid>', views.show_menu, name='menu'),
]
