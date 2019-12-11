import os


"""
deletes labels without images to prevent errors

Parameters
----------

images_folder: str
      images path

labels_folder: str
      labels path

"""


def delete_images_with_no_labels(images_folder, labels_folder):

    images = [image.split(".")[0] for image in os.listdir(images_folder)]
    labels = [label.split(".")[0] for label in os.listdir(labels_folder)]

    labels_extension = os.listdir(labels_folder)[0].split(".")[1]

    intersection = set(labels).intersection(images)

    labels_with_no_images = set(labels) - intersection

    [os.remove(labels_folder+"/"+label+"."+labels_extension) for label in labels_with_no_images]
