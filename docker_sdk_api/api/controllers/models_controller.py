from fastapi import APIRouter, HTTPException

from containers import Services
from domain.exceptions.application_error import ApplicationError
from domain.models.api_response import ApiResponse
from domain.models.network_info import NetworkInfo

router = APIRouter()

models_architecture_service = Services.models_architecture_service()
checkpoint_service = Services.checkpoint_service()
download_models_service = Services.download_models_service()
"""
Get all models architectures

Returns
-------
list of str
    models architectures
"""


@router.get("/architecture")
async def get_all_architecture():
    try:
        return models_architecture_service.get_architecture()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get all the pre-trained weights (or checkpoints) for a specific models architecture

Parameters
----------
networkInfo: NetworkInfo
                   object of type NetworkInfo containing the name of the models architecture

Returns
-------
list of str
    checkpoints
"""




@router.post("/checkpoints")
async def get_checkpoints(network_info: NetworkInfo):
    try:
        return checkpoint_service.get_checkpoint(network_info=network_info)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get all models in the static folder called servable

Returns
-------
list of str
    servable models
"""


@router.get("/downloadable")
async def get_downloadable_models():
    try:
        return download_models_service.get_downloadable_models()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
