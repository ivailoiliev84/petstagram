from django.urls import path
from .views import ChatMessageView

urlpatterns = [
    path("api/messages/", ChatMessageView.as_view(), name="chat_message"),
]