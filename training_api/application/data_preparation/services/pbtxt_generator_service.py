import os

from typing import Dict

from application.paths.services.path_service import PathService
from domain.models.paths import Paths
from domain.services.contract.abstract_pbtxt_generator_service import AbstractPbtxtGenratorService
from shared.helpers.object_classes_from_json import get_labels_from_json_file


class PbtxtGeneratorService(AbstractPbtxtGenratorService):
    """
     A class used to generate pbtxt file

    ...

     Attributes
    ----------
    path : Paths
        DTO containing all necessary paths
    Methods
    -------
    generate_pbtxt(labels_info: LabelsInformation) -> None
        generate a pbtxt file containing the object classes of the dataset
    """

    def __init__(self, path: PathService):
        self.path: Paths = path.get_paths()

    def generate_pbtxt(self) -> None:
        labels: Dict[str, str] = get_labels_from_json_file(self.path.object_classes_path)
        f = open(os.path.join(self.path.training_dir, 'object-detection.pbtxt'), 'w+')
        for key, value in labels.items():
            f.write('item { \n')
            f.write('  name: "' + value + '"\n')
            f.write('  id: ' + key + '\n')
            f.write('  display_name: "' + value + '"\n')
            f.write("} \n")
        f.close()
