import os
import sys
#import random
#import math
import numpy as np
import skimage.io
import yaml
import tensorflow as tf
#import matplotlib
#import matplotlib.pyplot as plt
from mrcnn.config import Config
# Import Mask RCNN
import numpy as np
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
#sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
#sys.path.append(os.path.join(ROOR_ROOT_DIR, "cocoapi/PythonAPI"))

from skimage.measure import find_contours
from matplotlib import patches,  lines
from matplotlib.patches import Polygon

#%matplotlib inline 

def flip_bool_lol(ls):
    return ~np.array(ls)

class CocoConfig(Config):
    """Configuration for training on MS COCO.
    Derives from the base Config class and overrides values specific
    to the COCO dataset.
    """
    # Give the configuration a recognizable name
    NAME = "coco"
    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2
    # Uncomment to train on 8 GPUs (default is 1)
    # GPU_COUNT = 8
    # Number of classes (including background)
    NUM_CLASSES = 1 + 80  # COCO has 80 classes
    
class InferenceConfig(CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

class Segmentation():
    def __init__(self, class_names_path = './source/class_names.yaml'):
        # Root directory of the project
        ROOT_DIR = os.path.abspath("./")
        sys.path.append(ROOT_DIR)  # To find local version of the library

        # Directory to save logs and trained model
        MODEL_DIR = os.path.join(ROOT_DIR, "logs")

        # Local path to trained weights file
        coco_model_path = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
        # Download COCO trained weights from Releases if needed
        if not os.path.exists(coco_model_path):
            utils.download_trained_weights(coco_model_path)

        # Directory of images to run detection on
        #images_path = os.path.join(ROOT_DIR, "images")

        config = InferenceConfig()
        config.display()
        # Create model object in inference mode.
        model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
        # Load weights trained on MS-COCO
        global graph
        graph = tf.get_default_graph()
        with graph.as_default():
            model.load_weights(coco_model_path, by_name=True)
            #model._make_predict_function()
            self.model = model

        # COCO Class names
        # Index of the class in the list is its ID. For example, to get ID of
        # the teddy bear class, use: class_names.index('teddy bear')
        self.class_names = yaml.full_load(open(class_names_path))
    
    def run_list_segmentation(self, image_set, output_path = './'):
        for img in image_set:
            output_files = self.run_segmentation(img['image_path'], img['image_file_name'], output_path = output_path)
            img['output_files'] = output_files
        return image_set

    def run_segmentation(self, image_path, file_name, output_path = './'):
        output_files = []
        file_path = os.path.join(image_path,file_name)
        #'../../../auto_vlogger/auto_vlog/static/spacex_musk/raw_images/106806377-1607090600215-gettyimages-1229893101-AFP_8WA6E2.jpeg'
        image = skimage.io.imread(file_path)
        results = self.model.detect([image], verbose=1)[0]

        masked_image = self.all_segments(image, results['rois'], results['masks'], results['class_ids'], self.class_names, results['scores'])
        img_path = os.path.join(output_path,f'{file_name}_all.jpg')
        self.save_image(img_path,masked_image)
        output_files.append(img_path)
        for mask_idx in range(len(results['scores'])):
            masked_image = self.image_segment(mask_idx, image, results, min_perc_image = 0.05, color = None)
            img_path = os.path.join(output_path,f'{file_name}_{mask_idx}.jpg')
            if len(masked_image)>0:
                print('Saved',img_path)
                self.save_image(img_path,masked_image)
                output_files.append(img_path)
            else:
                print('Too small',img_path)
        return output_files

    def image_segment(self, mask_id, image, results, min_perc_image = 0.05, color = None):
        masked_image = image.astype(np.uint32).copy()
        mask = results['masks'][:, :, mask_id]

        mask_array = np.array(mask)
        perc_image = np.sum(mask_array) / mask_array.size
        if perc_image > min_perc_image:
            color = color if color else visualize.random_colors(2)[0]

            masked_image = visualize.apply_mask(masked_image, flip_bool_lol(mask), color, alpha=1)
            return masked_image.astype(np.uint8)
        else:
            return []

    def save_image(self,image_path,image):
        skimage.io.imsave(image_path,image)

    def all_segments(self,image, boxes, masks, class_ids, class_names,
                        scores=None, title="",
                        figsize=(16, 16), ax=None,
                        show_mask=True, show_bbox=True,
                        colors=None, captions=None):
        """
        'INSPIRED' by visualize.display_instances
        boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
        masks: [height, width, num_instances]
        class_ids: [num_instances]
        class_names: list of class names of the dataset
        scores: (optional) confidence scores for each box
        title: (optional) Figure title
        show_mask, show_bbox: To show masks and bounding boxes or not
        figsize: (optional) the size of the image
        colors: (optional) An array or colors to use with each object
        captions: (optional) A list of strings to use as captions for each object
        """
        # Number of instances
        N = boxes.shape[0]
        if not N:
            print("\n*** No instances to display *** \n")
        else:
            assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

        # Generate random colors
        colors = colors or visualize.random_colors(N)

        masked_image = image.astype(np.uint32).copy()
        for i in range(N):
            color = colors[i]

            # Bounding box
            if not np.any(boxes[i]):
                # Skip this instance. Has no bbox. Likely lost in image cropping.
                continue
            y1, x1, y2, x2 = boxes[i]
            if show_bbox:
                p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2,
                                    alpha=0.7, linestyle="dashed",
                                    edgecolor=color, facecolor='none')
                #ax.add_patch(p)

            # Label
            if not captions:
                class_id = class_ids[i]
                score = scores[i] if scores is not None else None
                label = class_names[class_id]
                caption = "{} {:.3f}".format(label, score) if score else label
            else:
                caption = captions[i]
            #ax.text(x1, y1 + 8, caption,
            #        color='w', size=11, backgroundcolor="none")

            # Mask
            mask = masks[:, :, i]
            if show_mask:
                masked_image = visualize.apply_mask(masked_image, mask, color)

            # Mask Polygon
            # Pad to ensure proper polygons for masks that touch image edges.
            padded_mask = np.zeros(
                (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
            padded_mask[1:-1, 1:-1] = mask
            contours = find_contours(padded_mask, 0.5)
            for verts in contours:
                # Subtract the padding and flip (y, x) to (x, y)
                verts = np.fliplr(verts) - 1
                p = Polygon(verts, facecolor="none", edgecolor=color)
                #ax.add_patch(p)
        return masked_image.astype(np.uint8)
            



