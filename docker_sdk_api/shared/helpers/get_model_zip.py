from typing import List,Dict
import  os 
def get_downloadable_zip(folder_path : str)-> Dict[str,str]:

        servable_models: Dict[str, str] = {}
        for root, dirs, files in os.walk(folder_path):
            for directory in dirs:
                for f in os.listdir(os.path.join(root, directory)):
                    if f.endswith(".zip"):
                        servable_models[f] = directory

        return servable_models




