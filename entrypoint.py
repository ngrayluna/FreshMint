import argparse
import pandas as pd

from schemas.response import ResponseObject
from prompts.escalation_criteria import ESCALATION_CRITERIA
from utils.logging_config import LOGGER
from graphs.escalation import FEEDBACK_GRAPH

def main(args):
    LOGGER.info("Starting the feedback processing graph.")

    # Read file CSV file into a DataFrame
    data = pd.read_csv(args.input_file)

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

    # Test on a single feedback entry
    FEEDBACK_GRAPH.invoke({
        "feedback": test.comment,
        "response_object": test,
        "escalation_text_criteria": ESCALATION_CRITERIA,
        "requires_escalation": False,
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the feedback processing graph.")
    parser.add_argument("--input_file", required=True, help="Path to the input file containing feedback messages.")
    main(args = parser.parse_args())