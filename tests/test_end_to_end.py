"""Runs the real CLI on the demo repo, offline (no API key needed)."""
import subprocess
from pathlib import Path

from whychanged.cli import main
from whychanged.store import load

ROOT = Path(__file__).resolve().parent.parent


def make_repo(tmp_path):
    repo = tmp_path / "lab"
    subprocess.run(["bash", str(ROOT / "demo" / "make_demo_repo.sh"), str(repo)], check=True, capture_output=True)
    return str(repo)


def test_log_then_history_then_compare(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("WHYCHANGED_OFFLINE", "1")
    repo = make_repo(tmp_path)
    main(["--repo", repo, "init", "--watch", "configs/train.yaml", ".env.example"])
    main(["--repo", repo, "log", "--base", "main", "--yes", "--decided-by", "Bob"])

    entries = {e.key: e for e in load(repo)}
    assert set(entries) == {"train.dropout", "train.batch_size"}
    assert entries["train.dropout"].why.startswith("raise dropout")
    assert entries["train.batch_size"].why == "unknown"
    assert entries["train.dropout"].changed_by == "Alice"
    assert entries["train.dropout"].status == "draft"

    capsys.readouterr()
    main(["--repo", repo, "history", "dropout"])
    assert "0.1 -> 0.3" in capsys.readouterr().out

    main(["--repo", repo, "compare", "feat/head-dropout", "exp/old-lr"])
    out = capsys.readouterr().out
    assert "train.lr" in out and "DATA_DIR" in out and "train.dropout" in out
