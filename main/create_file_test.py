import os
from PIL import Image, ImageDraw, ImageFont

def create_id_card(filename, name, id_number, position, department, width=800, height=600, font_size=20):
    # Create a new image with white background
    image = Image.new('RGB', (width, height), color='lightgray')

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
        header_font = ImageFont.truetype("arial.ttf", font_size + 10)
    except IOError:
        font = ImageFont.load_default()
        header_font = font

    # Draw the ID card header
    draw.rectangle([10, 10, width - 10, 100], outline='black', fill='white')
    draw.text((20, 20), "ID Card", fill='black', font=header_font)

    # Draw the ID card content
    draw.text((20, 120), f"Name: {name}", fill='black', font=font)
    draw.text((20, 160), f"ID Number: {id_number}", fill='black', font=font)
    draw.text((20, 200), f"Position: {position}", fill='black', font=font)
    draw.text((20, 240), f"Department: {department}", fill='black', font=font)

    # Draw a border around the ID card
    draw.rectangle([5, 5, width - 5, height - 5], outline='black', width=2)

    # Save the image
    image.save(filename)

def generate_id_cards(num_cards, folder_path, width=800, height=600):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Example data for ID cards
    names = [f"Person {i + 1}" for i in range(num_cards)]
    id_numbers = [f"{1000 + i}" for i in range(num_cards)]
    positions = [f"Position {i + 1}" for i in range(num_cards)]
    departments = [f"Department {i + 1}" for i in range(num_cards)]

    for i in range(num_cards):
        name = names[i]
        id_number = id_numbers[i]
        position = positions[i]
        department = departments[i]
        filename = os.path.join(folder_path, f'id_card_{i + 1}.png')
        create_id_card(filename, name, id_number, position, department, width, height)

# Set the folder where ID cards will be saved
output_folder = r'/home/p3/IdeaProjects/OCR-Project/resources/id_card_folder'

# Generate 50 ID cards with the same dimensions in the specified folder
generate_id_cards(50, output_folder)
