# ADR 003: Provider abstraction

Status: Accepted

Agents depend on a small `LLMProvider.structured` interface and Pydantic response models. OpenAI and Groq adapters normalize structured output and usage. Provider/model selection is environment-only. Deterministic demo mode returns no provider object and follows an explicitly labeled offline path.
