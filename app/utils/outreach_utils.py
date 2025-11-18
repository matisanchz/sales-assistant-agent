from typing import Tuple

def get_outreach_provided_missing_info(idea_type, form) -> str:
    provided_information = "\nUser-provided context - Generate outreach using this information:\n"

    provided_information += f"— **idea_type**: The user want a crafted {idea_type}\n"

    provided_information += f"- **User additional context** — The user provides extra information to build outreach in this Q&A form:\n"

    for item in form:
        q_r = f"  - {item.question}: {item.response}\n"
        provided_information += q_r
    
    return provided_information