"""
Colores conforme a los numeros en cada matriz:
    - '0': Cuadro libre (Cuadro Blanco)
    - '1': Cuadro ocupado (Cuadro Negro)
    - '2': Punto de inicio (Cuadro Rojo)
    - '3': Punto de victoria (Cuadro Verde)
    - '4': Camino Recorriod (Cuadro Celeste)
"""
######################################################################################

from PIL import Image, ImageDraw
import numpy as np

def discretize_image(file_image : str, square_pixels = 20):
    img = Image.open(file_image)
    pixels = img.load()

    width = img.size[0]
    height = img.size[1]
                        
    # suma de los pixeles
    matrix = []
    for x in range(width):
        matrix_column = []
        aux_pixels = []
        for y in range(height):
            pixel = pixels[x, y]
            # suma y promedios de los colores para luego guardarlo en la matriz
            if(len(aux_pixels) >= square_pixels):
                pixel_mean = get_color_mean(aux_pixels)
                matrix_column.append(pixel_mean)
                aux_pixels = []
            else:                
                aux_pixels.append(pixel)
        matrix.append(matrix_column)
        
    # Revertir valores para obtener el promedio de los colores pendientes
    matrix_zip = zip(*matrix)
    matrix_zip_list = list(matrix_zip)
        
    # promedios pendientes
    pixels = matrix_zip_list
    matrix = []
    for x in range(len(matrix_zip_list)):
        matrix_column = []
        aux_pixels = []
        for y in range(len(matrix_zip_list[0])):
            pixel = pixels[x][y]
            if(len(aux_pixels) >= square_pixels):
                pixel_mean = get_color_mean(aux_pixels)
                matrix_column.append(pixel_mean)
                aux_pixels = []
            else:                
                aux_pixels.append(pixel)
        matrix.append(matrix_column)
        
    matrix_nums = matrix_redefine_colors(matrix)    
    return matrix_nums

def get_color_mean(pixels : list):
    sum_r = 0
    sum_g = 0
    sum_b = 0
    
    for colors in pixels:
        sum_r += colors[0]
        sum_g += colors[1]
        sum_b += colors[2]
        
    elements = len(pixels)        
    return (int(sum_r / elements), int(sum_g / elements), int(sum_b / elements))

def matrix_redefine_colors(matrix : list):
    matrix_with_numbers = []
    start_ready = False
    for x in range(len(matrix)):
        matrix_column_n = []
        for y in range(len(matrix[0])):
            r, g, b = matrix[x][y]
            
            if(r >= 250 and g <= 210 and b <= 210): # Color Rojo                                
                num = 2 if not start_ready else 0
                matrix_column_n.append(num) 
                start_ready = True
                
            elif(r <= 210 and g >= 250 and b <= 210): # Color Verde                
                matrix_column_n.append(3)
            
            elif(r <= 140 and g <= 140 and b <= 140): # Color Negro                
                matrix_column_n.append(1)
                
            elif(r >= 140 and g >= 140 and b >= 140): # Color Blanco                
                matrix_column_n.append(0)
                                
            else: # Por si el color no es valido vamos a verificar
                print(f"=====> {r}, {g}, {b}")                
                matrix_column_n.append(-1)
                
        matrix_with_numbers.append(matrix_column_n)
        
    return matrix_with_numbers
    
def save_img_matrix(matrix : list, filename : str):
    square_size = 50
    border_size = 0
    height = len(matrix)
    width = max(len(matrix) for _ in matrix)

    img = Image.new(
        "RGBA", (width * square_size, height * square_size),
    )
    draw = ImageDraw.Draw(img)
    
    for i, x in enumerate(matrix):
        for j, y in enumerate(x):
            if matrix[i][j] == 0:
                color = (255, 255, 255)
            elif matrix[i][j] == 1:
                color = (0, 0, 0)
            elif matrix[i][j] == 2:
                color = (255, 0, 0)
            elif matrix[i][j] == 3:
                color = (0, 255, 0)
            elif matrix[i][j] == 4:
                color = (66, 155, 255)
            else:
                color = (0, 0, 255)
                
            draw.rectangle(
                ([(j * square_size + border_size, i * square_size + border_size),
                ((j + 1) * square_size - border_size, (i + 1) * square_size - border_size)]),
                fill=color
            )
            
    img.save(filename)    