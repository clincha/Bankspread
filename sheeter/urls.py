from django.urls import path

from sheeter import views

urlpatterns = [
    path('welcome/', views.welcome),
]

