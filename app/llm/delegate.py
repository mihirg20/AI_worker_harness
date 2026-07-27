import os

import httpx
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

PROXY_URL = "http://localhost:4000/v1/chat/completions"


def ask(
    system_prompt: str,
    user_prompt: str,
    model: str = "gemini-worker",
    temperature: float = 0.2,
    max_tokens: int = 4000,
) -> str:
    """
    Send a request to the local LiteLLM proxy.

    Args:
        system_prompt: Instructions for the AI agent.
        user_prompt: The actual task to perform.
        model: Model alias configured in LiteLLM.
        temperature: Sampling temperature.
        max_tokens: Maximum output tokens.

    Returns:
        The assistant's response as a string.
    """

    master_key = os.getenv("LITELLM_MASTER_KEY")

    if not master_key:
        raise ValueError(
            "LITELLM_MASTER_KEY not found in .env"
        )

    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    }

    response = httpx.post(
        PROXY_URL,
        json=payload,
        headers={
            "Authorization": f"Bearer {master_key}",
        },
        timeout=300,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]