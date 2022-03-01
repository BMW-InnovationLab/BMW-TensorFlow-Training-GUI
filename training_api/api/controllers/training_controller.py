from fastapi import APIRouter, HTTPException, BackgroundTasks
from domain.models.hyper_parameter_information import HyperParameterInformation
from containers import Services, Manager
from domain.models.network_information import NetworkInformation
from domain.exceptions.application_error import ApplicationError
from domain.models.api_response import ApiResponse
import threading

model_trainer_service = Services.model_trainer_service()
tensorboard_service = Services.tensorboard_service()
export_manager = Manager.export_manager()
train_eval_continuously_manager = Manager.train_eval_continuously_manager()
router = APIRouter()

"""
Starts the training in the background and export the resulting model

Parameters
----------
hyper_params: HyperParameterInformation
                object of type HyperParameterInformation containing the hyper parameters for the training

Returns
-------
str
    Success Message
"""


@router.post('/')
async def start_training(hyper_params: HyperParameterInformation, background_tasks: BackgroundTasks):
    try:
        network_info: NetworkInformation = NetworkInformation(network_architecture=hyper_params.network_architecture,
                                                              model_name=hyper_params.name)
        background_tasks.add_task(model_trainer_service.train, hyper_params=hyper_params)
        background_tasks.add_task(export_manager.save_trained_model, network_info=network_info)
        # model_trainer_service.train(hyper_params=hyper_params)

        # export_manager.save_trained_model(network_info=network_info)
        return ApiResponse(success=True)
    except ApplicationError as e:
        print(e.__str__())
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Starts the training and evaluation in the background and export the resulting model

Parameters
----------
hyper_params: HyperParameterInformation
                object of type HyperParameterInformation containing the hyper parameters for the training

Returns
-------
str
    Success Message
"""


@router.post('/eval')
async def start_eval(hyper_params: HyperParameterInformation, background_tasks: BackgroundTasks):
    try:
        network_info: NetworkInformation = NetworkInformation(network_architecture=hyper_params.network_architecture,
                                                              model_name=hyper_params.name)

        background_tasks.add_task(train_eval_continuously_manager.train_eval_continuously, hyper_params=hyper_params)
        background_tasks.add_task(export_manager.save_trained_model, network_info=network_info)
        return ApiResponse(success=True)
    except ApplicationError as e:
        print(e.__str__())
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
