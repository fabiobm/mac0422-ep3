# mac0422-ep3
MAC0422 (Sistemas Operacionais) - EP 3

*Esquema do arquivo que representa o sistema de arquivos*

Bitmap: 1 = livre, 0 = ocupado, essa parte do arquivo é binária, são 25600 bytes e termina com um \n, e aí começa direto metadados.

Metadados do diretório raiz: instantes de última modificação, criação e acesso, termina com \n e passa aos metadados dos arquivos do diretório.

Metadados dos arquivos: nome, tamanho (em bytes), instantes de última modificação, criação e acesso, número do bloco no qual o início do arquivo está armazenado (os números começam de 0 mas representam apenas os blocos após bitmap, FAT e metadados). Termina com \n e passa aos subdiretórios.

Subdiretórios: sempre começam com uma / pra identificar que é informação de diretório; aparecem sempre depois de todos os arquivos normais do diretório e além dos metadados iguais aos do diretório raiz, também têm o caminho até o diretório pai (p. ex.: /.../nome_dir_pai) e o nome do próprio diretório. Após metadadados tem \n e metadados de arquivos, novos subdiretórios, etc. Após o último diretório e seus arquivos e metadados, \n e começa a FAT.

FAT: sequências de números de blocos terminadas em -1, a sequência é feita em pares (p. ex.: 0 1 2 3 -1 significa 0->1->2->3->fim). Termina com espaços (se necessário para completar um bloco de 4KB) e depois \n, e aí começam os blocos com conteúdo dos arquivos.

Blocos c/ conteúdo dos arquivos: conteúdo dos arquivos em texto puro, se o arquivo termina antes do fim de um bloco de 4KB espaços completam até o fim do bloco. O sistema de arquivos acaba com o último bloco que foi alocado, e cresce conforme novos blocos são alocados (até o limite de 100 MB).

==============================================================================

[Bitmap] 1 0 0 0 1 ...
[Diretório raiz] ult_mod_dir criado_dir acessado_dir
[Arquivos] nome_1 tamanho_1 ult_mod_1 criado_1 acessado_1 bloco_inicio_1
[Diretório 1] / /.../nome_pai nome_dir_1 ult_mod_dir_1 criado_dir_1 acessado_dir_1
.
. [outros diretórios e seus arquivos e metadados]
.
[FAT] 1 2 3 -1 4 5 6 -1 ...
[Blocos] b0 b1 b2 ... bn
