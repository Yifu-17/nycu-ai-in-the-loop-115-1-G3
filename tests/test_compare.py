import subprocess
from pathlib import Path

from whychanged.compare import compare
from whychanged.models import LogEntry

ROOT = Path(__file__).resolve().parent.parent


def test_compare_branches_with_reason(tmp_path):
    repo = str(tmp_path / "lab")
    subprocess.run(["bash", str(ROOT / "demo" / "make_demo_repo.sh"), repo], check=True, capture_output=True)
    logged = LogEntry(key="train.lr", old="0.001", new="0.0005", file="configs/train.yaml",
                      branch="exp/old-lr", commit="x", changed_by="A", decided_by="B",
                      why="loss unstable", ai_draft="", status="confirmed", created_at="2026-11-01")

    rows = {r["key"]: r for r in compare("main", "exp/old-lr", ["configs/train.yaml", ".env.example"], [logged], cwd=repo)}

    assert set(rows) == {"train.lr", "DATA_DIR"}
    assert rows["train.lr"]["b"] == "0.0005"
    assert rows["train.lr"]["why_b"].why == "loss unstable"
    assert rows["train.lr"]["why_a"] is None


def test_latest_reason_picks_newest_for_that_value():
    from whychanged.compare import latest_reason

    def e(new, when, why):
        return LogEntry(key="train.lr", old="x", new=new, file="f", branch="b", commit="c", changed_by="A",
                        decided_by="B", why=why, ai_draft="", status="confirmed", created_at=when)

    entries = [e("0.001", "2026-11-01", "first"), e("0.0005", "2026-11-02", "lower"), e("0.001", "2026-11-03", "revert")]
    assert latest_reason(entries, "train.lr", "0.001").why == "revert"
    assert latest_reason(entries, "model.lr", "0.001") is None
