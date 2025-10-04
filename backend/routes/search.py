from fastapi import APIRouter, Body, HTTPException

from constants.search_models import SearchUserPayload, SearchUserResponse
from services.linkedin_scraper_service import service as linkedin_service
from services.logger_service import logger_service

search_router = APIRouter()

@search_router.post("/v1/search_user")
async def search_user(payload: SearchUserPayload = Body(...)) -> SearchUserResponse:
    try:
        logger_service.info(f"Received search request for: {payload.name}")

        profiles = await linkedin_service.get_user_profiles(payload.name)

        if payload.limit and len(profiles) > payload.limit:
            profiles = profiles[:payload.limit]

        response = SearchUserResponse(
            profiles=profiles,
            total_found=len(profiles),
            query=payload.name,
            success=True
        )

        logger_service.info(f"Search completed successfully. Found {len(profiles)} profiles")
        return response

    except RuntimeError as e:
        logger_service.error(f"Runtime error during search: {e}")
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        logger_service.error(f"Unexpected error during search: {e}")
        return SearchUserResponse(
            profiles=[],
            total_found=0,
            query=payload.name,
            success=False,
            error_message=str(e)
        )
