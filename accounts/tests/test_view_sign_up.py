from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from accounts.forms import SignUpForm
from accounts.views import sign_up

class SignUpViewTests(TestCase):
	def setUp(self):
		self.url = reverse('auth:sign_up')
		self.response = self.client.get(self.url)

	def test_successful_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_url_resolves_correct_view_function(self):
		view = resolve(self.url)
		self.assertEqual(view.func, sign_up)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, SignUpForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input type="text"', 1)
		self.assertContains(self.response, '<input type="email"', 1)
		self.assertContains(self.response, '<input type="password"', 2)

class SignUpViewSuccessfulPostRequestTests(TestCase):
	def setUp(self):
		url = reverse('auth:sign_up')
		data = {
			'username': 'user',
			'email': 'email@gmail.com',
			'password1': 'thisisapassword21',
			'password2': 'thisisapassword21'
		}
		self.response = self.client.post(url, data)

	def test_redirection(self):
		home_url = reverse('notes:home')
		self.assertRedirects(self.response, home_url)

	def test_user_created(self):
		self.assertTrue(User.objects.exists())

	def test_user_authenticated(self):
		response = self.client.get(reverse('notes:home'))
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)

class SignUpViewInvalidPostRequestTests(TestCase):
	def setUp(self):
		url = reverse('auth:sign_up')
		self.response = self.client.post(url, {})

	def test_redirection(self):
		self.assertEquals(self.response.status_code, 200)

	def test_user_not_created(self):
		self.assertFalse(User.objects.exists())

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)
		