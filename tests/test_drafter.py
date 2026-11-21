from whychanged.drafter import evidence_is_real, offline_draft
from whychanged.models import ChangeContext, SettingChange

CHANGE = SettingChange(key="train.dropout", old="0.1", new="0.3", file="configs/train.yaml")


def ctx(*messages, note=""):
    return ChangeContext(branch="b", commit="abc", changed_by="A", commit_messages=list(messages), note=note)


def test_offline_uses_line_that_names_the_setting():
    d = offline_draft(CHANGE, ctx("fix typo", "raise dropout, overfitting"))
    assert d.reason == "raise dropout, overfitting"


def test_offline_says_unknown_without_evidence():
    assert offline_draft(CHANGE, ctx("update model")).reason == "unknown"


def test_made_up_evidence_is_rejected():
    c = ctx("raise dropout, overfitting")
    assert evidence_is_real("raise dropout", CHANGE, c)
    assert not evidence_is_real("dropout reduces variance", CHANGE, c)
    assert not evidence_is_real("", CHANGE, c)
