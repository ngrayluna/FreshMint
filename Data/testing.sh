#!/usr/bin/env bash
set -euo pipefail

DATE_FROM="2026-01-01"
DATE_TO="2026-05-15"

echo "Fetching responses from ${DATE_FROM} to ${DATE_TO}..."
bash get_responses.sh "$DATE_FROM" "$DATE_TO" "feedback_${DATE_FROM//-/}_${DATE_TO//-/}.json"

echo "Converting JSON to CSV..."
bash json_to_csv.sh "feedback_${DATE_FROM//-/}_${DATE_TO//-/}.json" "feedback_${DATE_FROM//-/}_${DATE_TO//-/}.csv"

#echo "Processing dataset..."
python process_dataset.py --file_path "feedback_${DATE_FROM//-/}_${DATE_TO//-/}.csv"