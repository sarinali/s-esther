from typing import List, Optional
from pydantic import BaseModel


class SearchUserPayload(BaseModel):
    profile_url: str
    location: Optional[str] = None
    limit: Optional[int] = 10


class UserProfile(BaseModel):
    name: str
    profile_link: str
    job_title: Optional[str] = None
    location: Optional[str] = None
    profile_image_url: Optional[str] = None
    platform: str = "linkedin"


class SearchUserResponse(BaseModel):
    profiles: List[UserProfile]
    total_found: int
    query: str
    success: bool
    error_message: Optional[str] = None