"""Program to solve a problem of a linear puzzle."""

import os
import time
import yaml

# Global variable to store nodes
nodes_expanded = []
debug_level = 'none'
initial_state = [1, 2, 3, 4]

def initialize_global_variables(settings_file):
    """
    Initializes global variables by loading and validating settings from a YAML file.
    
    :param settings_file: Path to the settings YAML file.
    :raises ValueError: If any validation fails.
    """
    global debug_level, initial_state

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
    
    # Validate and set `debug_level`
    if 'debug_level' not in settings:
        raise ValueError("Error: 'debug_level' is missing in the settings file.")
    debug_level = settings['debug_level']
    valid_debug_levels = ['none', 'info', 'debug', 'warning', 'error']
    if debug_level not in valid_debug_levels:
        raise ValueError(f"Error: 'debug_level' must be one of {valid_debug_levels}.")

    # Output initialization status
    print(f"Debug level set to: {debug_level}")
    print(f"Initial state set to: {initial_state}")


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
    if debug_level == 'debug':
        print(message)

def info_print(message):
    """Prints a debug message if the debug level is 'info'."""
    if debug_level == 'info':
        print(message)

# Definition of the problem
def problema(initial_state):
    """Defines the problem structure including initial state, operators, and goal test."""
    return [
        rl_operadores(),
        (lambda info_nodo_padre, estado, nombre_operador: []),  # Additional information
        initial_state,  # Initial state taken from settings
        (lambda estado: estado == [1, 2, 3, 4]),  # Objective function
        (lambda estado: [])  # Additional information associated to the state
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

def rl_operadores():
    """Defines the list of operators available to the system."""
    return [['ie', mov_ie], ['ic', mov_ic], ['id', mov_id]]

def rl_funcion_objetivo(estado):
    """Checks if the given state is the solution."""
    return estado == [1, 2, 3, 4]

def selecciona_nodo(arbol):
    """Selects the next node to expand from the tree."""
    nodo = car(arbol[0])  # Select from `nodos_a_expandir`
    debug_print(f"Debug: selecciona_nodo - arbol: {arbol}, nodo seleccionado: {nodo}")
    if isinstance(nodo, list) and len(nodo) == 1:
        return nodo[0]  # Unwrap single-node lists
    return nodo

def candidatos(arbol):
    """Checks if there are candidates left in the tree for expansion."""
    return bool(arbol)

def eliminar_estados_vacios(lista_nodos):
    """Filters out nodes with an empty state."""
    return [n for n in lista_nodos if estado(n) != 'vacio']

# Gensym to generate unique identifiers for nodes
def gensym():
    """Generates a unique symbol for nodes."""
    gensym.counter += 1
    return f"node_{gensym.counter}"
gensym.counter = 0

# Core functionality
def busqueda(problema, estrategia, arbol):
    """Performs a search to find the solution to the problem."""
    if not candidatos(arbol):
        return ['There is no solution']

    nodo = selecciona_nodo(arbol)
    nuevo_arbol = elimina_seleccion(arbol)

    if solucion(problema, nodo):
        return camino(arbol, nodo)

    return busqueda(
        problema,
        estrategia,
        expande_arbol(problema, estrategia, nuevo_arbol, nodo)
    )

def hacer_busqueda(problema, estrategia):
    """Starts the search process with the given strategy."""
    return busqueda(problema, estrategia, arbol_inicial(estado_inicial(problema), info_inicial(problema)))

def solucion(problema, nodo):
    """Checks if a node satisfies the goal condition."""
    ff = funcion_objetivo(problema)
    return ff(estado(nodo))

def camino(arbol, nodo):
    """Constructs the solution path from the initial state to the current node."""
    if not id_padre(nodo):
        return []

    lp = camino(arbol, nodo_arbol(id_padre(nodo), arbol))
    return lp + [operador(nodo)]

def nodo_arbol(id_nodo, arbol):
    """Finds a node in the tree by its identifier."""
    def check_nodo(nodo):
        return ident(nodo) == id_nodo

    a_expandir = member_if(check_nodo, arbol[0])
    if a_expandir:
        return a_expandir

    return find_if(check_nodo, arbol[1])

def expande_arbol(problema, estrategia, arbol, nodo):
    """Expands the tree by adding new nodes based on available operators."""
    debug_print(f"Debug: expande_arbol - Initial tree: {arbol}, node expanded: {nodo}")
    nuevos_nodos_a_expandir = expande_nodo(
        nodo,
        operadores(problema),
        funcion_info_adicional(problema)
    )
    for nuevo_nodo in nuevos_nodos_a_expandir:
        info_print(f"Info: Adding node {nuevo_nodo} to the tree.")
        save_node_to_file(nuevo_nodo)  # Save the node to the output file

    # Ensure new nodes are appended to the appropriate part of the tree
    nuevo_arbol = construye_arbol(arbol, estrategia, nodo, nuevos_nodos_a_expandir)
    debug_print(f"Debug: expande_arbol - tree updated: {nuevo_arbol}")
    return nuevo_arbol

def construye_arbol(arbol, estrategia, nodo_expandido, nuevos_nodos_a_expandir):
    """Constructs the tree with the expanded nodes."""
    debug_print(f"Debug: construye_arbol - tree received: {arbol}")
    nodos_a_expandir = car(arbol) or []
    debug_print(f"Debug: construye_arbol - nodos_a_expandir: {nodos_a_expandir}")
    lista_actualizada = estrategia(nodos_a_expandir, nuevos_nodos_a_expandir)
    debug_print(f"Debug: construye_arbol - lista_actualizada: {lista_actualizada}")
    list_nodes_previously_expanded = cadr(arbol) or []
    list_nodes_already_expanded = list_nodes_previously_expanded + [nodo_expandido]

    arbol_actualizado = [lista_actualizada, list_nodes_already_expanded]
    debug_print(f"Debug: construye_arbol - tree updated: {arbol_actualizado}")
    return arbol_actualizado

def elimina_seleccion(arbol):
    """Removes the selected node from the list of nodes to expand."""
    list_nodes_to_expand = arbol[0]
    del list_nodes_to_expand[0]

    return [list_nodes_to_expand, arbol[1]]

def arbol_inicial(estado, info):
    """Initializes the tree with the starting state."""
    infres = info(estado)
    if not isinstance(infres, list):
        infres = [infres]  # Ensure it's a list
    nodo = construye_nodo(gensym(), estado, None, None, infres)
    return [[nodo], []]

def construye_nodo(ident, estado, id_padre, op, info):
    """Construct a new node from state, father identifier, operation and information."""
    if not isinstance(info, list):
        raise TypeError(f"'info' must be a list, got {type(info).__name__}")
    if not isinstance(estado, list):
        raise ValueError(f"'estado' must be a list, got {type(estado).__name__}")
    return [ident, estado, id_padre, op] + info

def expande_nodo(nodo, operadores, funcion):
    """Expand a new node for the operators."""
    st = estado(nodo)
    id_nodo = ident(nodo)
    info_nodo = info(nodo)
    nuevos_nodos = []

    for op in operadores:
        nuevo_simbolo = gensym()
        ff = cadr(op)
        ffapp = ff(st, info_nodo)
        nuevos_nodos.append(construye_nodo(
            nuevo_simbolo, ffapp, id_nodo, car(op), funcion([st, info_nodo], ffapp, car(op))
        ))

    return eliminar_estados_vacios(nuevos_nodos)

# Node-related functions

def ident(nodo):
    """Returns the identifier of a node."""
    return nodo[0]

def estado(nodo):
    """Gets the status of the node."""
    debug_print(f"Debug: estado - nodo recibido: {nodo}")
    # Unwrap if the node is accidentally nested
    if isinstance(nodo, list) and len(nodo) == 1:
        nodo = nodo[0]
    if not isinstance(nodo, list):
        print(f"Error: node is not a list, node: {nodo}, type: {type(nodo)}")
        raise ValueError(f"Node is not a list: {nodo}")
    if len(nodo) < 2:
        raise ValueError(f"Node has insufficient elements: {nodo}")
    return nodo[1]

def id_padre(nodo):
    """Get the identifier of the father."""
    return nodo[2]

def operador(nodo):
    """Get the operator applied to the node."""
    return nodo[3]

def info(nodo):
    """Gets the additional info of the node."""
    return nodo[4:]

# Problem-related functions.
def operadores(problema):
    """Get operadores from problem."""
    return problema[0]

def funcion_info_adicional(problema):
    """Get additional information from problem."""
    return problema[1]

def estado_inicial(problema):
    """Get initial state from problem."""
    return problema[2]

def funcion_objetivo(problema):
    """Get objective function from problem."""
    return problema[3]

def info_inicial(problema):
    """Get initial information from problem."""
    return problema[4]

if __name__ == "__main__":
    # Initialize global variables
    try:
        initialize_global_variables("data/input/settings.yml")
    except ValueError as e:
        print(e)
        exit(1)  # Exit if initialization fails

    # Measure processing time
    start_time = time.time()
    # Initialize problem with validated settings
    prob = problema(initial_state)

    # Perform search (existing logic assumed here)
    resultado = hacer_busqueda(
        prob,
        lambda cola, nuevos: cola + nuevos if isinstance(cola, list) and isinstance(nuevos, list) else cola
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
