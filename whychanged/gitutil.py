"""Small wrappers around the git command line."""
import subprocess
from typing import Optional


def git(*args: str, cwd: str = ".") -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def show_file(rev: str, path: str, cwd: str = ".") -> Optional[str]:
    """Return the file content at a revision, or None if it does not exist there."""
    try:
        return git("show", f"{rev}:{path}", cwd=cwd)
    except RuntimeError:
        return None


def changed_files(base: str, head: str, cwd: str = ".") -> list[str]:
    out = git("diff", "--name-only", f"{base}...{head}", cwd=cwd)
    return [line for line in out.splitlines() if line]
