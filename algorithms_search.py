from collections import deque

# Clase Nodo donde guardara estado, padre, accion y el costo
class Node():
    def __init__(self, state, parent = None, action = None, path_cost = 0) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost   
        
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
    