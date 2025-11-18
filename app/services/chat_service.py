from bson import ObjectId
from datetime import date
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph_supervisor.supervisor import create_supervisor
import logging

from app.agents.calendar_agent import GoogleCalendarMCPAgent
from app.core.config import get_settings
from app.databases.redis_client import get_chat_history, get_redis_store, get_user_profile, save_chat_history
from app.prompts.supervisor import supervisor_prompt

logger = logging.getLogger(__name__)

settings = get_settings()

calendar_agent = GoogleCalendarMCPAgent()

class ChatService():
    def __init__(self):
        self.model = ChatAnthropic(
            model = settings.DEFAULT_ANTHROPIC_MODEL,
            temperature = settings.CHAT_TEMPERATURE,
            api_key = settings.ANTHROPIC_API_KEY
        )

        self.store = get_redis_store().store

        self.supervisor = create_supervisor(
            agents=[calendar_agent.get_agent()],
            model=self.model,
            output_mode="last_message",
            prompt=self.prompt,
            add_handoff_messages=False,
            supervisor_name="sales_assistant_supervisor",
            tools=[]
        ).compile(
            store=self.store
        )

    def prompt(self, state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
        user_preferences = config["configurable"].get("user_preferences")
        user_ctx = config["configurable"].get("user_ctx")

        logger.info(f"USER INFO: {user_ctx}")

        system_msg = supervisor_prompt.format(
            #user_preferences = user_preferences,
            user_ctx = user_ctx,
            date = date.today()
        )

        return [{"role": "system", "content": system_msg}] + state["messages"]
    
    async def process_message(self, user_id, session_id, user_input):

        try:
            if not session_id:
                session_id = str(ObjectId())
                logger.info(f"Creating session: {session_id}")

            thread_id = f"chat:{user_id}:{session_id}"

            config = {
                "configurable": {
                    "user_id": user_id,
                    "user_ctx": await get_user_profile(user_id),
                    "user_input": user_input,
                    "thread_id": thread_id,
                    "user_preferences": None
                }
            }

            text_content = {"type": "text", "text": user_input}

            message = {
                "role": "user",
                "content": [text_content]
            }

            history, current_title = await get_chat_history(thread_id)
            messages = history + [message] if user_input else history

            response = await self.supervisor.ainvoke({"messages": messages}, config)

            if response["messages"][-1].content:
                cleaned_response = response["messages"][-1].content
            else:
                cleaned_response = response["messages"][-2].content

            logger.info(f"Complete response: {response['messages']}")

            save_messages = []

            save_messages.append({"role": "user", "content": user_input})
            save_messages.append({"role": "assistant", "content": cleaned_response})

            if len(save_messages) > 0:
                await save_chat_history(thread_id, save_messages, settings.TTL_CHAT, current_title)

            return {
                "user_id": user_id,
                "session_id": session_id,
                "response": cleaned_response
            }
        except Exception as e:
            logger.warning(f"HttpError: {e}")
            raise e