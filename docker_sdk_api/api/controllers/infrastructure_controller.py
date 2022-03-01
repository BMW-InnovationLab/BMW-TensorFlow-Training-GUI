from fastapi import APIRouter, HTTPException

from application.infrastructure.services.gpu_service import GpuService
from application.infrastructure.services.port_scanner_service import PortScannerService
from containers import Services
from domain.exceptions.application_error import ApplicationError
from domain.models.container_info import ContainerInfo

tensorboard_port_service = Services.tensorboard_port_scanner_service()
router = APIRouter()

"""
Gets the available gpus.

Returns
-------
list of str
    a list of gpu names wuth less than 25% memory consumption

"""


@router.get("/gpu/info")
async def get_gpu_info():
    try:
        return GpuService().get_gpu_info()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Get all the used ports on the system

Returns
-------
list of str
    used ports
"""


@router.get("/used/ports")
async def get_used_ports():
    try:
        return PortScannerService().get_used_ports()
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Gets the tensorboard port for a specific job

Parameters
----------
containerInfo: ContainerInfo
               object of type ContainerInfo containing the container name 

Returns
-------
str
    the port on which tensorboard for that specific container is running

"""


@router.post("/tensorboard/port")
async def get_tensorboard_ports(container_info: ContainerInfo):
    try:
        return tensorboard_port_service.get_tensorboard_port(container_info=container_info)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())


"""
Gets the tensorboard port for a specific archived job

Parameters
----------
containerInfo: ContainerInfo
               object of type ContainerInfo containing the container name 

Returns
-------
int
    the port on which tensorboard for that specific container is running

"""


@router.post("/archived/tensorboard/port")
async def get_tensorboard_ports(container_info: ContainerInfo):
    try:
        return tensorboard_port_service.get_archived_tensorboard_port(container_info=container_info)
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=e.__str__())
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.__str__())
