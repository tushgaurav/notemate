from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/<username>', views.profileView, name='profile'),
    path('add/', views.createNote, name='add_note'),
]