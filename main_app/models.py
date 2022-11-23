from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Destination(models.Model):
  place = models.CharField(max_length=100)
  description = models.TextField(max_length=300)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.place}"

  def get_absolute_url(self):
    return reverse('detail', kwargs={'destination_id': self.id})

class Photo(models.Model):
  url = models.CharField(max_length=200)
  destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for destination_id: {self.destination_id} @ {self.url}"

class Comment(models.Model):
  text = models.TextField(max_length=250)
  destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def get_absolute_url(self):
    return reverse('detail', kwargs={'destination_id': self.destination.id})
