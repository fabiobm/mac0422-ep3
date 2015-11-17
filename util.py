# funções utilizadas para executar os comandos
from time import time
from estruturas import *


def rm(dir_arq, nome_arq, sistema_arquivos):
    blocos_arq = dir_arq.arquivo(nome_arq).lista_blocos(sistema_arquivos.fat)
    for bloco in blocos_arq:
        # os blocos dos arquivos estão sempre depois dos blocos usados pra
        # guardar os metadados e a FAT, então tem que checar se tá usando
        # blocos a mais pros metadados (a mais em relação ao bloco que vai ser
        # usado com certeza). os blocos dos arquivos que são removidos são
        # marcados no bitmap como livres e tirados da FAT, mas o conteúdo deles
        # não é apagado, então o tamanho do arquivo que representa o sistema de
        # arquivos pode não diminuir quando arquivos são removidos, mas esse
        # arquivo pode ter 100 MB e ainda ter espaço livre; pra saber o tamanho
        # ocupado tem que usar a função calcula_tamanho() do sistema de arquivos.
        sistema_arquivos.bitmap[bloco+sistema_arquivos.blocos_extras_meta] = 1
        del sistema_arquivos.fat[bloco]

    dir_arq.remove_por_nome(nome_arq)
    dir_arq.acessado = int(time())
    dir_arq.modificado = int(time())


def rmdir(caminho, diretorio, dir_pai, sistema_arquivos):
    # se tá vazio, remove direto
    if diretorio.arquivos == []:
        if caminho[-1] == '/':
            caminho = caminho[:-1]
        print(caminho)
        dir_pai.arquivos.remove(diretorio)
        dir_pai.acessado = int(time())
        dir_pai.modificado = int(time())

    # se não tá vazio tem que remover tudo que tem dentro antes
    else:
        # itera sobre uma cópia pra poder remover elementos do original
        for arq in diretorio.arquivos[:]:
            # arquivos são removidos pelo rm como se tivesse chamado o rm
            if isinstance(arq, Arquivo):
                print(caminho + '/' + arq.nome)
                rm(diretorio, arq.nome, sistema_arquivos)
            # diretórios são removidos com chamadas recursivas pro rmdir
            elif isinstance(arq, Diretorio):
                caminho_sub = caminho + '/' + arq.nome
                rmdir(caminho_sub, arq, diretorio, sistema_arquivos)
        # depois de tudo que tá dentro do diretório, remove ele próprio
        print(caminho)
        dir_pai.arquivos.remove(diretorio)
        dir_pai.acessado = int(time())
        dir_pai.modificado = int(time())
