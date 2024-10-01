# Define paths to the input and output files
train_input_file = 'dataset/train/train_bbx_gt_reduced.txt'
val_input_file = 'dataset/val/val_bbx_gt_reduced.txt'
train_output_file = 'dataset/train/train_list.txt'
val_output_file = 'dataset/val/val_list.txt'

# Function to read the input file and extract image paths
def create_image_list(input_file, output_file, folder='./images/'):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Assuming each line in the input file contains the image filename
            image_filename = line.strip()
            # Write the image path with the specified folder to the output file
            if image_filename.endswith('.jpg'):
                outfile.write(f'{folder}{image_filename}\n')

# Process the train and validation sets
create_image_list(train_input_file, train_output_file)
create_image_list(val_input_file, val_output_file)

print("Image list files created successfully.")
