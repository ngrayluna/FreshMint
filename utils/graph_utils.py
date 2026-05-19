import os
from dotenv import load_dotenv

import requests
from requests.auth import HTTPBasicAuth

from utils.logging_config import LOGGER
from schemas.response import ResponseObject

load_dotenv()

def create_ticket(response: ResponseObject) -> str:
    """Create a Jira ticket for the feedback, with different handling based on escalation status."""
    LOGGER.info("Creating Jira ticket for escalated feedback...")
    LOGGER.info(f"  response_id:    {response.response_id}")
    LOGGER.info(f"  date_submitted: {response.date_submitted}")
    LOGGER.info(f"  comment:        {response.comment}")