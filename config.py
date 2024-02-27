""" File: config.py
    
    This module holds the Config class.
"""
from simulator import Simulator
import tkinter as tk
from tkinter import filedialog

class Config:
    """ This is class starts up a window with several 
        options for configuring a Game of Life simulation.
    """
    def __init__(self, cell_size, rows, columns) -> None:
        """ Initializes an instance of the Config
            
            Args:
                cell_size (int): the desired cell size in pixels (at least 1).
                rows (int): the desired number of rows (at least 10).
                columns (int): the desired number of columns (at least 10).
            Returns:
                None
        """
        self.root = tk.Tk()

        background_color = "#F4F4F4"
        foreground_color = "black"
        
        self.root.title("Conway's Game of Life")
        self.root.iconbitmap("assets/gol.ico")
        self.root.configure(bg=background_color)

        # creating cell size widget
        numeric_validation = self.root.register(self.validate_numeric)

        if cell_size < 10:
            self.cell_size = 10
        else:
            self.cell_size = cell_size

        cell_size_element = tk.Frame(self.root, bg=background_color)
        cell_size_element.grid(row=1, column=0, columnspan=2, pady=10)

        cell_size_label = tk.Label(cell_size_element, justify="center", text="Set Cell Size", bg=background_color, fg=foreground_color, width=20, font=("Helvetica", 13))
        cell_size_label.pack()

        self.cell_size_text = tk.Entry(cell_size_element, justify="center", bg=background_color, fg=foreground_color, width=13, font=("Helvetica", 13), 
                                  validate="key", validatecommand=(numeric_validation, "%P"), relief=tk.SOLID)
        self.cell_size_text.pack()
        self.cell_size_text.insert(0, str(self.cell_size))
        self.cell_size_text.bind("<Return>",self.cell_size_text_entry)
        self.cell_size_text.bind("<FocusOut>",self.cell_size_text_entry)   

        # creating row widget
        if columns < 10:
            self.rows = 10
        else:
            self.rows = rows

        row_element = tk.Frame(self.root, bg=background_color)
        row_element.grid(row=2, column=0, padx=(20,10), pady=(0,10))

        row_label = tk.Label(row_element, text="Set Rows", bg=background_color, fg=foreground_color, width=10, font=("Helvetica", 13))
        row_label.pack()

        self.row_text = tk.Entry(row_element, justify="center", bg=background_color, fg=foreground_color, width=10, font=("Helvetica", 13), 
                                  validate="key", validatecommand=(numeric_validation, "%P"), relief=tk.SOLID)
        self.row_text.pack()
        self.row_text.insert(0, str(self.rows))
        self.row_text.bind("<Return>",self.row_text_entry)
        self.row_text.bind("<FocusOut>",self.row_text_entry)   

        # creating column widget
        if columns < 10:
            self.columns = 10
        else:
            self.columns = columns

        col_element = tk.Frame(self.root, bg=background_color)
        col_element.grid(row=2, column=1, padx=(10,20), pady=(0,10))

        col_label = tk.Label(col_element, text="Set Columns", bg=background_color, fg=foreground_color, width=10, font=("Helvetica", 13))
        col_label.pack()

        self.col_text = tk.Entry(col_element, justify="center", bg=background_color, fg=foreground_color, width=10, font=("Helvetica", 13), 
                                  validate="key", validatecommand=(numeric_validation, "%P"), relief=tk.SOLID)
        self.col_text.pack()
        self.col_text.insert(0, str(self.columns))
        self.col_text.bind("<Return>",self.col_text_entry)
        self.col_text.bind("<FocusOut>",self.col_text_entry)   

        # creating generation buttons
        random_button = tk.Button(self.root, text="Generate Random World", command=self.random, bg=background_color, fg=foreground_color, font=("Helvetica", 11), width=20, relief=tk.SOLID)
        random_button.grid(row=3, column=0, columnspan=2, pady=(0,10))

        from_file_button = tk.Button(self.root, text="Generate World From File", command=self.from_file, bg=background_color, fg=foreground_color, font=("Helvetica", 11), width=20, relief=tk.SOLID)
        from_file_button.grid(row=4, column=0, columnspan=2, pady=(0,10))

        # starting up window
        window_x = self.root.winfo_screenwidth() // 2 - self.root.winfo_width() // 2
        window_y = self.root.winfo_screenheight() // 2 - self.root.winfo_height() // 2
        self.root.geometry(f"+{window_x}+{window_y}")

        self.root.mainloop()
        
    def validate_numeric(self, entry:str) -> bool:
        """ Checks if a text entry is numeric
            
            Args:
                entry (str): a string input from one of the text boxes
            Returns:
                (bool): True if the entry is numeric, False otherwise.
        """
        if entry.isdigit() or entry == "":
            return True
        else:
            return False
        
    def cell_size_text_entry(self, event:object=None) -> None:
        """ Updates cell_size based on cell size text entry.
        
            If the input value is less than 1, the value will be 1.
            If the input value is greater than 50, the value will be 50.

            Args:
                event: the text box event which called the function.
            Returns:
                None
        """
        if self.cell_size_text.get() == "" or int(self.cell_size_text.get()) < 1:
            self.cell_size_text.delete(0, tk.END)
            self.cell_size_text.insert(0, "1")
        elif int(self.cell_size_text.get()) > 50:
            self.cell_size_text.delete(0, tk.END)
            self.cell_size_text.insert(0, "50")
        if self.cell_size != int(self.cell_size_text.get()):
            self.cell_size = int(self.cell_size_text.get())
        
    def row_text_entry(self, event:object=None) -> None:
        """ Updates cell_size based on rows text entry.
        
            If the input value is less than 10, the value will be 10.
            If the input value is greater than 1000, the value will be 1000.

            Args:
                event: the text box event which called the function.
            Returns:
                None
        """
        if self.row_text.get() == "" or int(self.row_text.get()) < 10:
            self.row_text.delete(0, tk.END)
            self.row_text.insert(0, "10")
        elif int(self.row_text.get()) > 1000:
            self.row_text.delete(0, tk.END)
            self.row_text.insert(0, "1000")
        if self.rows != int(self.row_text.get()):
            self.rows = int(self.row_text.get())

    def col_text_entry(self, event:object=None) -> None:
        """ Updates cell_size based on columns text entry.
        
            If the input value is less than 10, the value will be 10.
            If the input value is greater than 1000, the value will be 1000.

            Args:
                event: the text box event which called the function.
            Returns:
                None
        """
        if self.col_text.get() == "" or int(self.col_text.get()) < 10:
            self.col_text.delete(0, tk.END)
            self.col_text.insert(0, "10")
        elif int(self.col_text.get()) > 1000:
            self.col_text.delete(0, tk.END)
            self.col_text.insert(0, "1000")
        if self.columns != int(self.col_text.get()):
            self.columns = int(self.col_text.get())

    def random(self) -> None:
        """ Action for when random generation button is pressed.
            Invokes an instance of the Simulator class.
            
            Returns:
                None
        """
        self.cell_size_text_entry()
        self.row_text_entry()
        self.col_text_entry()
        self.root.destroy()
        Simulator(rows=self.rows, columns=self.columns, cell_size=self.cell_size)   

    def from_file(self) -> None:
        """ Action for when generate from preset button is pressed.
            Invokes an instance of the Simulator class.
            
            Returns:
                None
        """
        filepath = filedialog.askopenfilename(initialdir="./worlds")
        if filepath != "":
            self.root.destroy()
            Simulator(rows=self.rows, columns=self.columns, filepath=filepath)