from django.urls import path

from hitter import views

urlpatterns = [
    path('welcome/', views.welcome),
]
