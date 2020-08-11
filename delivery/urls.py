from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('list/', views.LeadListCreate),
    path('pointSearch/', views.ClosestPoint ),

]