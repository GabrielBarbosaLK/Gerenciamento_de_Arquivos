from g_inode import g_inode

sistema = True
gerenciador = g_inode()
print("Iniciando Sistema...")
print("Terminal Disponivel...")

while sistema:
    dir_atual = gerenciador.dir_atual()

    comando = []
    comando = input(f'root@ENIAC:~{dir_atual}$ ').split(' ')

    match comando[0]:
        # Comandos arquivos
        case "touch": # Pronto - local
            if len(comando) == 2:
                gerenciador.touch(comando[1])
            else:
                print("touch: Operação invalida")
                print("Tente 'touch [file_name]'")
        case "rm": # pronto - local
            if len(comando) == 2:
                gerenciador.rm(comando[1])
            else:
                print("rm: Operação invalida")
                print("Tente 'rm [file_name]'")
        case "echo":
            if len(comando) >= 4 and (comando[-2] == '>' or comando[-2] == '>>'):
                gerenciador.echo(' '.join(comando[1:-2]), comando[-2], comando[-1])
            else:
                print("echo: Operação invalida")
                print("Tente 'echo [string] > [file_name]'")
                print("Ou 'echo [string] >> [file_name]'")
        case "cat":
            print("Ler arquivo")
        case "cp":
            print("Copiar arquivo")
        case "mva":
            print("Renomear/mover arquivo")
        case "lna":
            print("Criar links entre arquivos")
        # Comandos diretorios
        case "mkdir":
            if len(comando) > 1:
                absoluto = comando[-1].split('/')
                caminho, nome = gerenciador.absoluto(absoluto, True)
            if len(comando) == 2:
                gerenciador.mkdir(nome, caminho[-1])
            else:
                print("mkdir: Operação invalida")
                print("Tente 'mkdir [nome_diretorio]'")
        case "rmdir":
            if len(comando) > 1:
                absoluto = comando[-1].split('/')
                caminho, nome = gerenciador.absoluto(absoluto, True)
            if len(comando) == 2:
                gerenciador.rmdir(nome, caminho[-1])
            else:
                print("rmdir: Operação invalida")
                print("Tente 'rmdir [nome_diretorio]'")
        case "ls":
            if len(comando) > 1:
                absoluto = comando[-1].split('/')
                caminho, nome = gerenciador.absoluto(absoluto, False)
            if len(comando) == 2:
                gerenciador.ls(caminho[-1])
            elif len(comando) == 1:
                gerenciador.ls('atual')
            else:
                print("ls: Operação invalida")
                print("Tente 'ls' ou 'ls [caminho]'")
        case "cd":
            if len(comando) > 1:
                absoluto = comando[-1].split('/')
                caminho, nome = gerenciador.absoluto(absoluto, False)
            if len(comando) == 2:
                gerenciador.cd(caminho[-1])
            else:
                print("cd: Operação invalida")
                print("Tente: 'cd [nome_diretorio]'")
        case "mv":
            if len(comando) > 1:
                absoluto1 = comando[-2].split('/')
                absoluto2 = comando[-1].split('/')
                caminho_destino, nome_destino = gerenciador.absoluto(absoluto2, True)
                caminho_origen, nome_origen = gerenciador.absoluto(absoluto1, True)
            if len(comando) == 3:
                gerenciador.mv(caminho_origen[-1], caminho_destino[-1], nome_origen, nome_destino)
            else:
                print("mv: Operação invalida")
                print("Tente: 'mv [diretorio_origen] [destino]")
        case "ln":
            print("Link simbolico")
        # Encerrando
        case "poweroff":
            print("Encerrando sistema...")
            sistema = False
        case _:
            print(f"Comando {comando[0]} não encontrado")
