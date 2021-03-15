from django.urls import path

from starling import views

app_name = 'starling'
urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('callback/', views.callback, name='callback'),
    path('transactions/', views.transactions, name='transactions'),
]
