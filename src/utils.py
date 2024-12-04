# src/utils.py
import os


def create_directories(directories):
    """Create necessary directories."""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def get_image_path(image_folder, sentence_num):
    """Get the image path for the sentence, defaulting to the last available image if not found."""
    image_path = os.path.join(image_folder, f'{sentence_num}.png')
    
    if not os.path.exists(image_path):
        available_images = [f for f in os.listdir(image_folder) if f.endswith('.png')]
        if available_images:
            available_images.sort()
            image_path = os.path.join(image_folder, available_images[-1])
        else:
            raise FileNotFoundError(f"No images found for sentence {sentence_num}")
    
    return image_path
