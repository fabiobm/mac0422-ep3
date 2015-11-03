class Arquivo:
    '''
    Representação de um arquivo com nome, tamanho (em bytes) e
    instantes em que foi criado, modificado e acessado, além do
    conteúdo do arquivo.
    '''

    modificado = 0
    acessado = 0

    def __init__(self, nome, tamanho, instante, conteudo):
        self.nome = nome
        self.tamanho = tamanho
        self.criado = instante
        self.modificado = instante
        self.conteudo = conteudo
