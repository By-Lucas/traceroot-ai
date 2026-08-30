import json

from groq import AsyncGroq

from app.core.errors import ProviderError
from app.core.llm.base import LLMProvider, LLMResponse, T


class GroqProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, timeout: int) -> None:
        self.client = AsyncGroq(api_key=api_key, timeout=timeout, max_retries=2)
        self.model = model

    async def structured(
        self, *, system: str, prompt: str, output_model: type[T], temperature: float = 0
    ) -> LLMResponse:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=temperature,
            )
            content = response.choices[0].message.content or "{}"
            parsed = output_model.model_validate(json.loads(content))
            usage = response.usage
            return LLMResponse(
                output=parsed,
                input_tokens=usage.prompt_tokens if usage else 0,
                output_tokens=usage.completion_tokens if usage else 0,
            )
        except Exception as exc:
            raise ProviderError(f"Groq request failed: {type(exc).__name__}") from exc
