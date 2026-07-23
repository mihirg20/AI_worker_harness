from openai import OpenAI

from config.settings import settings


def get_client() -> OpenAI:
    """
    Returns an OpenAI client configured to talk to LiteLLM.
    """

    client = OpenAI(
        base_url=settings.LITELLM_BASE_URL,
        api_key=settings.LITELLM_API_KEY,
    )

    return client