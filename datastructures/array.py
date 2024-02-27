# datastructures.array.Array

""" This module defines an Array class that represents a one-dimensional array. 
    The Array class is a dynamically growing array data structure. 
    The Array class uses a numpy array as the internal data structure. 
    The Array class adheres to the docstring requirements per method, including raising appropriate exceptions where indicated.
"""

from typing import Any
import numpy as np
class Array:
    """Array class - representing a one-dimensional array.
        Stipulations:
            1. Uses a numpy array as the internal data structure.
            2. Adheres to the docstring requirements per method, including raising
               raising appropriate exceptions where indicated.
    """

    def __init__(self, size: int = 0, default_item_value: Any = None) -> None:
        """ Array Constructor. Initializes the Array with a default capacity and default value.

        Examples:
            >>> array_one = Array()
            >>> print(array_one)
            []
            >>> array_two = Array(size=10)
            >>> print(array_two)
            [None, None, None, None, None, None, None, None, None, None]
            >>> array_three = Array(size=10, default_item_value=0)
            >>> print(array_three)
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        Args:
            size (int): the desired capacity of the Array (default is 0)
            default_item_value (Any): the desired default value of the Array (default is None)

        Returns:
            None
        """
        self._array = np.array([default_item_value]*size)

    @staticmethod
    def from_list(list_items: list) -> 'Array':
        """
        Create an Array from a Python list.
        
        Examples: 
            >>> array = Array.from_list([1, 2, 3])
            >>> print(array) 
            [1, 2, 3]
        
        Args:
            list_items (list): the list to create the Array from.
            
        Returns:
            array (Array): A new Array instance containing the items from `list_items`
        
        Raises:
            TypeError: if list_items is not a list.
        """
        if isinstance(list_items, list):
            array = Array(len(list_items))
            for i in range(len(list_items)):
                array[i] = list_items[i]
            return array
        
        raise TypeError(f'"{list_items}" is not a list.')
    
    def __getitem__(self, index: int) -> Any:
        """ Bracket operator for getting an item from an Array.

        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(array[0]) # invokes __getitem__ using the [] operator
            zero

        Args:
            index (int): the desired index.
        
        Returns:
            Any: the item at the index.
        
        Raises:
            IndexError: if the index is out of bounds.
        """
        if (index >= 0 and index >= len(self._array)) or (index < 0 and index < -len(self._array)):
            raise IndexError(f"index {index} is out of bounds.")
        return self._array[index]


        

    def __setitem__(self, index: int, data: Any) -> None:
        """ Bracket operator for setting an item in an Array.

        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array[0] = 'new zero' # invokes __setitem__
            >>> print(array[0])
            new zero

        Args:
            index (int): the desired index to set.
            data (Any): the desired data to set at index.
        
        Returns:
            None
        
        Raises: 
            IndexError: if the index is out of bounds.
        """
        if index >= len(self._array) or -index > len(self._array):
            raise IndexError(f"index {index} is out of bounds.")
        self._array[index] = data

    def append(self, data: Any) -> None:
        """ Append an item to the end of the Array

        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array.append('five') # invokes append
            >>> print(array)
            [zero, one, two, three, four, five]

        Args:
            data (Any): the desired data to append.

        Returns:
            None
        """
        self.resize(len(self._array) + 1)
        self._array[-1] = data
        
    def __len__(self) -> int:
        """ Length operator for getting the logical length of the Array (number of items in the Array).

        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(len(array))
            5

        Returns:
            length (int): the length of the Array.
        """
        return len(self._array)

    def resize(self, new_size: int, default_value: Any = None) -> None:
        """ Resize an Array. Resizing to a size smaller than the current size will truncate the Array. Resizing to a larger size will append None to the end of the Array.

        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array.resize(3) 
            >>> print(array)
            [zero, one, two]
            >>> array.resize(5)
            >>> print(len(array))
            5
            >>> print(array)
            [zero, one, two, None, None]

        Args:
            new_size (int): the desired new size of the Array.
            default_value (Any): the desired default value to append to the Array if the new size is larger than the current size. Only makes sense if the new_size is larger than the current size. (default is None).
        
        Returns:
            None
        
        Raises:
            ValueError: if the new size is less than 0.
        """
        if new_size < 0:
            raise ValueError("{new_size} is not an appropriate size. Value must be a positive integer.")
        
        array = Array(new_size, default_value)
        for i in range(new_size):
            if i < len(self._array):
                array[i] = self._array[i]
        self._array = array

    def __eq__(self, other: object) -> bool:
        """ Equality operator == to check if two Arrays are equal (deep check).

        Examples:
            >>> array1 = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array2 = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(array1 == array2) 
            True

        Args:
            other (object): the instance to compare self to.
        
        Returns:
            is_equal (bool): true if the arrays are equal (deep check).
        """
        return [value for value in self] == [value for value in other]

    def __ne__(self, other: object) -> bool:
        """ Non-Equality operator !=.
        
        Examples:
            >>> array1 = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array2 = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(array1 != array2)
            False
        
        Args:
            other (object): the instance to compare self to.
            
        Returns:
            is_not_equal (bool): true if the arrays are NOT equal (deep check).
        """
        return [value for value in self] != [value for value in other]

    def __iter__(self) -> Any:
        """ Iterator operator. Allows for iteration over the Array.
        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> for item in array: print(item, end=' ') # invokes iter
            zero one two three four 

        Yields:
            item (Any): yields the item at index
        """
        for value in self._array:
            yield value

    def __reversed__(self) -> Any:
        """ Reversed iterator operator. Allows for iteration over the Array in reverse.
        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> for item in reversed(array): print(item, end= ' ') # invokes __reversed__
            four three two one zero 

        Yields:
            item (Any): yields the item at index starting at the end
        """
        for value in reversed(self._array):
            yield value

    def __delitem__(self, index: int) -> None:
        """ Delete an item in the array. Copies the array contents from index + 1 down
            to fill the gap caused by deleting the item and shrinks the array size down by one.

        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> del array[2]
            >>> print(array)
            [zero, one, three, four]
            >>> len(array)
            4

        Args:
            index (int): the desired index to delete.
        
        Returns:
            None
        """
        if index >= len(self._array) or -index > len(self._array):
            raise IndexError(f"index {index} is out of bounds.")
        
        array = Array(len(self._array) - 1)
        j = 0
        for i in range(len(array)):
            if i == index:
                j += 1
            array[i] = self._array[j]
            j += 1
        self._array = array

    def __contains__(self, item: Any) -> bool:
        """ Contains operator (in). Checks if the array contains the item.

        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print('three' in array)
            True

        Args:
            item (Any): the desired item to check whether it's in the array.

        Returns:
            contains_item (bool): true if the array contains the item.
        """
        for value in self._array:
            if item == value:
                return True
            
        return False
    
    
    def __does_not_contain__(self, item: Any) -> bool:
        """ Does not contain operator (not in)

        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print('five' not in array)
             True

        Args:
            item (Any): the desired item to check whether it's in the array.

        Returns:
            does_not_contains_item (bool): true if the array does not contain the item.
        """ 
        for value in self._array:
            if item == value:
                return True
            
        return False

    def clear(self) -> None:
        """ Clear the Array
        
        Examples:
        
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array.clear()
            >>> print(array)
            []
            >>> print(len(array))
            0
            
        Returns:
            None
        """
        self._array = np.array([])

    def __str__(self) -> str:
        """ Return a string representation of the data and structure. 

        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(array)
            [zero, one, two, three, four]

        Returns:
            string (str): the string representation of the data and structure.
        """
        array = "["
        for i in range(len(self._array)):
            if i != len(self._array) - 1:
                array += f"{self._array[i]}, "
            else:
                array += str(self._array[i]) + "]"
        
        return array
        
    def __repr__(self) -> str:
        """ Return a string representation of the data and structure.
        
        Examples:
    
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(repr(array))
        [zero, one, two, three, four]
        
        Returns:
            string (str): the string representation of the data and structure.
        """
        return self.__str__()