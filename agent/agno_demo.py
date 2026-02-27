from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.hackernews import HackerNewsTools
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Claude(id="claude-sonnet-4-5-20250929"),
    tools=[],
    instructions="you are a English assistant",
    markdown=True,
)
agent.print_response("what's debate meaning", stream=True)