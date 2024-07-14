import os
from PIL import Image, ImageDraw, ImageFont

def create_image(filename, content, width=800, height=600, font_size=30):
    # Create a new image with white background
    image = Image.new('RGB', (width, height), color='white')

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size
    bbox = draw.textbbox((0, 0), content, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate text position
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    # Draw the text on the image
    draw.text((text_x, text_y), content, fill='black', font=font)

    # Save the image
    image.save(filename)

def generate_images(num_images, folder_path, width=800, height=600):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i in range(num_images):
        content = f"Image {i + 1}"
        filename = os.path.join(folder_path, f'image_{i + 1}.png')
        create_image(filename, content, width, height)

# Set the folder where images will be saved
output_folder = r'/home/p3/IdeaProjects/OCR-Project/resources/test_folder'

# Generate 50 images with the same dimensions in the specified folder
generate_images(50, output_folder)
