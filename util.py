# funções utilizadas para executar os comandos
from math import ceil
from time import time
from estruturas import *


def rm(dir_arq, nome_arq, sistema):
    blocos_arq = dir_arq.arquivo(nome_arq).lista_blocos(sistema.fat)
    for bloco in blocos_arq:
        # os blocos dos arquivos que são removidos são marcados no bitmap como
        # livres e tirados da FAT, mas o conteúdo deles não é apagado, então o
        # tamanho do arquivo que representa o sistema de arquivos pode não
        # diminuir quando arquivos são removidos, mas esse arquivo pode ter
        # 100 MB e ainda ter espaço livre; pra saber o tamanho ocupado tem que
        # usar a função calcula_tamanho() do sistema de arquivos.
        sistema.bitmap[bloco] = 1
        del sistema.fat[bloco]

    dir_arq.remove_por_nome(nome_arq)
    dir_arq.acessado = int(time())
    dir_arq.modificado = int(time())


def rmdir(caminho, diretorio, dir_pai, sistema):
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
                rm(diretorio, arq.nome, sistema)
            # diretórios são removidos com chamadas recursivas pro rmdir
            elif isinstance(arq, Diretorio):
                caminho_sub = caminho + '/' + arq.nome
                rmdir(caminho_sub, arq, diretorio, sistema)
        # depois de tudo que tá dentro do diretório, remove ele próprio
        print(caminho)
        dir_pai.arquivos.remove(diretorio)
        dir_pai.acessado = int(time())
        dir_pai.modificado = int(time())


# calcula se a adição de algo novo ao sistema (arquivo e/ou metadados)
# extrapola ou não o limite de 100 MB de tamanho do sistema de arquivos
def extrapola_limite(tamanho_novo, sistema):
    if tamanho_novo + sistema.calcula_tamanho() > 100 * 1024 * 1024:
        return True
    return False


def adiciona_arquivo_vazio(nome_arq, dir_arq, sistema):
    arquivo = Arquivo(None, nome_arq, 0, int(time()), -1)

    tamanho_meta = len(arquivo.metadados()) + 1
    if extrapola_limite(tamanho_meta, sistema):
        print('Limite de 100 MB extrapolado, operação não pode ser feita')
        return False

    dir_arq.adiciona_arquivo(arquivo)
    return True


# lê um arquivo no sistema de arquivos externo (do computador rodando a
# simulação e devolve uma instância de Arquivo com as informações dele
def le_arquivo_externo(nome_arquivo):
    arq_ext = open(nome_arquivo, 'r')
    conteudo = arq_ext.read()
    return conteudo


# aloca um arquivo no sistema considerando que já se tem certeza que ele não
# irá extrapolar o limite de 100 MB
def aloca_arquivo(arquivo, conteudo, sistema):
    tamanho = len(conteudo)

    if tamanho == 0:
        adiciona_arquivo_vazio(arquivo.nome, sistema)

    else:

        num_blocos = ceil(tamanho / 4096)
        espaco_desperdicado = 4096 - tamanho % 4096

        for i in range(num_blocos):

            # pode ser que o último bloco tenha espaço desperdiçado
            if i == num_blocos - 1 and espaco_desperdicado != 0:
                conteudo_bloco = conteudo[i*4096:tamanho] + ' ' * espaco_desperdicado

            else:
                conteudo_bloco = conteudo[i*4096:(i+1)*4096]

            num_bloco_livre = sistema.bitmap.index(1)
            sistema.bitmap[num_bloco_livre] = 0
            if i == 0:
                arquivo.bloco_inicio = num_bloco_livre
            else:
                sistema.fat[num_bloco_anterior] = num_bloco_livre

            # se o bloco já existe (era ocupado por algum arquivo apagado)
            if len(sistema.blocos) >= num_bloco_livre + 1:
                sistema.blocos[num_bloco_livre] = conteudo_bloco

            # se precisamos criar um bloco novo
            else:
                sistema.blocos.append(conteudo_bloco)

            num_bloco_anterior = num_bloco_livre

        sistema.fat[num_bloco_anterior] = -1
