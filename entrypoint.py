import argparse
import pandas as pd
from typing import TypedDict

from chains.response_extraction import ResponseObject
from chains.escalation_check import ESCALATION_CHECK_CHAIN
from langgraph.graph import END, START, StateGraph

from prompts.escalation_criteria import ESCALATION_CRITERIA
from utils.logging_config import LOGGER
from utils.graph_utils import create_ticket

class GraphState(TypedDict):
    feedback: str
    response_object: ResponseObject | None
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

def main(args):
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
    ##################################

    # Read file CSV file into a DataFrame
    data = pd.read_csv(args.input_file)

    # Step 1: Extract response information from the feedback messages. Store this info into the ResponseObject model.
    # for index, row in data.iterrows():
    #     test = ResponseObject(
    #         response_id=row['id'],
    #         path=row['path'],
    #         comment=row['comment'],
    #         source=row['source'],
    #         status=row['status'],
    #         helpful=row['helpful'],
    #         contact=row['contact'],
    #         date_submitted=row['createdAt']
    #     )
    #     break

    entry_num = 5
    test = ResponseObject(
        response_id=data.iloc[entry_num]['id'],
        path=data.iloc[entry_num]['path'],
        comment=data.iloc[entry_num]['comment'],
        source=data.iloc[entry_num]['source'],
        status=data.iloc[entry_num]['status'],
        helpful=data.iloc[entry_num]['helpful'],
        contact=data.iloc[entry_num]['contact'],
        date_submitted=data.iloc[entry_num]['createdAt']
    )


    LOGGER.info(f"Extracted response information: {test}")

    
    # LOGGER.info("Checking escalation status for the extracted response...")
    # print(ESCALATION_CHECK_CHAIN.invoke(
    #     {
    #         "escalation_criteria": escalation_criteria,
    #         "message": test.comment,
    #     }))


    escalation_criteria = ESCALATION_CRITERIA
    LOGGER.info(f"Using the following escalation criteria:\n{escalation_criteria}")

    # image = FEEDBACK_GRAPH.get_graph().draw_mermaid_png()
    # with open("notice_extraction_graph.png", mode="wb") as f:
    #     f.write(image)

    # Test on a single feedback entry
    FEEDBACK_GRAPH.invoke({
        "feedback": test.comment,
        "response_object": test,
        "escalation_text_criteria": escalation_criteria,
        "requires_escalation": False,
    })
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the feedback processing graph.")
    parser.add_argument("--input_file", required=True, help="Path to the input file containing feedback messages.")
    main(args = parser.parse_args())