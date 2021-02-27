from django.urls import path

from hitter import views

app_name = 'hitter'
urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('make-sheet/', views.make_sheet, name='make-sheet')
]
