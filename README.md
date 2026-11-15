# MTG Commander Deck Agent

A learning project for building agents with LangChain, LangGraph, and Deep Agents, traced in LangSmith.
Open `learning-path.html` in a browser for the curriculum. Progress is tracked in `PROGRESS.md`.

## Setup

```bash
uv sync                  # creates .venv from uv.lock
cp .env.example .env     # if .env doesn't exist yet, then fill in the blanks
```

Fill these in `.env`:

| Var | Where to get it |
|---|---|
| `OPENAI_API_KEY` | API key / bearer token from your OpenAI-compatible LLM provider |
| `OPEN_AI_BASE_URL` | Provider base URL, e.g. `https://<llm-host>/api/v1` |
| `MODEL` | A model ID your provider accepts |
| `LANGSMITH_API_KEY` | smith.langchain.com → Settings → API Keys |

The LangSmith tracing vars (`LANGSMITH_TRACING`, `LANGSMITH_ENDPOINT`, `LANGSMITH_AGENT_ID`, `LANGSMITH_AGENT_ENVIRONMENT`) are already set.

## Running

```bash
uv run --env-file .env python path/to/script.py
```

`--env-file` loads `.env` into the process, so LangChain picks up the tracing vars automatically.
`python-dotenv` is also installed if you'd rather call `load_dotenv()` in code.

## Notes

- **The LLM is any OpenAI-compatible API.** Use `ChatOpenAI` from `langchain-openai` with `base_url`, `api_key` and `model` taken from the vars above. If the provider only supports Chat Completions, set `use_responses_api=False`.
- **Don't set `LANGSMITH_PROJECT`** while `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` are set. The SDK treats that as a conflict and stops tracing.
- If you get SSL errors on the corporate network, try `export SSL_CERT_FILE=...` (your corporate CA bundle) or ask in your team channel.

## Dependencies

- Runtime: `langchain`, `langchain-openai`, `langgraph`, `deepagents`, `langsmith`, `httpx` (Scryfall), `pydantic`, `python-dotenv`
- Dev: `langgraph-cli[inmem]` (`langgraph dev` server + Studio, Stage 8), `pytest`, `ruff`

## Agent skills

LangSmith skills are installed in `.agents/skills/` (symlinked for Claude Code in `.claude/`).
`langsmith-trace` covers querying traces with the `langsmith` CLI. Install the CLI if you want it:
https://github.com/langchain-ai/langsmith-cli
