from time import time

while True:

    # Lê entrada
    entrada = input('[ep3]: ')
    comandos = entrada.split(' ')

    if comandos[0] == 'sai':
        break

    # Por enquanto cada comando só olha se os argumentos tão lá
    # e marca o tempo que levou pra executar (vamos usar isso na hora
    # de fazer os testes depois)

    if comandos[0] == 'mount':
        try:
            inicio = time()
            comandos[1]
            print('Tempo:', time() - inicio)
        except IndexError:
            print('Especifique o nome do arquivo')

    if comandos[0] == 'cp':
        try:
            inicio = time()
            comandos[1] + comandos[2]
            print('Tempo:', time() - inicio)
        except IndexError:
            print('Especifique a origem e o destino')

    if comandos[0] == 'mkdir':
        try:
            inicio = time()
            comandos[1]
            print('Tempo:', time() - inicio)
        except IndexError:
            print('Especifique o nome do diretório')

    if comandos[0] == 'rmdir':
        try:
            inicio = time()
            comandos[1]
            print('Tempo:', time() - inicio)
        except IndexError:
            print('Especifique o nome do diretório')

    if comandos[0] == 'cat':
        try:
            inicio = time()
            comandos[1]
            print('Tempo:', time() - inicio)
        except IndexError:
            print('Especifique o nome do arquivo')

    if comandos[0] == 'touch':
        try:
            inicio = time()
            comandos[1]
            print('Tempo:', time() - inicio)
        except IndexError:
            print('Especifique o nome do arquivo')

    if comandos[0] == 'rm':
        try:
            inicio = time()
            comandos[1]
            print('Tempo:', time() - inicio)
        except IndexError:
            print('Especifique o nome do arquivo')

    if comandos[0] == 'ls':
        try:
            inicio = time()
            comandos[1]
            print('Tempo:', time() - inicio)
        except IndexError:
            print('Especifique o nome do diretório')

    if comandos[0] == 'find':
        try:
            inicio = time()
            comandos[1] + comandos[2]
            print('Tempo:', time() - inicio)
        except IndexError:
            print('Especifique os nomes do diretório e do arquivo')

    if comandos[0] == 'df':
        print('df')

    if comandos[0] == 'umount':
        print('umount')
