# Usage: python process_dataset.py path/to/dataset.csv

import argparse
import pandas as pd

def read_dataset(file_path: str) -> pd.DataFrame:
    """Reads the dataset from a CSV file and returns a DataFrame.
    
    Args:
        file_path (str): Path to the CSV file.
    """
    return pd.read_csv(file_path)

def clean_helpful_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Replace missing values in the 'helpful' column with 'Other'."""
    return df.assign(
        helpful=lambda d: d["helpful"].fillna("Other")
    )


def clean_contact_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Replace missing values in the 'contact' column with a default message."""
    return df.assign(
        contact=lambda d: d["contact"].fillna("No contact provided")
    )


def filter_non_helpful_feedback(df: pd.DataFrame) -> pd.DataFrame:
    """Keep feedback entries that were not marked as helpful."""
    return df.loc[df["helpful"].ne(True)].copy()

def remove_non_english_feedback(df: pd.DataFrame) -> pd.DataFrame:
    """TODO: Remove feedback entries that are not in English."""

def process(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Load, clean, and filter doc feedback."""
    return (
        raw_df
        .pipe(clean_helpful_nan)
        .pipe(clean_contact_nan)
        .pipe(filter_non_helpful_feedback)
    )


    

def main(args):

    # Read dataset into a DataFrame
    print(f"Reading dataset from {args.file_path}...")
    dataset = read_dataset(args.file_path).copy()

    # Make a copy of the dataset to avoid modifying the original DataFrame
    dataset_copy = dataset.copy()

    # Process the dataset
    processed_feedback = process(dataset_copy)
    
    # Save the processed feedback to a new CSV file
    # Extract dataset name from the input file path for naming the output file
    output_file_name = args.file_path.replace(".csv", "")
    processed_feedback.to_csv(f"processed_{output_file_name}.csv", index=False)
    print(f"Processed feedback saved to 'processed_{output_file_name}.csv'.")

    # Save procssed feedbak as a JSON file for use in the next step of the pipeline
    processed_feedback.to_json(f"processed_{output_file_name}.json", orient="records", lines=True)
    print(f"Processed feedback saved to 'processed_{output_file_name}.json'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process doc feedback dataset.")
    parser.add_argument("--file_path", help="Path to the CSV file containing the dataset.")
    args = parser.parse_args()
    main(args)