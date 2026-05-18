#!/usr/bin/env bash
# Usage: ./json_to_csv.sh INPUT_JSON OUTPUT_CSV
set -euo pipefail

INPUT_JSON="${1:?Usage: $0 INPUT_JSON OUTPUT_CSV}"
OUTPUT_CSV="${2:?Usage: $0 INPUT_JSON OUTPUT_CSV}"

jq -r '
  [
    "id",
    "path",
    "comment",
    "createdAt",
    "source",
    "status",
    "helpful",
    "contact"
  ],
  (
    .feedback[] |
    [
      .id,
      .path,
      .comment,
      .createdAt,
      .source,
      .status,
      .helpful,
      .contact
    ]
  )
  | @csv
' "$INPUT_JSON" > "$OUTPUT_CSV"

echo "Saved CSV to $OUTPUT_CSV"
