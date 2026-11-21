from whychanged import confirm, store
from whychanged.models import ChangeContext, Draft, SettingChange

CHANGE = SettingChange(key="train.lr", old="0.001", new="0.0005", file="configs/train.yaml")
CTX = ChangeContext(branch="exp", commit="abc123", changed_by="Alice", commit_messages=["lower lr"])


def answers(*replies):
    it = iter(replies)
    return lambda _prompt: next(it)


def test_accept_draft_and_fill_decider():
    e = confirm.ask(CHANGE, CTX, Draft("lower lr", "lower lr", "ai"), answers("a", "Bob"))
    assert (e.why, e.decided_by, e.status) == ("lower lr", "Bob", "confirmed")


def test_edit_replaces_reason_but_keeps_ai_draft():
    e = confirm.ask(CHANGE, CTX, Draft("lower lr", "lower lr", "ai"), answers("e", "loss spiked", "Bob"))
    assert e.why == "loss spiked" and e.ai_draft == "lower lr"


def test_unknown_draft_asks_for_reason():
    e = confirm.ask(CHANGE, CTX, Draft("unknown", "", "ai"), answers("a", "advisor asked", "Prof. Lin"))
    assert e.why == "advisor asked" and e.status == "confirmed"


def test_no_decider_stays_draft():
    e = confirm.ask(CHANGE, CTX, Draft("lower lr", "lower lr", "ai"), answers("a", ""))
    assert e.status == "draft" and e.decided_by == "(not filled)"


def test_skip_returns_none():
    assert confirm.ask(CHANGE, CTX, Draft("x", "x", "ai"), answers("s")) is None


def test_store_round_trip(tmp_path):
    e = confirm.auto(CHANGE, CTX, Draft("lower lr", "lower lr", "ai"), "Bob")
    store.append([e, e], repo=str(tmp_path))
    loaded = store.load(str(tmp_path))
    assert len(loaded) == 2 and loaded[0] == e


def test_load_missing_log_is_empty(tmp_path):
    assert store.load(str(tmp_path)) == []
