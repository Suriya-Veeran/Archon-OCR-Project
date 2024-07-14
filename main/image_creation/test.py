import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_cheque(filename, payee_name, amount, date, cheque_number, width=1000, height=500, font_size=20):
    # Create a new image with white background
    image = Image.new('RGB', (width, height), color='white')

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Load fonts
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
        header_font = ImageFont.truetype("arial.ttf", font_size + 10)
    except IOError:
        font = ImageFont.load_default()
        header_font = font

    # Draw cheque border
    draw.rectangle([10, 10, width - 10, height - 10], outline='black', width=2)

    # Draw the header
    draw.text((20, 20), "BANK CHEQUE", fill='black', font=header_font)

    # Draw cheque details
    draw.text((20, 80), f"Pay to the order of: {payee_name}", fill='black', font=font)
    draw.text((20, 120), f"Amount: ${amount}", fill='black', font=font)
    draw.text((20, 160), f"Date: {date}", fill='black', font=font)
    draw.text((20, 200), f"Cheque Number: {cheque_number}", fill='black', font=font)

    # Draw a line for signature
    draw.line([(20, height - 80), (width - 20, height - 80)], fill='black', width=1)
    draw.text((20, height - 60), "Signature", fill='black', font=font)

    # Save the image
    image.save(filename)

def add_noise(image_path, noise_level=30):
    # Open the image
    with Image.open(image_path) as img:
        # Convert image to numpy array
        img_array = np.array(img)

        # Generate random noise
        noise = np.random.normal(0, noise_level, img_array.shape)

        # Add noise to the image
        noisy_img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)

        # Convert back to image
        noisy_img = Image.fromarray(noisy_img_array)

        # Save the noisy image
        noisy_filename = image_path.replace('.png', '_noisy.png')
        noisy_img.save(noisy_filename)

        return noisy_filename

def flip_image_horizontally(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Flip the image horizontally
        flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)

        # Save the flipped image
        flipped_filename = image_path.replace('.png', '_flipped.png')
        flipped_img.save(flipped_filename)

def generate_and_process_cheques(num_cheques, folder_path, width=1000, height=500):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Example data for cheques
    payees = [f"Payee {i + 1}" for i in range(num_cheques)]
    amounts = [f"{1000 + i * 10:.2f}" for i in range(num_cheques)]
    dates = [f"01/01/2024" for i in range(num_cheques)]
    cheque_numbers = [f"{10000 + i}" for i in range(num_cheques)]

    for i in range(num_cheques):
        payee_name = payees[i]
        amount = amounts[i]
        date = dates[i]
        cheque_number = cheque_numbers[i]
        filename = os.path.join(folder_path, f'cheque_{i + 1}.png')

        # Create the cheque image
        create_cheque(filename, payee_name, amount, date, cheque_number, width, height)

        # Add noise to the cheque image
        noisy_filename = add_noise(filename)

        # Flip the noisy image horizontally
        flip_image_horizontally(noisy_filename)

# Set the folder where cheques will be saved
output_folder = r'/home/p3/Videos/bank-cheque-test'

# Generate cheques and process them (add noise and flip) in the specified folder
generate_and_process_cheques(5, output_folder)

