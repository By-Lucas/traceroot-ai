from app.schemas.domain import ReproductionOutput
from app.tools.sandbox import RepositorySandbox


def reproduce(sandbox: RepositorySandbox | None) -> ReproductionOutput:
    if sandbox is None:
        return ReproductionOutput(
            command="not run",
            exit_code=125,
            stdout="",
            stderr="No approved repository was supplied",
            matched_hypotheses=[],
            duration_ms=0,
        )
    result = sandbox.run("reproduction")
    return ReproductionOutput(
        command=result.command,
        exit_code=result.exit_code,
        stdout=result.stdout,
        stderr=result.stderr,
        matched_hypotheses=["H1"] if "TRACEROOT_REPRODUCED" in result.stdout else [],
        duration_ms=result.duration_ms,
    )
