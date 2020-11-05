from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from notes.models import Note
from notes.views import note_detail
from .test_view_home import UserCreationTestCase
from model_bakery import baker

class NoteDetailViewTestCase(UserCreationTestCase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.url = reverse('notes:note_detail', kwargs={'pk': 1})

class NoteDetailViewTests(NoteDetailViewTestCase):
	def setUp(self):
		super().setUp()
		self.note = baker.make(Note, user=self.user)
		self.response = self.client.get(self.url)

	def test_successful_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_url_resolves_correct_view_function(self):
		view = resolve(self.url)
		self.assertEqual(view.func, note_detail)

	def test_context_object(self):
		note = self.response.context.get('note')
		self.assertEqual(note, self.note)

class NoteDetailViewIncorrectNoteTests(NoteDetailViewTestCase):
	def setUp(self):
		super().setUp()
		new_user = User.objects.create(username='newuser', email='mail@email.com', password='drowssap')
		self.random_note = baker.make(Note, user=new_user)
		self.response = self.client.get(self.url)

	def test_redirection(self):
		home_url = reverse('notes:home')
		self.assertRedirects(self.response, home_url)