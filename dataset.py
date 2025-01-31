import os
import shutil
import random


base_dir = "/workspaces/ENR107-Project"
image_dir = os.path.join(base_dir, "augmented_images")  

dataset_dir = os.path.join(base_dir, "dataset")
folders = {
    "train_img": os.path.join(dataset_dir, "images/train"),
    "val_img": os.path.join(dataset_dir, "images/val"),
    "train_label": os.path.join(dataset_dir, "labels/train"),
    "val_label": os.path.join(dataset_dir, "labels/val"),
}


for path in folders.values():
    os.makedirs(path, exist_ok=True)


files = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]  
random.shuffle(files)


split_idx = int(0.8 * len(files))  
train_files, val_files = files[:split_idx], files[split_idx:]


def move_files(file_list, img_dest, label_dest):
    for file in file_list:
        img_path = os.path.join(image_dir, file)
        label_path = os.path.join(image_dir, file.replace(".jpg", ".txt"))  

        
        if os.path.exists(img_path):
            shutil.move(img_path, img_dest)
            print(f"Moved image: {img_path}")
        else:
            print(f"Image not found: {img_path}")

        
        if os.path.exists(label_path):
            shutil.move(label_path, label_dest)
            print(f"Moved label: {label_path}")
        else:
            print(f"Label not found: {label_path}")


move_files(train_files, folders["train_img"], folders["train_label"])
move_files(val_files, folders["val_img"], folders["val_label"])

print("✅ Dataset organized successfully!")


dataset_yaml_path = os.path.join(dataset_dir, "dataset.yaml")
with open(dataset_yaml_path, "w") as f:
    f.write(f"""path: {dataset_dir}
train: images/train
val: images/val
nc: 2  # Number of classes (update if needed)
names: ["tool_1", "tool_2"]  # Class names
""")

print("dataset.yaml created!")

