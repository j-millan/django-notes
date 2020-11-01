from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from notes.models import Note
from notes.views import home
from model_bakery import baker

class UserCreationTestCase(TestCase):
	def setUp(self):
		self.username = 'user'
		self.password = '123'
		self.user = User.objects.create_user(username=self.username, email='mail@mail.com', password=self.password)

class HomeViewTests(UserCreationTestCase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.url = reverse('notes:home')

		self.note1 = baker.make(Note, user=self.user)
		self.note2 = baker.make(Note, user=self.user)

		self.response = self.client.get(self.url)

	def test_successful_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_url_resolves_correct_view_function(self):
		view = resolve(self.url)
		self.assertEqual(view.func, home)

	def test_context_objects(self):
		notes = self.response.context.get('notes')
		self.assertTrue(notes)
		self.assertIn(self.note1, notes)
		self.assertIn(self.note2, notes)

class HomeViewLoginRequiredTests(UserCreationTestCase):
	def setUp(self):
		super().setUp()
		url = reverse('notes:home')
		self.response = self.client.get(url)

	'''def test_redirection(self):
		self.assertEqual(self.response.status_code, 302)'''
