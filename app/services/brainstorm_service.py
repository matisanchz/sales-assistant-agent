from langchain_anthropic import ChatAnthropic
import logging

from app.agents.outreach_agent import OutreachAgent
from app.core.config import get_settings
from app.databases.redis_client import get_user_profile

logger = logging.getLogger(__name__)

settings = get_settings()

class BrainstormService():
    def __init__(self):
        self.model = ChatAnthropic(
            model = settings.DEFAULT_ANTHROPIC_MODEL,
            temperature = settings.CHAT_TEMPERATURE,
            api_key = settings.ANTHROPIC_API_KEY
        )

        self.agents = {
            "email": OutreachAgent(self.model).get_agent("email"),
            "pitch": OutreachAgent(self.model).get_agent("pitch"),
            "dm": OutreachAgent(self.model).get_agent("dm")
        }
    
    async def generate_idea(self, user_id, section, idea_type, form):

        try:
            config = {
                "configurable": {
                    "user_id": user_id,
                    "user_ctx": await get_user_profile(user_id),
                    "idea_type": idea_type,
                    "form": form,
                    "num_ideas": settings.NUM_IDEAS
                }
            }

            state = {
                "messages": [
                    {
                        "role": "user",
                        "content": f"Generate {settings.NUM_IDEAS} {idea_type} {section} ideas."
                    }
                ]
            }

            response = await self.agents[idea_type].ainvoke(state, config)

            logger.info(f"Complete response: {response['messages']}")

            cleaned_response = response["messages"][-1].content

            return {
                "user_id": user_id,
                "response": cleaned_response
            }
        except Exception as e:
            logger.warning(f"HttpError: {e}")
            raise