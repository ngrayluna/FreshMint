import os
from dotenv import load_dotenv

import requests
from requests.auth import HTTPBasicAuth

from utils.logging_config import LOGGER
from chains.response_extraction import ResponseExtract

load_dotenv()

def create_ticket(response: ResponseExtract) -> str:
    """Create a Jira ticket for the feedback, with different handling based on escalation status."""
    LOGGER.info("Creating Jira ticket for escalated feedback...")
    LOGGER.info(f"  response_id:    {response.response_id}")
    LOGGER.info(f"  date_submitted: {response.date_submitted}")
    LOGGER.info(f"  comment:        {response.comment}")


# def create_jira_ticket(response: ResponseExtract) -> str:
#     """Create a Jira ticket for the feedback and return the Jira issue key."""
#     LOGGER.info("Creating Jira ticket for escalated feedback...")
#     LOGGER.info("  response_id:    %s", response.response_id)
#     LOGGER.info("  date_submitted: %s", response.date_submitted)
#     LOGGER.info("  comment:        %s", response.comment)

#     jira_base_url = os.environ["JIRA_BASE_URL"].rstrip("/")
#     jira_email = os.environ["JIRA_EMAIL"]
#     jira_api_token = os.environ["JIRA_API_TOKEN"]
#     jira_project_key = os.environ["JIRA_PROJECT_KEY"]

#     url = f"{jira_base_url}/rest/api/3/issue"

#     payload = {
#         "fields": {
#             "project": {"key": jira_project_key},
#             "issuetype": {"name": "Task"},
#             "summary": f"Escalated feedback: {response.response_id}",
#             "description": {
#                 "type": "doc",
#                 "version": 1,
#                 "content": [
#                     {
#                         "type": "paragraph",
#                         "content": [
#                             {
#                                 "type": "text",
#                                 "text": (
#                                     "Escalated feedback was submitted.\n\n"
#                                     f"Response ID: {response.response_id}\n"
#                                     f"Date submitted: {response.date_submitted}\n"
#                                     f"Comment: {response.comment}"
#                                 ),
#                             }
#                         ],
#                     }
#                 ],
#             },
#         }
#     }

#     jira_response = requests.post(
#         url,
#         json=payload,
#         auth=HTTPBasicAuth(jira_email, jira_api_token),
#         headers={
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#         },
#         timeout=30,
#     )

#     if not jira_response.ok:
#         LOGGER.error("Failed to create Jira ticket: %s", jira_response.text)
#         jira_response.raise_for_status()

#     issue_key = jira_response.json()["key"]
#     LOGGER.info("Created Jira ticket: %s", issue_key)

#     return issue_key