import registry as reg

def main() -> None:
    
    root = reg.Registry(
        reg.winreg.HKEY_CURRENT_USER, 
        sub_key='Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU',
        entry=reg.winreg.KEY_ALL_ACCESS
        )
    
    # Adds Dayeya!
    root.add_value(reg.winreg.REG_SZ, 'Dayeya!')
    print(root.history_to_list())
    
    # Deletes Dayeya!
    root.remove_value('Dayeya!')
    print(root.history_to_list())
    
if __name__ == "__main__":
    main()
