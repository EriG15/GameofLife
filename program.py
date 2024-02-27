""" File: program.py

    This module starts a simulation of Conway's Game of Life.

    This module creates an instance of the Config class passing
    in value 10 to the cell_size and values 50 and 50 to rows 
    and columns.

    To play the game, run this file or type the following command:
    >>> python -m program
"""

from config import Config

if __name__ == "__main__":
    Config(cell_size=10, rows=50, columns=50)