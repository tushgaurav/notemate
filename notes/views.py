import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import Note
from .forms import NoteForm

def home(request):
    time = datetime.datetime.now()
    notes = Note.objects.all()[:2]
    context = {
        'notes': notes,
        'time': time
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
        'form': form,
        'notes': notes,
    }

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    return render(request, 'notes/add_note.html', context)

def deleteNote(request, note_id):
    note = Note.objects.get(id=note_id)

    if request.user != note.user:
        return HttpResponse("You don't have the persmission to delete this note.")
    if request.method == "POST":
        Note.delete(note)
        return redirect('home')

    context = {
        'note': note,
    }
    return render(request, 'notes/delete.html', context)

def updateNote(request, note_id):
    note = Note.objects.get(id=note_id)
    form = NoteForm(instance=note)

    if request.user != note.user:
        return HttpResponse("You don't have permission to edit this note.")
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)       
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'notes/update_note.html', context)