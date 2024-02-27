# datastructures.array2d.Array2D

""" This module defines an Array2D class that represents a two-dimensional array. 
    The Array class uses a datastructures.Array object as the internal data structure. 
    The Array class adheres to the docstring requirements per method, including raising 
    appropriate exceptions where indicated.
"""



from typing import Any
from datastructures.array import Array


class Array2D:
    """ Class Array2D - representing 2D data using a 1D Array
            1. Uses an Array object as the internal data 
                structure from the Array file.
            2. Adheres to the docstring requirements per method, 
                including raising raising appropriate exceptions where indicated.
    """

    def __init__(self, rows: int = 0, columns: int = 0, default_item_value = None) -> None:
        """ Array2D Constructor. Initializes the Array2D with the desired size and default value.
            
        Examples:
            >>> array2d = Array2D(rows=2, columns=3)
            >>> print(array2d)
            [[None, None, None], [None, None, None]]

        Args:
            rows (int): the desired number of rows.
            columns (int): the desired number of columns.
            default_item_value (Any): the default value to initialize the Array2D items with.
        
        Returns:
            None
        """
        if rows < 0:
            raise ValueError("rows cannot be less than 0.")
        if columns < 0:
            raise ValueError("columns cannot be less than 0.")
        
        self._row_n = rows
        self._col_n = columns
        self._array = Array(self._row_n * self._col_n, default_item_value)

    @staticmethod
    def from_list(items):
        """
        Create a 2D Array from a Python list.
        
        Examples: 
            >>> array = Array2D.from_list([1, 2, 3], [4, 5, 6], [7, 8, 9])
            >>> print(array) 
            [[1, 2, 3], [4,5,6], [7,8,9]]
        
        Args:
            list_items (list): the 2D list to create the Array from. Each row should have the same number of columns.
            
        Returns:
            array (Array): A new Array2D instance containing the items from `list_items`
        
        Raises:
            TypeError: if list_items is not a list.
        """
        if not isinstance(items, list) or not isinstance(items[0], list):
            raise ValueError('"items" is not a 2-dimensional list.')
        
        col_len = len(items[0])
        row_len = len(items)

        array = Array2D(row_len, col_len)

        for i in range(row_len):
            if not isinstance(items[i], list):
                raise ValueError('"items" is not a 2-dimensional list.')
            if len(items[i]) != col_len:
                raise ValueError('"items" is not a rectangular list.')
            for j in range(col_len):
                array[i][j] = items[i][j]

        return array     

    class _Item:
        """ Class _Item - internal class for Array2D storing methods 
            which require access to the second bracket operator.
                Stipulations:
                1. Must use an object from the Array2D object as the
                    internal data structure.
                2. Must adhere to the docstring requirements per method, 
                    including raising raising appropriate exceptions where 
                    indicated.
        """
        def __init__(self, array_obj, row_index: int) -> None:
            """ _Item Constructor. Requires row_index from the __getitem__ special method in Array2D."""
            self._array_obj = array_obj
            self._row_index = row_index

        def __getitem__(self, col_index: int) -> Any:
            """ Bracket operator for getting an item from an Array.

            Examples:
                >>> array2d = Array2D(rows=2, columns=3)
                >>> array2d[0][0] = 1
                >>> print(array2d[0][0])
                1

            Args:
                array_obj  (object): the desired object
                index (int): the desired column index.
            
            Returns:
                Any: the item at the indexes
            
            Raises:
                IndexError: if the index is out of bounds.
            """
            row_n, col_n = self._array_obj.dimensions

            if (col_index >= 0 and col_index >= col_n) or (col_index < 0 and col_index < -col_n):
                raise IndexError(f"index {col_index} is out of bounds.")
            if col_index < 0:
                col_index = col_n + col_index
            
            return self._array_obj._array[self._row_index * col_n + col_index]

        def __setitem__(self, col_index: int, data: any) -> None:
            """ Bracket operator for setting an item in an Array.

            Examples:
                >>> array2d = Array2D(rows=2, columns=3)
                >>> array2d[0][0] = 1
                >>> print(array2d[0][0])
                1

            Args:
                index (int): the desired index to set.
                data (Any): the desired data to set at index.
            
            Returns:
                None
            
            Raises: 
                IndexError: if the index is out of bounds.
            """
            row_n, col_n = self._array_obj.dimensions

            if (col_index >= 0 and col_index >= col_n) or (col_index < 0 and col_index < -col_n):
                raise IndexError(f"index {col_index} is out of bounds.")
            if col_index < 0:
                col_index = col_n + col_index
            self._array_obj._array[self._row_index * col_n + col_index] = data

    def __getitem__(self, row_index: int) -> Any:
        """ Bracket operator for accessing an item. This bracket operator is used to 
            access the first dimension (row). This should return an object that allows
            the bracket operator to be used again to access the second dimension (column).
        
        Examples:
            >>> array2d = Array2D(rows=2, columns=3)
            >>> array2d[0][0] = 1
            >>> print(array2d[0][0])
            1
        
        Args:
            row_index (int): the index of the row to access.

        Returns:
            Any: an object that allows the bracket operator to be used again to access the second dimension (column).

        Raises:
            IndexError: if the row_index is out of range.
        """
        if (row_index >= 0 and row_index >= self._row_n) or (row_index < 0 and row_index < -self._row_n):
            raise IndexError(f"index {row_index} is out of bounds.")
        if row_index < 0:
            row_index = self._row_n + row_index
        
        return self._Item(self, row_index)
    
    @property
    def dimensions(self) -> tuple[int, int]:
        """ Property for getting dimensions of the Array2D.

        Examples:
            >>> array2d = Array2D(rows=2, columns=3)
            >>> print(array2d.dimensions)
            (2, 3)
            >>> rows, columns = array2d.dimensions
            >>> print(rows)
            2
            >>> print(columns)
            3

        Returns:
            tuple[int, int]: a tuple of the number of rows and columns.
        """
        return self._row_n, self._col_n
    
    def clear(self) -> None:
        """ Clear the Array2D
        
        Examples:
        
            >>> array = Array2D.from_list([1, 2, 3], [4, 5, 6], [7, 8, 9])
            >>> array.clear()
            >>> print(array)
            []
            >>> print(array.dimensions)
            (0, 0)
            
        Returns:
            None
        """
        self._row_n = 0
        self._col_n = 0
        self._array.clear()

    def resize_columns(self, new_columns_len: int, default_val: Any = None) -> None:
        """ Resize the length of the columns. Must be able to handle both increasing and 
            decreasing the size of the columns. Must not lose any data when resizing
            the columns. If the new length is smaller, then the data will be truncated.

        Examples:
            >>> array2d = Array2D(rows=2, columns=3)
            >>> array2d.resize_columns(4)
            >>> print(array2d.dimensions)
            (2, 4)
            >>> array2d.resize_columns(2)
            >>> print(array2d.dimensions)
            (2, 2)
        
        Args:
            new_columns_len (int): the new length of the columns.

        Returns:
            None
        
        Raises: 
            ValueError: if the new_columns_len is less than 1.
        
        """
        if new_columns_len < 0:
            raise ValueError("new_rows_len cannot be less than 0.") 

        array = Array(new_columns_len * self._row_n)
        index = 0
        
        for i in range(self._row_n):
            for j in range(new_columns_len):
                if j < self._col_n:
                    array[i * new_columns_len + j] = self._array[i * self._col_n + j]
                else:
                    array[i * new_columns_len + j] = default_val

        self._array = array
        self._col_n = new_columns_len

    def resize_rows(self, new_rows_len: int, default_val: Any = None) -> None:
        """ Resize the length of the rows. Must be able to handle both increasing and
            decreasing the size of the rows. Must not lose any data when resizing the rows.
            If the new length is smaller, then the data will be truncated.
            
        Examples:
            >>> array2d = Array2D(rows=2, columns=3)
            >>> array2d.resize_rows(4)
            >>> print(array2d.dimensions)
            (4, 3)
            >>> array2d.resize_rows(2)
            >>> print(array2d.dimensions)
            (2, 3)
        
        Args:
            new_rows_len (int): the new length of the rows.

        Returns:
            None

        Raises:
            ValueError: if the new_rows_len is less than 1.
        """
        if new_rows_len < 0:
            raise ValueError("new_rows_len cannot be less than 0.") 
        array = Array(new_rows_len * self._col_n)
        for i in range(new_rows_len):
            for j in range(self._col_n):
                if i < self._row_n:
                    array[i * self._col_n + j] = self._array[i * self._col_n + j]
                else:
                    array[i * self._col_n + j] = default_val
        self._array = array
        self._row_n = new_rows_len

    def __eq__(self, other: object) -> bool:
        """ Equality operator ==.

        Examples:
            >>> array2d1 = Array2D(rows=2, columns=3)
            >>> array2d2 = Array2D(rows=2, columns=3)
            >>> print(array2d1 == array2d2)
            True
            >>> array2d2[0][0] = 1
            >>> print(array2d1 == array2d2)
            False
        
        Args:
            other (object): the other object to compare to.
        
        Returns:
            bool: True if the two objects are equal, False otherwise.
        """
        if not isinstance(other, Array2D):
            return False
        
        return self.dimensions == other.dimensions and self._array == other._array

    def __ne__(self, other: object) -> bool:
        """ Non-equality operator !=.
        
        Examples:
            >>> array2d1 = Array2D(rows=2, columns=3)
            >>> array2d2 = Array2D(rows=2, columns=3)
            >>> print(array2d1 != array2d2)
            False
            >>> array2d2[0][0] = 1
            >>> print(array2d1 != array2d2)
            True

        Args:
            other (object): the other object to compare to.

        Returns:    
            bool: True if the two objects are not equal, False otherwise.
        """
        if not isinstance(other, Array2D):
            return False
        
        return self.dimensions != other.dimensions or self._array != other._array

    def __contains__(self, item: Any) -> bool:
        """ Contains operator (in).

        Examples:
            >>> array2d = Array2D(rows=2, columns=3)
            >>> print(3 in array2d)
            False
            >>> array2d[0][0] = 3
            >>> print(3 in array2d)
            True

        Args:   
            item (Any): the item to search for.

        Returns:    
            bool: True if the item is found, False otherwise.
        """
        for i in self._array:
            if i == item:
                return True
        return False
    
    def __does_not_contain__(self, item: Any) -> bool:
        """ Does not contain operator (not in).

        Examples:
            >>> array2d = Array2D(rows=2, columns=3)
            >>> print(3 not in array2d)
            True
            >>> array2d[0][0] = 3
            >>> print(3 not in array2d)
            False

        Args:   
            item (Any): the item to search for.

        Returns:    
            bool: False if the item is found, True otherwise.
        """
        for i in self._array:
            if i == item:
                return False
        return True

    def __str__(self) -> str:
        """ Return a string representation of the data and structure

        Examples:
            >>> array2d = Array2D(rows=2, columns=3)
            >>> print(array2d)
            [[None, None, None], [None, None, None]]
        
        Returns:
            str: a string representation of the data and structure.
        """
        output = "["
        for row in range(self._row_n):
            if row != 0:
                output += ", ["
            else:
                output += "["
            for col in range(self._col_n):
                if col != 0:
                    output += ", "
                output += str(self._array[row * self._col_n + col])
            output += "]"
        output += "]"

        return output

    def __repr__(self) -> str:
        """ Return a string representation of the data and structure.

        Examples:
            >>> array2d = Array2D(rows=2, columns=3)
            >>> print(repr(array2d))
            [[None, None, None], [None, None, None]]

        Returns:
            str: a string representation of the data and structure.
        """
        return str(self)
