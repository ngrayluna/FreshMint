import argparse

from fileinput import filename
from turtle import pd
from typing import TypedDict
from chains.escalation_check import ESCALATION_CHECK_CHAIN
from chains.response_extraction import ResponseExtract
from langgraph.graph import END, START, StateGraph
from utils.logging_config import LOGGER

class GraphState(TypedDict):
    """GraphState defines the structure of the state used in the feedback processing graph. It includes fields for the notice message, extracted response information, escalation criteria, and follow-up details. This structured state allows for consistent data handling throughout the graph's execution."""
    feedback: str
    feedback_extracted: ResponseExtract | None
    escalation_text_criteria: str
    requires_escalation: bool
    follow_ups: dict[str, bool] | None
    current_follow_up: str | None

workflow = StateGraph(GraphState)



def main(args):
    LOGGER.info("Starting the feedback processing graph.")

    # Read file CSV file into a DataFrame
    data = pd.read_csv(args.input_file)

    # Step 1: Extract response information from the feedback messages. Store this info into the ResponseExtract model.



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the feedback processing graph.")
    parser.add_argument("--input_file", required=True, help="Path to the input file containing feedback messages.")
    main(args = parser.parse_args())