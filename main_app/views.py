import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Destination


# Create your views here.
def home(request):
    destinations = Destination.objects.all().order_by('-id')
    return render(request, 'home.html', { 'destinations': destinations })

def destination_details(request, destination_id):
  destination = Destination.objects.get(id=destination_id)
  return render(request, 'destinations/detail.html', {'destination': destination})
#def some_function(request):
  #secret_key = os.environ['SECRET_KEY']

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # automatically login new user
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign-up. Try again.'
  # A bad POST or GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class DestinationCreate(CreateView):
  model = Destination
  fields = ['place', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)