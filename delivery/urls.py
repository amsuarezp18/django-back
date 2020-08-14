from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('list/', views.LeadListCreate),
    path('list_delivery/', views.LeadListDelivery),
    path('pointSearch/', views.ClosestPoint ),
]