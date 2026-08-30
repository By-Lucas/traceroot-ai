class TraceRootError(Exception):
    """Base domain error."""


class ProviderError(TraceRootError):
    """LLM provider failed or returned invalid output."""


class SandboxViolation(TraceRootError):
    """A tool attempted to escape the controlled sandbox."""


class BudgetExceeded(TraceRootError):
    """An investigation exceeded a configured execution budget."""
