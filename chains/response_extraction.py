"""
BaseModel that defines the structure of the response extraction output. This model includes fields for response ID, path, date submitted, source, status, helpfulness, and contact information. It also includes a computed field to convert the date string into a date object for easier manipulation in downstream processes.
"""

from datetime import datetime, date
from pydantic import BaseModel, Field, computed_field

class ResponseExtract(BaseModel):
    response_id: str | None = Field(
        default=None,
        description="The unique identifier for the response."
    )

    path: str | None = Field(
        default=None,
        description="The path or URL to the source document."
    )

    date_submitted: datetime | None = Field(
        default=None,
        description="Timestamp when the feedback was submitted in YYYY-MM-DD format."
    )

    source: str | None = Field(
        default=None,
        description="Where the feedback originated. code_snippet is feedback on a code block, contextual is page-level feedback."
    )

    status: str | None = Field(
        default=None,
        description="The current status of the feedback."
    )

    helpful: bool | None = Field(
        default=None,
        description="Whether the user found the content helpful."
    )

    contact: str | None = Field(
        default=None,
        description="Email address the user provided for follow-up."
    )

    @computed_field
    @property
    def date_submitted_as_date(self) -> date | None:
        if self.date_submitted is None:
            return None
        return self.date_submitted.date()