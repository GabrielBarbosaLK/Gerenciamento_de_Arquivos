from datetime import datetime
from inode import Inode

def formatar():
    print("Formatando sistema aguarde...")
    with open('sistema.txt', 'r+') as file:
        for i in range(63658+7959):
            file.seek(i)
            file.write('0')
            pc = (i/(63658+7959))
            print(f"[{'#'*int(10*pc)}{' '*(1+(int(10-10*pc)))}] - {(pc*100):,.2f} % ", end='\r')
        print(f"[{'#'*10}] ")
        file.seek(63658)
        file.write('1')
        file.seek(63658+7959)
        node = Inode('0000', '/', True)
        file.write(node.gravar())
    print("Sistema formatado...")

formatar()