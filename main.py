import os
import processing_image
from algorithms_search import bfs, dfs, a_star,heuristic_1, heuristic_2
from frameworks import Labyrinth

def graph_search_lab(image_lab: str, size_square: int, algorithm):
    # Discretizar imagen
    matrix_discreted_image = processing_image.discretize_image(image_lab, size_square)
    
    image_name = os.path.splitext(os.path.basename(image_lab))[0]
    preview_folder = f"img/preview/{image_name}"
    os.makedirs(preview_folder, exist_ok=True)
    processing_image.save_img_matrix(matrix_discreted_image, f"{preview_folder}/preview_{algorithm}.png")
    
    # Framework tipo Laberinto
    labyrinth = Labyrinth(matrix_discreted_image)
    heuristic_function1 = heuristic_1
    heuristic_function2 = heuristic_2
    # Seleccionar algoritmo
    if algorithm == 'bfs':
        solution = bfs(labyrinth)
    elif algorithm == 'dfs':
        solution = dfs(labyrinth)
    elif algorithm == 'a-star':
        solution = a_star(labyrinth,heuristic_function1)
    elif algorithm == 'a-star2':
        solution = a_star(labyrinth,heuristic_function2)
    else:
        raise ValueError("Algoritmo no soportado")
    
    # Guardar solución en una carpeta específica basada en el nombre de la imagen y algoritmo
    solution_folder = f"img/solutions/{image_name}"
    os.makedirs(solution_folder, exist_ok=True)
    processing_image.save_img_matrix(solution, f"{solution_folder}/solution_{algorithm}.png")

if __name__ == "__main__":
    images = ["img/Test.bmp", "img/Prueba.bmp", "img/Test2.bmp"] 
    size_square = 25  # Tamaño del cuadrado para discretizar
    
    for image_path in images:
        for algorithm in ['bfs', 'dfs','a-star','a-star2']:  # Ejecutar ambos algoritmos
            graph_search_lab(image_path, size_square, algorithm)
