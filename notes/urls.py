from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/<username>', views.profileView, name='profile'),
    path('add/', views.createNote, name='add_note'),
    path('delete/<note_id>', views.deleteNote, name='delete'),
    path('edit/<note_id>', views.updateNote, name='edit'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.registerUser, name='signup'),
]