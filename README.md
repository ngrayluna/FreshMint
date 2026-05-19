# MintFresh

Automated triage for user feedback submitted through our Mintlify documentation site.

## What it does

<img width="3528" height="2038" alt="image" src="https://github.com/user-attachments/assets/2947011b-8dc1-4cbf-965b-3a968557d9d7" />


Reads exported feedback (CSV) and runs each entry through a LangGraph workflow that:

1. **Extracts** the response into a structured `ResponseExtract` model (id, path, comment, source, status, helpfulness, contact, timestamp).
2. **Classifies** whether the feedback warrants a documentation update, using an LLM (`gpt-4o-mini`) checked against a configurable escalation criteria prompt.
3. **Escalates** by creating a Jira ticket when the criteria are met; otherwise the workflow ends.

## Layout

- `entrypoint.py` — builds and runs the LangGraph state machine
- `chains/` — LLM chains (escalation check) and the `ResponseExtract` schema
- `prompts/` — escalation criteria prompt
- `utils/graph_utils.py` — Jira ticket creation (currently stubbed to log; live Jira call is staged)
- `Data/` — raw exports, processing scripts, and a notebook for inspection

## Run

```bash
python entrypoint.py --input_file Data/ProcessedDataset/<file>.csv
```

## Status

MVP. Jira integration is wired but commented out pending credentials; the graph currently logs ticket details instead of posting.
