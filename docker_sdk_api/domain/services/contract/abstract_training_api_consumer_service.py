from abc import ABCMeta, ABC, abstractmethod

from domain.models.container_info import ContainerInfo


class AbstractTrainingApiConsumerService(ABC):
    metaclass = ABCMeta

    @abstractmethod
    def refresh_training_api_tensorboard(self, container_info: ContainerInfo) -> None:
        pass
