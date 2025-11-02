from django.urls import path
from gallery.views import Gallery, CreatePost , PostDetails, EditPost, DeleteComment
urlpatterns = [
    path('list/', Gallery.as_view(), name='gallery'),
    path('create-post/', CreatePost.as_view(), name='create_post'),
    path('edit-post/<int:pk>', EditPost.as_view(), name='edit_post'),
    path('post-details/<int:pk>', PostDetails.as_view(), name='post_details'),
    path('delete-comment/<int:pk>', DeleteComment.as_view(), name='delete_comment')

]