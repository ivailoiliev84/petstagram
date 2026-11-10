import json
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from chatbot.models import Conversation
from chatbot.services.chat import ChatService
from chatbot.services.providers.mock import MockLLMProvider


class ChatMessageView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400,
            )

        if not isinstance(data, dict):
            return JsonResponse(
                {"error": "Expected JSON object"},
                status=400,
            )

        content = data.get("message")
        conversation_id = data.get("conversation_id")

        if not isinstance(content, str) or not content.strip():
            return JsonResponse(
                {"error": "Message cannot be empty"},
                status=400,
            )

        content = content.strip()

        if len(content) > 2000:
            return JsonResponse(
                {"error": "Message is too long"},
                status=400,
            )

        if conversation_id is not None:
            if type(conversation_id) is not int or conversation_id < 1:
                return JsonResponse(
                    {"error": "Invalid conversation ID"},
                    status=400,
                )

            try:
                conversation = ChatService.get_conversation(
                    user=request.user,
                    conversation_id=conversation_id,
                )
            except Conversation.DoesNotExist:
                return JsonResponse(
                    {"error": "Conversation not found"},
                    status=404,
                )
        else:
            conversation = ChatService.create_conversation(
                user=request.user,
            )

        provider = MockLLMProvider()

        try:
            answer = ChatService.send_message(
                conversation=conversation,
                content=content,
                provider=provider,
            )
        except Exception:
            return JsonResponse(
                {"error": "Unable to generate AI response"},
                status=503,
            )

        return JsonResponse({
            "conversation_id": conversation.id,
            "message_id": answer.id,
            "role": answer.role,
            "content": answer.content,
        })
