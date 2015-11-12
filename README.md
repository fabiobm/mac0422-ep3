# mac0422-ep3
MAC0422 (Sistemas Operacionais) - EP 3

## Esquema do arquivo que representa o sistema de arquivos

Bitmap: 1 = livre, 0 = ocupado, essa parte do arquivo é binária, são 8533 bytes (25600 blocos, mas os 3 primeiros com certeza vão estar ocupados pelo próprio bitmap e os metadados e FAT; representando 3 blocos por byte temos 8532 \* 3 = 25596 e sobra um bloco que vai ser representado por um byte inteiro) e termina com um \n, e aí começa direto metadados.

Metadados do diretório raiz: instantes de última modificação, criação e acesso, termina com espaço e passa aos metadados dos arquivos do diretório.

Metadados dos arquivos: nome, tamanho (em bytes), instantes de última modificação, criação e acesso, número do bloco no qual o início do arquivo está armazenado (os números começam de 0 mas representam apenas os blocos após bitmap, FAT e metadados). Termina com \n e passa aos subdiretórios.

Subdiretórios: sempre começam com uma / pra identificar que é informação de diretório; aparecem sempre depois de todos os arquivos normais do diretório e além dos metadados iguais aos do diretório raiz, também têm o caminho até o diretório pai (p. ex.: /.../nome_dir_pai) e o nome do próprio diretório. Após metadadados tem espaço e metadados de arquivos, novos subdiretórios, etc. Após o último diretório e seus arquivos e metadados, \n e começa a FAT.

FAT: começa com número indicando tamanho das informações a seguir: sequências de números de blocos terminadas em -1, a sequência é feita em pares (p. ex.: 0 1 2 3 -1 significa 0->1->2->3->fim). Termina com espaços (se necessário para completar um bloco de 4KB) e depois \n, e aí começam os blocos com conteúdo dos arquivos.

Blocos c/ conteúdo dos arquivos: conteúdo dos arquivos em texto puro, se o arquivo termina antes do fim de um bloco de 4KB espaços completam até o fim do bloco. O sistema de arquivos acaba com o último bloco que foi alocado, e cresce conforme novos blocos são alocados (até o limite de 100 MB).

==============================================================================

[Bitmap] 1 0 0 0 1 ...

[Diretório raiz] ult\_mod\_dir criado\_dir acessado\_dir

[Arquivos] nome\_1 tamanho\_1 ult\_mod\_1 criado\_1 acessado\_1 bloco\_inicio\_1

[Diretório 1] / /.../nome\_pai nome\_dir\_1 ult\_mod\_dir\_1 criado\_dir\_1 acessado\_dir\_1

.

. [outros diretórios e seus arquivos e metadados]

.

[FAT] 1 2 3 -1 4 5 6 -1 ...

[Blocos] b0 b1 b2 ... bn
