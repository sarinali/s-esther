from pydantic import BaseModel

class StartProspectingPayload(BaseModel):
    profile_url: str
    intent: str