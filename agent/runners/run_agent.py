class AgentRunner():
    def __init__(self, agent, **kwargs):
        self.agent=agent
        self.kwargs = kwargs
    async def run(self, user_input: str):
        result = await self.agent.run(user_input, **self.kwargs)
        return result