import hashlib
import os
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from app.core.errors import SandboxViolation

MAX_READ_BYTES = 250_000
ALLOWED_COMMANDS: dict[str, tuple[str, ...]] = {
    "pytest": ("python", "-m", "pytest"),
    "reproduction": ("python", "reproduce.py"),
}


@dataclass(frozen=True)
class CommandResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int


class RepositorySandbox:
    def __init__(self, root: Path, allowed_base: Path) -> None:
        self.allowed_base = allowed_base.resolve()
        self.root = root.resolve()
        try:
            self.root.relative_to(self.allowed_base)
        except ValueError as exc:
            raise SandboxViolation("Repository is outside the approved sandbox") from exc

    def _safe_path(self, relative_path: str) -> Path:
        if "\0" in relative_path:
            raise SandboxViolation("Invalid path")
        candidate = (self.root / relative_path).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise SandboxViolation("Path traversal blocked") from exc
        if candidate.is_symlink():
            target = candidate.resolve()
            try:
                target.relative_to(self.root)
            except ValueError as exc:
                raise SandboxViolation("Symlink escape blocked") from exc
        return candidate

    def read_file(self, relative_path: str) -> str:
        path = self._safe_path(relative_path)
        if not path.is_file():
            raise FileNotFoundError(relative_path)
        if path.stat().st_size > MAX_READ_BYTES:
            raise SandboxViolation("File exceeds read limit")
        return path.read_text(encoding="utf-8", errors="replace")

    def search_files(self, pattern: str) -> list[str]:
        safe = re.compile(pattern, re.IGNORECASE)
        matches: list[str] = []
        for path in self.root.rglob("*"):
            if path.is_file() and not path.is_symlink() and path.stat().st_size <= MAX_READ_BYTES:
                rel = str(path.relative_to(self.root)).replace(os.sep, "/")
                if safe.search(rel) or safe.search(
                    path.read_text(encoding="utf-8", errors="replace")
                ):
                    matches.append(rel)
                if len(matches) >= 100:
                    break
        return matches

    def hash_file(self, relative_path: str) -> str:
        return hashlib.sha256(self.read_file(relative_path).encode()).hexdigest()

    def run(self, command_name: str, timeout_seconds: int = 30) -> CommandResult:
        if command_name not in ALLOWED_COMMANDS:
            raise SandboxViolation(f"Command is not allowlisted: {command_name}")
        started = time.perf_counter()
        try:
            completed = subprocess.run(
                ALLOWED_COMMANDS[command_name],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=min(timeout_seconds, 60),
                check=False,
                env={"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"},
            )
            return CommandResult(
                command=" ".join(ALLOWED_COMMANDS[command_name]),
                exit_code=completed.returncode,
                stdout=completed.stdout[-20_000:],
                stderr=completed.stderr[-20_000:],
                duration_ms=int((time.perf_counter() - started) * 1000),
            )
        except subprocess.TimeoutExpired as exc:
            raw_stdout = exc.stdout or ""
            timeout_stdout = (
                raw_stdout.decode("utf-8", errors="replace")
                if isinstance(raw_stdout, bytes)
                else raw_stdout
            )
            return CommandResult(
                command=" ".join(ALLOWED_COMMANDS[command_name]),
                exit_code=124,
                stdout=timeout_stdout[-20_000:],
                stderr="Command timed out",
                duration_ms=int((time.perf_counter() - started) * 1000),
            )
