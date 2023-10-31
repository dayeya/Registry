import registry as reg

def main() -> None:
    
    root = reg.Registry(
        reg.winreg.HKEY_CURRENT_USER, 
        sub_key='Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU',
        entry=reg.winreg.KEY_ALL_ACCESS
        )
    
    # Adds Dayeya!, uses __str__ to print history.
    root.add_value(reg.winreg.REG_SZ, 'Dayeya!')
    print(root)
    
    # Deletes Dayeya!, uses __str__ to print history.
    root.add_value('Dayeya!')
    print(root)
    
if __name__ == "__main__":
    main()
