from django.urls import path

from sheeter import views

app_name = 'sheeter'
urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('callback/', views.callback),
]
