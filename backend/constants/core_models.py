from pydantic import BaseModel

class StartProspectingPayload(BaseModel):
    profile_url: str
    intent: str
    dry_run: bool = False