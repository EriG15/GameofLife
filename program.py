""" projects.gameoflife.program

    This module starts a simulation of Conway's Game of Life.

    This module creates an instance of the Config class passing
    in value 10 to the cell_size and values 50 and 50 to rows 
    and columns.

    For the best success in running this file, run the following
    command:
    >>> python -m projects.gameoflife.program
"""

from config import Config

if __name__ == "__main__":
    Config(cell_size=10, rows=50, columns=50)