from config.settings import settings
from app.llm.client import get_client


def ask(prompt: str) -> str:
    """
    Sends a prompt to the LLM and returns the response.
    """

    client = get_client()

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content