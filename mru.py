
class MRU:
    
    def __init__(self) -> None:
        self.l = []
    
    @property
    def last(self) -> int:
        """
        Returns:
            int: Last key in MRU list.
        """
        return self.l[-1] if self.l else 'a'