from datetime import date
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from app.core.config import get_settings
from app.mcp.calendar_client import get_calendar_client
from app.prompts.calendar_agent import calendar_agent_prompt

settings = get_settings()
mcp_client = get_calendar_client()

class GoogleCalendarMCPAgent:
    def __init__(self):
        self.llm = ChatAnthropic(
            model = settings.DEFAULT_ANTHROPIC_MODEL,
            temperature = settings.CHAT_TEMPERATURE,
            api_key = settings.ANTHROPIC_API_KEY
        )
        self.calendar_tools = None

    def load_tools(self):
        if self.calendar_tools is None:
            client = get_calendar_client()
            self.calendar_tools = client.get_tools()
        return self.calendar_tools

    def prompt(self, state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
        
        system_msg = calendar_agent_prompt.format(
            date = date.today()
        )

        return [{"role": "system", "content": system_msg}] + state["messages"]
    
    def get_agent(self):
        return create_react_agent(
            tools=self.load_tools(),
            model=self.llm,
            name=f"calendar_agent",
            prompt=self.prompt,
        )