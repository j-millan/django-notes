from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
	COLOR_CHOICES = [
		('RED', 'red'),
		('BLU', 'blue'),
		('YEL', 'yellow'),
		('ORA', 'orange'),
		('GRE', 'green'),
		('PUR', 'purple'),
		('BRO', 'brown'),
		('FUX', 'fuxia')
	]

	content = models.TextField(max_length=350)
	user = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now_add=True)
	color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='yellow')

	def __str__(self):
		return f"{self.user.username}'s note no. {self.pk}"