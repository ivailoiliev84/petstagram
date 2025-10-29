from django.urls import path
from gallery.views import Gallery
urlpatterns = [
    path('posts/', Gallery.as_view(), name='gallery')
]