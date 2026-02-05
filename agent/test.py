from build_agent.openai import OpenAIAgent
from runners.stream import StreamAgentRunner
from typing import Annotated
from pydantic import Field
from amazon.client import Amazon


def gift_finder_tool(
    query: Annotated[str, Field(description="The query to find gifts according to.")]
) -> str:
    """
    Find gifts according to the query.
    """
    amazon = Amazon()  # init errors will raise normally
    response = amazon.search(query=query, domain="amazon.in")

    if hasattr(response, "status_code"):
        try:
            return response.status_code, response.json()
        except Exception:
            return response.status_code, response.text

    return response
    


# Build agents
budget_agent_def = OpenAIAgent(
    name="budget_analyst",
    instructions="You are a budget expert agent. Help users determine appropriate gift budgets based on their financial situation, relationship type, and occasion. Provide budget ranges and recommendations.",
)
budget_agent = budget_agent_def.build_agent()

recipient_agent_def = OpenAIAgent(
    name="recipient_specialist",
    instructions="You are an expert in understanding recipients. Ask about the recipient's interests, hobbies, age, lifestyle, and preferences. Gather detailed information to make personalized gift recommendations.",
)
recipient_agent = recipient_agent_def.build_agent()

occasion_agent_def = OpenAIAgent(
    name="occasion_expert",
    instructions="You are an occasion specialist. Help identify the perfect gifts for different occasions: birthdays, anniversaries, weddings, holidays, thank you gifts, etc. Consider occasion-specific gift etiquette.",
)
occasion_agent = occasion_agent_def.build_agent()

gift_curator_def = OpenAIAgent(
    name="gift_curator",
    instructions="You are a gift curation expert. Based on budget, recipient profile, and occasion, suggest creative and thoughtful gift ideas. Provide diverse options across different categories.",
)
gift_curator = gift_curator_def.build_agent()

personalization_agent_def = OpenAIAgent(
    name="personalization_expert",
    instructions="You are an expert in personalizing gifts. Suggest ways to add personal touches to gifts like custom engravings, monogramming, custom packaging, or heartfelt messages.",
)
personalization_agent = personalization_agent_def.build_agent()

presentation_agent_def = OpenAIAgent(
    name="presentation_specialist",
    instructions="You are a gift presentation expert. Provide advice on gift wrapping, presentation, delivery methods, and accompanying message suggestions to make the gift special.",
)
presentation_agent = presentation_agent_def.build_agent()


async def main():
    budget_thread = budget_agent.get_new_thread()
    recipient_thread = budget_agent.get_new_thread()
    occasion_thread = budget_agent.get_new_thread()
    gift_curator_thread = gift_curator.get_new_thread()
    personalization_thread = personalization_agent.get_new_thread()
    presentation_thread = presentation_agent.get_new_thread()

    budget_runner = StreamAgentRunner(budget_agent, budget_thread)
    recipient_runner = StreamAgentRunner(recipient_agent, recipient_thread)
    occasion_runner = StreamAgentRunner(occasion_agent, occasion_thread)
    gift_curator_runner = StreamAgentRunner(gift_curator, gift_curator_thread)
    personalization_runner = StreamAgentRunner(personalization_agent, personalization_thread)
    presentation_runner = StreamAgentRunner(presentation_agent, presentation_thread)

    while True:
        user = input("User: ")
        if(user == "exit"):
            break
        print("Budget Agent Response:")
        async for chunk in budget_runner.run(user):
            user += chunk
            print(f"Budget Agent: {chunk}", end="", flush=True)
        print('\n')
        print ("Recipient Agent Response:")
        async for chunk in recipient_runner.run(user):
            user += chunk
            print(f"Recipient Agent: {chunk}", end="", flush=True)
        print('\n')
        print("Occasion Agent Response:")         
        async for chunk in occasion_runner.run(user):
            user += chunk
            print(f"Occasion Agent: {chunk}", end="", flush=True)
        print('\n')

        print("Gift Curator Agent Response:")
        async for chunk in gift_curator_runner.run(user):
            user += chunk
            print(f"Gift Curator Agent: {chunk}", end="", flush=True)
        print('\n')
        print("Personalization Agent Response:")
        async for chunk in personalization_runner.run(user):
            user += chunk
            print(f"Personalization Agent: {chunk}", end="", flush=True)
        print('\n')
        print("Presentation Agent Response:")
        async for chunk in presentation_runner.run(user):
            user += chunk
            print(f"Presentation Agent: {chunk}", end="", flush=True)
        print('\n') 

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
       