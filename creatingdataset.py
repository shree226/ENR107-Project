from PIL import Image, ImageEnhance
import random
import os

image_path = '/workspaces/ENR107-Project/tools.jpg'
original_image = Image.open(image_path)


output_dir = 'augmented_images'
os.makedirs(output_dir, exist_ok=True)


def augment_image(image, save_path):
    image = image.rotate(random.choice([0, 90, 180, 270]))

    
    if random.random() > 0.5:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)


    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(random.uniform(0.8, 1.5))

    
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(random.uniform(0.8, 1.5))

    image.save(save_path)

for i in range(100):
    aug_image_path = os.path.join(output_dir, f'augmented_{i}.jpg')
    augment_image(original_image, aug_image_path)

print(f"Dataset created with 100 augmented images in {output_dir}")
