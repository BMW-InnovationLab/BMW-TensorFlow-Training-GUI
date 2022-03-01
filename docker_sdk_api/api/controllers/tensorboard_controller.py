from fastapi import APIRouter, HTTPException

from containers import Services
from domain.exceptions.application_error import ApplicationError
from domain.models.api_response import ApiResponse
from domain.models.container_info import ContainerInfo

router = APIRouter()

tensorboard_service = Services.tensorboard_service()
tensorboard_refresh_service = Services.tensorboard_refresh_service()

"""
Refresh the tensorboard of certain container

Parameters
----------
container_info: ContainerInfo
             object of type ContainerInfo containing the container's name

Returns
-------
ApiResponse
        Success Message
"""


@router.post('/refresh')
async def refresh_tensorboard(container_info: ContainerInfo):
    try:
        tensorboard_refresh_service.tensorboard_refresh(container_info)
        return ApiResponse(success=True)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Delete tensorboard files of certain container 

Parameters
----------
container_info: ContainerInfo
             object of type ContainerInfo containing the container's name

Returns
-------
ApiResponse
        Success Message
"""


@router.post('/delete')
async def delete_tensorboard(container_info: ContainerInfo):
    try:
        tensorboard_service.tensorboard_delete(container_info)
        return ApiResponse(success=True)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
