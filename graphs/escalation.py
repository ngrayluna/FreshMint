from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from utils.logging_config import LOGGER
from schemas.response import ResponseObject
from chains.escalation_check import ESCALATION_CHECK_CHAIN
from utils.graph_utils import create_ticket

class GraphState(TypedDict):
    feedback: str
    response_object: ResponseObject | None
    escalation_text_criteria: str
    requires_escalation: bool
    doc_owner: str | None

def check_escalation_status_node(state: GraphState) -> GraphState:
    """Determine whether a response needs escalation""" 

    LOGGER.info("Determining escalation status...")

    text_check = ESCALATION_CHECK_CHAIN.invoke(
        {
            "escalation_criteria": state["escalation_text_criteria"],
            "message": state["feedback"],
        }
    ).needs_escalation

    state["requires_escalation"] = text_check
    return state

def create_ticket_node(state: GraphState) -> GraphState:
    """Create a Jira ticket for the feedback"""
    LOGGER.info("Creating a Jira ticket for the feedback...")
    create_ticket(state["response_object"])
    return state


def route_escalation_status_edge(state: GraphState) -> str:
    """Determine whether to route to create_ticket or end the workflow based on escalation status."""
    if state["requires_escalation"]:
        LOGGER.info("Escalation needed!")
        return "create_ticket"
    else:
        LOGGER.info("No escalation needed")
        return END


############################################################


LOGGER.info("Starting the feedback processing graph.")

######## GRAPH DEFINITION ########
workflow = StateGraph(GraphState)
workflow.add_node("check_escalation_status", check_escalation_status_node)
workflow.add_node("create_ticket", create_ticket_node)

workflow.add_edge(START, "check_escalation_status")
workflow.add_conditional_edges(
    "check_escalation_status",
    route_escalation_status_edge,
    {
        "create_ticket": "create_ticket",
        END: END,
    },
)

FEEDBACK_GRAPH = workflow.compile()
