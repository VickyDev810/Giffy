import asyncio
import logging
from typing import cast

from agent_framework import (
    MagenticAgentDeltaEvent,
    MagenticAgentMessageEvent,
    MagenticBuilder,
    MagenticFinalResultEvent,
    MagenticOrchestratorMessageEvent,
    MagenticPlanReviewDecision,
    MagenticPlanReviewReply,
    MagenticPlanReviewRequest,
    RequestInfoEvent,
    WorkflowOutputEvent,
)
from agent_framework.openai import OpenAIChatClient

from build_agent.openai import OpenAIAgent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def extract_message_text(msg) -> str:
    if msg is None:
        return ""
    if hasattr(msg, "content") and msg.content:
        parts = []
        for block in msg.content:
            if hasattr(block, "text") and block.text:
                parts.append(block.text)
        if parts:
            return " ".join(parts)
    if hasattr(msg, "text") and msg.text:
        return msg.text
    return str(msg)


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


async def main() -> None:
    
    def on_exception(exception: Exception) -> None:
        print(f"Exception occurred: {exception}")
        logger.exception("Workflow exception", exc_info=exception)

    last_stream_agent_id: str | None = None
    stream_line_open: bool = False

    print("\nBuilding Magentic Workflow...")

    workflow = (
        MagenticBuilder()
        .participants(
            budget_agent=budget_agent,
            recipient_agent=recipient_agent,
            occasion_agent=occasion_agent,
            gift_curator=gift_curator,
            personalization_agent=personalization_agent,
            presentation_agent=presentation_agent
        )
        .with_standard_manager(
            chat_client=OpenAIChatClient(),
            max_round_count=10,
            max_stall_count=3,
            max_reset_count=2,
        )
        .with_plan_review()
        .build()
    )
    
    occasion = input("What is the occasion? (e.g., birthday, anniversary, wedding): ")
    recipient_info = input("Tell me about the recipient (interests, age, preferences): ")
    budget = input("What is your budget? (e.g., $50, $100, $200): ")
    
    task = f"""
You are a gift recommendation team helping find the perfect gift. Here are the details:

Occasion: {occasion}
Recipient Information: {recipient_info}
Budget: {budget}

Please work together as a team:
1. Budget Analyst: Confirm if the budget is realistic for the occasion
2. Recipient Specialist: Dive deeper into what gifts the recipient would appreciate
3. Occasion Expert: Suggest gifts appropriate for this occasion
4. Gift Curator: Compile the best 3-5 personalized gift recommendations
5. Personalization Expert: Suggest how to make each gift more special
6. Presentation Specialist: Recommend the best way to present and wrap these gifts

Provide the user with thoughtful, creative, and actionable gift recommendations.
"""

    print(f"\nTask: {task}")
    print("\nStarting workflow execution...")

    try:
        pending_request: RequestInfoEvent | None = None
        pending_responses: dict[str, MagenticPlanReviewReply] | None = None
        completed = False
        workflow_output: str | None = None

        while not completed:
            if pending_responses is not None:
                stream = workflow.send_responses_streaming(pending_responses)
            else:
                stream = workflow.run_stream(task)

            async for event in stream:
                if isinstance(event, MagenticOrchestratorMessageEvent):
                    print(f"\n[ORCH:{event.kind}]\n\n{extract_message_text(event.message)}\n{'-' * 26}")

                elif isinstance(event, MagenticAgentDeltaEvent):
                    if last_stream_agent_id != event.agent_id or not stream_line_open:
                        if stream_line_open:
                            print()
                        print(f"\n[STREAM:{event.agent_id}]: ", end="", flush=True)
                        last_stream_agent_id = event.agent_id
                        stream_line_open = True
                    if event.text:
                        print(event.text, end="", flush=True)

                elif isinstance(event, MagenticAgentMessageEvent):
                    if stream_line_open:
                        print(" (final)")
                        stream_line_open = False
                        print()
                    msg = event.message
                    text = extract_message_text(msg)
                    print(f"\n[AGENT:{event.agent_id}] {msg.role.value}\n\n{text}\n{'-' * 26}")

                elif isinstance(event, MagenticFinalResultEvent):
                    print("\n" + "=" * 50)
                    print("FINAL RESULT:")
                    print("=" * 50)
                    print(extract_message_text(event.message))
                    print("=" * 50)

                if isinstance(event, RequestInfoEvent) and event.request_type is MagenticPlanReviewRequest:
                    pending_request = event
                    review_req = cast(MagenticPlanReviewRequest, event.data)
                    if review_req.plan_text:
                        print(f"\n=== Gift Recommendation Plan ===\n{review_req.plan_text}\n")

                elif isinstance(event, WorkflowOutputEvent):
                    workflow_output = extract_message_text(event.data) if event.data else None
                    completed = True

            if stream_line_open:
                print()
                stream_line_open = False
            pending_responses = None

            if pending_request is not None:
                print("Plan review options:")
                print("1. approve - Approve the plan as-is")
                print("2. revise - Request revision of the plan")
                print("3. exit - Exit the workflow")

                while True:
                    choice = input("Enter your choice (approve/revise/exit): ").strip().lower()
                    if choice in ["approve", "1"]:
                        reply = MagenticPlanReviewReply(decision=MagenticPlanReviewDecision.APPROVE)
                        break
                    if choice in ["revise", "2"]:
                        edit = input("Enter your revision request: ")
                        reply = MagenticPlanReviewReply(
                            decision=MagenticPlanReviewDecision.REVISE,
                            comments=edit or "Please revise the plan to be more specific."
                        )
                        break
                    if choice in ["exit", "3"]:
                        print("Exiting workflow...")
                        return
                    print("Invalid choice. Please enter 'approve', 'revise', or 'exit'.")

                pending_responses = {pending_request.request_id: reply}
                pending_request = None

        if workflow_output:
            print(f"Workflow completed with result:\n\n{workflow_output}")

    except Exception as e:
        print(f"Workflow execution failed: {e}")
        on_exception(e)


if __name__ == "__main__":
    asyncio.run(main())