from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
import os

model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")   
# Create Ollama client using OpenAI-compatible interface
chat_client = OpenAIChatClient(
    base_url='http://localhost:11434/v1',
    api_key='*',  # Ollama doesn't require an API key
    model_id="llama3.1:8b"  # Specify the model

)


class OllamaAgent():
    def __init__(self, **kwargs):
        self.kwargs = kwargs  # store everything for later use

    def build_agent(self) -> ChatAgent:
        return ChatAgent(
            chat_client=chat_client,
            **self.kwargs  
        )
