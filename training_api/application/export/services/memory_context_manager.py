from numba import cuda
from typing import List
from domain.services.contract.abstract_memory_context_manager import AbstractMemoryContextManager
import tensorflow.compat.v2 as tf


class MemoryContextManager(AbstractMemoryContextManager):

    """
     A class used to clear GPU memory after training and model exporting is completed
    ...


    Methods
    -------
    clear_context() -> None
        search for available GPUs context and reset them using numba cuda, when using CPU training this function has no functionality

    """


    def clear_context(self)->None:
        try:
            print("Clearing Context")
            devices_list : List[cuda.cudadrv.devices._DeviceContextManager] = cuda.list_devices().lst
            for device in devices_list:
                print("GPU device id:{}".format(device.id))
                cuda.select_device(device.id)
                cuda.close()
                device.reset()
        except cuda.cudadrv.error.CudaSupportError as e :
            pass
        finally:
            print("Context Cleared")

