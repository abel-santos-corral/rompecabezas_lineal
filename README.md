# Rompecabezas lineal

Hold a lineal puzzle (breadth-first search algorithm)

Based on UOC module _Resolucion de problemas y búsqueda_

## Specs

The data is contained in a `data` folder. It contains two subfolders: `input` and `output`.


Input folder contains a settings file where is possible to:

* Specify the input array
* Set the debugging status

The input array has to cover the following requirements:

* It's a list with 4 elements
* Only allowed values are: 1, 2, 3, 4

Output folder contains a file with the nodes expanded.

## How to execute

To execute it from console:

> ``` python3 rompecabezas_lineal ```

Depending upon the node entered, it will take less or more time to expand the tree. [1,2,3,4] will be automatic and [4,3,2,1] is the one which takes more time and expands more node.