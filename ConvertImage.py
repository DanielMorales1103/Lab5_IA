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

# library https://docs.python.org/3/library/abc.html

from PIL import Image, ImageDraw
import numpy as np
from abc import ABC, abstractmethod


# Function to convert the image into a grid-like pattern with visible grid lines
def convert_to_grid(image):
    image_array = np.array(image)
    square_size = 10  
    output_image = Image.new('RGB', (image_array.shape[1], image_array.shape[0]), (255, 255, 255))
    output_matrix = np.zeros((image_array.shape[0] // square_size, image_array.shape[1] // square_size, 3), dtype=np.uint8)
    
    for i in range(0, image_array.shape[0], square_size):
        for j in range(0, image_array.shape[1], square_size):
            if i // square_size < output_matrix.shape[0] and j // square_size < output_matrix.shape[1]:
                square = image_array[i:i+square_size, j:j+square_size]
                unique, counts = np.unique(square.reshape(-1, square.shape[2]), axis=0, return_counts=True)
                dominant_color = unique[counts.argmax()]
                output_matrix[i // square_size, j // square_size] = dominant_color
                output_image.paste(tuple(dominant_color), (j, i, j + square_size, i + square_size))
    
    return output_matrix, output_image

# Load the input image and convert to RGB to ignore any alpha channel
input_image_path = 'test3.bmp'
input_image = Image.open(input_image_path).convert('RGB')

# Apply the conversion to the input image
output_matrix, output_image_with_visible_lines = convert_to_grid(input_image)

# Print the matrix
print("Output Matrix:")
print(output_matrix)


# Save the output image with visible grid lines to a file
output_image_with_visible_lines_path = 'sol_img4.png'
output_image_with_visible_lines.save(output_image_with_visible_lines_path)

print(f"Output image saved to {output_image_with_visible_lines_path}")


#structure

class ProblemFramework(ABC):
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    @abstractmethod
    def actions(self, state):
        """
        Returns a list of possible actions from the current state.        
        """
        pass

    @abstractmethod
    def step_cost(self, state, action, next_state):
        """
        Calculates the cost of performing an action from the current state to the next state
        """
        pass

    @abstractmethod
    def is_goal(self, state):
        """
        Verify whether the current state is a target state
        """
        pass


class MazeProblem(ProblemFramework):
    def __init__(self, initial_state, goal_state, maze_matrix):
        super().__init__(initial_state, goal_state)
        self.maze_matrix = maze_matrix

    def actions(self, state):
        row, col = state
        possible_actions = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(self.maze_matrix) and 0 <= new_col < len(self.maze_matrix[0]) and self.maze_matrix[new_row][new_col] != '#':
                possible_actions.append((new_row, new_col))
        return possible_actions

    def step_cost(self, state, action, next_state):
        return 1

    def is_goal(self, state):
        return state == self.goal_state


initial_state = (0, 0)  # Define initial state
goal_state = (len(output_matrix) - 1, len(output_matrix[0]) - 1)  # Define goal state
maze_problem_instance = MazeProblem(initial_state, goal_state, output_matrix)
