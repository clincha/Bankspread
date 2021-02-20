from django.urls import path

from sheeter import views

urlpatterns = [
    path('callback/', views.callback),
    path('welcome/', views.welcome),
]

