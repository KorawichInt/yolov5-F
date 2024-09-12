import os
from PIL import Image
from torchvision.transforms import v2
from torchvision import tv_tensors
import torch

# Define the paths
# Train
# input_images_path = 'dataset/train_Y1/images'
# input_labels_path = 'dataset/train_Y1/labels'
# output_images_path = 'dataset/train_Y2/images'
# output_labels_path = 'dataset/train_Y2/labels'

# Test
input_images_path = 'dataset/test/images'
input_labels_path = 'dataset/test/labels'
output_images_path = 'dataset/test_Y2/images'
output_labels_path = 'dataset/test_Y2/labels'

# Create the output folder if it does not exist
os.makedirs(output_images_path, exist_ok=True)
os.makedirs(output_labels_path, exist_ok=True)

def xyxy2xywh(bbox_xyxy, img_width, img_height):
    x_min, y_min, x_max, y_max = bbox_xyxy
    cx = (x_min + x_max) / 2 / img_width
    cy = (y_min + y_max) / 2 / img_height
    w = (x_max - x_min) / img_width
    h = (y_max - y_min) / img_height
    return [cx, cy, w, h]

def xywh2xyxy(yolo_label, img_size):
    CX, CY, W, H = yolo_label
    x_min = CX - (W / 2)
    y_min = CY - (H / 2)
    x_max = CX + (W / 2)
    y_max = CY + (H / 2)

    bbox_xyxy = [x_min * img_size, y_min * img_size, x_max * img_size, y_max * img_size]
    return bbox_xyxy

# Loop through each file in the input folder
for filename in os.listdir(input_images_path):
    if filename.endswith('.jpg'):
        # Open the image file
        image_path = os.path.join(input_images_path, filename)
        image = Image.open(image_path)
        img_width, img_height = image.size
        boxes_data = []
        class_ids = []

        with open(input_labels_path+'/'+filename.replace('.jpg', '.txt'), 'r') as f:
            for line in f:
                components = line.split()  # Don't skip the first element, which is the class ID
                class_id = components[0]
                box_data = [float(x) for x in components[1:]]
                box_xyxy = xywh2xyxy(box_data, img_width)  # Convert to XYXY format
                boxes_data.append(box_xyxy)
                class_ids.append(class_id)  # Keep track of the class IDs

        # Create BoundingBoxes object
        boxes = tv_tensors.BoundingBoxes(
            torch.tensor(boxes_data),
            format='XYXY',
            canvas_size=(img_height, img_width)
        )

        ### Augmentation
        croped_img, croped_boxes = v2.RandomCrop(size=(224, 224))(image, boxes)
        blured_img, blured_boxes = v2.GaussianBlur(kernel_size=9, sigma=(0.8, 1.2))(image, boxes)
        brightnessed_img, brightnessed_boxes = v2.ColorJitter(brightness=(1.1,1.5))(image, boxes)
        darknessed_img, darknessed_boxes = v2.ColorJitter(brightness=(0.6,0.9))(image, boxes)

        augmentations = {
            'croped': (croped_img, croped_boxes, 224, 224),
            'blured': (blured_img, blured_boxes, img_width, img_height),
            'brightnessed': (brightnessed_img, brightnessed_boxes, img_width, img_height),
            'darknessed': (darknessed_img, darknessed_boxes, img_width, img_height),
        }

        for prefix, (aug_img, aug_boxes, aug_width, aug_height) in augmentations.items():
            # Save the augmented bounding boxes
            output_label_file = os.path.join(output_labels_path, f'{filename.replace(".jpg", "")}_{prefix}.txt')
            with open(output_label_file, 'w') as f:
                for class_id, box in zip(class_ids, aug_boxes.tolist()):
                    # Convert XYXY to center_x, center_y, width, height in range 0-1
                    box_xywh = xyxy2xywh(box, aug_width, aug_height)
                    formatted_box = ' '.join([f'{x:.6f}' for x in box_xywh])
                    f.write(f'{class_id} {formatted_box}\n')

        # Save the augmented images (if needed)
        # croped_img.save(os.path.join(output_images_path, f'cropped_{filename}'))
        # blured_img.save(os.path.join(output_images_path, f'blurred_{filename}'))
        # brightnessed_img.save(os.path.join(output_images_path, f'brightnessed_{filename}'))
        # darknessed_img.save(os.path.join(output_images_path, f'darknessed_{filename}'))
