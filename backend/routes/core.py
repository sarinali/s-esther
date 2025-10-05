from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import StreamingResponse

from constants.core_models import StartProspectingPayload
from services.tool_calling_service import service as tool_calling_service
from services.logger_service import logger_service

core_router = APIRouter()

@core_router.post("/v1/start_prospecting")
async def start_prospecting(payload: StartProspectingPayload = Body(...)):
    try:
        logger_service.info(f"Starting agent execution for: {payload.profile_url}")

        return StreamingResponse(
            tool_calling_service.execute_with_streaming(
                user_goal=payload.intent,
                linkedin_profile_url=payload.profile_url,
                dry_run=payload.dry_run
            ),
            media_type="text/event-stream"
        )

    except RuntimeError as e:
        logger_service.error(f"Runtime error during agent execution: {e}")
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        logger_service.error(f"Unexpected error during agent execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))
