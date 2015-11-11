class Arquivo:
    '''
    Representação de um arquivo com nome, tamanho (em bytes) e
    instantes em que foi criado, modificado e acessado, além do
    bloco em que começa o conteúdo do arquivo.
    '''

    modificado = 0
    acessado = 0

    def __init__(self, nome, tamanho, instante, bloco_inicio):
        self.nome = nome
        self.tamanho = tamanho
        self.criado = instante
        self.modificado = instante
        self.bloco_inicio = bloco_inicio

    def conteudo(self, fat, blocos):
        prox_bloco = self.bloco_inicio
        texto = ''
        while prox_bloco != -1:
            texto += blocos[prox_bloco]
            prox_bloco = fat[prox_bloco]

        return texto


class Diretorio:
    modificado = 0
    acessado = 0

    def __init__(self, nome, instante):
        self.nome = nome
        self.criado = instante
        self.modificado = instante
        self.arquivos = []

    def adiciona_arquivo(self, arquivo):
        self.arquivos.append(arquivo)

    def acha_diretorio(self, nome):
        nome = nome[1:]
        nome = nome.split('/')
        diretorio = self.arquivos[self.arquivos.index(nome[0])]
        i = 1
        while len(nome) > i:
            diretorio = diretorio.arquivos[diretorio.arquivos.index(nome[i])]
            i += 1

        return diretorio
