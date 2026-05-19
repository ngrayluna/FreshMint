from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class EscalationCheck(BaseModel):
    needs_escalation: bool = Field(
        description="""Whether the feedback indicates a documentation
        update based on the escalation criteria."""
    )

escalation_criteria = """
- The user indicates that the documentation is outdated or incorrect.
- The user expresses confusion or misunderstanding that could be resolved with clearer documentation.
- The user provides specific suggestions for improving the documentation.
- The feedback highlights a gap in the documentation that led to a negative experience.
"""

escalation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Determine whether the following response received
            from a user requires a documentation update based on the following
            criteria: {escalation_criteria}.

            Here's the notice message:

            {message}
            """,
        )
    ]
)

escalation_check_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

ESCALATION_CHECK_CHAIN = (
    escalation_prompt
    | escalation_check_model.with_structured_output(EscalationCheck)
)