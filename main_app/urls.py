from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # signup url
    path('accounts/signup/', views.signup, name='signup'),
    path('destinations/<int:destination_id>/', views.destination_details, name='detail'),
    path('destinations/create/', views.DestinationCreate.as_view(), name='destinations_create'),
    path('destinations/<int:pk>/update/', views.DestinationUpdate.as_view(), name='destinations_update'),
    path('destinations/<int:pk>/delete/', views.DestinationDelete.as_view(), name='destinations_delete'),
    path('destinations/<int:destination_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comments/<int:pk>/update', views.CommentUpdate.as_view(), name='comments_update'),
    path('destinations/<int:pk>/comment_delete', views.CommentDelete.as_view(), name='comments_delete'),
    
]