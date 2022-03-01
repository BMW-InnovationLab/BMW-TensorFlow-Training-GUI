from fastapi import APIRouter, HTTPException
from containers import Manager
from domain.models.labels_information import LabelsInformation
from domain.models.api_response import ApiResponse
from domain.exceptions.application_error import ApplicationError

router = APIRouter()

tfrecord_manager = Manager.tfrecord_manager()

"""
Create Tf Records 
Parameters
----------
labels_info: LabelsInformation
                object of type LabelsInformation containing the labels_type and the train test split ratio
            
Returns
-------
str
    Success Message
"""


@router.post('/')
async def create_tfrecord(labels_info: LabelsInformation):
    try:
        tfrecord_manager.prepare_dataset(labels_info=labels_info)
        return ApiResponse(success=True)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
