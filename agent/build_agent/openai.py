import os
from agent_framework.openai import OpenAIResponsesClient, OpenAIChatClient
from agent_framework import ChatAgent
from dotenv import load_dotenv
load_dotenv()

class OpenAIAgent():
    def __init__(self, **kwargs):
        self.kwargs = kwargs  # store everything for later use

    def build_agent(self) -> ChatAgent:
        return OpenAIResponsesClient(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_id=os.getenv('OPENAI_RESPONSES_MODEL_ID'),
        ).create_agent(
        **self.kwargs
    )
    
    def build_agent_chat(self) -> ChatAgent:
        return OpenAIChatClient(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_id=os.getenv('OPENAI_CHAT_MODEL_ID'),
        ).create_agent(
            **self.kwargs
        )
