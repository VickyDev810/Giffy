from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
import os
from dotenv import load_dotenv

load_dotenv()

model = os.getenv("OPENROUTER_MODEL", "llama3.1:8b")   
api_key = os.getenv("OPENROUTER_API_KEY")
# Create Ollama client using OpenAI-compatible interface
chat_client = OpenAIChatClient(
    base_url='https://openrouter.ai/api/v1',
    api_key=api_key,  # Ollama doesn't require an API key
    model_id=model  # Specify the model
)

class OpenRouterAgent():
    def __init__(self, **kwargs):
        self.kwargs = kwargs  # store everything for later use

    def build_agent(self) -> ChatAgent:
        return ChatAgent(
            chat_client=chat_client,
            **self.kwargs  
        )
