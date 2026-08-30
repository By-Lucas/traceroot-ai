from dataclasses import dataclass, field
from typing import Any


@dataclass
class InvestigationContext:
    title: str
    description: str
    logs: str
    stack_trace: str
    repository_path: str | None
    case_metadata: dict[str, Any] = field(default_factory=dict)
