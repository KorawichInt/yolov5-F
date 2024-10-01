import random

# Define file paths
train_txt = 'dataset/train/wider_face_train_bbx_gt.txt'
val_txt = 'dataset/val/wider_face_val_bbx_gt.txt'

# Count number of dataset (before reduce)

with open(train_txt) as f:
    lines = f.readlines()


with open(val_txt) as f:
    val_lines = f.readlines()

# Count occurrences of .jpg in the lines
train_count = sum(1 for line in lines if line.endswith('.jpg\n'))
val_count = sum(1 for line in val_lines if line.endswith('.jpg\n'))

print(f"# Before reduce")
print(f"Number of .jpg files in train: {train_count}")
print(f"Number of .jpg files in val: {val_count}")

# Define the number of images to select
train_subset_size = 1400
val_subset_size = 400

# Function to extract .jpg files and their annotations
def filter_jpg_and_annotations(lines, num_images):
    filtered_lines = []
    current_img_count = 0
    i = 0
    while i < len(lines):
        if lines[i].endswith('.jpg\n'):
            # Add .jpg line and the next annotation lines
            filtered_lines.append(lines[i])  # .jpg file line
            annotation_count = int(lines[i+1].strip())  # Number of annotations
            filtered_lines.append(lines[i+1])  # Add the annotation count line
            filtered_lines.extend(lines[i+2:i+2+annotation_count])  # Add annotation lines

            current_img_count += 1
            if current_img_count >= num_images:
                break
            # Move the index forward by number of annotations + 2
            i += 2 + annotation_count
        else:
            i += 1
    return filtered_lines

# Read the train file
with open(train_txt) as f:
    train_lines = f.readlines()

# Read the val file
with open(val_txt) as f:
    val_lines = f.readlines()

# Select random subset for train
random.seed(42)  # For reproducibility
train_subset = filter_jpg_and_annotations(train_lines, train_subset_size)

# Select random subset for val
val_subset = filter_jpg_and_annotations(val_lines, val_subset_size)

# Save the reduced train set
with open('dataset/train/train_bbx_gt_reduced.txt', 'w') as f:
    f.writelines(train_subset)

# Save the reduced val set
with open('dataset/val/val_bbx_gt_reduced.txt', 'w') as f:
    f.writelines(val_subset)

# print(f"Reduced train set size: {len(train_subset)} lines")
# print(f"Reduced val set size: {len(val_subset)} lines")


# Count number of reduce dataset
train_txt_reduced = r'dataset\train\train_bbx_gt_reduced.txt'
val_txt_reduced = r'dataset\val\val_bbx_gt_reduced.txt'

with open(train_txt_reduced) as f:
    lines = f.readlines()


with open(val_txt_reduced) as f:
    val_lines = f.readlines()

# Count occurrences of .jpg in the lines
train_reduced_count = sum(1 for line in lines if line.endswith('.jpg\n'))
val_reduced_count = sum(1 for line in val_lines if line.endswith('.jpg\n'))

print(f"\n# After reduce")
print(f"Number of .jpg files in train: {train_reduced_count}")
print(f"Number of .jpg files in val: {val_reduced_count}")
