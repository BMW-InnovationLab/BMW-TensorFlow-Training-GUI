from typing import Dict

from application.configuration.models.network_configuration_enum import NetworkConfigurationEnum
from application.configuration.templates.centernet_hourglass104_1024x1024 import CenternetHourglass104S2
from application.configuration.templates.centernet_hourglass104_512x512 import CenternetHourglass104S1
from application.configuration.templates.centernet_resenet50_v2_512x512 import CenternetResnet50V2
from application.configuration.templates.centernet_resnet101_v1_fpn_512x512 import CenternetResnet101V1Fpn
from application.configuration.templates.faster_rcnn_inception_resnet_v2_1024x1024 import FrcnnResnetInceptionV2S2
from application.configuration.templates.faster_rcnn_inception_resnet_v2_640x640 import FrcnnResnetInceptionV2S1
from application.configuration.templates.faster_rcnn_resnet101_v1_1024x1024 import FrcnnResnet101V1S2
from application.configuration.templates.faster_rcnn_resnet101_v1_640x640 import FrcnnResnet101V1S1
from application.configuration.templates.faster_rcnn_resnet101_v1_800x1333 import FrcnnResnet101V1S3
from application.configuration.templates.faster_rcnn_resnet152_v1_1024x1024 import FrcnnResnet152V1S2
from application.configuration.templates.faster_rcnn_resnet152_v1_640x640 import FrcnnResnet152V1S1
from application.configuration.templates.faster_rcnn_resnet152_v1_800x1333 import FrcnnResnet152V1S3
from application.configuration.templates.faster_rcnn_resnet50_v1_1024x1024 import FrcnnResnet50V1S2
from application.configuration.templates.faster_rcnn_resnet50_v1_640x640 import FrcnnResnet50V1S1
from application.configuration.templates.faster_rcnn_resnet50_v1_800x1333 import FrcnnResnet50V1S3
from application.configuration.templates.ssd_efficientdet_d0_512x512 import EfficientdetD0
from application.configuration.templates.ssd_efficientdet_d1_640x640 import EfficientdetD1
from application.configuration.templates.ssd_efficientdet_d4_1024x1024 import EfficientdetD4
from application.configuration.templates.ssd_mobilenet_v1_fpn_640x640 import SsdMobilenetV1Fpn
from application.configuration.templates.ssd_mobilenet_v2_fpnlite_320x320 import SsdMobilenetV2FpnliteS1
from application.configuration.templates.ssd_mobilenet_v2_fpnlite_640x640 import SsdMobilenetV2FpnliteS2
from application.configuration.templates.ssd_resnet_101_v1_fpn_1024x1024 import SsdResnet101V1FpnS2
from application.configuration.templates.ssd_resnet_101_v1_fpn_640x640 import SsdResnet101V1FpnS1
from application.configuration.templates.ssd_resnet_152_v1_fpn_1024x1024 import SsdResnet152V1FpnS2
from application.configuration.templates.ssd_resnet_152_v1_fpn_640x640 import SsdResnet152V1FpnS1
from application.configuration.templates.ssd_resnet_50_v1_fpn_1024x1024 import SsdResnet50V1FpnS2
from application.configuration.templates.ssd_resnet_50_v1_fpn_640x640 import SsdResnet50V1FpnS1
from domain.exceptions.configuration_exception import NetworkArchitectureNotFound
from domain.models.network_information import NetworkInformation
from domain.services.contract.abstract_configuration_manager import AbstractConfigurationManager
from domain.services.contract.abstract_configure_network_service import AbstractConfigureNetworkService


class ConfigurationFactory(AbstractConfigurationManager):
    """
     A class used to create a configuration template object

    ...

     Attributes
    ----------
    network_instances : Dict[str, AbstractConfigureNetworkService]
        dict containing created instance of class AbstractConfigureNetworkService
    network_mappings :Dict[str, AbstractConfigureNetworkService]
        dict used to map between configuration network name and configuration class template

    Methods
    -------
    create_config_file(network_info: NetworkInformation) -> AbstractConfigureNetworkService
        take a network name from the user and search if it has instance.
        if yes it return back the instance of type AbstractConfigureNetworkService
        if no it register the network/template config  and create instance and return it

    _initialize_mappings_() -> None:
        method that uses the preconfigured Enum containing the mapping between class name and network name
        and initialize the Var:network_mappings
    """

    def __init__(self):
        self.network_instances: Dict[str, AbstractConfigureNetworkService] = {}
        self.network_mappings: Dict[str, AbstractConfigureNetworkService] = {}
        self._initialize_mappings_()

    def _initialize_mappings_(self) -> None:
        self.network_mappings = {
            NetworkConfigurationEnum.CENTERNET_HOURGLASS104_512x512.value: CenternetHourglass104S1,
            NetworkConfigurationEnum.CENTERNET_HOURGLASS104_1024x1024.value: CenternetHourglass104S2,
            NetworkConfigurationEnum.CENTERNET_RESNET50_V2_512x512.value: CenternetResnet50V2,
            NetworkConfigurationEnum.CENTERNET_RESNET101_V1_FPN_512x512.value: CenternetResnet101V1Fpn,
            NetworkConfigurationEnum.FRCNN_INCEPTION_RESNET_V2_640x640.value: FrcnnResnetInceptionV2S1,
            NetworkConfigurationEnum.FRCNN_INCEPTION_RESNET_V2_1024x1024.value: FrcnnResnetInceptionV2S2,
            NetworkConfigurationEnum.FRCNN_RESNET50_V1_640x640.value: FrcnnResnet50V1S1,
            NetworkConfigurationEnum.FRCNN_RESNET50_V1_1024x1024.value: FrcnnResnet50V1S2,
            NetworkConfigurationEnum.FRCNN_RESNET50_V1_800x1333.value: FrcnnResnet50V1S3,
            NetworkConfigurationEnum.FRCNN_RESNET101_V1_640x640.value: FrcnnResnet101V1S1,
            NetworkConfigurationEnum.FRCNN_RESNET101_V1_1024x1024.value: FrcnnResnet101V1S2,
            NetworkConfigurationEnum.FRCNN_RESNET101_V1_800x1333.value: FrcnnResnet101V1S3,
            NetworkConfigurationEnum.FRCNN_RESNET152_V1_640x640.value: FrcnnResnet152V1S1,
            NetworkConfigurationEnum.FRCNN_RESNET152_V1_1024x1024.value: FrcnnResnet152V1S2,
            NetworkConfigurationEnum.FRCNN_RESNET152_V1_800x1333.value: FrcnnResnet152V1S3,
            NetworkConfigurationEnum.SSD_EFFICIENTDET_D0_512x512.value: EfficientdetD0,
            NetworkConfigurationEnum.SSD_EFFICIENTDET_D1_640x640.value: EfficientdetD1,
            NetworkConfigurationEnum.SSD_EFFICIENTDET_D4_1024x1024.value: EfficientdetD4,
            NetworkConfigurationEnum.SSD_MOBILENET_V1_FPN_640x640.value: SsdMobilenetV1Fpn,
            NetworkConfigurationEnum.SSD_MOBILENET_V2_FPNLITE_320x320.value: SsdMobilenetV2FpnliteS1,
            NetworkConfigurationEnum.SSD_MOBILENET_V2_FPNLITE_640x640.value: SsdMobilenetV2FpnliteS2,
            NetworkConfigurationEnum.SSD_RESNET50_V1_FPN_640x640.value: SsdResnet50V1FpnS1,
            NetworkConfigurationEnum.SSD_RESNET50_V1_FPN_1024X1024.value: SsdResnet50V1FpnS2,
            NetworkConfigurationEnum.SSD_RESNET101_V1_FPN_640x640.value: SsdResnet101V1FpnS1,
            NetworkConfigurationEnum.SSD_RESNET101_V1_FPN_1024X1024.value: SsdResnet101V1FpnS2,
            NetworkConfigurationEnum.SSD_RESNET152_V1_FPN_640x640.value: SsdResnet152V1FpnS1,
            NetworkConfigurationEnum.SSD_RESNET152_V1_FPN_1024X1024.value: SsdResnet152V1FpnS2
        }

    def create_config_file(self, network_info: NetworkInformation) -> AbstractConfigureNetworkService:
        try:
            network_name: str = network_info.network_architecture.lower()
            if network_name in self.network_instances:
                return self.network_mappings.get(network_name.lower())

            else:
                config: AbstractConfigureNetworkService = self.network_mappings.get(network_name)()
                self.network_instances[network_name] = config
                return config
        except Exception as e:
            raise NetworkArchitectureNotFound(additional_message=e.__str__(), network_architecture=network_name)
