from bson import ObjectId
from datetime import date
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_core.messages import AnyMessage, ToolMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph_supervisor.supervisor import create_supervisor
import logging

from app.core.config import get_settings
from app.prompts.supervisor import supervisor_prompt
from app.databases.redis_client import get_chat_history, get_redis_store, save_chat_history

logger = logging.getLogger(__name__)

settings = get_settings()

class ChatService():
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model=settings.DEFAULT_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )

        self.store = get_redis_store().store

        self.supervisor = create_supervisor(
            agents=[],
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

        system_msg = supervisor_prompt.format(
            user_preferences = user_preferences,
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

            cleaned_response = await self.supervisor.ainvoke({"messages": messages}, config)

            logger.info(f"Complete response: {cleaned_response['messages']}")

            save_messages = []

            save_messages.append({"role": "user", "content": user_input})
            save_messages.append({"role": "assistant", "content": cleaned_response["messages"][-1].content})

            if len(save_messages) > 0:
                await save_chat_history(thread_id, save_messages, settings.TTL_CHAT, current_title)

            return {
                "user_id": user_id,
                "session_id": session_id,
                "response": cleaned_response["messages"][-1].content
            }
        except Exception as e:
            logger.warning(f"HttpError: {e}")
            raise