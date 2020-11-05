from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from notes.models import Note
from notes.forms import NoteForm

@login_required
def home(request):
	user = request.user
	notes = user.notes.all()
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

@login_required
def note_detail(request, pk):
	user = request.user
	note = get_object_or_404(Note, pk=pk)
	if note.user == user:
		return render(request, 'notes/note_detail.html', {'note': note})

	return redirect('notes:home')