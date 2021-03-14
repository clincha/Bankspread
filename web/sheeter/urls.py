from django.urls import path

from web.sheeter import views

app_name = 'sheeter'
urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('callback/', views.callback),
]
