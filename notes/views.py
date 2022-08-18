from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import Note
from .forms import NoteForm

def home(request):
    notes = Note.objects.all()
    context = {
        'notes': notes
    }
    return render(request, 'notes/home.html', context)

def profileView(request, username):
    user = User.objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'notes/user.html', context)

def createNote(request):
    notes = Note.objects.all()
    form = NoteForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    return render(request, 'notes/add_note.html', context)