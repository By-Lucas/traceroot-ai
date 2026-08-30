from app.core.config import Settings
from app.core.errors import ProviderError
from app.core.llm.base import LLMProvider
from app.core.llm.groq_provider import GroqProvider
from app.core.llm.openai_provider import OpenAIProvider


def create_provider(settings: Settings) -> LLMProvider | None:
    if settings.llm_provider == "demo":
        return None
    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ProviderError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        return OpenAIProvider(
            settings.openai_api_key,
            settings.llm_model or "gpt-5-mini",
            settings.llm_timeout_seconds,
        )
    if settings.llm_provider == "groq":
        if not settings.groq_api_key:
            raise ProviderError("GROQ_API_KEY is required when LLM_PROVIDER=groq")
        return GroqProvider(
            settings.groq_api_key,
            settings.llm_model or "openai/gpt-oss-20b",
            settings.llm_timeout_seconds,
        )
    raise ProviderError(f"Unsupported LLM provider: {settings.llm_provider}")
