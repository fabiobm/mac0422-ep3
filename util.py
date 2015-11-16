# funções utilizadas para executar os comandos
from time import time
from estruturas import *


def rm(dir_arq, nome_arq, sistema_arquivos, blocos_extras_meta):
    blocos_arq = dir_arq.arquivo(nome_arq).lista_blocos(sistema_arquivos.fat)
    for i in blocos_arq:
        sistema_arquivos.bitmap[i+blocos_extras_meta] = 1

    dir_arq.remove_por_nome(nome_arq)
    dir_arq.acessado = int(time())
    dir_arq.modificado = int(time())


def rmdir(caminho, diretorio, dir_pai, sistema_arquivos, blocos_extras_meta):
    if diretorio.arquivos == []:
        if caminho[-1] == '/':
            caminho = caminho[:-1]
        print(caminho)
        dir_pai.arquivos.remove(diretorio)
        dir_pai.acessado = int(time())
        dir_pai.modificado = int(time())

    else:
        for arq in diretorio.arquivos[:]:
            if isinstance(arq, Arquivo):
                print(caminho + '/' + arq.nome)
                rm(diretorio, arq.nome, sistema_arquivos, blocos_extras_meta)
            elif isinstance(arq, Diretorio):
                caminho_sub = caminho + '/' + arq.nome
                rmdir(caminho_sub, arq, diretorio, sistema_arquivos, blocos_extras_meta)
        print(caminho)
        dir_pai.arquivos.remove(diretorio)
        dir_pai.acessado = int(time())
        dir_pai.modificado = int(time())
