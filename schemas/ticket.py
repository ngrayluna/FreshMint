from pydantic import BaseModel, Field
from typing import List, Optional, Type

class TicketInputSchema(BaseModel):
    summary: str | None = Field(
        default=None,
        description="Summary of the ticket"
        )

    project: str | None= Field(
        default="DOCS",
        description="project name"
        )

    description: str | None = Field(
        default=None,
        description="Description of the work performed under this ticket."
        )

    issuetype: str | None = Field(
        default=None,
        description="The issue type of the ticket ",
        enum=["Task", "Epic"]
        )

    priority: Optional(str) | None = Field(
        description="The issue type of the ticket ", 
        enum=["Urgent", "Highest","High", "Low", "Lowest"]
        )