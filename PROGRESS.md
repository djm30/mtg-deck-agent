# Progress

Current stage: **1 · Tools: give the model real card data**
Time budget: 2h (core) / 4h / 6h
Time spent so far: ~0h

## Stage 0 status
- [x] uv project scaffolded, deps installed (`uv sync`)
- [x] LangSmith tracing env vars configured in `.env` (endpoint, agent id `mtg-agent`, env `local`)
- [x] Fill `OPENAI_API_KEY`, `OPEN_AI_BASE_URL`, `MODEL`, `LANGSMITH_API_KEY` in `.env`
- [x] Write your first model call (you write it): `ChatOpenAI` pointed at the OpenAI-compatible API
- [x] See the trace in LangSmith under agent `mtg-agent` / `local`

## Completed
<!-- stage · date · one-line note on what you learned -->
- Stage 0: LangChain auto-traces via callbacks; `LANGSMITH_TRACING=true` makes it attach a `LangChainTracer`, which batches runs (with parent IDs) to LangSmith. `.env` must be loaded *before* `env.py` is imported.

## Open questions

## Later (parked ideas)
