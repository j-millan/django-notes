from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginViewTests(TestCase):
	def setUp(self):
		login_url = reverse('auth:login')
		self.home_url = reverse('notes:home')

		username = 'user'
		password = '123'
		User.objects.create_user(username=username, email='mail@mail.com', password=password)

		self.response = self.client.post(login_url, data={'username': username, 'password': password})

	def test_user_authenticated(self):
		response = self.client.get(self.home_url)
		self.assertTrue(response.context.get('user').is_authenticated)

	def test_redirection(self):
		self.assertRedirects(self.response, self.home_url)