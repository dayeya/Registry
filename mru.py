
class MRU:
    
    def __init__(self) -> None:
        self._l = []
    
    @property
    def last(self) -> int:
        """
        Returns:
            int: Last key in MRU list.
        """
        return self._l[-1] if self._l else 'a'
