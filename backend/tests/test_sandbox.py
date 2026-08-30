from pathlib import Path

import pytest

from app.core.errors import SandboxViolation
from app.tools.sandbox import RepositorySandbox


def sandbox() -> RepositorySandbox:
    base = Path(__file__).resolve().parents[2] / "evaluation_cases"
    return RepositorySandbox(base / "02_null_handling_regression", base)


def test_reads_and_runs_allowlisted_reproduction() -> None:
    box = sandbox()
    assert "promo_code.strip" in box.read_file("checkout_service.py")
    result = box.run("reproduction")
    assert result.exit_code == 0 and "TRACEROOT_REPRODUCED" in result.stdout


@pytest.mark.parametrize(
    "path", ["../01_missing_environment_variable/app.py", "../../.env", "C:/Windows/win.ini"]
)
def test_blocks_path_escape(path: str) -> None:
    with pytest.raises(SandboxViolation):
        sandbox().read_file(path)


def test_blocks_arbitrary_commands() -> None:
    with pytest.raises(SandboxViolation):
        sandbox().run("shell")
