from typing import List
from pydantic import BaseModel, Field
from langchain.tools import tool

from typing import List
from pydantic import BaseModel, Field
from langchain.tools import tool

# ---------- RESPONSE SCHEMAS (pitch, email, dm) ----------

class OutreachPitch(BaseModel):
    """
    Use this schema ONLY when the user requests to write a Pitch.
    """
    title: str = Field(
        description=(
            "A clear and engaging subject line or label for the outreach pitch.\n"
            "- Must quickly communicate the core value or angle of the pitch.\n"
            "- Examples:\n"
            "  - 'Boost your onboarding efficiency by 30%'\n"
            "  - 'Reducing manual workflows for your CS team'\n"
            "  - 'Helping your sales reps close faster with automation'"
        )
    )
    body: str = Field(
        description=(
            "The full pitch text in a professional yet personable B2B tone.\n"
            "- Clearly introduce the sender (AE/CSM) and their company.\n"
            "- Highlight the prospect's likely pains or goals based on the provided context.\n"
            "- Connect those pains/goals to the product's value proposition.\n"
            "- Keep it concise, persuasive, and easy to scan.\n"
            "- End with a clear, low-friction call to action (e.g. 'worth a 15-min fit check?')."
        )
    )


class OutreachEmail(BaseModel):
    """
    Use this schema ONLY when the user requests to write an Email.
    """
    title: str = Field(
        description=(
            "The subject line of the email.\n"
            "- Must be clear, concise, and relevant to the prospect's role and problem.\n"
            "- Examples:\n"
            "  - 'Quick idea to streamline your CS workflows'\n"
            "  - 'Improving pipeline visibility for your sales team'\n"
            "  - 'Reducing manual busywork for your ops team'"
        )
    )
    body: str = Field(
        description=(
            "The complete B2B outreach email text.\n"
            "- Must be formatted with proper paragraph breaks (using '\\n').\n"
            "- Include all of the following in order:\n"
            "  1. Professional greeting (e.g., 'Hi [First Name],').\n"
            "  2. Brief intro of the sender and company.\n"
            "  3. One or two sentences showing relevance (role, industry, or pain point).\n"
            "  4. Clear value proposition or idea (focused on outcomes, not features).\n"
            "  5. Simple, low-friction call to action (e.g. propose a short call or ask a yes/no question).\n"
            "  6. Professional closing (e.g., 'Best regards,').\n"
            "  7. Signature placeholders ('[Your Name]', '[Your Role]', '[Company]', '[Contact Info]')."
        )
    )


class OutreachDM(BaseModel):
    """
    Use this schema ONLY when the user requests to write a DM (Direct Message).
    """
    body: str = Field(
        description=(
            "The entire text content of the DM.\n"
            "- Must be concise (ideally under 80–100 words).\n"
            "- Conversational, friendly, and easy to read.\n"
            "- Include: quick greeting, micro-intro, relevant value hook, and a soft CTA.\n"
            "- Examples of CTAs: 'open to a quick chat?', 'worth a short call?', 'ok if I send more details?'.\n"
            "- Emojis are allowed but should be used sparingly and stay professional."
        )
    )


class OutreachPitchResponse(BaseModel):
    """
    Final structured response with a list of outreach pitches.
    """
    pitches: List[OutreachPitch] = Field(
        description="List of structured outreach pitch ideas tailored to B2B prospects or customers."
    )


class OutreachEmailResponse(BaseModel):
    """
    Final structured response with a list of outreach emails.
    """
    emails: List[OutreachEmail] = Field(
        description="List of structured outreach email ideas for B2B prospects or customers."
    )


class OutreachDMResponse(BaseModel):
    """
    Final structured response with a list of outreach DMs.
    """
    dms: List[OutreachDM] = Field(
        description="List of structured outreach DM ideas for channels like LinkedIn or similar."
    )

# ---------- TOOLS (pitch, email, dm) ----------

@tool(args_schema=OutreachPitchResponse, return_direct=True)
def pitch_response_tool(pitches: List[OutreachPitch]):
    """
    Final response with B2B outreach pitches.

    You MUST use this tool only when:
    - All required context has been gathered.
    - You're ready to output final pitch ideas the user could send to a prospect or customer.

    Do NOT use unless ready to complete the task.
    """
    return [pitch.model_dump(mode="json") for pitch in pitches]


@tool(args_schema=OutreachEmailResponse, return_direct=True)
def email_response_tool(emails: List[OutreachEmail]):
    """
    Final response with B2B outreach emails.

    You MUST use this tool only when:
    - All required context has been gathered.
    - You're ready to output final email drafts the user could send directly (after minor edits).

    Do NOT use unless ready to complete the task.
    """
    return [email.model_dump(mode="json") for email in emails]


@tool(args_schema=OutreachDMResponse, return_direct=True)
def dm_response_tool(dms: List[OutreachDM]):
    """
    Final response with B2B outreach DMs.

    You MUST use this tool only when:
    - All required context has been gathered.
    - You're ready to output final DM drafts suitable for LinkedIn or similar channels.

    Do NOT use unless ready to complete the task.
    """
    return [dm.model_dump(mode="json") for dm in dms]