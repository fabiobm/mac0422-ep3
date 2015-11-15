from time import time
from os import path
from sistema import *

sistema_montado = False     # controla se algum sistema já foi montado

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
        if sistema_montado:
            print('Um sistema já está montado, desmonte ele para montar outro')
            continue

        try:
            inicio = time()
            if path.exists(comandos[1]):
                sistema_arquivos = SistemaArquivos(comandos[1], True)
            else:
                sistema_arquivos = SistemaArquivos(comandos[1])

            sistema_montado = True

            print('bitmap:', sistema_arquivos.bitmap.count(0), sistema_arquivos.bitmap.count(1))
            print('diretoriosmeta:', sistema_arquivos.raiz.metadados())
            print('fat:', sistema_arquivos.fat)
            print('blocos:', [len(i) for i in sistema_arquivos.blocos], len(sistema_arquivos.blocos))
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
        sistema_montado = False
