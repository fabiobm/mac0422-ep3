from sys import argv  # argumentos estão em sys.argv


def gera_arquivo(nome, tamanho):
    '''
    Gera um arquivo com nome nome e tamanho tamanho (em bytes) composto
    pelo número 7 repetido tamanho vezes, sem espaços nem linhas em
    branco.
    '''
    arquivo = open(nome, 'w')
    arquivo.write('7' * tamanho)
    arquivo.close()

if __name__ == '__main__':
    argumentos = argv[1:]
    while True:
        try:
            gera_arquivo(argumentos[0], int(argumentos[1]))
            break
        except IndexError:
            argumentos = input(
                'Forneça os argumentos com o nome e o tamanho (em bytes) do'
                'arquivo a ser gerado.\n').split(' ')
