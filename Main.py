import cv2
import numpy as np
from google.colab.patches import cv2_imshow
from google.colab import files

# Upload images
uploaded = files.upload()

# Enter the uploaded file names here (or use list(uploaded.keys()))
input_image_path = "/content/images.jpeg"
virtual_bg_path = "/content/IMG-20250513-WA0003.jpg"

# Load images
input_image = cv2.imread(input_image_path)
virtual_bg = cv2.imread(virtual_bg_path)

if input_image is None:
    print(f"Error: Could not load image from {input_image_path}")
    exit()

if virtual_bg is None:
    print(f"Error: Could not load virtual background from {virtual_bg_path}")
    exit()

# Resize virtual background
input_height, input_width, _ = input_image.shape
virtual_bg_resized = cv2.resize(virtual_bg, (input_width, input_height))

# Grayscale + threshold to create a simple mask
gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY_INV)
mask_3channel = cv2.merge([mask, mask, mask])
mask_inv = cv2.bitwise_not(mask_3channel)

# Foreground and background separation
foreground = cv2.bitwise_and(input_image, mask_3channel)
background = cv2.bitwise_and(virtual_bg_resized, mask_inv)

# Combine foreground and new background
output_image = cv2.add(foreground, background)

# Save and display result
output_image_path = "output_image_alternate.jpg"
cv2.imwrite(output_image_path, output_image)
print(f"Output image saved as {output_image_path}")

# Show image in Colab
cv2_imshow(output_image)
