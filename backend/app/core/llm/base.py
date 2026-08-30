from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LLMResponse(BaseModel):
    output: BaseModel
    input_tokens: int = 0
    output_tokens: int = 0
    approximate_cost_usd: float = 0.0


class LLMProvider(ABC):
    @abstractmethod
    async def structured(
        self, *, system: str, prompt: str, output_model: type[T], temperature: float = 0
    ) -> LLMResponse:
        """Return provider output validated against a Pydantic model."""
