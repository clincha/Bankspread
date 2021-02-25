from django.urls import path

from hitter import views

app_name = 'hitter'
urlpatterns = [
    path('welcome/', views.welcome),
]
