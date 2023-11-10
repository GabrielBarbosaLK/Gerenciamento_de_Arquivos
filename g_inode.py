from inode import Inode

class g_inode:
    def __init__(self): # inodes 7959 | 63658 blocos | 62 ocioso
        self.inode_atual = '0000'
        self.base = 63658+7959
        self.map_inode = 63658

    def dir_atual(self):
        with open('sistema.txt', 'r') as file:
            file.seek(self.base + (int(self.inode_atual) * 167) + 4)
            nome_bruto = file.read(42)
            i = 0
            while i < 42:
                if nome_bruto[i] != '\0':
                    i += 1
                else:
                    break
            return nome_bruto[:i]
    
    def touch(self, nome_arquivo):
        with open('sistema.txt', 'r+') as file:
            file.seek(self.map_inode)
            map_node = file.read(7959)
            sucesso = False
            for id_node, bit_node in enumerate(map_node):
                if bit_node == '0':
                    file.seek(self.map_inode + id_node)
                    file.write('1')
                    id_srt = str(id_node)
                    while len(id_srt) < 4:
                        id_srt = '0' + id_srt
                    node = Inode(id_srt, nome_arquivo, False)
                    sucesso = True
                    break
            if sucesso is True:
                file.seek(self.base + id_node * 167)
                dado = node.gravar()
                file.write(dado)
            else:
                print("Não a Inodes disponiveis")
    
    def rm(self, nome_arquivo):
        with open('sistema.txt', 'r+') as file:
            file.seek(self.map_inode)
            map_node = file.read(7959)
            sucesso = False
            for id_node, bit_node in enumerate(map_node):
                if bit_node == '1':
                    file.seek(self.base + (id_node * 167) + 4)
                    nome = file.read(42)
                    nome = nome.replace('\0','')
                    if nome == nome_arquivo:
                        file.seek(self.map_inode + id_node)
                        file.write('0')
                        sucesso = True
            if sucesso is False:
                print('Nome de arquivo não encontrado')
    
    def echo(self, texto, opcao, nome_arquivo):
        with open('sistema.txt', 'r+') as file:
            file.seek(self.map_inode)
            map_node = file.read(7959)
            sucesso = False
            for id_node, bit_node in enumerate(map_node):
                if bit_node == '0':
                    file.seek(self.map_inode + id_node)
                    file.write('1')
                    id_srt = str(id_node)
                    while len(id_srt) < 4:
                        id_srt = '0' + id_srt
                    node = Inode(id_srt, nome_arquivo, False, True)
                    sucesso = True
                    break
            if sucesso is True:
                file.seek(self.base + id_node * 167)
                dado = node.gravar()
                file.write(dado)
                file.seek(self.base)
                print(file.read(167*3))
            else:
                print("Inodes ou blocos não disponiveis")
