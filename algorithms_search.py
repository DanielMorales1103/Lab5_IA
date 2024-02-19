from collections import deque
from queue import PriorityQueue

# Clase Nodo donde guardara estado, padre, accion y el costo
class Node():
    def __init__(self, state, parent = None, action = None, path_cost = 0, heuristic_cost=0) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost   
        self.heuristic_cost = heuristic_cost
    
    def total_cost(self):
        return self.path_cost + self.heuristic_cost
    
    def __lt__(self, other):
        return self.total_cost() < other.total_cost()

'''Justificación:
La heurística de la distancia de Manhattan es apropiada para problemas donde las acciones posibles son limitadas
a movimientos horizontales y verticales, como en un laberinto donde solo se permite avanzar en cuatro direcciones
(arriba, abajo, izquierda y derecha). '''
def heuristic_1(state, goal):
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])
'''Justificación 
La heurística euclidiana es adecuada cuando se quiere considerar la "distancia recta"
entre dos puntos en un espacio bidimensional.
'''
def heuristic_2(state, goal):
    return ((state[0] - goal[0]) ** 2 + (state[1] - goal[1]) ** 2) ** 0.5

        
# Breadth First Search
def bfs(framework):    
    frontier = deque([Node(framework.initial)]) # Definir Queue
    num_explored = 0

    explored = set()
    while frontier:        
        if len(frontier) == 0:
            raise Exception("No hay solucion para esta matriz")
                        
        node = frontier.popleft()
        num_explored += 1
        
        if framework.is_goal(node.state):
            actions = []
            states = []
            while node.parent is not None:
                actions.append(node.action)
                states.append(node.state)    
                node = node.parent
            actions.reverse()
            states.reverse()                
            return framework.result(actions, states)
        
        explored.add(node.state)

        for action, state in framework.actions(node.state):
            if not any(node.state == state for node in frontier) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.append(child)
        
    return None
    
# Depth First Search
def dfs(framework):
    frontier = [Node(state=framework.initial, parent=None, action=None)] # Stack
    num_explored = 0

    explored = set()
    while frontier:        
        if len(frontier) == 0:
            raise Exception("No hay solucion para esta matriz")
                        
        node = frontier.pop()
        num_explored += 1
        
        if framework.is_goal(node.state):
            actions = []
            states = []
            while node.parent is not None:
                actions.append(node.action)
                states.append(node.state)    
                node = node.parent
            actions.reverse()
            states.reverse()                
            return framework.result(actions, states)
        
        explored.add(node.state)

        for action, state in framework.actions(node.state):
            if not any(node.state == state for node in frontier) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.append(child)
        
    return None

def a_star(framework, heuristic_func):
    start_node = Node(state=framework.initial, heuristic_cost=heuristic_func(framework.initial, framework.goal))
    frontier = PriorityQueue()
    frontier.put((start_node.total_cost(), start_node))

    explored = set()

    while not frontier.empty():
        _, node = frontier.get()

        if framework.is_goal(node.state):
            actions, states = [], []
            while node.parent is not None:
                actions.append(node.action)
                states.append(node.state)
                node = node.parent
            actions.reverse()
            states.reverse()
            return framework.result(actions, states)

        explored.add(node.state)

        for action, state in framework.actions(node.state):
            child_path_cost = node.path_cost + framework.path_cost(node.path_cost, node.state, action, state)
            child_heuristic_cost = heuristic_func(state, framework.goal)
            child = Node(state=state, parent=node, action=action, path_cost=child_path_cost, heuristic_cost=child_heuristic_cost)

            if state not in explored:
                frontier.put((child.total_cost(), child))

    return None