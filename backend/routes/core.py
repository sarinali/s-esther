from fastapi import APIRouter, Body, HTTPException

from constants.core_models import StartProspectingPayload
from services.linkedin_service import service as linkedin_service
from services.logger_service import logger_service

core_router = APIRouter()

@core_router.post("/v1/start_prospecting")
async def start_prospecting(payload: StartProspectingPayload = Body(...)):
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
