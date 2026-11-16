# Progress

Current stage: **2 · Structured output and a validator**
Time budget: 2h (core) / 4h / 6h
Time spent so far: ~1.5h

## Stage 0 status
- [x] uv project scaffolded, deps installed (`uv sync`)
- [x] LangSmith tracing env vars configured in `.env` (endpoint, agent id `mtg-agent`, env `local`)
- [x] Fill `OPENAI_API_KEY`, `OPEN_AI_BASE_URL`, `MODEL`, `LANGSMITH_API_KEY` in `.env`
- [x] Write your first model call (you write it): `ChatOpenAI` pointed at the OpenAI-compatible API
- [x] See the trace in LangSmith under agent `mtg-agent` / `local`

## Completed
<!-- stage · date · one-line note on what you learned -->
- Stage 0: LangChain auto-traces via callbacks; `LANGSMITH_TRACING=true` makes it attach a `LangChainTracer`, which batches runs (with parent IDs) to LangSmith. `.env` must be loaded *before* `env.py` is imported.
- Stage 1 · 2026-11-16: Agent calls `search_for_cards` (Scryfall) and returns real green ramp creatures with MV ≤ 3. Trace: 3 model calls at 458 → 20.1K → 25.9K input tokens. Raw tool output (~300 cards as Python reprs) dominates context, and every later model call re-reads it.

## Next session: start here
- Shrink the tool output before Stage 2: cap results (10–20), use one compact line per card (no `id`), and say in the docstring that the model should refine the query instead of paging. Re-run and compare token counts with the 25.9K baseline.
- Consider adding a Commander-legality filter to the query by default (Alchemy/digital cards are showing up).
- Fix the remaining ty errors (`uvx ty check src`), e.g. the `backoff` Callable annotation in `retry_transport.py`.
- TODO: tool error handling in `tools/scryfall.py` (currently only `not_found` becomes a message; everything else re-raises). Rule: *can the model fix it by changing its input?*
  - 400 bad query syntax → return a message with Scryfall's `details`, so the model can rewrite the query
  - 404 no matches → return a message (done)
  - Pydantic validation error → raise (it's our bug, so fail loudly)
  - 429 / 5xx / timeout after retries → decide: raise, or return "search unavailable, don't retry" (watch for retry loops that run until the recursion limit)
  - Open question: branch on `status_code` or `code`?

## Open questions

## Later (parked ideas)
- Per-route rate limits for the Scryfall transport (one conservative global limit is enough for now)
