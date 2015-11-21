from math import ceil


class Arquivo:
    '''
    Representação de um arquivo com nome, tamanho (em bytes) e instantes em
    que foi criado, modificado e acessado, além do bloco em que começa o
    conteúdo do arquivo. Instâncias podem ser criadas a partir das informações
    extraídas de um arquivo que representa um sistema de arquivos (nesse caso
    o argumento metadados é diferente de None e é o único fornecido) ou a
    partir de informações de nome, tamanho, instante e bloco, que são
    fornecidos como argumentos após o argumento metadados que, nesse caso, tem
    que ser None
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

    # monta o conteúdo do arquivo e retorna uma string com ele
    def conteudo(self, fat, blocos):
        prox_bloco = self.bloco_inicio
        texto = ''
        while prox_bloco != -1:
            texto += blocos[prox_bloco]
            prox_bloco = fat[prox_bloco]

        # o que estiver depois do limite do tamanho do arquivo é espaço em
        # branco que deve ser ignorado
        return texto[:self.tamanho]

    # lista dos blocos percorridos para montar o conteúdo do arquivo
    def lista_blocos(self, fat):
        prox = self.bloco_inicio
        if prox != -1:
            blocos = [prox]
        else:
            return []
        while True:
            prox = fat[prox]
            if prox == -1:
                break
            blocos += [prox]

        return blocos

    # retorna os metadados do arquivo (nome, tamanho, instantes, bloco de
    # início) no formato usado para guardar essas informações no arquivo que
    # representa o sistema de arquivos
    def metadados(self):
        atributos = [self.nome, str(self.tamanho), str(self.modificado)]
        atributos += [str(self.criado), str(self.acessado)]
        atributos += [str(self.bloco_inicio)]
        return ' '.join(atributos)


class Diretorio:

    '''
    Representação de um diretório com nome, instantes em que foi criado,
    acessado e modificado pela última vez, caminho no sistema de arquivos e
    lista com arquivos e diretórios diretamente abaixo. Instâncias podem ser
    criadas a partir das informações extraídas de um arquivo que representa um
    sistema de arquivos (nesse caso o argumento metadados é diferente de None
    e é o único fornecido) ou a partir de informações de nome, instante e
    caminho, que são fornecidos como argumentos após o argumento metadados
    que, nesse caso, tem que ser None
    '''

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

    # calcula o espaço desperdiçado pelos arquivos nesse diretório e em todos
    # abaixo, considerando apenas o espaço usado para completar os blocos que
    # guardam o conteúdo dos arquivos, pois o espaço para completar os blocos
    # que guardam bitmap/metadados/FAT na verdade ainda poderão ser usados
    def espaco_desperdicado(self):
        espaco = 0
        for arq in self.arquivos:
            if isinstance(arq, Arquivo):
                espaco += 4096 * ceil(arq.tamanho / 4096) - arq.tamanho
            elif isinstance(arq, Diretorio):
                espaco += arq.espaco_desperdicado()

        return espaco

    # retorna tupla (d, a) onde d é o número de diretórios e a o número de
    # arquivos embaixo desse diretório (direta e indiretamente)
    def count(self):
        num_arqs = len([arq for arq in self.arquivos if isinstance(arq, Arquivo)])
        num_dirs = len(self.arquivos) - num_arqs
        if self.nome == '/':
            num_dirs += 1       # tem que contar o próprio raiz

        for subdir in self.arquivos:
            if isinstance(subdir, Diretorio):
                nums_subdir = subdir.count()
                num_dirs += nums_subdir[0]
                num_arqs += nums_subdir[1]

        return (num_dirs, num_arqs)

    # adiciona um arquivo ou diretório embaixo de si, deixando sempre os
    # diretórios no final da lista
    def adiciona_arquivo(self, arquivo):
        self.arquivos.append(arquivo)
        # reorganiza lista para diretórios ficarem no final
        arqs = [arq for arq in self.arquivos if isinstance(arq, Arquivo)]
        subdirs = [subdir for subdir in self.arquivos if isinstance(subdir, Diretorio)]
        self.arquivos = arqs + subdirs

    # remove o arquivo (não diretório) nome_arquivo da lista de arquivos
    def remove_por_nome(self, nome_arquivo):
        arquivo = self.arquivo(nome_arquivo)
        if arquivo is not None:
            self.remove(arquivo)

    # remove o arquivo recebido como argumento da lista de arquivos
    def remove(self, arquivo):
        if isinstance(arquivo, Arquivo):
            self.arquivos.remove(arquivo)

    # retorna, se houver, o arquivo da lista de arquivos de nome nome
    def arquivo(self, nome):
        for arq in self.arquivos:
            if arq.nome == nome:
                return arq

    # esse método só é chamado pelo diretório raiz e retorna o diretório cujo
    # caminho está no argumento nome 
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

    # retorna o caminho de todos os arquivos com nome nome_arquivo embaixo
    # desse diretório (direta ou indiretamente)
    def find(self, nome_arquivo):
        achados = [self.arquivo(nome_arquivo)]  # no próprio diretório
        if achados == [None]:
            achados = []
        else:
            achados = [achados[0].nome]

        # nos subdiretórios
        for subdir in self.arquivos:
            if isinstance(subdir, Diretorio):
                achados_sub = subdir.find(nome_arquivo)
                achados += [subdir.nome + '/' + i for i in achados_sub]

        return achados

    # retorna os metadados do diretório (nome, instantes, caminho e metadados
    # dos arquivos e diretórios abaixo tanto direta quanto indiretamente) no
    # formato usado para guardar essas informações no arquivo que representa o
    # sistema de arquivos
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
