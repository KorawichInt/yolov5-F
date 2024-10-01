# import os
# from PIL import Image

# def create_directory_structure(base_dir):
#     os.makedirs(os.path.join(base_dir, "train", "images"), exist_ok=True)
#     os.makedirs(os.path.join(base_dir, "train", "labels"), exist_ok=True)
#     os.makedirs(os.path.join(base_dir, "val", "images"), exist_ok=True)
#     os.makedirs(os.path.join(base_dir, "val", "labels"), exist_ok=True)

# def resize_and_move_image(img_path, dest_dir):
#     try:
#         with Image.open(img_path) as img:
#             resized_img = img.resize((320, 320))  # Resize to 320x320
#             dest_path = os.path.join(dest_dir, os.path.basename(img_path))
#             resized_img.save(dest_path)  # Save resized image
#             print(f"Moved and resized image to {dest_path}")
#     except Exception as e:
#         print(f"Failed to process image {img_path}: {e}")

# def move_images(image_list_file, dest_image_dir):
#     with open(image_list_file, "r") as f:
#         image_paths = f.readlines()
    
#     for relative_img_path in image_paths:
#         # relative_img_path = relative_img_path.strip().replace("./images/", "")  # Get image path relative to ./images/
#         # img_path = os.path.join(relative_img_path)
#         img_path = relative_img_path
#         if os.path.exists(img_path):
#             resize_and_move_image(img_path, dest_image_dir)
#         else:
#             print(f"Image not found: {img_path}")

# def convert_bounding_boxes(train_bbox_file, dest_label_dir):
#     with open(train_bbox_file, "r") as f:
#         lines = f.readlines()

#     i = 0
#     while i < len(lines):
#         image_filename = lines[i].strip().split('/')[-1]
#         label_filename = image_filename.replace('.jpg', '.txt')
#         num_boxes = int(lines[i+1].strip())
#         boxes = []
        
#         for j in range(num_boxes):
#             box = list(map(int, lines[i+2+j].strip().split()[:4]))  # Extract x, y, width, height
#             x_min, y_min, box_width, box_height = box

#             # Convert box to YOLO format (normalized xywh)
#             x_center = (x_min + box_width / 2) / 640
#             y_center = (y_min + box_height / 2) / 640
#             norm_width = box_width / 640
#             norm_height = box_height / 640

#             boxes.append(f"0 {x_center} {y_center} {norm_width} {norm_height}")

#         with open(os.path.join(dest_label_dir, label_filename), "w") as f:
#             f.write("\n".join(boxes) + "\n")

#         i += 2 + num_boxes

# def process_dataset(base_dir, train_list_file, val_list_file, train_bbox_file, val_bbox_file):
#     create_directory_structure(base_dir)
    
#     # Move and resize train images
#     move_images(train_list_file, os.path.join(base_dir, "train", "images"))
#     # Move and resize validation images
#     move_images(val_list_file, os.path.join(base_dir, "val", "images"))
    
#     # Convert bounding boxes for train images
#     convert_bounding_boxes(train_bbox_file, os.path.join(base_dir, "train", "labels"))
#     # Convert bounding boxes for val images
#     convert_bounding_boxes(val_bbox_file, os.path.join(base_dir, "val", "labels"))

# # Example usage:
# process_dataset('dataset_wider_face',                       # base_dir
#                 'dataset/train/train_list.txt',             # train_list_file
#                 'dataset/val/val_list.txt',                 # val_list_file
#                 'dataset/train/train_bbx_gt_reduced.txt',   # train_bbox_file
#                 'dataset/val/val_bbx_gt_reduced.txt')       # val_bbox_file



import os
from PIL import Image

def create_directory_structure(base_dir):
    os.makedirs(os.path.join(base_dir, "train", "images"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "train", "labels"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "val", "images"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "val", "labels"), exist_ok=True)

def resize_and_move_image(img_path, dest_dir):
    try:
        with Image.open(img_path) as img:
            resized_img = img.resize((320, 320))  # Resize to 320x320
            dest_path = os.path.join(dest_dir, os.path.basename(img_path))  # Only move the image filename
            resized_img.save(dest_path)  # Save resized image
            print(f"Moved and resized image to {dest_path}")
    except Exception as e:
        print(f"Failed to process image {img_path}: {e}")

def move_images(image_list_file, dest_image_dir):
    with open(image_list_file, "r") as f:
        image_paths = f.readlines()
    
    for relative_img_path in image_paths:
        relative_img_path = relative_img_path.strip()  # Strip newlines
        if os.path.exists(relative_img_path):  # Check if the image exists at the relative path
            resize_and_move_image(relative_img_path, dest_image_dir)
        else:
            print(f"Image not found: {relative_img_path}")

def convert_bounding_boxes(train_bbox_file, dest_label_dir):
    with open(train_bbox_file, "r") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        image_filename = lines[i].strip().split('/')[-1]
        label_filename = image_filename.replace('.jpg', '.txt')
        num_boxes = int(lines[i+1].strip())
        boxes = []
        
        for j in range(num_boxes):
            box = list(map(int, lines[i+2+j].strip().split()[:4]))  # Extract x, y, width, height
            x_min, y_min, box_width, box_height = box

            # Convert box to YOLO format (normalized xywh)
            x_center = (x_min + box_width / 2) / 320  # Use 320 as the resized width
            y_center = (y_min + box_height / 2) / 320  # Use 320 as the resized height
            norm_width = box_width / 320
            norm_height = box_height / 320

            boxes.append(f"0 {x_center} {y_center} {norm_width} {norm_height}")

        with open(os.path.join(dest_label_dir, label_filename), "w") as f:
            f.write("\n".join(boxes) + "\n")

        i += 2 + num_boxes

def process_dataset(base_dir, train_list_file, val_list_file, train_bbox_file, val_bbox_file):
    create_directory_structure(base_dir)
    
    # Move and resize train images
    move_images(train_list_file, os.path.join(base_dir, "train", "images"))
    # Move and resize validation images
    move_images(val_list_file, os.path.join(base_dir, "val", "images"))
    
    # Convert bounding boxes for train images
    convert_bounding_boxes(train_bbox_file, os.path.join(base_dir, "train", "labels"))
    # Convert bounding boxes for val images
    convert_bounding_boxes(val_bbox_file, os.path.join(base_dir, "val", "labels"))

# Example usage:
process_dataset('dataset_wider_face',                       # base_dir
                'dataset/train/train_list.txt',             # train_list_file
                'dataset/val/val_list.txt',                 # val_list_file
                'dataset/train/train_bbx_gt_reduced.txt',   # train_bbox_file
                'dataset/val/val_bbx_gt_reduced.txt')       # val_bbox_file
