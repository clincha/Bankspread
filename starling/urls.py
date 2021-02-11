from django.urls import path

from starling import views

urlpatterns = [
    path('welcome/', views.hello)
]
