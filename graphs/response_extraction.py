from typing import TypedDict
from utils.logging_config import LOGGER
from chains.escalation_check import ESCALATION_CHECK_CHAIN
from chains.response_extraction import ResponseExtract

class GraphState(TypedDict):
    feedback: str
    feedback_extracted: ResponseExtract | None
    escalation_text_criteria: str
    requires_escalation: bool
    follow_ups: dict[str, bool] | None
    current_follow_up: str | None


def check_escalation_status_node(state: GraphState) -> GraphState:
    """Determine whether a response needs escalation""" 

    LOGGER.info("Determining escalation status...")

    text_check = ESCALATION_CHECK_CHAIN.invoke(
        {
            "escalation_criteria": state["escalation_text_criteria"],
            "message": state["feedback"],
        }
    ).needs_escalation