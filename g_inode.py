from inode import Inode

class g_inode:
    def __init__(self): # inodes 7959 | 63658 blocos | 62 ocioso
        self.inode_atual = '0000'
        self.base = 63658+7959
        self.map_inode = 63658
        self.max_inode = 7959

    def dir_atual(self):
        with open('sistema.txt', 'r') as file:
            nome_completo = []
            lendo = True
            node_auxiliar = self.inode_atual

            while lendo:
                file.seek(self.base + (int(node_auxiliar) * 167) + 4)
                nome_bruto = file.read(42)
                i = 0
                while i < 42:
                    if nome_bruto[i] != '\0':
                        i += 1
                    else:
                        break
                nome_completo.append(nome_bruto[:i])

                file.seek(self.base + int(node_auxiliar) * 167 + 135)
                ponteiro_bruto = file.read(32)
                ponteiro = []
                i = 0
                id = 4
                while i < 8:
                    ponteiro.append(ponteiro_bruto[id * i : id * (i + 1)])
                    i += 1
                
                if int(ponteiro[1]) != 0:
                    node_auxiliar = ponteiro[1]
                else:
                    lendo = False
            
            if len(nome_completo) > 1:
                nome_completo.reverse()
                nome_completo = "/".join(nome_completo)
                nome_completo = "/" + nome_completo
            elif nome_completo[0] != "/":
                nome_completo = "/" + nome_completo[0]
            else:
                nome_completo = nome_completo[0]

            return nome_completo
    
    # Arquivos -- Aqui #
    
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
                    node = Inode(id_srt, nome_arquivo, False, False)
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
    
    # Diretorios -- Aqui #

    def mkdir(self, nome_diretorio, caminho):
        if not self._existe_diretorio(nome_diretorio, caminho):
            file = open('sistema.txt', 'r+')
            novo_id = self._novo_inode_diretorio(nome_diretorio, file, caminho)
            erro = False
            erro_caminho = False
            if caminho == 'erro':
                print("Nome de diretorios não encontrados")
                erro_caminho = True
            elif caminho != 'erro':
                node_auxiliar = caminho
            if novo_id is None:
                erro = True

            auxiliar = True
            while auxiliar and not erro and not erro_caminho:
                node_atual = node_auxiliar
                grava = True
                file.seek(self.base + int(node_atual) * 167 + 135)
                ponteiro_bruto = file.read(32)
                ponteiro = []
                i = 0
                id = 4
                while i < 8:
                    ponteiro.append(ponteiro_bruto[id * i : id * (i + 1)])
                    i += 1

                for indice, elem in enumerate(ponteiro):
                    if indice > 1:

                        if indice == 7 and int(elem) == 0:
                            node_auxiliar = self._novo_inode_diretorio("Inode_Auxiliar", file, caminho)
                            if node_auxiliar is None:
                                erro = True
                                grava = False
                                break
                            ponteiro[indice] = node_auxiliar
                        elif indice != 7 and int(elem) == 0:
                                ponteiro[indice] = novo_id
                                auxiliar = False
                                break
                        elif indice == 7 and int(elem) != 0:
                            node_auxiliar = elem
                            grava = False
                
                if grava:
                    ponteiro_bruto = "".join(ponteiro)
                    file.seek(self.base + int(node_atual) * 167 + 135)
                    file.write(ponteiro_bruto)

            if erro:
                print("Não a Inodes disponiveis")
            
            file.close()

    def rmdir(self, nome_diretorio, caminho):
        with open('sistema.txt', 'r+') as file:
            lendo = True
            vazio = True
            node_atual = caminho
            while lendo:
                file.seek(self.base + int(node_atual) * 167 + 135)
                ponteiro_bruto = file.read(32)
                ponteiro = []
                i = 0
                id = 4
                while i < 8:
                    ponteiro.append(ponteiro_bruto[id * i : id * (i + 1)])
                    i += 1
                
                sucesso = False
                for id, i in enumerate(ponteiro):
                    if id > 1:
                        if int(i) != 0 and id != 7:
                            file.seek(self.base + (int(i) * 167) + 4)
                            nome = file.read(42)
                            nome = nome.replace('\0','')
                            if nome == nome_diretorio:
                                file.seek(self.base + (int(i) * 167) + 93)
                                diretorio = file.read(1)
                                if diretorio == 'd':
                                    for iii in ponteiro[2:]:
                                        if iii != '0000':
                                            sucesso = True
                                            lendo = False
                                            print("Este diretorio nao esta vazio e nao pode ser removido")
                                            vazio = False
                                    
                                    if vazio:
                                        sucesso = True
                                        lendo = False
                                        file.seek(self.map_inode + int(i))
                                        file.write('0')
                                        ponteiro[id] = '0000'
                                        ponteiro_bruto = "".join(ponteiro)
                                        file.seek(self.base + int(node_atual) * 167 + 135)
                                        file.write(ponteiro_bruto)
                                        break
                        elif id == 7 and int(i) != 0:
                            node_atual = i
                        elif id == 7 and int(i) == 0:
                            lendo = False

            if not sucesso:
                print('Nome do diretorio não encontrado')
    
    def ls(self, caminho):
        with open('sistema.txt', 'r+') as file:
            lendo = True
            if caminho == 'atual':
                node_atual = self.inode_atual
            elif caminho is None:
                print("Nome de diretorio nao encontrado")
                lendo = False
            else:
                node_atual = caminho
            
            while lendo:
                file.seek(self.base + int(node_atual) * 167 + 135)
                ponteiro_bruto = file.read(32)
                ponteiro = []
                i = 0
                id = 4
                while i < 8:
                    ponteiro.append(ponteiro_bruto[id * i : id * (i + 1)])
                    i += 1
                
                for id, i in enumerate(ponteiro):
                    if id > 1:
                        if int(i) != 0 and id != 7:
                            file.seek(self.base + (int(i) * 167) + 4)
                            nome = file.read(42)
                            nome = nome.replace('\0','')
                            print(nome)
                        elif id == 7 and int(i) != 0:
                            node_atual = i
                        elif id == 7 and int(i) == 0:
                            lendo = False
    
    def cd(self, caminho):
        if caminho is None:
            print("Nome de Diretorio não encontrado")
        else:
            self.inode_atual = caminho
    
    def mv(self, caminho_origen, caminho_destino, nome_origen, nome_destino):

        if caminho_origen == 'erro':
            print("Nome de diretorio nao encontrado")
        
        if not self._existe_diretorio(nome_destino, caminho_destino):
            origem = False
            
            with open('sistema.txt', 'r+') as file:
                lendo = True
                node_atual = caminho_origen
                while lendo:
                    file.seek(self.base + int(node_atual) * 167 + 135)
                    ponteiro_bruto = file.read(32)
                    ponteiro = []
                    i = 0
                    id = 4
                    while i < 8:
                        ponteiro.append(ponteiro_bruto[id * i : id * (i + 1)])
                        i += 1

                    sucesso = False
                    for id, i in enumerate(ponteiro):
                        if id > 1:
                            if int(i) != 0 and id != 7:
                                file.seek(self.base + (int(i) * 167) + 4)
                                nome = file.read(42)
                                nome = nome.replace('\0','')
                                if nome == nome_origen:
                                    file.seek(self.base + (int(i) * 167) + 93)
                                    diretorio = file.read(1)
                                    if diretorio == 'd':
                                        if not origem:
                                            while len(nome_destino) < 42:
                                                nome_destino += '\0'
                                            file.seek(self.base + (int(i) * 167) + 4)
                                            file.write(nome_destino)
                                            ponteiro[id] = '0000'
                                            ponteiro_bruto = "".join(ponteiro)
                                            file.seek(self.base + int(node_atual) * 167 + 135)
                                            file.write(ponteiro_bruto)
                                            node_atual = caminho_destino
                                            destino = i
                                            origem = True
                                            lendo = False
                                        break
                            elif id == 7 and int(i) != 0:
                                node_atual = i
                            elif id == 7 and int(i) == 0:
                                lendo = False
        # destino #

                erro = False
                auxiliar = True
                node_auxiliar = node_atual
                while auxiliar:
                    node_atual = node_auxiliar
                    grava = True
                    file.seek(self.base + int(node_atual) * 167 + 135)
                    ponteiro_bruto = file.read(32)
                    ponteiro = []
                    i = 0
                    id = 4
                    while i < 8:
                        ponteiro.append(ponteiro_bruto[id * i : id * (i + 1)])
                        i += 1

                    for indice, elem in enumerate(ponteiro):
                        if indice > 1:

                            if indice == 7 and int(elem) == 0:
                                node_auxiliar = self._novo_inode_diretorio("Inode_Auxiliar", file, caminho)
                                if node_auxiliar is None:
                                    erro = True
                                    grava = False
                                    break
                                ponteiro[indice] = node_auxiliar
                            elif indice != 7 and int(elem) == 0:
                                    ponteiro[indice] = destino
                                    auxiliar = False
                                    break
                            elif indice == 7 and int(elem) != 0:
                                node_auxiliar = elem
                                grava = False
                    
                    if grava:
                        ponteiro_bruto = "".join(ponteiro)
                        file.seek(self.base + int(node_atual) * 167 + 135)
                        file.write(ponteiro_bruto)

                if erro:
                    print("Não a Inodes disponiveis")
         
    def _novo_inode_diretorio(self, nome, file, caminho):
        file.seek(self.map_inode)
        map_node = file.read(self.max_inode)
        sucesso = False
        for id_node, bit_node in enumerate(map_node):
            if bit_node == '0':
                file.seek(self.map_inode + id_node)
                file.write('1')
                id_str = str(id_node)
                while len(id_str) < 4:
                    id_str = '0' + id_str
                node = Inode(id_str, nome, True, False)
                sucesso = True
                break
        
        if sucesso:
            file.seek(self.base + id_node * 167)
            dado = node.gravar()
            file.write(dado)

            file.seek(self.base + int(id_node) * 167 + 135)
            ponteiro_bruto = file.read(32)
            ponteiro = []
            i = 0
            id = 4
            while i < 8:
                ponteiro.append(ponteiro_bruto[id * i : id * (i + 1)])
                i += 1
            
            ponteiro[0] = id_str
            ponteiro[1] = caminho

            ponteiro_bruto = "".join(ponteiro)
            file.seek(self.base + int(id_node) * 167 + 135)
            file.write(ponteiro_bruto)

            return id_str
        else:
            print("Não a Inodes disponiveis")
            return None
    
    def absoluto(self, caminho, criar):
        with open('sistema.txt', 'r+') as file:
            lendo = True
            node_destino = []
            node_destino.append(self.inode_atual)
            absoluto = True
            atual = 0

            if len(caminho) == 2:
                if caminho[0] == '' and caminho[1] == '':
                    node_destino.append('0000')
                    sucesso = True
                    absoluto = False
            if caminho[0] == '':
                node_destino.append('0000')
                atual += 1
            
            if len(caminho) == 1 and criar:
                return node_destino, caminho[-1]

            if absoluto:
                while lendo:
                    especial = False
                    file.seek(self.base + int(node_destino[atual]) * 167 + 135)
                    ponteiro_bruto = file.read(32)
                    ponteiro = []
                    i = 0
                    id = 4
                    while i < 8:
                        ponteiro.append(ponteiro_bruto[id * i : id * (i + 1)])
                        i += 1

                    sucesso = False
                    if caminho[atual] == '.':
                        node_destino.append(ponteiro[0])
                        especial = True
                        if caminho[atual] == caminho[-1] and atual == len(caminho) - 1:
                            sucesso = True
                            lendo = False 
                        elif caminho[-2] == caminho[atual] and criar and atual ==  len(caminho) - 2:
                            sucesso = True
                            lendo = False

                    elif caminho[atual] == '..':
                        node_destino.append(ponteiro[1])
                        especial = True
                        if caminho[atual] == caminho[-1] and atual == len(caminho) - 1:
                            sucesso = True
                            lendo = False 
                        elif caminho[-2] == caminho[atual] and criar and atual == len(caminho) - 2:
                            sucesso = True
                            lendo = False

                    if lendo and not especial:
                        for id, i in enumerate(ponteiro):
                            if int(i) != 0 and id != 7:
                                file.seek(self.base + (int(i) * 167) + 4)
                                nome = file.read(42)
                                nome = nome.replace('\0','')
                                if nome == caminho[atual]:
                                    file.seek(self.base + (int(i) * 167) + 93)
                                    diretorio = file.read(1)
                                    if diretorio == 'd':
                                        node_destino.append(i)
                                        if nome == caminho[-1]:
                                            sucesso = True
                                            lendo = False 
                                        elif caminho[-2] == nome and criar:
                                            sucesso = True
                                            lendo = False
                                        break
                            elif id == 7 and int(i) != 0:
                                node_destino.append(i)
                            elif id == 7 and int(i) == 0:
                                lendo = False
                    
                    atual += 1

            if sucesso:
                return node_destino, caminho[-1]
            else:
                return [None], None
    
    def _existe_diretorio(self, nome_diretorio, caminho):
        with open('sistema.txt', 'r+') as file:
            lendo = True
            node_atual = caminho
            while lendo:
                file.seek(self.base + int(node_atual) * 167 + 135)
                ponteiro_bruto = file.read(32)
                ponteiro = []
                i = 0
                id = 4
                while i < 8:
                    ponteiro.append(ponteiro_bruto[id * i : id * (i + 1)])
                    i += 1
                
                sucesso = False
                for id, i in enumerate(ponteiro):
                    if id > 1:
                        if int(i) != 0 and id != 7:
                            file.seek(self.base + (int(i) * 167) + 4)
                            nome = file.read(42)
                            nome = nome.replace('\0','')
                            if nome == nome_diretorio:
                                file.seek(self.base + (int(i) * 167) + 93)
                                diretorio = file.read(1)
                                if diretorio == 'd':
                                    sucesso = True
                                    lendo = False
                                    break
                        elif id == 7 and int(i) != 0:
                            node_atual = i
                        elif id == 7 and int(i) == 0:
                            lendo = False

            if sucesso:
                print('Nome do diretorio ja existe')
                return True
            else:
                return False