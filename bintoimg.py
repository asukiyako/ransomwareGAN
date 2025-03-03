import os
import numpy as np
from PIL import Image
import magic  # Cross-platform way to detect file types

# Define input and output directories
input_folder = "./malware"  # Folder containing executable files
output_folder = "./output_images"  # Folder to save .png images

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# Function to check if a file is an executable
def is_executable(file_path):
    mime = magic.Magic()
    file_type = mime.from_file(file_path)
    return "executable" in file_type

# Function to convert an executable file to an image
def exe_to_image(file_path, image_size=(128, 128)):
    with open(file_path, "rb") as f:
        binary_data = f.read()

    # Convert binary data to numpy array
    data = np.frombuffer(binary_data, dtype=np.uint8)

    # Reshape data to form an image
    image_size = (min(len(data), image_size[0] * image_size[1]),)  # Adjust size if data is small
    data = np.pad(data, (0, max(0, np.prod(image_size) - len(data))), 'constant')  # Pad if necessary
    data = data[:np.prod(image_size)].reshape(image_size)

    # Convert numpy array to grayscale image
    image = Image.fromarray(data, mode="L")
    return image

# Process all executable files in the input folder
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)

    # Check if the file is an executable
    if os.path.isfile(file_path) and is_executable(file_path):
        image = exe_to_image(file_path)
        output_path = os.path.join(output_folder, filename + ".png")  # Add .png extension
        image.save(output_path)
        print(f"Saved: {output_path}")

print("Conversion completed!")
