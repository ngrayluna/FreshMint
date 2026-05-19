from typing import TypedDict

class GraphState(TypedDict):
    feedback: str
    feedback_extracted: ResponseExtract | None
    escalation_text_criteria: str
    requires_escalation: bool
    follow_ups: dict[str, bool] | None
    current_follow_up: str | None
