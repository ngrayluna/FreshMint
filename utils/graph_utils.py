from utils.logging_config import LOGGER
from chains.response_extraction import ResponseExtract

def create_ticket(response: ResponseExtract) -> str:
    """Create a Jira ticket for the feedback, with different handling based on escalation status."""
    LOGGER.info("Creating Jira ticket for escalated feedback...")
    LOGGER.info(f"  response_id:    {response.response_id}")
    LOGGER.info(f"  date_submitted: {response.date_submitted}")
    LOGGER.info(f"  comment:        {response.comment}")