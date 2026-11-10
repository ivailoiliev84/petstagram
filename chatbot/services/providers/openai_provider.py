
from django.conf import settings
from openai import OpenAI

from chatbot.services.providers.base import BaseLLMProvider


SYSTEM_PROMPT = """
You are the Petstagram AI Assistant.

You help users with:
- General pet care questions.
- Using the Petstagram application.

Be friendly and concise.
Do not invent Petstagram features.
For serious pet health concerns, recommend a veterinarian.
"""


class OpenAIProvider(BaseLLMProvider):

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=20.0,
            max_retries=1,
        )
        self.model = settings.OPENAI_CHAT_MODEL

    def generate_response(self, messages: list[dict]) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=messages,
            store=False,
        )

        answer = response.output_text

        if not answer:
            raise RuntimeError("LLM returned an empty response")

        return answer
