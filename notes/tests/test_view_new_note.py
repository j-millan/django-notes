from django.test import TestCase
from django.urls import reverse, resolve

from notes.models import Note
from notes.forms import NoteForm
from notes.views import new_note
from .test_view_home import UserCreationTestCase

class CreateNoteViewTestCase(UserCreationTestCase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.url = reverse('notes:new_note')

class CreateNoteViewTests(CreateNoteViewTestCase):
	def setUp(self):
		super().setUp()
		self.response = self.client.get(self.url)

	def test_successful_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_url_resolves_correct_view_function(self):
		view = resolve(self.url)
		self.assertEqual(view.func, new_note)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, NoteForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<textarea', 1)
		self.assertContains(self.response, '<select', 1)

class CreateNoteLoginRequiredTests(UserCreationTestCase):
	def setUp(self):
		super().setUp()
		self.url = reverse('notes:new_note')
		self.response = self.client.get(self.url)

	def test_redirection(self):
		login_url = reverse('auth:login')
		self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class CreateNoteValidPostDataTests(CreateNoteViewTestCase):
	def setUp(self):
		super().setUp()
		data = {
			'content': 'This is a note.',
			'color': 'YEL'
		}
		self.response = self.client.post(self.url, data)

	def test_redirection(self):
		home_url = reverse('notes:home')
		self.assertRedirects(self.response, home_url)

	def test_note_created(self):
		self.assertTrue(Note.objects.exists())

class CreateNoteInvalidPostDataTests(CreateNoteViewTestCase):
	def setUp(self):
		super().setUp()
		self.response = self.client.post(self.url, {})

	def test_redirection(self):
		self.assertEqual(self.response.status_code, 200)

	def test_note_not_created(self):
		self.assertFalse(Note.objects.exists())

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)