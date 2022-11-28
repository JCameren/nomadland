from django.contrib import admin
from .models import Destination, Comment, Photo

# Register your models here.
admin.site.register(Destination)
admin.site.register(Comment)
admin.site.register(Photo)