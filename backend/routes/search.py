from fastapi import APIRouter, Body, HTTPException

from constants.search_models import SearchUserPayload, SearchUserResponse
from services.linkedin_service import service as linkedin_service
from services.logger_service import logger_service

search_router = APIRouter()

@search_router.post("/v1/search_user")
async def search_user(payload: SearchUserPayload = Body(...)):
    try:
        logger_service.info(f"Received search request for: {payload.profile_url}")

        response_payload = linkedin_service.get_profile_details(payload.profile_url)

        return response_payload

    except RuntimeError as e:
        logger_service.error(f"Runtime error during search: {e}")
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        logger_service.error(f"Unexpected error during search: {e}")
        return {"error": str(e), "success": False}
