import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Environment:
    """Easy access container to all environment variables"""

    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
    OPEN_AI_BASE_URL: str = os.environ["OPEN_AI_BASE_URL"]
    MODEL: str = os.environ["MODEL"]

    LANGSMITH_API_KEY: str = os.environ["LANGSMITH_API_KEY"]
    LANGSMITH_TRACING: str = os.environ["LANGSMITH_TRACING"]
    LANGSMITH_ENDPOINT: str = os.environ["LANGSMITH_ENDPOINT"]
    LANGSMITH_AGENT_ID: str = os.environ["LANGSMITH_AGENT_ID"]
    LANGSMITH_AGENT_ENVIRONMENT: str = os.environ["LANGSMITH_AGENT_ENVIRONMENT"]
