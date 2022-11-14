from fastapi import APIRouter, HTTPException
from typing import Dict
from domain.models.api_response import ApiResponse
from domain.models.configuration_content import ConfigurationContent
from domain.models.hyper_parameter_information import HyperParameterInformation
from containers import Services
from domain.models.network_information import NetworkInformation
from domain.exceptions.application_error import ApplicationError
from application.configuration.services.configuration_factory import ConfigurationFactory

configuration_service = Services.configuration_service()
configuration_content_service = Services.configuration_content_service()
configuration_writer_service = Services.configuration_writer_service()
router = APIRouter()

"""
Get the default configuration  content with number of classes generated 
Parameters
----------
network_info: NetworkInformation
                object of type NetworkInformation containing the network architecture name 

Returns
-------
Dict
    Configuration content
"""


@router.post('/default')
async def get_configuration_content(network_info: NetworkInformation):
    try:
        return configuration_service.get_default_configuration(network_info=network_info)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get the configuration file content 
Parameters
----------
network_info: NetworkInformation
                object of type NetworkInformation containing the network architecture name 

Returns
-------
str
    pipeline.config file content
"""


@router.post('/content')
async def get_configuration_content(network_info: NetworkInformation):
    try:
        return configuration_content_service.get_configuration_content(network_info=network_info)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Create  configuration file  
Parameters
----------
hyper_config_params: HyperParameterInformation
                object of type HyperParameterInformation containing hyper parameter 

Returns
-------
ApiResponse
        Success Message
"""


@router.post('/')
async def create_configuration(hyper_config_params: HyperParameterInformation):
    try:
        # Round training_steps up to nearest 100
        hyper_config_params.training_steps = int(round(hyper_config_params.training_steps / 100) * 100) if hyper_config_params.training_steps > 100 else 100
        network_info: NetworkInformation = NetworkInformation(model_name=hyper_config_params.name,
                                                              network_architecture=hyper_config_params.network_architecture)
        configuration_file_content = configuration_service.get_config_file_content(network_info=network_info)

        configuration_obj = ConfigurationFactory().create_config_file(network_info=network_info)

        configuration_pipeline: Dict[str, str] = configuration_obj.config_network(
            config_file_content=configuration_file_content, config_params=hyper_config_params)
        configuration_writer_service.write_configuration(configuration_pipeline=configuration_pipeline)
        return ApiResponse(success=True)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Gets a configuration string from the user and and save it to pipeline.config 

Parameters
----------
configuration_content: ConfigurationContent
                object of type ConfigurationContent containing the content of the configuration

Returns
-------
ApiResponse
    Success Message
"""


@router.post('/advanced')
async def create_advance_configuration(configuration_content: ConfigurationContent):
    try:
        configuration_writer_service.write_advanced_configuration(configuration_content=configuration_content)
        return ApiResponse(success=True)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
