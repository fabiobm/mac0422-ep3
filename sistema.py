from struct import *
from time import *
from estruturas import *

# monta sistema a partir de arquivo com sistema já existente
def monta_sistema(nome_sistema):
    arq_sistema = open(nome_sistema, 'rb')
    # lê bitmap (binário), transforma em decimal, guarda em vetor
    bitmap = [i for i in unpack('b' * 3200, arq_sistema.readline()[:3200])]
    arq_sistema.close()
    arq_sistema = open(nome_sistema, 'r')   # o resto não é binário
    arq_sistema.seek(4096)      # pula o bitmap que já leu antes
    # lê informações sobre o diretório raiz
    info_raiz = arq_sistema.readline().split(' ')

    # cria representação do diretório raiz
    raiz = Diretorio('/', int(info_raiz[1]))
    raiz.modificado = int(info_raiz[0])
    raiz.acessado = int(info_raiz[2])
    print(raiz.nome, ctime(raiz.acessado), ctime(raiz.modificado), ctime(raiz.criado))

    # lê arquivos do diretório raiz, cria eles e adiciona ao diretório
    for i in range(3, len(info_raiz), 6):
        arq = Arquivo(info_raiz[i], int(info_raiz[i+1]), int(info_raiz[i+3]), int(info_raiz[i+5]))
        raiz.adiciona_arquivo(arq)

    for arq in raiz.arquivos:
        print(arq.nome, arq.tamanho, ctime(arq.criado))

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
        subdir = Diretorio(info_subdir[2], int(info_subdir[3]))
        pai.adiciona_arquivo(subdir)

        print(subdir.nome, ctime(subdir.criado), subdir.arquivos)

        # lê arquivos do subdiretório, cria eles e adiciona ao diretório
        for i in range(6, len(info_subdir), 6):
            arq = Arquivo(info_subdir[i], int(info_subdir[i+1]), int(info_subdir[i+3]), int(info_raiz[i+5]))
            subdir.adiciona_arquivo(arq)

        for arq in subdir.arquivos:
            print(arq.nome, arq.tamanho, ctime(arq.criado))

        # lê próxima linha, que novamente pode ser subdiretório ou FAT
        info_subdir = arq_sistema.readline().split(' ')

    fat = {}
    # linha atual se trata de informações para montar FAT
    info_fat = info_subdir

    # monta FAT
    for i in range(info_fat.index('')):
        print(info_fat[i], info_fat[i+1], i)
        if info_fat[i] == '-1':
            continue
        fat[int(info_fat[i])] = int(info_fat[i + 1])

    print(fat)

    # não é só isso o espaço desperdiçado, vou mexer ainda
    espaco_desperdicado = info_fat.count('')

    # depois da FAT, são os blocos com conteúdo dos arquivos
    blocos_conteudo = arq_sistema.read()
    # guarda esses blocos num vetor
    blocos = [blocos_conteudo[0+i:4096+i] for i in range(0, len(blocos_conteudo), 4096)]

    for arq in raiz.arquivos:
        if isinstance(arq, Arquivo):
            print(arq.nome, arq.conteudo(fat, blocos))



if __name__ == '__main__':
    monta_sistema('sistema2')
