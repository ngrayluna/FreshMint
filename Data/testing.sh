#!/usr/bin/env bash
set -euo pipefail

DATE_FROM="2026-01-01"
DATE_TO="2026-05-15"

RAW_DATASET_DIR="RawDataset"
PROCESSED_DATASET_DIR="ProcessedDataset"

echo "Fetching responses from ${DATE_FROM} to ${DATE_TO}..."
bash get_responses.sh "$DATE_FROM" "$DATE_TO" "${RAW_DATASET_DIR}/feedback_${DATE_FROM//-/}_${DATE_TO//-/}.json"

echo "Converting JSON to CSV..."
bash json_to_csv.sh "${RAW_DATASET_DIR}/feedback_${DATE_FROM//-/}_${DATE_TO//-/}.json" "${RAW_DATASET_DIR}/feedback_${DATE_FROM//-/}_${DATE_TO//-/}.csv"

#echo "Processing dataset..."
python process_dataset.py --file_path "${RAW_DATASET_DIR}/feedback_${DATE_FROM//-/}_${DATE_TO//-/}.csv" --output_dir "${PROCESSED_DATASET_DIR}"