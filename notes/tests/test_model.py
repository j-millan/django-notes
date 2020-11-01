from django.test import TestCase
from django.contrib.auth.models import User

from notes.models import Note
from model_bakery import baker

class NoteModelTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user', email='mail@mail.com', password='123')
		self.note1 = baker.make(Note, user=self.user)
		self.note2 = baker.make(Note, user=self.user)

	def test_can_save_and_retrieve_objects(self):

		saved_notes = Note.objects.all()
		saved_note1 = saved_notes[0]
		saved_note2 = saved_notes[1]

		self.assertEqual(self.note1, saved_note1)
		self.assertEqual(self.note2, saved_note2)

	def test_user_has_notes(self):
		self.assertTrue(hasattr(self.user, 'notes'))
		user_notes = self.user.notes.all()
		notes = Note.objects.all()
		self.assertSetEqual(user_notes, notes)

	def test_str(self):
		self.assertEqual(str(self.note1), f"{self.user.username}'s note no. {self.note1.pk}")

	def test_cascade_deletion(self):
		self.user.delete()
		self.assertFalse(Note.objects.exists())