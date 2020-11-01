from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

from accounts.forms import SignUpForm

def sign_up(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('notes:home')
	else:
		form = SignUpForm()

	return render(request, 'accounts/sign_up.html', {'form': form})