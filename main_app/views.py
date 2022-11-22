import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Destination, Comment
from .forms import CommentForm


# Create your views here.
def home(request):
    destinations = Destination.objects.all().order_by('-id')
    return render(request, 'home.html', { 'destinations': destinations })

def destination_details(request, destination_id):
  destination = Destination.objects.get(id=destination_id)
  comment_form = CommentForm()
  comments = Comment.objects.all()
  return render(request, 'destinations/detail.html', {
    'destination': destination, 
    'comment_form': comment_form,
    'comments': comments,
    })

class DestinationUpdate(UpdateView):
  model = Destination
  fields = ['description']

class DestinationDelete(DeleteView):
  model = Destination
  success_url = '/'

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


# class CommentCreate(CreateView):
#   model = Comment
#   fields = ['text']
  
#   def form_valid(self, form, destination_id):
#     form.instance.user = self.request.user
#     form.instance.destination = destination_id
#     return super().form_valid(form)

def add_comment(request, destination_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.destination_id = destination_id
    new_comment.user_id = request.user.id
    new_comment.save()
  return redirect('detail', destination_id=destination_id)