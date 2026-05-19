import argparse
import pandas as pd
from typing import TypedDict

from chains.response_extraction import ResponseExtract
from chains.escalation_check import ESCALATION_CHECK_CHAIN
from langgraph.graph import END, START, StateGraph

from utils.logging_config import LOGGER
from utils.graph_utils import create_ticket

class GraphState(TypedDict):
    feedback: str
    feedback_extracted: ResponseExtract | None
    escalation_text_criteria: str
    requires_escalation: bool

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
    create_ticket(state["requires_escalation"])
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

def main(args):
    LOGGER.info("Starting the feedback processing graph.")

    ######## GRAPH DEFINITION ########

    escalation_criteria = """
- The user indicates that the documentation is outdated or incorrect.
- The user expresses confusion or misunderstanding that could be resolved with clearer documentation.
- The user provides specific suggestions for improving the documentation.
- The feedback highlights a gap in the documentation that led to a negative experience.
"""

    workflow = StateGraph(GraphState)
    workflow.add_node("check_escalation_status", check_escalation_status_node)
    workflow.add_node("create_ticket", create_ticket_node)

    workflow.add_edge(START, check_escalation_status_node)
    workflow.add_conditional_edge(
        "check_escalation_status_node",
        route_escalation_status_edge,
        {
            "create_ticket": "create_ticket",
            END: END,
        },
    )
    FEEDBACK_GRAPH = workflow.compile()

    ##################################

    # Read file CSV file into a DataFrame
    data = pd.read_csv(args.input_file)

    # Step 1: Extract response information from the feedback messages. Store this info into the ResponseExtract model.
    for index, row in data.iterrows():
        test = ResponseExtract(
            response_id=row['id'],
            path=row['path'],
            comment=row['comment'],
            source=row['source'],
            status=row['status'],
            helpful=row['helpful'],
            contact=row['contact'],
            date_submitted=row['createdAt']
        )
        break
    LOGGER.info(f"Extracted response information: {test}")

    
    # LOGGER.info("Checking escalation status for the extracted response...")
    # print(ESCALATION_CHECK_CHAIN.invoke(
    #     {
    #         "escalation_criteria": escalation_criteria,
    #         "message": test.comment,
    #     }))

    # Test on a single feedback entry
    FEEDBACK_GRAPH.invoke(test)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the feedback processing graph.")
    parser.add_argument("--input_file", required=True, help="Path to the input file containing feedback messages.")
    main(args = parser.parse_args())