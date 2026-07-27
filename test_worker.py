from app.agents.worker import Worker


backend = Worker("backend")

response = backend.run(
    "Write a FastAPI endpoint for login."
)

print(response)