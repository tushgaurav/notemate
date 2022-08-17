from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from .models import Note

def home(request):
    notes = Note.objects.all()
    context = {
        'notes': notes
    }
    return render(request, 'notes/home.html', context)