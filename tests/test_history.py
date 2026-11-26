from whychanged.history import history
from whychanged.models import LogEntry


def entry(key, old, new, when, why="r"):
    return LogEntry(key=key, old=old, new=new, file="f", branch="b", commit="c",
                    changed_by="A", decided_by="B", why=why, ai_draft=why,
                    status="confirmed", created_at=when)


ENTRIES = [
    entry("train.lr", "0.0005", "0.001", "2026-11-10", "revert"),
    entry("train.lr", "0.001", "0.0005", "2026-11-02", "unstable"),
    entry("model.lr", "1", "2", "2026-11-05"),
    entry("train.dropout", "0.1", "0.3", "2026-11-01"),
]


def test_history_by_full_key_is_sorted_oldest_first():
    assert [e.why for e in history(ENTRIES, "train.lr")] == ["unstable", "revert"]


def test_history_by_short_key_matches_all_sections():
    assert len(history(ENTRIES, "lr")) == 3


def test_history_unknown_key_is_empty():
    assert history(ENTRIES, "epochs") == []
