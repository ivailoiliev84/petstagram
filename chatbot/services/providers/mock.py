from chatbot.services.providers.base import BaseLLMProvider


class MockLLMProvider(BaseLLMProvider):

    def generate_response(self, messages: list[dict]) -> str:
        last_message = messages[-1]["content"]

        return (
            f"Mock AI response to: {last_message}"
        )
