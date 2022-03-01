from enum import Enum


# noinspection SpellCheckingInspection
class NetworkConfigurationEnum(Enum):
    """
        A class containing the mapping between config name and template class name
    """
    CENTERNET_HOURGLASS104_512x512 = "centernet_hourglass104_512x512"
    CENTERNET_HOURGLASS104_1024x1024 = "centernet_hourglass104_1024x1024"
    CENTERNET_RESNET50_V2_512x512 = "centernet_resnet50_v2_512x512"
    CENTERNET_RESNET101_V1_FPN_512x512 = "centernet_resnet101_v1_fpn_512x512"
    FRCNN_INCEPTION_RESNET_V2_640x640 = "faster_rcnn_inception_resnet_v2_640x640"
    FRCNN_INCEPTION_RESNET_V2_1024x1024 = "faster_rcnn_inception_resnet_v2_1024x1024"
    FRCNN_RESNET50_V1_640x640 = "faster_rcnn_resnet50_v1_640x640"
    FRCNN_RESNET50_V1_1024x1024 = "faster_rcnn_resnet50_v1_1024x1024"
    FRCNN_RESNET50_V1_800x1333 = "faster_rcnn_resnet50_v1_800x1333"
    FRCNN_RESNET101_V1_640x640 = "faster_rcnn_resnet101_v1_640x640"
    FRCNN_RESNET101_V1_1024x1024 = "faster_rcnn_resnet101_v1_1024x1024"
    FRCNN_RESNET101_V1_800x1333 = "faster_rcnn_resnet101_v1_800x1333"
    FRCNN_RESNET152_V1_640x640 = "faster_rcnn_resnet152_v1_640x640"
    FRCNN_RESNET152_V1_1024x1024 = "faster_rcnn_resnet152_v1_1024x1024"
    FRCNN_RESNET152_V1_800x1333 = "faster_rcnn_resnet152_v1_800x1333"
    SSD_EFFICIENTDET_D0_512x512 = "ssd_efficientdet_d0_512x512"
    SSD_EFFICIENTDET_D1_640x640 = "ssd_efficientdet_d1_640x640"
    SSD_EFFICIENTDET_D4_1024x1024 = "ssd_efficientdet_d4_1024x1024"
    SSD_MOBILENET_V1_FPN_640x640 = "ssd_mobilenet_v1_fpn_640x640"
    SSD_MOBILENET_V2_FPNLITE_320x320 = "ssd_mobilenet_v2_fpnlite_320x320"
    SSD_MOBILENET_V2_FPNLITE_640x640 = "ssd_mobilenet_v2_fpnlite_640x640"
    SSD_RESNET50_V1_FPN_640x640 = "ssd_resnet_50_v1_fpn_640x640"
    SSD_RESNET50_V1_FPN_1024X1024 = "ssd_resnet_50_v1_fpn_1024x1024"
    SSD_RESNET101_V1_FPN_640x640 = "ssd_resnet_101_v1_fpn_640x640"
    SSD_RESNET101_V1_FPN_1024X1024 = "ssd_resnet_101_v1_fpn_1024x1024"
    SSD_RESNET152_V1_FPN_640x640 = "ssd_resnet_152_v1_fpn_640x640"
    SSD_RESNET152_V1_FPN_1024X1024 = "ssd_resnet_152_v1_fpn_1024x1024"

    @classmethod
    def is_name_valid(cls, requested_network_name: str) -> bool:
        requested_network_name: bool = any(requested_network_name.lower().strip() == network.value for network in cls)
        return requested_network_name
