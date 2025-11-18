import logging
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from app.prompts.outreach_agent import outreach_agent_prompt
from app.schemas.structured_outputs.outreach import dm_response_tool, email_response_tool, pitch_response_tool
from app.utils.outreach_utils import get_outreach_provided_missing_info

logger = logging.getLogger(__name__)

response_tool_map = {
    "pitch": pitch_response_tool,
    "email": email_response_tool,
    "dm": dm_response_tool
}

class OutreachAgent():
    def __init__(self, model):
        super().__init__()
        self.model = model
    
    def prompt(self, state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
        user_ctx = config["configurable"].get("user_ctx")
        idea_type = config["configurable"].get("idea_type")
        form = config["configurable"].get("form")
        num_ideas = config["configurable"].get("num_ideas")

        system_msg = outreach_agent_prompt.format(
            user_ctx=user_ctx,
            provided_info=get_outreach_provided_missing_info(idea_type, form),
            idea_type=idea_type,
            tool_name=f"'{str(response_tool_map[idea_type].name)}'",
            num_ideas=num_ideas
        )

        return [{"role": "system", "content": system_msg}] + state["messages"]
    
    def get_agent(self, idea_type):

        return create_react_agent(
            tools=[response_tool_map[idea_type]],
            model=self.model,
            name="outreach_agent",
            prompt=self.prompt
        )