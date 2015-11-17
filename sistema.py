from struct import pack, unpack
from time import time, ctime
from estruturas import *


# recebe bitmap lido do arquivo e retorna lista com ele descompactado e
# completo
def processa_bitmap(bitmap_preliminar):
    # "desempacota" do formato binário e passa pra uma lista
    bitmap_preliminar = [i for i in unpack('B' * 8485, bitmap_preliminar)]
    bitmap = []

    for idx, elm in enumerate(bitmap_preliminar):
        # o último elemento da lista "desempacotada" é 1 bit só mesmo
        if idx == len(bitmap_preliminar) - 1:
            bitmap += [elm]

        # os outros elementos são 3 bits juntos, precisa separar
        else:
            # 000, 001, 010 e 011 foram representados como 0, 1, 10 e 11
            # porque como são números não poderia ter 0s a mais no começo
            if elm == 0:
                bitmap += [0, 0, 0]
            elif elm == 1:
                bitmap += [0, 0, 1]
            elif elm == 10:
                bitmap += [0, 1, 0]
            elif elm == 11:
                bitmap += [0, 1, 1]
            else:
                # 100, 101, 110 e 111 só precisa separar em 3 dígitos cada
                bitmap += list(map(int, str(elm)))

    return bitmap


# recebe lista com bitmap completo e compacta ele para o formato no
# qual vai ser salvo no arquivo
def bitmap_para_arquivo(bitmap):
    compactado = []
    for i in range(0, len(bitmap), 3):

        # o último bit é compactado sozinho
        if i == len(bitmap) - 1:
            compactado += [bitmap[i]]

        # os outros são compactados juntando 3 bits
        else:
            # os que teriam 0s no começo a mais têm que ser transformados
            # nos equivalentes sem os 0s extras
            if bitmap[i:i+3] == [0, 0, 0]:
                compactado += [0]
            elif bitmap[i:i+3] == [0, 0, 1]:
                compactado += [1]
            elif bitmap[i:i+3] == [0, 1, 0]:
                compactado += [10]
            elif bitmap[i:i+3] == [0, 1, 1]:
                compactado += [11]
            # 1,0,0, 1,0,1, 1,1,0 e 1,1,1 só precisam ser juntados
            else:
                compactado += [int(''.join(map(str, bitmap[i:i+3])))]

    # "empacota" o bitmat nesse formato binário menor
    return pack('B' * 8485, *compactado)


# recebe FAT e converte para informações que ficam guardadas no arquivo
# que representa o sistema de arquivos
def fat_para_arquivo(fat):
    inicios = []
    caminhos = []

    # acha os inícios de caminhos
    for num_bloco in fat:
        if num_bloco not in fat.values():
            inicios += [num_bloco]

    # percorre os caminhos e os salva
    for num_bloco in inicios:
        caminhos += [str(num_bloco)]
        prox = fat[num_bloco]
        while prox != -1:
            caminhos += [str(prox)]
            prox = fat[prox]
        caminhos += ['-1']

    # escreve um caminho após o outro com cada número de bloco separado por
    # um espaço em branco
    return ' '.join([str(len(caminhos))] + caminhos)


# lê sistema a partir de arquivo com sistema já existente
def le_sistema(nome_sistema):
    arq_sistema = open(nome_sistema, 'rb')
    # lê bitmap (binário), transforma em decimal, guarda em vetor
    dados_bitmap = arq_sistema.readline()[:8485]
    bitmap = processa_bitmap(dados_bitmap)
    print(bitmap.count(0), 'zeros e', bitmap.count(1), 'uns')
    arq_sistema.close()

    arq_sistema = open(nome_sistema, 'r')   # o resto não é binário
    arq_sistema.seek(8486)      # pula o bitmap que já leu antes

    # lê informações sobre o diretório raiz
    info_raiz = arq_sistema.readline().split(' ')

    # cria representação do diretório raiz
    raiz = Diretorio(['', '', '/'] + info_raiz[0:3])
    raiz.modificado = int(info_raiz[0])
    raiz.acessado = int(info_raiz[2])
    print(raiz.nome, ctime(raiz.acessado), ctime(raiz.modificado), ctime(raiz.criado))

    # lê arquivos do diretório raiz, cria eles e adiciona ao diretório
    for i in range(3, len(info_raiz), 6):
        arq = Arquivo(info_raiz[i:i+6])
        raiz.adiciona_arquivo(arq)

    for arq in raiz.arquivos:
        print(arq.nome, arq.tamanho, ctime(arq.criado), arq.bloco_inicio)

    # próxima linha pode ser info sobre subdiretório ou FAT
    info_subdir = arq_sistema.readline().split(' ')
    while info_subdir[0] == '/':    # a / sinaliza que é info sobre diretório
        caminho_pai = info_subdir[1]
        if caminho_pai == '/':
            pai = raiz
        else:
            # se pai não é raiz, precisamos achá-lo
            pai = raiz.acha_diretorio(caminho_pai)

        # cria subdiretório e o põe no diretório pai
        subdir = Diretorio(info_subdir[0:6])
        pai.adiciona_arquivo(subdir)

        print(subdir.caminho+subdir.nome, ctime(subdir.criado), subdir.arquivos)

        # lê arquivos do subdiretório, cria eles e adiciona ao diretório
        for i in range(6, len(info_subdir), 6):
            arq = Arquivo(info_subdir[i:i+6])
            subdir.adiciona_arquivo(arq)

        for arq in subdir.arquivos:
            print(arq.nome, arq.tamanho, ctime(arq.criado), arq.bloco_inicio)

        # lê próxima linha, que novamente pode ser subdiretório ou FAT
        info_subdir = arq_sistema.readline().split(' ')

    fat = {}
    # linha atual se trata de informações para montar FAT
    info_fat = info_subdir

    # monta FAT
    tamanho_fat = int(info_fat[0])
    print('tamanho do FAT:', tamanho_fat, 'len =', len(info_fat[1:tamanho_fat+1]))
    for i in range(1, tamanho_fat):
        if info_fat[i] == '-1':
            continue
        fat[int(info_fat[i])] = int(info_fat[i + 1])

    print(fat)

    # não é só isso o espaço desperdiçado, vou mexer ainda
    espaco_desperdicado = info_fat.count('')

    # depois da FAT, são lidos os blocos com conteúdo dos arquivos
    # se a FAT termina exatamente no final de um bloco, os blocos já
    # foram lidos junto com ela e têm que ser separados
    if info_fat[-1] != '\n':
        blocos_conteudo = info_fat[tamanho_fat:]
    else:
        blocos_conteudo = arq_sistema.read()
    # guarda esses blocos num vetor
    blocos = [blocos_conteudo[0+i:4096+i] for i in range(0, len(blocos_conteudo), 4096)]

    for arq in raiz.arquivos:
        if isinstance(arq, Arquivo):
            print(arq.nome, len(arq.conteudo(fat, blocos)))

    print('agora, metadados de tudo...:', raiz.metadados())
    return (bitmap, raiz, fat, blocos)


def grava_sistema(nome_sistema, sistema):
    bytes_gravados = 0
    arq_sistema = open(nome_sistema, 'wb')
    # escreve o bitmap
    bitmap = bitmap_para_arquivo(sistema.bitmap)
    bytes_gravados += arq_sistema.write(bitmap)
    bytes_gravados += arq_sistema.write(b'\n')

    # escreve os metadados de arquivos e diretórios
    metadados_arqs_dirs = sistema.raiz.metadados()
    bytes_gravados += arq_sistema.write(bytes(metadados_arqs_dirs, 'ascii'))
    bytes_gravados += arq_sistema.write(b'\n')

    # escreve a FAT
    fat = fat_para_arquivo(sistema.fat)
    bytes_gravados += arq_sistema.write(bytes(fat, 'ascii'))

    # olha se o término da escrita da FAT coincide ou não com o término de um
    # bloco; se sim, os blocos com conteúdos de arquivos virão diretamente em
    # seguida; caso contrário, completa esse bloco com espaços em branco e na
    # última posição uma quebra de linha
    completa_bloco = bytes_gravados % 4096
    print('modulo', bytes_gravados)
    if completa_bloco != 0:
        espacos = 4096 - completa_bloco - 1
        print('espacos', espacos)
        arq_sistema.write(b' ' * espacos + b'\n')

    # escreve blocos com o conteúdo dos arquivos
    blocos = ''.join(sistema.blocos)
    arq_sistema.write(bytes(blocos, 'ascii'))
    arq_sistema.close()


class SistemaArquivos:

    def __init__(self, nome, existe=None):
        if existe is None:
            self.bitmap = [1] * 25453
            self.raiz = Diretorio(None, '/', int(time()), '')
            self.fat = {}
            self.blocos = []
            grava_sistema(nome, self)

        else:
            self.bitmap, self.raiz, self.fat, self.blocos = le_sistema(nome)

        # número de blocos além do inicial guardando metadados de
        # arquivos/diretórios e FAT
        self.blocos_extras_meta = 0

    # calcula o tamanho (em bytes) do sistema de arquivos
    def calcula_tamanho(self):
        # 8485 mais o /n no fim
        tam_bitmap = 8486
        # completa um bloco mais o número de blocos extras
        tam_metadados_fat = 3802 + 4096 * self.blocos_extras_meta

        tam_blocos_arq = 0
        for num, bloco in enumerate(self.blocos):
            # só conta os blocos que não forem de arquivos removidos
            if self.bitmap[num] == 0:
                tam_blocos_arq += 4096

        return tam_bitmap + tam_metadados_fat + tam_blocos_arq
