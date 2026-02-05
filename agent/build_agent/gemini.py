from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
import os
from dotenv import load_dotenv


load_dotenv()

__api_key = os.getenv("GEMINI_API_KEY")   
_gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")



# Create Gemini client using OpenAI-compatible interface
chat_client = OpenAIChatClient(
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
    api_key=_gemini_api_key,  # Ollama doesn't require an API key
    model_id=_gemini_model  # Specify the model
)


class GeminiAgent():
    def __init__(self, **kwargs):
        self.kwargs = kwargs  # store everything for later use

    def build_agent(self) -> ChatAgent:
        return ChatAgent(
            chat_client=chat_client,
            **self.kwargs  
        )



