import asyncio
from functools import lru_cache
from langchain_mcp_adapters.client import MultiServerMCPClient
import logging
from app.core.config import get_settings

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

settings = get_settings()

class GoogleCalendarMCPClient:
    def __init__(self, url: str):
        self.url = url
        self.client = MultiServerMCPClient(  
            {
                "calendar": {
                    "transport": "streamable_http",
                    "url": url,
                }
            }
        )

    def get_tools(self):
        """
        Connect to the MCP server over HTTP,
        initialize the session and load its tools.
        """

        return asyncio.run(self.client.get_tools())

@lru_cache
def get_calendar_client():
    return GoogleCalendarMCPClient(url=settings.CALENDAR_MCP_URL)