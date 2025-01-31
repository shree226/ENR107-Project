
import os
from PIL import Image

def create_annotation(image_path, tools):
    """
    Create YOLO annotation file from the tools' bounding box data
    :param image_path: Path to the image
    :param tools: List of tuples with tool details: (class_id, x_center, y_center, width, height)
    """
    
    image = Image.open(image_path)
    width, height = image.size
    txt_filename = os.path.splitext(image_path)[0] + ".txt"
    
    with open(txt_filename, 'w') as f:
        for tool in tools:
            class_id, x_center, y_center, tool_width, tool_height = tool
            x_center_norm = x_center / width
            y_center_norm = y_center / height
            width_norm = tool_width / width
            height_norm = tool_height / height
            
            f.write(f"{class_id} {x_center_norm} {y_center_norm} {width_norm} {height_norm}\n")

def label_images_in_folder(image_folder, tools_data):
    """
    Iterate through all the images in the specified folder, label them, and create annotation files.
    :param image_folder: Folder containing the images
    :param tools_data: Dictionary mapping image filenames to tool bounding box data
    """
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg"):  # Process only .jpg images
            image_path = os.path.join(image_folder, filename)
            if filename in tools_data:
                print(f"Processing {filename}...")
                create_annotation(image_path, tools_data[filename])

tools_data = {}

for i in range(100):  
    filename = f"augmented_{i}.jpg"
    tools_data[filename] = [
        (0, 100 + i, 150 + i, 50, 30),  
        (1, 250 + i, 200 + i, 60, 40) 
    ]


image_folder = "/workspaces/ENR107-Project/augmented_images"

label_images_in_folder(image_folder, tools_data)