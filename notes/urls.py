from django.urls import path
from notes import views

app_name = 'notes'

urlpatterns = [
	path('', views.home, name='home'),
	path('notes/new/', views.new_note, name='new_note')
]