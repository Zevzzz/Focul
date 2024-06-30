import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = 'img.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Apply a Gaussian blur to reduce noise and improve contour detection
blurred = cv2.GaussianBlur(image, (11, 11), 0)

# Apply thresholding
_, thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Count the number of contours found
num_particles = len(contours)

# Draw contours on the original image (optional)
output_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)

# Display the result
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
plt.title(f'Number of particles: {num_particles}')
plt.axis('off')
plt.show()

print(f'Number of particles detected: {num_particles}')
