from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('api/search/', views.company_search, name = "company_search"),
    path('api/stock-data/', views.stock_data, name = "stock_data"),
]