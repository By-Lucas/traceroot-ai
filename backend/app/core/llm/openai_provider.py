from openai import AsyncOpenAI

from app.core.errors import ProviderError
from app.core.llm.base import LLMProvider, LLMResponse, T


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, timeout: int) -> None:
        self.client = AsyncOpenAI(api_key=api_key, timeout=timeout, max_retries=2)
        self.model = model

    async def structured(
        self, *, system: str, prompt: str, output_model: type[T], temperature: float = 0
    ) -> LLMResponse:
        try:
            response = await self.client.responses.parse(
                model=self.model,
                input=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                text_format=output_model,
                temperature=temperature,
            )
            if response.output_parsed is None:
                raise ProviderError("OpenAI returned no structured output")
            usage = response.usage
            return LLMResponse(
                output=response.output_parsed,
                input_tokens=usage.input_tokens if usage else 0,
                output_tokens=usage.output_tokens if usage else 0,
            )
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError(f"OpenAI request failed: {type(exc).__name__}") from exc
