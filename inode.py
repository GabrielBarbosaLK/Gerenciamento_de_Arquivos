from datetime import datetime

class Inode:
    def __init__(self, id, nome, diretorio_permissao, bloco): # 167
        self.id = id # 4
        self.nome = self.novo_nome(nome) # 42
        self.criador = "Admin" # 5
        self.dono = "Admin" # 5
        data = self.nova_data() # gera data atual
        self.data_criacao = data # 14
        self.data_modificacao = data # 14
        self.permissoes = self.nova_permissao(diretorio_permissao) # 10
        ponteiro_bloco, ponteiro_inode = self.zerar_ponteiro(bloco)
        self.ponteiros = ponteiro_bloco # 4*8 = 32
        self.ponteiros_inode = ponteiro_inode # 4*8 = 32
        self.tamanho = self.novo_tamanho() # 9
    
    def novo_nome(self, nome): # Arrumar - problema - ta feio
        tam = len(nome)
        if tam < 42:
            nome = list(nome)
            for _ in range(42 - tam):
                nome.append('\0')
            nome = ''.join(nome)
        else:
            nome = nome[:42]
        return nome
    
    def novo_tamanho(self): # Arrumar - problema
        if len(self.ponteiros) > 0 or len(self.ponteiros_inode) > 0:
            return '000000000'
        else:
            return '000000000'
    
    def nova_data(self): # data - funcional
        data = datetime.now()
        data = [data.day, data.month, data.year, data.hour, data.minute, data.second]
        data = list(map(str, data))
        for i, j in enumerate(data):
            if len(j) == 1:
                data[i] = '0' + j
        data = ''.join(data)  
        return data

    def nova_permissao(self, diretorio): # errado arruma ai
        if diretorio is True:
            return 'drwxrwxrwx'
        else:
            return '-rwxrwxrwx'
    
    def zerar_ponteiro(self, bloco):
        if bloco is True:
            with open('sistema.txt', 'r+') as file:
                file.seek(0)
                map_bloco = file.read(63658)
                sucesso = False
                for id_bloco, bit_bloco in enumerate(map_bloco):
                    if bit_bloco == '0':
                        file.seek(id_bloco)
                        file.write('1')
                        id_bloco = str(id_bloco)
                        while len(id_bloco) < 4:
                            id_bloco = '0' + id_bloco
                        ponteiro_bloco = id_bloco + '0000' * 7
                        sucesso = True
                        break
                if sucesso is False:
                    print("bugo o jogo")
        else:
            ponteiro_bloco = '0000' * 8    
        ponteiro_inode = '0000' * 8
        return ponteiro_bloco, ponteiro_inode
    
    # interacao apartir daqui #

    def gravar(self): # nao funfa
        dados = f"{self.id+self.nome+self.criador+self.dono+self.tamanho+self.data_criacao+self.data_modificacao+self.permissoes+self.ponteiros+self.ponteiros_inode}"
        return dados
