"""Program to solve a problem of a linear puzzle."""

import os
import time
import yaml

# Global variable to store nodes
nodes_expanded = []
DEBUG_LEVEL = 'none'
initial_state = [1, 2, 3, 4]
limit = 6
STRATEGY = 'breadth'

def initialize_global_variables(settings_file):
    """
    Initializes global variables by loading and validating settings from a YAML file.
    
    :param settings_file: Path to the settings YAML file.
    :raises ValueError: If any validation fails.
    """
    global DEBUG_LEVEL, initial_state

    # Load settings from the YAML file
    settings = load_settings(settings_file)

    # Validate and set `initial_state`
    if 'initial_state' not in settings:
        raise ValueError("Error: 'initial_state' is missing in the settings file.")
    initial_state = settings['initial_state']
    if not isinstance(initial_state, list) or len(initial_state) != 4:
        raise ValueError("Error: 'initial_state' must be a list with exactly 4 elements.")
    if sorted(initial_state) != [1, 2, 3, 4]:
        raise ValueError("Error: 'initial_state' must contain exactly the numbers 1, 2, 3, and 4.")
    
    # Validate and set `DEBUG_LEVEL`
    if 'debug_level' not in settings:
        raise ValueError("Error: 'debug_level' is missing in the settings file.")
    DEBUG_LEVEL = settings['debug_level']
    valid_debug_levels = ['none', 'info', 'debug', 'warning', 'error']
    if DEBUG_LEVEL not in valid_debug_levels:
        raise ValueError(f"Error: 'debug_level' must be one of {valid_debug_levels}.")

    # Output initialization status
    print(f"Debug level set to: {DEBUG_LEVEL}")
    print(f"Initial state set to: {initial_state}\n")


# Accessor functions for list elements (standardized for Python indexing)
def car(lst):
    """Returns the first element of the list or None if the list is empty."""
    return lst[0] if lst else None

def cadr(lst):
    """Returns the second element of the list or None if the list has less than two elements."""
    return lst[1] if len(lst) > 1 else None

def caddr(lst):
    """Returns the third element of the list or None if the list has less than three elements."""
    return lst[2] if len(lst) > 2 else None

def cadddr(lst):
    """Returns the fourth element of the list or None if the list has less than four elements."""
    return lst[3] if len(lst) > 3 else None

# Functions to manage files.

def load_settings(filepath):
    """Loads settings from the YAML file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def save_node_to_file(node):
    """
    Converts a node to plain text and appends it to the nodes_expanded list.
    Each node is saved in the format:
    "node_34", "[4, 1, 3, 2]", "node_11", "id"
    """
    global nodes_expanded

    # Convert the node to the required plain text format
    node_text = f'"{node[0]}", "{node[1]}", "{node[2]}", "{node[3]}"'
    
    # Append the formatted node to the list
    nodes_expanded.append(node_text)

    # Create the output directory if it doesn't exist
    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate the output filename with timestamp
    timestamp = time.strftime("%Y%m%d-%H%M")
    output_file = os.path.join(output_dir, f"nodes_expanded_{timestamp}.yml")

    # Write the list to the YAML file
    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.dump(nodes_expanded, file, allow_unicode=True)

# Function to manage logging and debugging

def debug_print(message):
    """Prints a debug message if the debug level is 'info'."""
    if DEBUG_LEVEL == 'debug':
        print(message)

def info_print(message):
    """Prints a debug message if the debug level is 'info'."""
    if DEBUG_LEVEL == 'info':
        print(message)

# Definition of the problem
def problem(initial_state):
    """Defines the problem structure including initial state, operators, and goal test."""
    global STRATEGY
    # Depending on strategy, set additional information
    if (STRATEGY == 'breadth'):
        return [
            rl_operators_breadth(),
            (lambda parent_state, info_node_parent, state, operator_name: []),  # Additional information
            initial_state,  # Initial state taken from settings
            (lambda estado: estado == [1, 2, 3, 4]),  # Objective function
            (lambda estado: [])  # Additional information associated to the state
        ]
    else:
        def auxf(node_parent, info_node_parent, generated_state, operator_name):
            return [generated_state, 1 + cadr(info_node_parent)]

        return [
            rl_operators_depth(),
            auxf,  # Additional information
            initial_state,  # Initial state taken from settings
            (lambda estado: estado == [1, 2, 3, 4]),  # Objective function
            (lambda estado: [estado, 0])  # Additional information associated to the state
        ]

def member_if(predicate, lst):
    """Returns the first item in `lst` for which `predicate` is True. If no such item exists, returns None."""
    if not callable(predicate):
        raise ValueError("The predicate must be a callable function.")
    if not isinstance(lst, list):
        raise TypeError("The second argument must be a list.")
    return next((item for item in lst if predicate(item)), None)

def find_if(predicate, lst):
    """Finds and returns the first item in `lst` that satisfies the `predicate`."""
    return next((item for item in lst if predicate(item)), None)

# Modeling system actions
def mov_ie(estado, info=None):
    """Performs a left exchange on the state."""
    debug_print(f"Left exchange: {cadr(estado)} - {car(estado)} - {caddr(estado)} - {cadddr(estado)}")
    return [cadr(estado), car(estado), caddr(estado), cadddr(estado)]

def mov_ic(estado, info=None):
    """Performs a central exchange on the state."""
    debug_print(f"Central Exchange: {car(estado)} - {caddr(estado)} - {cadr(estado)} - {cadddr(estado)}")
    return [car(estado), caddr(estado), cadr(estado), cadddr(estado)]

def mov_id(estado, info=None):
    """Performs a right exchange on the state."""
    debug_print(f"Right Exchange: {car(estado)} - {cadr(estado)} - {cadddr(estado)} - {caddr(estado)}")
    return [car(estado), cadr(estado), cadddr(estado), caddr(estado)]

def rl_operators_breadth():
    """Defines the list of operators available to the system."""
    return [['ie', mov_ie], ['ic', mov_ic], ['id', mov_id]]

def mov_ie_depth(estado, info=None):
    """Performs a left exchange on the state."""
    global limit
    if (cadr(info) < limit):
        debug_print(f"Left exchange: {cadr(estado)} - {car(estado)} - {caddr(estado)} - {cadddr(estado)}")

        return [cadr(estado), car(estado), caddr(estado), cadddr(estado)]
    else:
        return 'empty'
          

def mov_ic_depth(estado, info=None):
    """Performs a central exchange on the state."""
    global limit
    if (cadr(info) < limit):
        debug_print(f"Central Exchange: {car(estado)} - {caddr(estado)} - {cadr(estado)} - {cadddr(estado)}")

        return [car(estado), caddr(estado), cadr(estado), cadddr(estado)]
    else:
        return 'empty'

def mov_id_depth(estado, info=None):
    """Performs a right exchange on the state."""
    global limit
    if (cadr(info) < limit):
        debug_print(f"Right Exchange: {car(estado)} - {cadr(estado)} - {cadddr(estado)} - {caddr(estado)}")

        return [car(estado), cadr(estado), cadddr(estado), caddr(estado)]
    else:
        return 'empty'

def rl_operators_depth():
    """Defines the list of operators available to the system."""
    return [['ie', mov_ie_depth], ['ic', mov_ic_depth], ['id', mov_id_depth]]

def rl_objective_function(estado):
    """Checks if the given state is the solution."""
    return estado == [1, 2, 3, 4]

def select_node(arbol):
    """Selects the next node to expand from the tree."""
    nodo = car(arbol[0])  # Select from `nodes_to_expand`
    debug_print(f"Debug: select_node - arbol: {arbol}, nodo seleccionado: {nodo}")
    if isinstance(nodo, list) and len(nodo) == 1:
        return nodo[0]  # Unwrap single-node lists
    return nodo

def candidates(arbol):
    """Checks if there are candidates left in the tree for expansion."""
    return bool(arbol)

def remove_empty_states(lista_nodos):
    """Filters out nodes with an empty state."""
    return [n for n in lista_nodos if get_state(n) != 'empty']

# Gensym to generate unique identifiers for nodes
def gensym():
    """Generates a unique symbol for nodes."""
    gensym.counter += 1
    return f"node_{gensym.counter}"
gensym.counter = 0

# Core functionality
def search(problem, estrategia, arbol):
    """Performs a search to find the solution to the problem."""
    if not candidates(arbol):
        return ['There is no solution']

    nodo = select_node(arbol)
    nuevo_arbol = eliminate_selection(arbol)

    if solution(problem, nodo):
        return get_path(arbol, nodo)

    return search(
        problem,
        estrategia,
        expand_tree(problem, estrategia, nuevo_arbol, nodo)
    )

# Define strategies

def rl_strategy_breadth(queue, new_elements):
    """
    Strategy function for breadth-first search.
    
    Combines the current queue (queue) with new elements (new_elements).
    Only performs the operation if both inputs are lists.
    
    Parameters:
    - queue: list, the current queue.
    - new_elements: list, new elements to add to the queue.
    
    Returns:
    - list: Combined list of cola and new_elements, or just queue if inputs are invalid.
    """
    if isinstance(queue, list) and isinstance(new_elements, list):
        return queue + new_elements
    return queue

def rl_strategy_depth(queue, new_elements):
    """
    Strategy function for depth-first search.
    
    Combines the current queue (queue) with new elements (new_elements).
    Only performs the operation if both inputs are lists.
    
    Parameters:
    - queue: list, the current queue.
    - new_elements: list, new elements to add to the queue.
    
    Returns:
    - list: Combined list of new_elements and queue, or just new_elements if inputs are invalid.
    """
    if isinstance(queue, list) and isinstance(new_elements, list):
        return new_elements + queue
    return queue


def perform_search(problem, estrategia):
    """Starts the search process with the given strategy."""
    return search(problem, estrategia, initial_tree(estado_inicial(problem), initial_info(problem)))

def solution(problem, nodo):
    """Checks if a node satisfies the goal condition."""
    ff = objective_function(problem)
    return ff(get_state(nodo))

def get_path(arbol, nodo):
    """Constructs the solution path from the initial state to the current node."""
    if not get_id_father(nodo):
        return []

    lp = get_path(arbol, nodo_arbol(get_id_father(nodo), arbol))
    return lp + [get_operator(nodo)]

def nodo_arbol(id_node, arbol):
    """Finds a node in the tree by its identifier."""
    def check_nodo(nodo):
        return ident(nodo) == id_node

    a_expandir = member_if(check_nodo, arbol[0])
    if a_expandir:
        return a_expandir

    return find_if(check_nodo, arbol[1])

def expand_tree(problem, estrategia, arbol, nodo):
    """Expands the tree by adding new nodes based on available operators."""
    debug_print(f"Debug: expand_tree - Initial tree: {arbol}, node expanded: {nodo}")
    new_nodes_to_expand = expand_node(
        nodo,
        operators(problem),
        funtion_aditional_info(problem)
    )
    for nuevo_nodo in new_nodes_to_expand:
        info_print(f"Info: Adding node {nuevo_nodo} to the tree.")
        save_node_to_file(nuevo_nodo)  # Save the node to the output file

    # Ensure new nodes are appended to the appropriate part of the tree
    nuevo_arbol = build_tree(arbol, estrategia, nodo, new_nodes_to_expand)
    debug_print(f"Debug: expand_tree - tree updated: {nuevo_arbol}")
    return nuevo_arbol

def build_tree(arbol, estrategia, expanded_node, new_nodes_to_expand):
    """Constructs the tree with the expanded nodes."""
    debug_print(f"Debug: build_tree - tree received: {arbol}")
    nodes_to_expand = car(arbol) or []
    debug_print(f"Debug: build_tree - nodes_to_expand: {nodes_to_expand}")
    lista_actualizada = estrategia(nodes_to_expand, new_nodes_to_expand)
    debug_print(f"Debug: build_tree - lista_actualizada: {lista_actualizada}")
    list_nodes_previously_expanded = cadr(arbol) or []
    list_nodes_already_expanded = list_nodes_previously_expanded + [expanded_node]

    arbol_actualizado = [lista_actualizada, list_nodes_already_expanded]
    debug_print(f"Debug: build_tree - tree updated: {arbol_actualizado}")
    return arbol_actualizado

def eliminate_selection(arbol):
    """Removes the selected node from the list of nodes to expand."""
    list_nodes_to_expand = arbol[0]
    del list_nodes_to_expand[0]

    return [list_nodes_to_expand, arbol[1]]

def initial_tree(estado, info):
    """Initializes the tree with the starting state."""
    infres = info(estado)
    if not isinstance(infres, list):
        infres = [infres]  # Ensure it's a list
    nodo = build_node(gensym(), estado, None, None, infres)
    return [[nodo], []]

def build_node(ident, estado, id_padre, op, info):
    """Construct a new node from state, father identifier, operation and information."""
    if not isinstance(info, list):
        raise TypeError(f"'info' must be a list, got {type(info).__name__}")
    if (estado == 'empty'): return ['empty']
    if not isinstance(estado, list):
        raise ValueError(f"'estado' must be a list, got {type(estado).__name__}")
    return [ident, estado, id_padre, op] + info

def expand_node(node, operators, funcion):
    """
    Expand a new node for the operators.

    Args:
        node: The current node to expand. It is the father node.
        operators: A list or collection of operators used to determine the expansion logic.
        funcion: A callable or function that defines how the node should be processed or expanded.

    Returns:
        A list or collection of expanded nodes, depending on the logic implemented.
    """
    # Prepare the data from parent node.
    parent_state = get_state(node)
    parent_id = ident(node)
    parent_info_node = info(node)
    parent_operator = get_operator(node)
    generated_nodes = []

    for op in operators:
        if (parent_operator == car(op)):
            generated_nodes.append(['empty'])
        else:
            # Get new identifier for the generated node
            generated_node_identifier = gensym()
            # Get the function to apply for current operator
            function_to_apply = cadr(op)
            # Generate new state
            generated_state = function_to_apply(parent_state, parent_info_node)
            generated_nodes.append(build_node(
                generated_node_identifier, generated_state, parent_id, car(op), funcion(parent_state, parent_info_node, generated_state, car(op))
            ))

    return remove_empty_states(generated_nodes)

# Node-related functions

def ident(nodo):
    """Returns the identifier of a node."""
    return nodo[0]

def get_state(nodo):
    """Gets the status of the node."""
    debug_print(f"Debug: estado - nodo recibido: {nodo}")
    # Unwrap if the node is accidentally nested
    if isinstance(nodo, list) and len(nodo) == 1:
        nodo = nodo[0]
    # After unwrapping, if we received an empty node, we raise 'empty'
    if nodo == 'empty':
      return 'empty'
    if not isinstance(nodo, list):
        print(f"Error: node is not a list, node: {nodo}, type: {type(nodo)}")
        raise ValueError(f"Node is not a list: {nodo}")
    if len(nodo) < 2:
        raise ValueError(f"Node has insufficient elements: {nodo}")
    return nodo[1]

def get_id_father(nodo):
    """Get the identifier of the father."""
    return nodo[2]

def get_operator(nodo):
    """Get the operator applied to the node."""
    return nodo[3]

def info(nodo):
    """Gets the additional info of the node."""
    return nodo[4:]

# Problem-related functions.
def operators(problem):
    """Get operators from problem."""
    return problem[0]

def funtion_aditional_info(problem):
    """Get additional information from problem."""
    return problem[1]

def estado_inicial(problem):
    """Get initial state from problem."""
    return problem[2]

def objective_function(problem):
    """Get objective function from problem."""
    return problem[3]

def initial_info(problem):
    """Get initial information from problem."""
    return problem[4]

if __name__ == "__main__":
    # Initialize global variables
    global strategy

    try:
        initialize_global_variables("data/input/settings.yml")
    except ValueError as e:
        print(e)
        exit(1)  # Exit if initialization fails

    # Get user input for the search strategy
    print("Please select the \033[1mSearch strategy\033[0m")
    print("1 - \033[3mBreadth-first search algorithm\033[0m")
    print("2 - \033[3mDepth-first search algorithm\033[0m")
    print("X - \033[3mExit application\033[0m")

    while True:  # Loop until valid input is provided or the user exits
        chosen_strategy = input("Enter your selection, please: ").strip().lower()

        if chosen_strategy == "1":
            function_strategy = rl_strategy_breadth
            STRATEGY = 'breadth'
            print("\nStrategy set to Breadth-First Search.\n")
            break  # Exit the loop after valid input
        elif chosen_strategy == "2":
            function_strategy = rl_strategy_depth
            STRATEGY = 'depth'
            print("\nStrategy set to Depth-First Search.\n")
            break  # Exit the loop after valid input
        elif chosen_strategy == "x":
            print("\nExiting the application. Goodbye!\n")
            exit()  # Terminate the program
        else:
            print("\nInput value not correct, please try again.\n")


    # Measure processing time
    start_time = time.time()
    # Initialize problem with validated settings
    prob = problem(initial_state)

    # Perform search (existing logic assumed here)
    resultado = perform_search(
        prob,
        function_strategy
    )

    # Calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print total processing time
    if elapsed_time > 60:
        print(f"Total processing time: {elapsed_time / 60:.2f} minutes")
    else:
        print(f"Total processing time: {elapsed_time:.2f} seconds")

    # Print result
    print("Resultado:", resultado)
