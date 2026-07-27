# AI Worker Harness

A small multi-agent orchestration framework I built to explore a question that kept bugging me: what happens if you stop treating an LLM as one generalist and instead give it a team structure?

Most "AI coding assistant" setups are a single model juggling every role at once — architecture, implementation, tests, docs — in one long context window. That works until the context gets messy and the model starts blending concerns. This project takes the opposite approach: a **Manager Agent** breaks a task down and hands it off to specialized **Worker Agents** (Backend, Frontend, QA, Security, Docs, DevOps), each with its own system prompt, its own persona, and its own persistent memory of what it's worked on before.

It's not a framework trying to be the next LangChain. It's deliberately small — a Manager, some Workers, a proxy layer, and a memory store — so it's easy to read end to end in one sitting and easy to extend without fighting the abstraction.

## Architecture

```
                    User
                     │
                     ▼
              Manager Agent
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
  Backend Agent  Frontend Agent  QA Agent   ...
        │            │            │
        └────────────┼────────────┘
                     │
              LiteLLM Proxy
                     │
                     ▼
              Gemini / OpenAI
```

The Manager reads a task, decides which worker (or workers) it belongs to, and delegates. Each worker builds its own request from three ingredients — its system prompt, the task, and any relevant memory/context files — sends it through the LiteLLM proxy, and logs the exchange.


## Getting started

**Requirements:** Python 3.12+, and a Gemini or OpenAI API key.

```bash
git clone https://github.com/mihirg20/AI_worker_harness.git
cd AI_worker_harness

python -m venv .venv
source .venv/bin/activate    # .venv\Scripts\activate on Windows

pip install -r requirements.txt
```

Add your key(s) to `.env`:

```env
LITELLM_MASTER_KEY=sk-local
GEMINI_KEY_1=your_gemini_api_key
```

Point `config/litellm_config.yaml` at the model you want workers to use:

```yaml
model_list:
  - model_name: gemini-worker
    litellm_params:
      model: gemini/gemini-2.5-flash-lite
      api_key: os.environ/GEMINI_KEY_1

general_settings:
  master_key: sk-local
```

Start the proxy:

```bash
litellm --config config/litellm_config.yaml --port 4000
```

## Running it

Talk to a single worker directly:

```bash
python test_worker.py
```

```python
from app.agents.worker import Worker

backend = Worker("backend")
response = backend.run("Write a FastAPI endpoint for login.")
print(response)
```

Or delegate a task file to a specific worker:

```bash
python scripts/delegate.py --agent backend --task-file tasks/hello.md
```

Or let the Manager decide which worker should own it:

```bash
python scripts/orchestrator.py --task-file tasks/hello.md
```

## Adding a new worker

Two steps, no core changes:

1. Write a system prompt — `harness/agents/security.md`
2. Register it — add an entry in `app/agents/registry.py`

That's the whole extension point. The Manager, the memory system, and the proxy layer don't need to know anything changed.

## Currently supported roles

Backend · Frontend · QA · Security · Documentation · DevOps

## Roadmap

Things I'm deliberately leaving out for now, in rough order of what I'd tackle next:

- Parallel worker execution (right now delegation is sequential)
- Tool calling, so workers can actually run tests/linters instead of just writing code
- Task dependency graphs, so the Manager can sequence multi-worker tasks properly
- Long-term memory via embeddings, once flat JSON actually becomes a bottleneck
- A human-approval step before a worker's output is considered "done"
- Docker support and a minimal web dashboard for watching agents work

## Stack

Python · LiteLLM · HTTPX · Pydantic · Gemini API · Markdown-based prompts · JSON-based memory

## Contributing

This started as a personal exploration, so the codebase is small on purpose — which actually makes it a decent place to contribute if you're curious about multi-agent systems and don't want to read 10k lines before your first PR.

If you want to help out:

1. Fork the repo and create a branch off `main` (`feature/your-idea` or `fix/your-fix` is fine).
2. Keep changes scoped — one worker, one feature, one fix per PR is easier for me to review and merge than a big bundle.
3. If you're adding a new worker role, follow the existing pattern: a markdown prompt in `harness/agents/`, plus a registry entry — don't hardcode role logic into `manager.py`.
4. If you're touching `app/agents/worker.py`, `memory.py`, or `delegate.py`, run `test_worker.py` locally against your own API key before opening the PR, since there isn't CI for this yet.
5. Open an issue first for anything bigger than a small fix (new features, architecture changes, dependency swaps) so we can align before you put the work in.

Good first contributions if you want to get familiar with the codebase:

- A new worker role (e.g. Data/ML, Mobile)
- Better error handling when the LiteLLM proxy is unreachable
- A `--dry-run` flag for `orchestrator.py` to preview delegation without calling the model
- Tests around `memory.py` (there currently aren't any)

If something in the roadmap above interests you, mention it in an issue — happy to hand off pieces of it.

## License

MIT