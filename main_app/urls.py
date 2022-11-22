from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # signup url
    path('accounts/signup/', views.signup, name='signup'),
    path('destinations/<int:destination_id>/', views.destination_details, name='detail'),
    path('destinations/create/', views.DestinationCreate.as_view(), name='destinations_create'),
]