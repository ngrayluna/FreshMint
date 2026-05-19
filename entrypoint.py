import argparse
import pandas as pd
from fileinput import filename

from chains.response_extraction import ResponseExtract
#from chains.escalation_check import ESCALATION_CHECK_CHAIN

from utils.logging_config import LOGGER


def main(args):
    LOGGER.info("Starting the feedback processing graph.")

    # Read file CSV file into a DataFrame
    data = pd.read_csv(args.input_file)

    # Step 1: Extract response information from the feedback messages. Store this info into the ResponseExtract model.
    for index, row in data.iterrows():
        test = ResponseExtract(
            response_id=row['id'],
            path=row['path'],
            source=row['source'],
            status=row['status'],
            helpful=row['helpful'],
            contact=row['contact'],
            date_submitted=row['createdAt']
        )
        break
    print(test)
    LOGGER.info(f"Extracted response information: {test}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the feedback processing graph.")
    parser.add_argument("--input_file", required=True, help="Path to the input file containing feedback messages.")
    main(args = parser.parse_args())