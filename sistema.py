from struct import pack, unpack
from time import time
from estruturas import *


# recebe bitmap lido do arquivo que representa o sistema de arquivos e retorna
# lista com ele "descompactado" e do tamanho completo
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


# recebe lista com bitmap completo e "compacta" ele para o formato no
# qual vai ser salvo no arquivo que representa o sistema de arquivos
def bitmap_para_arquivo(bitmap):
    compactado = []
    for i in range(0, len(bitmap), 3):

        # o último bit é "compactado" sozinho
        if i == len(bitmap) - 1:
            compactado += [bitmap[i]]

        # os outros são "compactados" juntando 3 bits
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

    # "empacota" o bitmap nesse formato binário menor
    return pack('B' * 8485, *compactado)


# recebe lista com FAT e converte para formato de informações que ficam
# guardadas no arquivo que representa o sistema de arquivos
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


# lê sistema de arquivos já existente guardado em arquivo no computador e
# retorna tupla com a lista representando o bitmap, o diretório raiz, a lista
# representando a FAT e a lista com os blocos com os conteúdos dos arquivos
def le_sistema(nome_sistema):
    arq_sistema = open(nome_sistema, 'rb')
    # lê bitmap (binário), transforma em decimal, guarda em vetor
    dados_bitmap = arq_sistema.readline()[:8485]
    bitmap = processa_bitmap(dados_bitmap)
    # não precisa mais ler nada em modo binário
    arq_sistema.close()

    arq_sistema = open(nome_sistema, 'r')   # o resto não é binário
    arq_sistema.seek(8486)      # pula o bitmap que já leu antes

    # lê informações sobre o diretório raiz
    info_raiz = arq_sistema.readline().split(' ')

    # cria representação do diretório raiz
    raiz = Diretorio(['', '', '/'] + info_raiz[0:3])
    raiz.modificado = int(info_raiz[0])
    raiz.acessado = int(info_raiz[2])

    # lê arquivos do diretório raiz, cria eles e adiciona ao diretório
    for i in range(3, len(info_raiz), 6):
        arq = Arquivo(info_raiz[i:i+6])
        raiz.adiciona_arquivo(arq)

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

        # lê arquivos do subdiretório, cria eles e adiciona ao diretório
        for i in range(6, len(info_subdir), 6):
            arq = Arquivo(info_subdir[i:i+6])
            subdir.adiciona_arquivo(arq)

        # lê próxima linha, que novamente pode ser subdiretório ou FAT
        info_subdir = arq_sistema.readline().split(' ')

    fat = {}
    # linha atual se trata de informações para montar FAT
    info_fat = info_subdir

    # monta FAT
    tamanho_fat = int(info_fat[0])
    for i in range(1, tamanho_fat):
        if info_fat[i] == '-1':
            continue
        fat[int(info_fat[i])] = int(info_fat[i + 1])

    # depois da FAT, são lidos os blocos com conteúdo dos arquivos
    # se a FAT termina exatamente no final de um bloco, os blocos já
    # foram lidos junto com ela e têm que ser separados
    if info_fat[-1] != '\n':
        blocos_conteudo = info_fat[tamanho_fat:]
    else:
        blocos_conteudo = arq_sistema.read()
    # guarda esses blocos numa lista
    blocos = [blocos_conteudo[0+i:4096+i] for i in range(0, len(blocos_conteudo), 4096)]

    return (bitmap, raiz, fat, blocos)


# recebe um sistema de arquivos em sistema, com o nome nome_sistema, e grava
# ele num arquivo de nome nome_sistema de acordo com o formato usado para
# guardar as informações sobre o sistema de arquivos
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
    if completa_bloco != 0:
        espacos = 4096 - completa_bloco - 1
        arq_sistema.write(b' ' * espacos + b'\n')

    # escreve blocos com o conteúdo dos arquivos
    blocos = ''.join(sistema.blocos)
    arq_sistema.write(bytes(blocos, 'ascii'))
    arq_sistema.close()


class SistemaArquivos:

    '''
    Representação de um sistema de arquivos, com uma lista com o bitmap de
    blocos livres para conteúdo de arquivos, um diretório raiz abaixo do qual
    estão todos os outros diretórios e arquivos, uma lista com a FAT e uma com
    os blocos com o conteúdo dos arquivos. Instâncias podem ser criadas por
    meio da leitura de um arquivo que contém a representação de um sistema já
    existente (nesse caso, o argumento existe é True) ou por meio da criação
    de um sistema novo vazio (nesse caso o argumento existe é None ou ausente)
    '''

    def __init__(self, nome, existe=None):
        if existe is None:
            self.bitmap = [1] * 25453
            self.raiz = Diretorio(None, '/', int(time()), '')
            self.fat = {}
            self.blocos = []
            grava_sistema(nome, self)

        else:
            self.bitmap, self.raiz, self.fat, self.blocos = le_sistema(nome)

    # calcula a quantidade (em bytes) de espaço ocupado no sistema de
    # arquivos, excluindo o espaço que pode estar ocupado em disco mas
    # na verdade é livre (que corresponde a conteúdo de arquivos removidos)
    def calcula_tamanho(self):
        tam_meta = self.espaco_meta()

        tam_blocos_arq = 0
        for num, bloco in enumerate(self.blocos):
            # só conta os blocos que não forem de arquivos removidos
            if self.bitmap[num] == 0:
                tam_blocos_arq += 4096

        return tam_meta + tam_blocos_arq

    # calcula a quantidade (em bytes) de espaço usada pelos bloco que estão
    # sendo usado para guardar bitmap/metadados/FAT
    def espaco_meta(self):

        # 8485 mais o \n no fim
        tam_bitmap = 8486

        # metadados de arquivos e diretórios mais \n no fim
        tam_meta_arq_dir = len(self.raiz.metadados()) + 1
        tam_fat = len(fat_para_arquivo(self.fat))

        # se precisa completar o bloco com espaços em branco
        completa_bloco = (tam_bitmap + tam_meta_arq_dir + tam_fat) % 4096
        espaco_livre = 4096 - completa_bloco

        return tam_bitmap + tam_meta_arq_dir + tam_fat + espaco_livre
