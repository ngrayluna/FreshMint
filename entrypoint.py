import argparse
import pandas as pd
from typing import TypedDict

from chains.response_extraction import ResponseExtract
from chains.escalation_check import ESCALATION_CHECK_CHAIN

from utils.logging_config import LOGGER

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

    state["requires_escalation"] = text_check

    return state



############################################################

def main(args):
    LOGGER.info("Starting the feedback processing graph.")

    escalation_criteria = """
- The user indicates that the documentation is outdated or incorrect.
- The user expresses confusion or misunderstanding that could be resolved with clearer documentation.
- The user provides specific suggestions for improving the documentation.
- The feedback highlights a gap in the documentation that led to a negative experience.
"""

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

    
    LOGGER.info("Checking escalation status for the extracted response...")
    print(ESCALATION_CHECK_CHAIN.invoke(
        {
            "escalation_criteria": escalation_criteria,
            "message": test.comment,
        }))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the feedback processing graph.")
    parser.add_argument("--input_file", required=True, help="Path to the input file containing feedback messages.")
    main(args = parser.parse_args())