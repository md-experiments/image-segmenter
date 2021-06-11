import os
from mrcnn import utils

ROOT_DIR = os.path.abspath("./")

# Local path to trained weights file
coco_model_path = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(coco_model_path):
    utils.download_trained_weights(coco_model_path)