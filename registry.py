from typing import Any
import winreg
from mru import MRU_List


class Registry:

    DEFAULT: str = 'a'
    MRU: str = 'MRUList'
    NO_HISTORY: list = []    
    SOFTWARE: str =  r"SOFTWARE\\"
    
    def __init__(self, reg_loc: int, sub_key: str , entry: int) -> None:
        """
        Creats Registry, a more comfortable way to access it.

        Args:
            reg_loc (int): root
            sub_key (str): sub_key
            entry (int): there is access or not to all keys.
        Raises:
            Exception: OSError
        """
        try:
            # Open the CURR USER key.
            self._mru_list = MRU_List()
            self._key = winreg.OpenKeyEx(reg_loc, sub_key, reserved=0, access=entry)
            
        except OSError as e:
            raise Exception(f'{e}, make sure to provide a correct key!')
    
    @property
    def mru_list(self) -> MRU_List:
        """
        Getter for _l

        Returns:
            MRU_List: current MRU_List state.
        """
        return self._mru_list
    
    def __del__(self) -> None:
        """
        Delets self.
        """
        if self._key:
            winreg.CloseKey(self._key)
    
    def set_mru(self, data: str) -> None:
        """
        Sets _mru_list.

        Args:
            data (Any): data to set MRU / vals with.
        """
        self._mru_list = MRU_List(data)
    
    def history_to_list(self) -> list:
        """
        Tracks the history of the regisrty.

        Returns:
            list: 
        """
        try:
            values = dict([])
            _, key_values, _ = winreg.QueryInfoKey(self._key)

            for idx in range(key_values):
                key_name, data, _ = winreg.EnumValue(self._key, idx)
                mru = key_name == Registry.MRU
                if mru:
                    self.set_mru(data)
                else:
                    values[key_name] = data

            return self._mru_list.unpack_values(values)

        except WindowsError as e:
            print(f"Error accessing the Registry: {e}")
            return Registry.NO_HISTORY
        
    def add_value(self, type: int, val: str) -> None:
        """
        Addsa val as type 'type' to the registry history.
        
        Args:
            val (str): value.
        """  
        try:
            values = dict([])
            _, key_values, _ = winreg.QueryInfoKey(self._key)

            for idx in range(key_values):
                key_name, data, _ = winreg.EnumValue(self._key, idx)
                if key_name == Registry.MRU:
                    self.set_mru(data)
                    break
        
            key_name = ''
            if len(self._mru_list.mru) == MRU_List.MAX_LEN:
                key_name = self._mru_list.last
                
            elif not self._mru_list:
                key_name = Registry.DEFAULT
                
            else:
                biggest = max(self._mru_list.mru)
                key_name = chr(ord(biggest))
                
            new_list: MRU_List = self._mru_list + key_name
            winreg.SetValueEx(self._key, Registry.MRU, 0, type, new_list.mru)
            winreg.SetValueEx(self._key, key_name, 0, type, val)

        except OSError as e:
            raise Exception(f"Error accessing the Registry: {e}")
        
    def remove_value(self, val: str) -> None:
        """
        Removes val from the registry history.
        
        Args:
            val (str): value.
        """
        try:
            values = dict([])
            _, key_values, _ = winreg.QueryInfoKey(self._key)

            for idx in range(key_values):
                key_name, data, _ = winreg.EnumValue(self._key, idx)
                if key_name == Registry.MRU:
                    self.set_mru(data)
                    break
        
            new_list: MRU_List = MRU_List(self._mru_list.mru.replace(val, ''))
            winreg.SetValueEx(self._key, Registry.MRU, 0, type, new_list.mru)
            winreg.SetValueEx(self._key, key_name, 0, type, val)

        except OSError as e:
            raise Exception(f"Error accessing the Registry: {e}")
        
    def __str__(self) -> str:
        """
        Returns:
            str: History of self. 
        """
        req_history = self.history_to_list()
        return req_history
        
