from django.db import transaction
from chatbot.models import Conversation, Message



class ChatService():
    
    @staticmethod
    def create_conversation(user, title="New conversation"):
        return Conversation.objects.create(user=user, title=title)
    
    @staticmethod
    def  get_conversation(user, conversation_id):
        return Conversation.objects.filter(user=user, id=conversation_id).get()
    
    @staticmethod
    def add_message(conversation, role, content):
        if role not in Message.Role.values:
            raise ValueError("Invalid role")
        
        if not content or not content.strip():
            raise ValueError("Content must be provided")
        
        with transaction.atomic():
            message = Message.objects.create(conversation=conversation, role=role, content=content)
            conversation.save(update_fields=['updated_at'])
        return message
    
    
    @staticmethod
    def send_message(conversation, content, provider):
        # 1. Save user message
        ChatService.add_message(conversation, role=Message.Role.USER, content=content)
        
        # 2. Prepare conversation history
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in ChatService.get_history(conversation)
        ]
        
        # 3. Call LLM Provider
        answer = provider.generate_response(history)
        
        # 4. Save AI response
        assistant_message = ChatService.add_message(conversation, role=Message.Role.ASSISTANT, content=answer)
        return assistant_message
        
        
    @staticmethod
    def get_history(conversation):
        return conversation.messages.order_by('created_at', 'id')
    