from time import time


class Arquivo:
    '''
    Representação de um arquivo com nome, tamanho (em bytes) e
    instantes em que foi criado, modificado e acessado, além do
    bloco em que começa o conteúdo do arquivo.
    '''

    def __init__(self, metadados, nome=None, tamanho=None, instante=None, bloco_inicio=None):
        if metadados is None:
            self.nome = nome
            self.tamanho = tamanho
            self.modificado = instante
            self.criado = instante
            self.acessado = instante
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

        # o que estiver depois do limite do tamanho do arquivo é espaço em
        # branco que deve ser ignorado
        return texto[:self.tamanho]

    def lista_blocos(self, fat):
        prox = self.bloco_inicio
        if prox != -1:
            blocos = [prox]
        else:
            blocos = []
        while True:
            prox = fat[prox]
            if prox == -1:
                break
            blocos += [prox]

        return blocos

    def metadados(self):
        atributos = [self.nome, str(self.tamanho), str(self.modificado)]
        atributos += [str(self.criado), str(self.acessado)]
        atributos += [str(self.bloco_inicio)]
        return ' '.join(atributos)


class Diretorio:

    def __init__(self, metadados, nome=None, instante=None, caminho=None):
        if metadados is None:
            self.nome = nome
            self.modificado = instante
            self.criado = instante
            self.acessado = instante
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
        # lembrar de garantir que diretórios vão estar sempre depois dos
        # arquivos regulares na lista de arquivos dos diretório

    def remove_por_nome(self, nome_arquivo):
        arquivo = self.arquivo(nome_arquivo)
        if arquivo is not None:
            self.remove(arquivo)

    def remove(self, arquivo):
        if isinstance(arquivo, Arquivo):
            self.arquivos.remove(arquivo)

    def arquivo(self, nome):
        for arq in self.arquivos:
            if arq.nome == nome:
                return arq

    # esse método só é chamado pelo diretório raiz
    def acha_diretorio(self, nome):
        nome = nome[1:]
        if nome == '':
            return self
        if nome[-1] == '/':
            nome = nome[:-1]
        nome = nome.split('/')
        diretorio = self
        i = 0
        while len(nome) > i:
            prox = diretorio.arquivo(nome[i])
            diretorio = diretorio.arquivos[diretorio.arquivos.index(prox)]
            i += 1

        return diretorio

    def find(self, nome_arquivo):
        achados = [self.arquivo(nome_arquivo)]  # no próprio diretório
        if achados == [None]:
            achados = []
        self.acessado = int(time())

        # nos subdiretórios
        for subdir in self.arquivos:
            if isinstance(subdir, Diretorio):
                achados_sub = subdir.find(nome_arquivo)
                achados += [subdir.nome + '/' + i for i in achados_sub]

        return achados

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
