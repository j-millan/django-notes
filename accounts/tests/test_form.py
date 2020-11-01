from django.test import TestCase
from accounts.forms import SignUpForm

class SignUpFormTests(TestCase):
	def test_form_fields(self):
		expected = ['username', 'email', 'password1', 'password2']
		actual = list(SignUpForm().fields)
		self.assertListEqual(expected, actual)

	def test_form_valid_data(self):
		data = {
			'username': 'user',
			'email': 'email@gmail.com',
			'password1': 'thisisapassword21',
			'password2': 'thisisapassword21'
		}
		self.assertTrue(SignUpForm(data).is_valid())

	def test_form_invalid_data(self):
		data = {
			'username': 'user',
			'email': 'email@gmail.com',
			'password1': '123',
			'password2': '1234'
		}
		self.assertFalse(SignUpForm(data).is_valid())