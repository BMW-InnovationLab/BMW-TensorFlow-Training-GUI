from fastapi import APIRouter, HTTPException
from containers import Services
from domain.models.api_response import ApiResponse
from domain.models.dataset_name import DatasetName
from domain.models.dataset_info import DatasetInfo
from domain.exceptions.application_error import ApplicationError

dataset_service = Services.dataset_service()
dataset_validator_service = Services.dataset_validator_service()
dataset_label_type_service = Services.dataset_label_type_service()

router = APIRouter()
"""
Get all datasets

Returns
-------
list of str
    datasets
"""


@router.get("/")
async def get_datasets():
    try:
        return dataset_service.get_datasets()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Checks if a dataset is valid

Parameters
----------
datasetInfo: DatasetInfo
             object of type DatasetInfo containing the dataset path and the labels type 

Returns
-------
Boolean
        true if the dataset is valid, false otherwise

"""


@router.post("/validate")
async def validate_dataset(dataset_info: DatasetInfo):
    try:
        dataset_validator_service.validate_dataset(dataset_info)
        return ApiResponse(success=True)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get the exisiting labels type for a specific dataset


Parameters
----------
datasetInfo: DatasetName
             object of type DatasetNamr containing the dataset name

Returns
-------
list of str
        labels types for the dataset
"""


@router.post("/labels/type")
async def get_labels_type(dataset_name: DatasetName):
    try:
        return dataset_label_type_service.get_labels_type(dataset_name)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
