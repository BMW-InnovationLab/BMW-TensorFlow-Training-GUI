from fastapi import APIRouter, HTTPException
from containers import Services
from domain.exceptions.application_error import ApplicationError
from domain.models.api_response import ApiResponse

router = APIRouter()

tensorboard_service = Services.tensorboard_service()

"""
Refresh the tensorboard 


Returns
-------
ApiResponse
        Success Message
"""


@router.get('/refresh')
async def refresh_tensorboard():
    try:
        tensorboard_service.tensorboard_stop()
        tensorboard_service.tensorboard_start()
        return ApiResponse(success=True)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
