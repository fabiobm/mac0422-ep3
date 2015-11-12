from struct import *
from time import *
from estruturas import *


def processa_bitmap(bitmap_preliminar):
    bitmap = []

    for idx, elm in enumerate(bitmap_preliminar):
        if idx == len(bitmap_preliminar) - 1:
            bitmap += [elm]
        else:
            if elm == 0:
                bitmap += [0, 0, 0]
            elif elm == 1:
                bitmap += [0, 0, 1]
            elif elm == 10:
                bitmap += [0, 1, 0]
            elif elm == 11:
                bitmap += [0, 1, 1]
            else:
                bitmap += list(map(int, str(elm)))

    return bitmap


# monta sistema a partir de arquivo com sistema já existente
def monta_sistema(nome_sistema):
    arq_sistema = open(nome_sistema, 'rb')
    # lê bitmap (binário), transforma em decimal, guarda em vetor
    dados_bitmap = [i for i in unpack('B' * 8533, arq_sistema.readline()[:8533])]
    bitmap = processa_bitmap(dados_bitmap)
    print(bitmap.count(0), 'zeros e', bitmap.count(1), 'uns')
    arq_sistema.close()
    arq_sistema = open(nome_sistema, 'r')   # o resto não é binário
    arq_sistema.seek(8534)      # pula o bitmap que já leu antes

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



if __name__ == '__main__':
    monta_sistema('sistema')
