import datetime
from email import message
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import Note
from .forms import NoteForm

def loginView(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if (request.method == "POST"):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User does not exist!")
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not match.")
        
    context = {
        'mode': 'Login',
        'page': 'login',            

    }
    return render(request, 'notes/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registering. Please try again.")
            
    context = {
        'form': form,
    }
    return render(request, 'notes/login_register.html', context)

def home(request):
    time = datetime.datetime.now()
    if request.user.is_authenticated:
        notes = Note.objects.filter(user = request.user)[:2]
    else:
        notes = None
    context = {
        'notes': notes,
        'time': time
    }
    return render(request, 'notes/home.html', context)

def profileView(request, username):
    user_obj = User.objects.get(username=username)
    notes = Note.objects.filter(user=user_obj)
    total_notes = notes.count()
    context = {
        'user': user_obj,
        'number': total_notes,
        'notes': notes,
    }
    return render(request, 'notes/user.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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