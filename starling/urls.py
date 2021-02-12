from django.urls import path

from starling import views

urlpatterns = [
    path('welcome/', views.welcome),
    path('callback/', views.callback),
    path('transactions/', views.transactions),
]
