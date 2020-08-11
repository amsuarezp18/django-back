from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('list/', views.LeadListCreate.as_view()),
    path('pointSearch/', views.ClosestPoint ),

]