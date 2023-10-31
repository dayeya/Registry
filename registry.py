from mru import MRU
import winreg

class Registry:
    
    MAX = 26
    DEFAULT = 'a'
    MRU = 'MRUList'
    NO_HISTORY = []    
    SOFTWARE =  r"SOFTWARE\\"
    
    def __init__(self, reg_loc: int, sub_key: str , entry: int) -> None:
        """
        Creats Registry, a more comfortable way to access it.

        Args:
            reg_loc (int): root
            sub_key (str): sub_key
            entry (int): there is access or not to all keys.

        Raises:
            Exception: _description_
        """
        try:
            # Open the CURR USER key.
            self.key = winreg.OpenKeyEx(reg_loc, sub_key, reserved=0, access=entry)
            self.mru_list = MRU()
            
        except OSError as e:
            raise Exception(f'{e}, make sure to provide a correct key!')
    
    def __del__(self) -> None:
        """
        Delets self.
        """
        if self.key:
            winreg.CloseKey(self.key)
    
    def unpack_values(self, values: dict, mru: list) -> list:
        """
        Unpacks the value of every key in mru list.

        Args:
            values (dict): values to unpack.
            mru (list): registry MRU list.

        Returns:
            list: unpacked values.
        """
        return [values[name] for name in mru] if mru else []
    
    def set_mru(self, mru, key, vals, data) -> None:
        """
        Updates vals or mru based on the key.

        Args:
            mru (_type_): MRU list.
            key (_type_): Key for checking correct data structure. 
            vals (_type_): Values of keys.
            data (_type_): data to set MRU / vals with.
        """
        (mru if key == Registry.MRU else vals).__setitem__(key, data)
    
    def history_to_list(self) -> list:
        try:
            
            values = {}
            mru_list = None
            _, key_values, _ = winreg.OpenKey(self.key)

            for idx in range(key_values):
                key_name, data, _ = winreg.EnumValue(self.key, idx)
                self.set_mru(
                    mru=mru_list,
                    key=key_name,
                    vals=values,
                    data=data
                )

            return self.unpack_values(values=values, mru=mru_list)

        except WindowsError as e:
            print(f"Error accessing the Registry: {e}")
            return Registry.NO_HISTORY
        
    def add_value(self, type: int, val: str) -> None:  
        try:

            values = dict([])
            _, key_values, _ = winreg.OpenKey(self.key)

            for idx in range(key_values):
                key_name, data, _ = winreg.EnumValue(self.key, idx)
                
                if key_name == Registry.MRU:
                    # set mru.
                    self.set_mru(
                        mru=self.mru_list,
                        key=key_name,
                        vals=values,
                        data=data
                    )
                    break
        
            key_name = ''
            if len(self.mru_list) == Registry.MAX:
                key_name = self.mru_list.last
                
            elif not self.mru_list:
                key_name = Registry.DEFAULT
                
            else:
                biggest = max(self.mru_list)
                key_name = chr(ord(biggest))
                
            new_mru = key_name + self.mru_list
            
            winreg.SetValueEx(self.key, self.mru_list, 0, type, new_mru)
            winreg.SetValueEx(self.key, key_name, 0, type, val)

        except OSError as e:
            print(f"Error accessing the Registry: {e}")
            return Registry.NO_HISTORY
        
    def remove_value(self, val: str) -> None:
        try:
            
            values = dict([])
            _, key_values, _ = winreg.OpenKey(self.key)

            for idx in range(key_values):
                key_name, data, _ = winreg.EnumValue(self.key, idx)
                
                if key_name == Registry.MRU:
                    # set mru.
                    self.set_mru(
                        mru=self.mru_list,
                        key=key_name,
                        vals=values,
                        data=data
                    )
                    break
        
            mruList = mruList.replace(val, '')
            
            winreg.SetValueEx(self.key, self.mru_list, 0, type, self.mru_list)
            winreg.SetValueEx(self.key, key_name, 0, type, val)

        except OSError as e:
            print(f"Error accessing the Registry: {e}")
            return Registry.NO_HISTORY
        
    def __str__(self) -> str:
        """
        Returns:
            str: History of self. 
        """
        
        return self.history_to_list()
        