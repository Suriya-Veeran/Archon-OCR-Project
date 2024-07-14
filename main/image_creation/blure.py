import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string

def generate_random_text(length=20):
    """Generate random text with a given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits + " ", k=length))

def create_image(filename, content, width=1000, height=500, font_size=20):
    # Create a new image with white background
    image = Image.new('RGB', (width, height), color='white')

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size
    bbox = draw.textbbox((0, 0), content, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Draw the content
    draw.text(((width - text_width) / 2, (height - text_height) / 2), content, fill='black', font=font)

    # Save the image
    image.save(filename)

def add_noise(image_path, noise_level=30):
    """Add random noise to an image."""
    with Image.open(image_path) as img:
        img_array = np.array(img)
        noise = np.random.normal(0, noise_level, img_array.shape)
        noisy_img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        noisy_img = Image.fromarray(noisy_img_array)
        noisy_filename = image_path.replace('.png', '_noisy.png')
        noisy_img.save(noisy_filename)

def apply_half_blur(image_path, radius=5):
    """Apply Gaussian blur to half of the image."""
    with Image.open(image_path) as img:
        width, height = img.size

        # Split the image into two halves
        left_half = img.crop((0, 0, width // 2, height))
        right_half = img.crop((width // 2, 0, width, height))

        # Apply blur to the left half
        blurred_left_half = left_half.filter(ImageFilter.GaussianBlur(radius))

        # Create a new image for the result
        result_img = Image.new('RGB', (width, height))

        # Paste the blurred left half and the original right half into the result image
        result_img.paste(blurred_left_half, (0, 0))
        result_img.paste(right_half, (width // 2, 0))

        # Save the result image
        blurred_filename = image_path.replace('.png', '_half_blurred.png')
        result_img.save(blurred_filename)

def generate_images(num_images, folder_path, width=1000, height=500):
    """Generate images with random content and apply noise and blur effects."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i in range(num_images):
        content = generate_random_text()
        filename = os.path.join(folder_path, f'image_{i + 1}.png')

        # Create the image with random content
        create_image(filename, content, width, height)

        # Apply random noise and half blur to the image
        add_noise(filename, noise_level=random.randint(20, 50))
        apply_half_blur(filename, radius=random.uniform(2, 10))

# Set the folder where images will be saved
output_folder = r'/home/p3/Videos/bank-cheque-blured'

# Generate 50 images with random content and apply noise and half blur effects
generate_images(5, output_folder)
