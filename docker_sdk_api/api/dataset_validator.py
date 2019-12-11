import os


"""
Logic to check if a dataset is valid

Parameters
----------
dataset_folder: str
               folder of the dataset

labels_type: str
             labels_type

Returns
-------
Boolean
        true if the dataset is valid, false otherwise

"""
def validate_dataset(dataset_folder, labels_type):
    valid = True
    
    valid = True if os.path.isdir(dataset_folder+'/images') else False 
    
    if valid == True:
        valid = True if os.path.isdir(dataset_folder+'/labels')  else False
    
    if valid == True:
        valid = True if os.path.isdir(dataset_folder+'/labels/'+labels_type) else False
    
    if valid ==True: 
        valid = True if os.path.isfile(dataset_folder+'/objectclasses.json') else False

    if valid == True:
        images = os.listdir(dataset_folder+'/images')
        for image in images:
            if not (image.endswith('.png') or image.endswith('.jpg') or image.endswith('.jpeg')):
                valid = False
                break
            
    
    if valid == True:
        labels = os.listdir(dataset_folder+'/labels/'+labels_type)
        extension = None
        
        if labels_type == 'json':
            extension = '.json'
        
        elif labels_type == 'pascal':
            extension = '.xml'

        for label in labels:

            if not (label.endswith(extension)):
                valid = False
                break      
    
    return valid


"""
Logic to check labels types for a dataset

Parameters
----------
dataset_folder: str
               folder of the dataset


Returns
-------
list of str
        supported label types

"""
def dataset_label_types(dataset_folder):
    supported_types = {"json", "pascal"}
    found_types = []
    label_types = os.listdir(dataset_folder+'/labels')
    print(label_types)
    for label_type in label_types:
        if label_type == "json" or label_type == "pascal":
            found_types.append(label_type)
    
    intersected_types = list(supported_types.intersection(set(found_types)))
    return intersected_types