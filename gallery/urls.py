from django.urls import path
from gallery.views import Gallery, CreatePost
urlpatterns = [
    path('list/', Gallery.as_view(), name='gallery'),
    path('create-post', CreatePost.as_view(), name='create_post')
]