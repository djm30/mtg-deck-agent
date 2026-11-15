import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Environment:
    """Easy access container to all environment variables"""

    OPENAI_API_KEY: str = field(default=os.environ.get("OPENAI_API_KEY"))
    OPEN_AI_BAASE_URL: str = field(default=os.environ.get("OPEN_AI_BAASE_URL"))
    MODEL: str = field(default=os.environ.get("MODEL"))

    LANGSMITH_API_KEY: str = field(default=os.environ.get("LANGSMITH_API_KEY"))
    LANGSMITH_TRACING: str = field(default=os.environ.get("LANGSMITH_TRACING"))
    LANGSMITH_ENDPOINT: str = field(default=os.environ.get("LANGSMITH_ENDPOINT"))
    LANGSMITH_AGENT_ID: str = field(default=os.environ.get("LANGSMITH_AGENT_ID"))
    LANGSMITH_AGENT_ENVIRONMENT: str = field(default=os.environ.get("LANGSMITH_AGENT_ENVIRONMENT"))
