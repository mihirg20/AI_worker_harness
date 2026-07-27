# from app.agents.manager import Manager
# from app.agents.worker import Worker

from app.agents.manager import Manager
from app.agents.worker import Worker

task = input("Task: ")

manager = Manager()

decision = manager.decide(task)

print(decision)

for worker in decision["workers"]:

    print("=" * 40)

    print(worker)

    agent = Worker(worker)

    response = agent.run(task)

    print(response)





# #!/usr/bin/env python3
# """Delegate a task brief to a Gemini sub-agent via the local LiteLLM proxy.

# Usage:
#     python scripts/delegate.py --agent backend --task-file tasks/T001-health.md \
#         [--context-file app/schemas/user.py ...] [--out logs/backend-<ts>.md]

# The agent's system prompt is harness/agents/<agent>.md. Context files are
# wrapped in <context file="..."> tags after the brief. Output (raw model text)
# is written to --out; path + token usage printed to stdout.

# Retries are NOT done here — the LiteLLM proxy handles retries/failover.
# """

# import argparse
# import datetime
# import os
# import sys
# from pathlib import Path

# import httpx

# REPO_ROOT = Path(__file__).resolve().parent.parent
# AGENTS_DIR = REPO_ROOT / "harness" / "agents"
# PROXY_URL = "http://localhost:4000/v1/chat/completions"
# AGENTS = ("backend", "frontend", "qa-db")


# def load_env_key() -> str:
#     """Load LITELLM_MASTER_KEY from env or .env"""
#     key = os.environ.get("LITELLM_MASTER_KEY")
#     if key:
#         return key

#     env_file = REPO_ROOT / ".env"
#     if env_file.exists():
#         for line in env_file.read_text(encoding="utf-8").splitlines():
#             line = line.strip()
#             if line.startswith("LITELLM_MASTER_KEY="):
#                 return line.split("=", 1)[1].strip()

#     print("ERROR: LITELLM_MASTER_KEY not found.", file=sys.stderr)
#     sys.exit(2)


# def main():
#     parser = argparse.ArgumentParser()

#     parser.add_argument("--agent", required=True, choices=AGENTS)
#     parser.add_argument("--task-file", required=True)
#     parser.add_argument("--context-file", action="append", default=[])
#     parser.add_argument("--out", default=None)

#     args = parser.parse_args()

#     system_prompt = (
#         AGENTS_DIR / f"{args.agent}.md"
#     ).read_text(encoding="utf-8")

#     task = Path(args.task_file).read_text(encoding="utf-8")

#     user_parts = [task]

#     for file in args.context_file:
#         content = Path(file).read_text(encoding="utf-8")
#         user_parts.append(
#             f'<context file="{file}">\n{content}\n</context>'
#         )

#     user_prompt = "\n\n".join(user_parts)

#     timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

#     out = (
#         Path(args.out)
#         if args.out
#         else REPO_ROOT / "logs" / f"{args.agent}-{timestamp}.md"
#     )

#     out.parent.mkdir(parents=True, exist_ok=True)

#     payload = {
#         "model": "gemini-worker",
#         "reasoning_effort": "low",
#         "max_tokens": 16000,
#         "messages": [
#             {
#                 "role": "system",
#                 "content": system_prompt,
#             },
#             {
#                 "role": "user",
#                 "content": user_prompt,
#             },
#         ],
#     }

#     print("Authorization:", f"Bearer {load_env_key()}")
#     print("Proxy URL:", PROXY_URL)

#     response = httpx.post(
#         PROXY_URL,
#         json=payload,
#         headers={
#             "Authorization": f"Bearer {load_env_key()}",
#         },
#         timeout=300,
#     )

#     if response.status_code != 200:
#         print(response.text)
#         sys.exit(1)

#     data = response.json()

#     output = data["choices"][0]["message"]["content"]

#     out.write_text(output, encoding="utf-8")

#     print("Saved to:", out)


# if __name__ == "__main__":
#     main()