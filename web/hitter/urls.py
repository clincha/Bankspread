from django.urls import path

from hitter import views

app_name = 'hitter'
urlpatterns = [
    path('', views.home, name='home'),
    path('make-sheet/', views.make_sheet, name='make-sheet'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms-of-service/', views.terms_of_service, name='terms-of-service'),
]
