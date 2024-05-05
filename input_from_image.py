from PIL import Image
import numpy as np
from scipy.ndimage import label, generate_binary_structure, find_objects
import matplotlib.pyplot as plt

COLORS = {
    'R': (180, 58, 57),
    'HG': (103, 170, 13),
    'B': (0, 37, 203),
    'T': (0, 230, 166),
    'RO': (220, 104, 125),
    'G': (255, 230, 65),
    'O': (217, 130, 53),
    'L': (104, 47, 142),
    'GR': (112, 112, 112),
    'HB': (85, 163, 229),
    'DG': (57, 82, 16),
    'P': (176, 89, 193)
}

def crop_image(filename):
    with Image.open(filename) as img:
        width, height = img.size
        top = height * 0.30
        bottom = height * 0.80
        box = (0, top, width, bottom)
        cropped_img = img.crop(box)

        return cropped_img

def extract_tubes(img, visualize=False):
    object_color = (184, 185, 190)
    color_threshold = 50
    min_size = 10

    img_array = np.array(img)
    
    # Compute color distance to filter by specified object color
    object_color = np.array(object_color)
    color_distance = np.sqrt(np.sum((img_array - object_color) ** 2, axis=-1))
    
    # Create a binary image where True represents pixels close to the object color
    object_mask = color_distance < color_threshold
    
    # Define the connectivity structure for the labeling (8-connectivity)
    struct = generate_binary_structure(2, 2)
    
    # Apply connected component labeling
    labeled, num_features = label(object_mask, structure=struct)

    # Visualization of the mask overlay on the original image
    if visualize:
        plt.figure(figsize=(10, 10))
        plt.imshow(img)
        plt.imshow(labeled != 0, alpha=0.5, cmap='jet')  # Overlaying the labeled mask with transparency
        plt.axis('off')
        plt.savefig('masked_screenshot.jpg')
        plt.show()

    object_slices = find_objects(labeled)
    object_images = []
    object_count = 0
    for i, slice_tuple in enumerate(object_slices):
        # Check dimensions to filter by minimum size
        if (slice_tuple[0].stop - slice_tuple[0].start >= min_size and
                slice_tuple[1].stop - slice_tuple[1].start >= min_size):
            object_image = img_array[slice_tuple]
            pil_img = Image.fromarray(object_image)
            object_image_path = f'object_{i+1}.jpg'
#            pil_img.save(object_image_path)
            object_images.append(pil_img)
            object_count += 1

    return object_images

def get_tube_colours(img):
    # Define relative positions as fractions of width and height
#    img.show()
    positions = [(0.5, 0.87), (0.5, 0.66), (0.5, 0.43), (0.5, 0.22)]
    colors = []

    # Ensure img is a numpy array
    img_array = np.array(img)
    height, width = img_array.shape[:2]

    # Compute actual positions and extract colors
    for pos in positions:
        # Convert relative positions to actual indices (integer)
        row = int(pos[1] * height)
        col = int(pos[0] * width)

        if row < height and col < width:
            color = tuple(img_array[row, col])
            colors.append(color)
        else:
            colors.append(None)  # Append None if the position is out of bounds

    # Return the list of colors
    return colors

def find_closest_color(test_color):
    min_distance = float('inf')  # Start with a very large number
    closest_color = None

    # Calculate distance from test_color to each color in the dictionary
    for color_key, color_value in COLORS.items():
        distance = np.sqrt((color_value[0] - test_color[0]) ** 2 +
                           (color_value[1] - test_color[1]) ** 2 +
                           (color_value[2] - test_color[2]) ** 2)
        
        # If the calculated distance is less than the current min_distance, update min_distance and closest_color
        if distance < min_distance:
            min_distance = distance
            closest_color = color_key

    return closest_color



# Specify the image file
filename = 'screenshot.jpg'
cropped_img = crop_image(filename)

tube_images = extract_tubes(cropped_img)

for tube_image in tube_images:
    extracted_colors = get_tube_colours(tube_image)
    for c in extracted_colors:
        color_key = find_closest_color(c)
        print(color_key)
        

