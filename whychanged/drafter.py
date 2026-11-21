"""STUB: always says unknown. Replaced by the real AI drafter."""
from .models import Draft


def draft_reason(change, ctx):
    return Draft(reason="unknown", evidence="", source="fake")
