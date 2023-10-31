class MRU_List:
    """
    MRU list, most recently used key.
    """
    
    MAX_LEN = 26
    DEFUALT = []
    
    def __init__(self, mru='') -> None:
        """
        MRU list object.

        Args:
            mru (list, optional): MRU list of keys. Defaults to empty str.
        """
        self._mru = mru
    
    def __set__(self, mru):
        self._mru = mru
        
    def __add__(self, key):
        """
        Adds key.

        Args:
            other (Any): Key.
        Returns:
            MRU_list: _description_
        """
        if isinstance(key, str):
            return MRU_List(key + self._mru)
        else:
            raise TypeError(f'Unsupported operand type for +: {str(type(key))}')
    
    @property
    def mru(self) -> str:
        """
        Returns:
            int:  current key in MRU list.
        """
        return self._mru
    
    @property
    def last(self) -> int:
        """
        Returns:
            int: Last key in MRU list.
        """
        return self.l[-1] if self.l else 'a'
           
    def unpack_values(self, values: dict) -> list:
        """
        Unpacks the value of every key in mru list.

        Args:
            values (dict): values to unpack.

        Returns:
            list: unpacked values.
        """
        mru = self.mru
        return [values[name] for name in mru] if mru else MRU_List.DEFUALT
    
    def __str__(self) -> str:
        """

        Returns:
            str: MRU list.
        """
        return "List: " + self.mru