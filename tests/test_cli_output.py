from whychanged.cli import as_markdown
from whychanged.models import LogEntry


def test_markdown_table_has_one_row_per_entry():
    e = LogEntry(key="train.lr", old="0.001", new="0.0005", file="f", branch="b", commit="c",
                 changed_by="A", decided_by="Bob", why="loss unstable", ai_draft="", status="confirmed",
                 created_at="2026-11-21")
    lines = as_markdown([e, e]).splitlines()
    assert len(lines) == 4
    assert "| `train.lr` | 0.001 → 0.0005 | loss unstable | Bob | confirmed |" == lines[2]


def test_pipe_and_newline_in_reason_do_not_break_table():
    e = LogEntry(key="train.lr", old="0.001", new="0.0005", file="f", branch="b", commit="c",
                 changed_by="A", decided_by="Bob", why="loss | unstable\nin epoch 1", ai_draft="",
                 status="confirmed", created_at="2026-11-21")
    row = as_markdown([e]).splitlines()[2]
    assert row == "| `train.lr` | 0.001 → 0.0005 | loss \\| unstable in epoch 1 | Bob | confirmed |"
