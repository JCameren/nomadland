import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from .models import Destination, Comment, User, Photo
from .forms import CommentForm


# Create your views here.
def home(request):
    destinations = Destination.objects.all().order_by('-id')
    return render(request, 'home.html', { 'destinations': destinations })

def destination_details(request, destination_id):
  destination = Destination.objects.get(id=destination_id)
  comment_form = CommentForm()
  comments = Comment.objects.filter(destination=destination_id)
  if Photo.objects.filter(destination=destination_id).exists():
    photo = Photo.objects.get(destination=destination_id)
  else:
    photo = None
  return render(request, 'destinations/detail.html', {
    'destination': destination, 
    'comment_form': comment_form,
    'comments': comments,
    'photo': photo
    })

class DestinationUpdate(LoginRequiredMixin, UpdateView):
  model = Destination
  fields = ['description']

class DestinationDelete(LoginRequiredMixin, DeleteView):
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

class DestinationCreate(LoginRequiredMixin, CreateView):
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

@login_required
def add_comment(request, destination_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.destination_id = destination_id
    new_comment.user_id = request.user.id
    new_comment.save()
  return redirect('detail', destination_id=destination_id)

class CommentUpdate(LoginRequiredMixin, UpdateView):
  model = Comment
  fields = ['text']

class CommentDelete(LoginRequiredMixin, DeleteView):
  model = Comment
  #success_url = 'destination/<int:destination_id>'
  def get_success_url(self):
    #destination_id = self.destination.id
    return f"/destinations/{self.object.destination.id}"

@login_required
def user_index(request, user_id):
  user_id = request.user.id
  user = User.objects.get(id=user_id)
  return render(request, 'user.html', {'user': user})

@login_required
def add_photo(request, destination_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, destination_id=destination_id)
    except Exception as e:
      print('An error occrued uploading file to S3')
      print(e)
  return redirect('detail', destination_id=destination_id)