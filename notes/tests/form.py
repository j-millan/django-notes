from django.test import TestCase
from django.contrib.auth.models import User

from notes.models import Note
from notes.forms import NoteForm
from .view import UserCreationTestCase

class NoteFormTests(UserCreationTestCase):
	def setUp(self):
		super().setUp()

	def test_form_fields(self):
		expected = ['content', 'color']
		actual = list(NoteForm().fields)
		self.assertListEqual(expected, actual)

	def test_form_valid_data(self):
		data = {'content': 'Hello this is contentllo this is contentllo this is contentllo this is content.', 'color': 'RED'}
		form = NoteForm(data)
		self.assertTrue(form.is_valid())

	def test_form_invalid_data(self):
		self.assertFalse(NoteForm().is_valid())