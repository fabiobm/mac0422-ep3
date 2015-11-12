class Arquivo:
    '''
    Representação de um arquivo com nome, tamanho (em bytes) e
    instantes em que foi criado, modificado e acessado, além do
    bloco em que começa o conteúdo do arquivo.
    '''

    modificado = 0
    acessado = 0

    def __init__(self, metadados, nome=None, tamanho=None, instante=None, bloco_inicio=None):
        if metadados is None:
            self.nome = nome
            self.tamanho = tamanho
            self.criado = instante
            self.modificado = instante
            self.bloco_inicio = bloco_inicio

        else:   # cria a partir de metadados obtidos do arquivo
            self.nome = metadados[0]
            self.tamanho = int(metadados[1])
            self.modificado = int(metadados[2])
            self.criado = int(metadados[3])
            self.acessado = int(metadados[4])
            self.bloco_inicio = int(metadados[5])

    def conteudo(self, fat, blocos):
        prox_bloco = self.bloco_inicio
        texto = ''
        while prox_bloco != -1:
            texto += blocos[prox_bloco]
            prox_bloco = fat[prox_bloco]

        return texto

    def metadados(self):
        atributos = [self.nome, str(self.tamanho), str(self.modificado)]
        atributos += [str(self.criado), str(self.acessado)]
        atributos += [str(self.bloco_inicio)]
        return ' '.join(atributos)


class Diretorio:
    modificado = 0
    acessado = 0

    def __init__(self, metadados, nome=None, instante=None, caminho=None):
        if metadados is None:
            self.nome = nome
            self.criado = instante
            self.modificado = instante
            self.caminho = caminho

        else:   # cria a partir de metadados obtidos do arquivo
            self.caminho = metadados[1]
            self.nome = metadados[2]
            self.modificado = int(metadados[3])
            self.criado = int(metadados[4])
            self.acessado = int(metadados[5])

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

    def metadados(self):
        meta_dir = []
        if self.nome != '/':
            meta_dir += ['/', self.caminho, self.nome]
        meta_dir += [str(self.modificado), str(self.criado), str(self.acessado)]

        meta_arquivos = []
        meta_subdirs = []
        for arquivo in self.arquivos:
            if isinstance(arquivo, Arquivo):
                meta_arquivos += [arquivo.metadados()]
            elif isinstance(arquivo, Diretorio):
                meta_subdirs += [arquivo.metadados()]
        return '\n'.join([' '.join(meta_dir + meta_arquivos)] + meta_subdirs)
