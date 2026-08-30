# ADR 004: Controlled execution tools

Status: Accepted

Never pass arbitrary LLM text to a shell. The reproduction agent selects a symbolic command identifier mapped to a fixed argument tuple. Paths are resolved beneath a configured root, symlink escapes are rejected, reads are size-limited, output is truncated and processes time out. The Docker evaluation mount is read-only.
