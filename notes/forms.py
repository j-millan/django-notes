from django import forms
from notes.models import Note

class NoteForm(forms.ModelForm):
	color = forms.Select()

	class Meta:
		model = Note
		fields = ['content', 'color']