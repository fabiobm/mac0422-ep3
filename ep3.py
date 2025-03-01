# Arquivo principal, é o que deve ser executado

from os import path
from time import time, ctime
from sistema import *
from util import *

sistema_arquivos = None
nome_sistema = ''
sistema_montado = False     # controla se algum sistema já foi montado

while True:

    # Lê entrada
    entrada = input('[ep3]: ')
    comandos = entrada.split(' ')

    if comandos[0] == 'sai':
        break

    if comandos[0] == 'mount':
        if sistema_montado:
            print(nome_sistema, 'já está montado, desmonte ele para montar outro')
            continue

        try:
            nome_sistema = comandos[1]
            if path.exists(comandos[1]):
                sistema_arquivos = SistemaArquivos(comandos[1], True)
            else:
                sistema_arquivos = SistemaArquivos(comandos[1])

            sistema_montado = True

        except IndexError:
            print('Especifique o nome do arquivo')

    elif sistema_montado:
        if comandos[0] == 'cp':
            try:

                caminho = comandos[2].split('/')
                nome_arq = caminho[-1]
                conteudo = le_arquivo_externo(comandos[1])
                arquivo = Arquivo(None, nome_arq, len(conteudo), int(time()), -1)

                tamanho_arq = arquivo.tamanho + len(arquivo.metadados()) + 1
                if extrapola_limite(tamanho_arq, sistema_arquivos):
                    print('Limite de 100 MB extrapolado, operação não pode ser feita')
                    continue

                aloca_arquivo(arquivo, conteudo, sistema_arquivos)

                caminho_dir = '/'.join(caminho[:-1])
                diretorio = sistema_arquivos.raiz.acha_diretorio(caminho_dir)
                diretorio.adiciona_arquivo(arquivo)
                diretorio.acessado = int(time())
                diretorio.modificado = int(time())

                grava_sistema(nome_sistema, sistema_arquivos)

            except IndexError:
                print('Especifique a origem e o destino')

        if comandos[0] == 'mkdir':
            try:

                caminho_dir = comandos[1].split('/')
                nome_dir = caminho_dir[-1]
                caminho_dir_pai = '/'.join(caminho_dir[:-1])

                # tira / extra no final se tiver
                if len(caminho_dir_pai) > 1 and caminho_dir_pai[-1] == '/':
                    caminho_dir_pai = caminho_dir_pai[:-1]

                dir_pai = sistema_arquivos.raiz.acha_diretorio(caminho_dir_pai)
                diretorio = Diretorio(None, nome_dir, int(time()), caminho_dir_pai)

                tamanho_meta = len(diretorio.metadados()) + 1
                if extrapola_limite(tamanho_meta, sistema_arquivos):
                    print('Limite de 100 MB extrapolado, operação não pode ser feita')
                    continue

                dir_pai.adiciona_arquivo(diretorio)
                dir_pai.acessado = int(time())
                dir_pai.modificado = int(time())

                grava_sistema(nome_sistema, sistema_arquivos)

            except IndexError:
                print('Especifique o nome do diretório')

        if comandos[0] == 'rmdir':
            try:

                if comandos[1] == '/':
                    print('Não é possível remover o diretório raiz')
                    continue

                caminho_dir_pai = '/'.join(comandos[1].split('/')[:-1])
                # acha o pai e o diretorio que vai remover
                dir_pai = sistema_arquivos.raiz.acha_diretorio(caminho_dir_pai)
                diretorio = sistema_arquivos.raiz.acha_diretorio(comandos[1])

                rmdir(comandos[1], diretorio, dir_pai, sistema_arquivos)

                grava_sistema(nome_sistema, sistema_arquivos)

            except IndexError:
                print('Especifique o nome do diretório')

        if comandos[0] == 'cat':
            try:
                caminho_dir = comandos[1].split('/')
                nome_arq = caminho_dir[-1]              # guarda o nome do arquivo
                caminho_dir = '/'.join(caminho_dir[:-1])
                # acha o diretório onde o arquivo tá
                dir_arq = sistema_arquivos.raiz.acha_diretorio(caminho_dir)
                arquivo = dir_arq.arquivo(nome_arq)
                arquivo.acessado = int(time())

                print(arquivo.conteudo(sistema_arquivos.fat, sistema_arquivos.blocos))
                grava_sistema(nome_sistema, sistema_arquivos)

            except IndexError:
                print('Especifique o nome do arquivo')

        if comandos[0] == 'touch':
            try:
                caminho_dir = comandos[1].split('/')
                nome_arq = caminho_dir[-1]              # guarda o nome do arquivo
                caminho_dir = '/'.join(caminho_dir[:-1])
                # acha o diretório onde o arquivo tá
                dir_arq = sistema_arquivos.raiz.acha_diretorio(caminho_dir)
                arquivo = dir_arq.arquivo(nome_arq)
                if arquivo is not None:
                    arquivo.acessado = int(time())

                else:
                    if not adiciona_arquivo_vazio(nome_arq, dir_arq, sistema_arquivos):
                        continue    # retorna False se extrapola limite de 100 MB

                dir_arq.acessado = int(time())
                dir_arq.modificado = int(time())
                grava_sistema(nome_sistema, sistema_arquivos)

            except IndexError:
                print('Especifique o nome do arquivo')

        if comandos[0] == 'rm':
            try:

                caminho_dir = comandos[1].split('/')
                nome_arq = caminho_dir[-1]
                caminho_dir = '/'.join(caminho_dir[:-1])
                dir_arq = sistema_arquivos.raiz.acha_diretorio(caminho_dir)

                rm(dir_arq, nome_arq, sistema_arquivos)

                grava_sistema(nome_sistema, sistema_arquivos)

            except IndexError:
                print('Especifique o nome do arquivo')

        if comandos[0] == 'ls':
            try:

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

                grava_sistema(nome_sistema, sistema_arquivos)

            except IndexError:
                print('Especifique o nome do diretório')

        if comandos[0] == 'find':
            try:
                caminho_dir = comandos[1]
                nome_arq = comandos[2]
                dir_inicio = sistema_arquivos.raiz.acha_diretorio(caminho_dir)
                resultado = dir_inicio.find(nome_arq)

                for arq in resultado:
                    if caminho_dir[-1] != '/':
                        print(caminho_dir + '/' + arq)
                    else:
                        print(caminho_dir + arq)

            except IndexError:
                print('Especifique os nomes do diretório e do arquivo')

        if comandos[0] == 'df':
            ndirs_arqs = sistema_arquivos.raiz.count()
            print(ndirs_arqs[0], 'diretório(s)')
            print(ndirs_arqs[1], 'arquivo(s)')
            espaco_livre = 100 * 1024 * 1024 - sistema_arquivos.calcula_tamanho()
            print('Espaço livre:', espaco_livre, 'byte(s)')
            espaco_desperdicado = sistema_arquivos.raiz.espaco_desperdicado()
            print('Espaço desperdiçado:', espaco_desperdicado, 'byte(s)')

        if comandos[0] == 'umount':
            sistema_montado = False

    else:
        print('Impossível executar os comandos sem montar um sistema')
