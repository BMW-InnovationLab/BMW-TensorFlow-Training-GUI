from domain.services.contract.abstract_gpu_service import AbstractGpuService
import GPUtil
from GPUtil import GPU
from typing import List,Dict
from domain.exceptions.infrastructure_exception import GpuInfoInvalid


class GpuService(AbstractGpuService):

    def get_gpu_info(self) -> Dict[str, str]:
        try:
            gpus : List[GPU] = GPUtil.getGPUs()
            available_gpus :List = GPUtil.getAvailable(order='memory', limit=10, maxLoad=0.4, maxMemory=0.4, includeNan=False,excludeID=[],excludeUUID=[]) 
            available_gpus: List = list(filter(lambda gpu : gpu.id in available_gpus , gpus))
            
            # return -1 if no nvidia-smi visible else return available gpus 
            # {"id":"gpu name"}
            if len(gpus)==0:
                return {"-1":"CPU"}
            else:
                gpus_dict : Dict [str, str] = {}

                for gpu in available_gpus:
                    gpus_dict[str(gpu.id)] = "GPU "+str(gpu.id)+" - "+str(gpu.name) + "- Available Memory: "+str(int(gpu.memoryFree)) + "MB/" + str(int(gpu.memoryTotal))+ "MB"

                return gpus_dict
        except Exception as e:
            raise GpuInfoInvalid(e._str_())
