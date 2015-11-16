from os import path
from time import time, ctime
from sistema import *
from util import *

sistema_arquivos = None
sistema_montado = False     # controla se algum sistema já foi montado
blocos_extras_meta = 0      # número de blocos além do inicial guardando
                            # metadados de arquivos/diretórios e FAT

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

            if comandos[1] == '/':
                print('Não é possível remover o diretório raiz')
                continue

            caminho_dir_pai = '/'.join(comandos[1].split('/')[:-1])
            # acha o pai e o diretorio que vai remover
            dir_pai = sistema_arquivos.raiz.acha_diretorio(caminho_dir_pai)
            diretorio = sistema_arquivos.raiz.acha_diretorio(comandos[1])

            rmdir(comandos[1], diretorio, dir_pai, sistema_arquivos, blocos_extras_meta)
            print(sistema_arquivos.bitmap.count(0), sistema_arquivos.bitmap.count(1))

            print('Tempo:', time() - inicio)

        except IndexError:
            print('Especifique o nome do diretório')

    if comandos[0] == 'cat':
        try:
            inicio = time()
            caminho_dir = comandos[1].split('/')
            nome_arq = caminho_dir[-1]              # guarda o nome do arquivo
            caminho_dir = '/'.join(caminho_dir[:-1])
            # acha o diretório onde o arquivo tá
            dir_arq = sistema_arquivos.raiz.acha_diretorio(caminho_dir)
            arquivo = dir_arq.arquivo(nome_arq)
            arquivo.acessado = int(time())
            # tá mostrando só o tamanho do conteúdo do arquivo pra não ficar
            # mostrando os arquivos gigantes de teste inteiros, depois é só
            # tirar esse len() que vai mostrar o conteúdo mesmo
            print(len(arquivo.conteudo(sistema_arquivos.fat, sistema_arquivos.blocos)))

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

            caminho_dir = comandos[1].split('/')
            nome_arq = caminho_dir[-1]
            caminho_dir = '/'.join(caminho_dir[:-1])
            dir_arq = sistema_arquivos.raiz.acha_diretorio(caminho_dir)

            rm(dir_arq, nome_arq, sistema_arquivos, blocos_extras_meta)
            print(sistema_arquivos.bitmap.count(0), sistema_arquivos.bitmap.count(1))

            print('Tempo:', time() - inicio)

        except IndexError:
            print('Especifique o nome do arquivo')

    if comandos[0] == 'ls':
        try:
            inicio = time()

            diretorio = sistema_arquivos.raiz.acha_diretorio(comandos[1])
            diretorio.acessado = int(time())
            for arq in diretorio.arquivos:
                descricao = ''
                # diretórios são representados com um [D] antes do nome
                if isinstance(arq, Diretorio):
                    descricao += '[D] '
                descricao += arq.nome + ' '
                # diretórios não têm tamanho
                if not isinstance(arq, Diretorio):
                    descricao += str(arq.tamanho) + ' '
                descricao += ctime(arq.modificado)
                print(descricao)

            print('Tempo:', time() - inicio)

        except IndexError:
            print('Especifique o nome do diretório')

    if comandos[0] == 'find':
        try:
            inicio = time()
            caminho_dir = comandos[1]
            nome_arq = comandos[2]
            dir_inicio = sistema_arquivos.raiz.acha_diretorio(caminho_dir)
            resultado = dir_inicio.find(nome_arq)

            for arq in resultado:
                if caminho_dir[-1] != '/':
                    print(caminho_dir + '/' + arq)
                else:
                    print(caminho_dir + arq)

            print('Tempo:', time() - inicio)

        except IndexError:
            print('Especifique os nomes do diretório e do arquivo')

    if comandos[0] == 'df':
        print('df')

    if comandos[0] == 'umount':
        sistema_montado = False
