import os
from build_agent.openai import OpenAIAgent
from build_agent.openrouter import OpenRouterAgent
from runners.stream import StreamAgentRunner
from agent_framework import MCPStdioTool

instructions = """
Identity

You are a Chaotic Procurement Agent. Your goal is to execute a high-speed, randomized purchase of a "mood-brightening" item within a strict budget and specific account parameters.
Capabilities

The optimal flow:

0. Check login using (blinkit_check_login) status if logged in go to step 3 else start from step 1 if no login found it means user already logged in.
1. Login with this mobile no. TEST_MOBILE_NO.
2. Ask user the otp.
3. Search that chaos product from your mind and users query.
4. Use Complete Checkout using (blinkit_complete_checkout)  function for the selected product. (Just keep in mind the budget constraints).

Rules:
Always follow the flow that is given above to get the most desirable results.
Find the best possible gift according to users vibe.


"""

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the local Blinkit MCP tool
base_dir = os.path.dirname(os.path.abspath(__file__))

mcp_tool = MCPStdioTool(
    name="blinkit-mcp",
    command="venv/bin/python",
    args=[f"{base_dir}/blinkit_mcp_new.py"],
    description="Blinkit Shopping Agent"
)

agent = OpenRouterAgent(
   instructions = instructions,
   name = "Blinkit Agent",
   tools = mcp_tool,
).build_agent()
async def main():
    thread = agent.get_new_thread()
    runner = StreamAgentRunner(agent=agent,thread=thread)
    
    while True:
        user_input = input("User: ")
        if(user_input == "exit"):
            break
        async for chunk in runner.run(user_input):
            print(chunk, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
