from django.urls import path

from web.starling import views

app_name = 'starling'
urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('callback/', views.callback),
    path('transactions/', views.transactions),
]
