from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from notes.models import Note
from notes.forms import NoteForm

@login_required
def home(request):
	notes = Note.objects.all()
	return render(request, 'notes/home.html', {'notes': notes})

@login_required
def new_note(request):
	if request.method == 'POST':
		form = NoteForm(request.POST)
		if form.is_valid():
			note = form.save(commit=False)
			note.user = request.user
			note.save()
			return redirect('notes:home')
	else:
		form = NoteForm()

	return render(request, 'notes/new_note.html', {'form': form})