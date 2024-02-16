# from PIL import Image
# import numpy as np

# # Load the input image and convert to RGB to ignore any alpha channel
# input_image_path = 'test1.bmp'
# input_image = Image.open(input_image_path).convert('RGB')

# # Function to convert the image into a grid-like pattern
# def convert_to_grid(image):
#     # Convert to numpy array for image manipulation
#     image_array = np.array(image)
    
#     # Define the size for each 'square' in the grid
#     square_size = 10  # You may change this size if needed
    
#     # Initialize the output image array with white color
#     output_array = np.full((image_array.shape[0], image_array.shape[1], 3), 255, dtype=np.uint8)
    
#     # Iterate over the image array in steps of 'square_size'
#     for i in range(0, image_array.shape[0], square_size):
#         for j in range(0, image_array.shape[1], square_size):
#             # Extract the current square from the image
#             square = image_array[i:i+square_size, j:j+square_size]

#             # Count the number of each color in the square
#             unique, counts = np.unique(square.reshape(-1, square.shape[2]), axis=0, return_counts=True)
#             # Determine the dominant color in the square
#             dominant_color = unique[counts.argmax()]

#             # Set the square in the output array to the dominant color
#             output_array[i:i+square_size, j:j+square_size] = dominant_color
    
#     # Convert the output array back to an image
#     output_image = Image.fromarray(output_array)
#     return output_image

# # Apply the conversion to the input image
# output_image = convert_to_grid(input_image)

# # Save the output image to a file
# output_image_path = 'sol_img1.png'
# output_image.save(output_image_path)

from PIL import Image, ImageDraw
import numpy as np

# Function to convert the image into a grid-like pattern with visible grid lines
def convert_to_grid_with_visible_lines(image, line_color=(180, 180, 180), line_width=2):
    # Convert to numpy array for image manipulation
    image_array = np.array(image)
    
    # Define the size for each 'square' in the grid
    square_size = 10  # Size of the square
    
    # Create an output image with the same dimensions as the input image
    output_image = Image.new('RGB', image.size, (255, 255, 255))
    draw = ImageDraw.Draw(output_image)
    
    # Paint the squares with the dominant color
    for i in range(0, image_array.shape[0], square_size):
        for j in range(0, image_array.shape[1], square_size):
            # Extract the current square from the image
            square = image_array[i:i+square_size, j:j+square_size]

            # Count the number of each color in the square
            unique, counts = np.unique(square.reshape(-1, square.shape[2]), axis=0, return_counts=True)
            # Determine the dominant color in the square
            dominant_color = unique[counts.argmax()]

            # Set the square in the output array to the dominant color
            draw.rectangle([(j, i), (j+square_size, i+square_size)], fill=tuple(dominant_color))
    
    # Draw the grid lines after painting the squares to ensure they are on top
    for i in range(0, image_array.shape[1], square_size):
        draw.line([(i, 0), (i, image_array.shape[0])], fill=line_color, width=line_width)
    for j in range(0, image_array.shape[0], square_size):
        draw.line([(0, j), (image_array.shape[1], j)], fill=line_color, width=line_width)

    return output_image

# Load the input image and convert to RGB to ignore any alpha channel
input_image_path = 'test4.bmp'
input_image = Image.open(input_image_path).convert('RGB')

# Apply the conversion with visible grid lines
output_image_with_visible_lines = convert_to_grid_with_visible_lines(input_image)

# Save the output image with visible grid lines to a file
output_image_with_visible_lines_path = 'sol_img4.png'
output_image_with_visible_lines.save(output_image_with_visible_lines_path)

print(f"Output image saved to {output_image_with_visible_lines_path}")
