""" File: simulator.py
    
    This module holds the Simulator class.
"""
import tkinter as tk
from tkinter import ttk, filedialog
import random
import time
import copy
import config
from datastructures.array2d import Array2D

class Simulator:
    """ This is class starts up a window with several 
        options for configuring a Game of Life simulation.
    """""
    def __init__(self, rows:int, columns:int, cell_size:int=10, filepath:str|None=None):
        """ Initializes an instance of the Simulator.
            
            Args:
                rows (int): the number of rows.
                columns (int): the number of columns.
                cell_size (int): the cell size in pixels.
                filepath (str): the filepath of a preset.
            Returns:
                None
        """
        self.root = tk.Tk()

        self.manual = False
        self.moving = False
        self.cell_size = cell_size
        self.speed = .1
        self.background_color = "white"
        self.foreground_color = "#323232"

        self.root.title("Conway's Game of Life")
        self.root.iconbitmap("assets/gol.ico")
        self.root.configure(bg=self.background_color, highlightcolor=self.foreground_color, highlightthickness=1)
        
        self.rows = rows
        self.columns = columns

        # making simulation console
        self.console = tk.Frame(self.root, bg=self.background_color, highlightbackground="black", highlightthickness=1)
        self.console.grid(row=0, column=0, sticky="nsew")

        # control button
        self.control_frame = tk.Frame(self.console, highlightbackground=self.foreground_color, highlightthickness=1)
        self.control_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=20)
        self.control_button = tk.Button(self.control_frame, text="Click to Play", command=self.control_action, bg=self.background_color, fg=self.foreground_color, font=("Helvetica", 11), width=15, borderwidth=0)
        self.control_button.pack()
        
        # speed slider
        self.slider_frame = tk.Frame(self.console, highlightbackground=self.foreground_color, highlightthickness=1)
        self.slider_frame.grid(row=1, column=0, rowspan=2, padx=10, pady=10)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Vertical.TScale", troughcolor=self.background_color, bordercolor=self.foreground_color, borderwidth=0)
        speed_slider = ttk.Scale(self.slider_frame, command=self.update_speed, style="Vertical.TScale", from_=.05, to=.7, orient="vertical", length=150)
        speed_slider.set(.4)
        speed_slider.pack()
        self.root.update()

        # manual/automatic toggle button
        self.manual_frame = tk.Frame(self.console, highlightbackground=self.foreground_color, highlightthickness=1)
        self.manual_frame.grid(row=1, column=1, padx=10)
        self.manual_button = tk.Button(self.manual_frame, text="Automatic", command=self.manual_action, bg=self.background_color, fg=self.foreground_color, font=("Helvetica", 11), width=10, borderwidth=0)
        self.manual_button.pack()

        # end simulation button
        self.end_frame = tk.Frame(self.console, highlightbackground=self.foreground_color, highlightthickness=1)
        self.end_frame.grid(row=2, column=1, padx=(20,0), pady=(25,0))
        end_button = tk.Button(self.end_frame, text="End", command=self.end_simulation, bg=self.background_color, fg=self.foreground_color, font=("Helvetica", 11), width=6, borderwidth=0)
        end_button.pack()
        
        # starting window
        self.boot_board(filepath)
        self.draw_board()
        self.center_window()
        self.root.mainloop()

    def boot_board(self, filepath:str|None):
        """ Depending on the initial configuration, makes board from
            random generation or makes board from file.

            Args:
                filepath (str|None): Stores filepath of preset if one
                is chosen, otherwise stores None.
            Returns:
                None
        """

        def make_board():
            self.board_frame = tk.Canvas(self.root, bg=self.background_color, highlightbackground=self.foreground_color, highlightthickness=1, height=self.cell_size*self.rows+1, width=self.cell_size*self.columns+1)
            self.board_frame.grid(row=0, column=1, sticky="nsew")
            self.initial_board = Array2D(self.rows, self.columns, False)

        if filepath is None:
            make_board()
            
            for row in range(self.rows):
                for column in range(self.columns):
                    self.initial_board[row][column] = random.choice((True, False))

            self.current_board = copy.deepcopy(self.initial_board)
        elif filepath != "":
            try:
                with open(filepath) as world:
                    self.cell_size = int(world.readline().rstrip()[5:])
                    self.rows = int(world.readline().rstrip()[5:])
                    self.columns = int(world.readline().rstrip()[5:])

                    make_board()

                    for row in range(self.rows):
                        line = world.readline().rstrip()
                        assert len(line) == self.columns
                        for column in range(self.columns):
                            if line[column] == "X":
                                self.initial_board[row][column] = True
                    
                    self.current_board = copy.deepcopy(self.initial_board)
            except:
                self.end_simulation("File Is Incompatible")
                self.center_window()
        else:
            self.end_simulation("Filepath Not Found")
            self.center_window()

    def center_window(self):
        """ Shortcut for centering the window when necessary.
            
            Returns:
                None
        """
        window_x = self.root.winfo_screenwidth() // 2 - self.root.winfo_width() // 2
        window_y = self.root.winfo_screenheight() // 2 - self.root.winfo_height() // 2
        self.root.geometry(f"+{window_x}+{window_y}")

    def control_action(self):
        """ Action for control button press.

            Returns:
                None
        """
        if self.manual is True:
            self.next_frame()
        elif self.moving is True:
            self.control_button.config(text="Paused")
            self.moving = False
        else:
            self.moving = True
            self.control_button.config(text="Playing")
            self.next_frame()
        self.root.update()

    def update_speed(self, speed):
        """ Action for change in speed slider.

            Returns:
                None
        """
        self.speed = float(speed) ** 3
        self.root.update_idletasks()

    def manual_action(self):
        """ Action for manual/automatic button press.

            Returns:
                None
        """
        if self.manual is True:
            self.manual_button.config(text="Automatic")
            self.manual = False
            if self.moving is True:
                self.control_button.config(text="Playing")
            else:
                self.control_button.config(text="Paused")
        else:
            self.manual_button.config(text="Manual")
            self.control_button.config(text="Next")
            self.manual = True
        if self.manual is False and self.moving is True:
            self.next_frame()
        self.root.update()

    def draw_board(self):
        """ Draws live cells onto the board canvas.
            
            returns:
                None
        """
        try:
            self.board_frame.delete("all")
        except: # if window has been closed
            self.moving = False
            return
        
        for row in range(self.rows):
            for column in range(self.columns):
                if self.current_board[row][column] == True:
                    self.board_frame.create_rectangle(self.cell_size*column+1, self.cell_size*row+1, self.cell_size*(column+1)+1, self.cell_size*(row+1)+1, fill=self.foreground_color, outline=self.background_color)
        self.root.update()

    def update_board(self):
        """ Calculates the next generation of cells and replaces
            the current generation with this.

            If there is no change from one generation to the
            next, the simulation will end.

            Returns:
                None
        """
        changes_made = False
        self.new_board = Array2D(self.rows, self.columns, False)
        for row in range(self.rows):
            for column in range(self.columns):
                count = self.count_nearby_active_cells(row, column)
                if self.current_board[row][column] == False:
                    if count == 3:
                        self.new_board[row][column] = True
                        changes_made = True
                    else:
                        self.new_board[row][column] = False
                else:
                    if count < 2 or count > 3:
                        self.new_board[row][column] = False
                        changes_made = True
                    else:
                        self.new_board[row][column] = True
        self.current_board = self.new_board
        if changes_made is False:
            self.end_simulation()

    def next_frame(self):
        """ Updates and draws board. Action will perform once if 
            in manual mode and continuously at a specified speed
            while in automatic mode if moving is true. 

            Returns:
                None
        """
        self.update_board()
        self.draw_board()
        while self.manual is False and self.moving is True:
            self.root.update_idletasks()
            time.sleep(self.speed)
            self.update_board()
            self.draw_board()

    def count_nearby_active_cells(self, row, column):
        """ Counts a cell's neighbors given the cell's coordinates.
            
            Args:
                row (int): The cell's row number.
                column (int): The cell's column number.
            Returns:
                count (int): the number of neighbors.
        """
        count = 0
        for test_row in range(-1,2):
            if test_row + row >= 0 and test_row + row < self.rows:
                for test_column in range(-1,2):
                    if (test_column + column >= 0 and test_column + column < self.columns) and (test_column != 0 or test_row != 0):
                        if self.current_board[test_row + row][test_column + column]:
                            count += 1
        return count

    def end_simulation(self, error=None):
        """ Ends the simulation, removing the simulation
            controls and adding options for where how to
            proceed.

            Args:
                error (str|None): str error message if 
                function was called because of an error,
                otherwise value is None.
            Returns:
                None
        """
        # removing simulation panel
        self.moving = False
        self.control_frame.destroy()
        self.slider_frame.destroy()
        self.manual_frame.destroy()
        self.end_frame.destroy()
        
        # adding options for how to proceed
        quit_frame = tk.Frame(self.console, highlightbackground=self.foreground_color, highlightthickness=1)
        quit_frame.grid(row=0, padx=10, pady=(20,10))
        quit_button = tk.Button(quit_frame, text="Quit Window", command=self.quit_window, bg=self.background_color, fg=self.foreground_color, font=("Helvetica", 11), width=15, borderwidth=0)
        quit_button.pack()

        reconf_frame = tk.Frame(self.console, highlightbackground=self.foreground_color, highlightthickness=1)
        reconf_frame.grid(row=1, padx=10, pady=10)
        reconf_button = tk.Button(reconf_frame, text="Reconfigure", command=self.reconfigure, bg=self.background_color, fg=self.foreground_color, font=("Helvetica", 11), width=15, borderwidth=0)
        reconf_button.pack()

        if error is None:
            save_current_frame = tk.Frame(self.console, highlightbackground=self.foreground_color, highlightthickness=1)
            save_current_frame.grid(row=2, padx=10, pady=10)
            save_current_button = tk.Button(save_current_frame, text="Save Current State", command=self.save_state, bg=self.background_color, fg=self.foreground_color, font=("Helvetica", 11), width=15, borderwidth=0)
            save_current_button.pack()

            save_initial_frame = tk.Frame(self.console, highlightbackground=self.foreground_color, highlightthickness=1)
            save_initial_frame.grid(row=3, padx=10, pady=10)
            save_initial_button = tk.Button(save_initial_frame, text="Save Initial World", command=self.save_initial_world, bg=self.background_color, fg=self.foreground_color, font=("Helvetica", 11), width=15, borderwidth=0)
            save_initial_button.pack()
        else:
            error_frame = tk.Frame(self.console, highlightbackground=self.foreground_color, highlightthickness=1)
            error_frame.grid(row=2, padx=10, pady=10)
            error_message = tk.Label(error_frame, text=error, bg=self.background_color, fg=self.foreground_color, font=("Helvetica", 9), width=15, borderwidth=0)
            error_message.pack()

    def quit_window(self):
        """ Exits out of the simulation window, completing 
            the program.
            
            Returns:
                None
        """
        self.root.destroy()

    def reconfigure(self):
        """ Exits out of the simulation window and starts a
            new configuration window.
            
            Returns:
                None        
        """
        self.root.destroy()
        config.Config(cell_size=self.cell_size, rows=self.rows, columns=self.columns)

    def save_state(self, initial=False):
        """ Saves the state of the world.

            Args:
                initial (bool): True if saving the
                initial world, otherwise False, saving
                the current world.
            
            Return:
                None
        """
        if initial is False:
            board = self.current_board
        else:
            board = self.initial_board
        filepath = filedialog.asksaveasfilename(initialdir="./worlds", defaultextension=".txt", confirmoverwrite=True)
        if filepath:
            with open(filepath, 'w') as world:
                world.write(f"size:{self.cell_size}\nrows:{self.rows}\ncols:{self.columns}\n")
                for row in range(self.rows):
                    for column in range(self.columns):
                        if board[row][column]:
                            world.write("X")
                        else:
                            world.write("O")
                    world.write("\n")

    def save_initial_world(self):
        """ Calls upon the save_state method with
            initial as True, saving the initial
            state.

            Return:
                None
        """
        self.save_state(initial=True)