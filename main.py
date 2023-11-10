from g_inode import g_inode

sistema = True
print("Iniciando Sistema...")
print("Terminal Disponivel...")

while sistema:
    gerenciador = g_inode()
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
        case "mv":
            print("Renomear/mover arquivo")
        case "ln":
            print("Criar links entre arquivos")
        # Comandos diretorios
        case "mkdir":
            print("Criar diretorio")
        case "rmdir":
            print("Remover diretorio")
        case "ls":
            print("Listar o conteudo de um diretorio")
        case "cd":
            print("Trocar de diretorio")
        case "ln":
            print("Criar links entre diretorio")
        # Encerrando
        case "poweroff":
            print("Encerrando sistema...")
            sistema = False
        case _:
            print(f"Comando {comando[0]} não encontrado")
