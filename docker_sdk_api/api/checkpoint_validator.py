import os


"""
Logic to check if a pre trained weights folder is valid

Parameters
----------
chackpoint_folder_path: str
               path of the folder

Returns
-------
Boolean
        true if the folder is valid, false otherwise

"""
def validate_checkpionts_folder(checkpoint_folder_path):
    valid = False
    
    data_file = None
    index_file = None
    meta_file = None

    for ckpt_file in os.listdir(checkpoint_folder_path):

        if ckpt_file.startswith("model.ckpt-") and ckpt_file.endswith(".data-00000-of-00001"):
            data_file = ckpt_file
        

        elif ckpt_file.startswith("model.ckpt-") and ckpt_file.endswith(".index"):
            index_file = ckpt_file


        elif ckpt_file.startswith("model.ckpt-") and ckpt_file.endswith(".meta"):
            meta_file = ckpt_file
    

    if meta_file is not None and index_file is not None and data_file is not None:
        valid = True

    
    return valid


