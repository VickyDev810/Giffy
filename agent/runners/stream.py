class StreamAgentRunner():
    def __init__(self, agent, **kwargs):
        self.agent=agent
        self.kwargs = kwargs
    async def run(self, user_input: str):
        async for update in self.agent.run_stream(user_input, **self.kwargs):
            if update.text:
                yield update.text  # Yield each chunk as it
