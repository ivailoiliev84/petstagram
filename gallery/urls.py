from django.urls import path
from gallery.views import Gallery, CreatePost , PostDetails, EditPost
urlpatterns = [
    path('list/', Gallery.as_view(), name='gallery'),
    path('create-post/', CreatePost.as_view(), name='create_post'),
    path('edit-post/<int:pk>', EditPost.as_view(), name='edit_post'),
    path('psot-details/<int:pk>', PostDetails.as_view(), name='post_details'),

]