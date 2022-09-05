# Processamento de Linguagem Natural - MIEBIOM

## Trabalho Prático 1

### Trabalho realizado por:
### Lara Vaz A88362
### Mariana Lindo A88360
### Tiago Novais A88397

Neste documento serão explicadas detalhadamente as 7 etapas que levaram ao desenvolvimento do Trabalho Prático 1, cujo objetivo é gerar um dicionário médico em formato JSON a partir do documento "medicina.pdf". 

---
### 1. Passos iniciais

O 1º passo a executar foi converter o ficheiro "medicina.pdf" no "medicina.xml", através da utilização do comando 'pdftohtml -xml' na linha de comandos. Escolheu-se usar o ficheiro em .xml e não em .html ou .txt, uma vez que nestes dois últimos foramtos, a explicação e a tradução dos termos não estavam contíguos em relação ao respetivo termo, o que dificultaria bastante a execução do trabalho.

Posteriormente, foram executados alguns passos genéricos, que incluem a abertura do ficheiro "medicina.xml" para leitura, a leitura desse mesmo ficheiro e também a criação de um ficheiro em JSON, "dicionario.json", com permissões de escrita, de forma a que posteriormente ficasse nele contido o dicionário médico.

---
### 2. Limpeza do documento

Nesta 2ª etapa procedeu-se à limpeza do documento, isto é, à eliminação de carateres e de linhas que estavam a dificultar o parsing do documento, pois não eram necessários e simultaneamente dificultavam a identificação de elementos marcadores de termos de interesse. Deste modo, procedeu-se à elaboração de um conjunto de expressões regulares a utilizar com a função sub, cujo o objetivo era:

* Eliminar as linhas iniciais que não fazem parte das entradas do dicionário em si, como, a capa, o prefácio, os agradecimentos, o limiar, entre outros;

* Eliminar as linhas que continham FFVocabulario, pois estas indicam as quebras de página e não são necessárias no parsing do documento;

* Eliminação das tags <text >, <fontspec>, </text>, <page>, </page> e de algum eventual conteúdo existente no seu interior;

* Eliminação das tags <b>, </b>,  <i> e </i> que não tinham nenhum conteúdo no seu interior;

* Eliminar espaços antes do início das palavras, para facilitar a leitura do ficheiro .xml;

* Eliminar as tags <i><b> e </b></i> que se encontravam juntas.

---
### 3. Correções

Nesta 3ª etapa procedeu-se à correção de algumas situações que dificultavam o parsing do documento. Deste modo, procedeu-se à elaboração de um conjunto de expressões regulares a utilizar com a função sub, cujo o objetivo era:

* Substituir as linhas das entradas normais que ocupam 2 linhas por 1 linha só com toda a expressão;

* Substituir as linhas das entradas normais que ocupam 3 linhas por 1 linha só com toda a expressão;

* Substituir as linhas das entradas normais que ficam apenas com a abreviatura na linha seguinte por 1 linha só com toda a expressão;

* Substituir as linhas das entradas remissivas que têm o índice numa linha e o resto da entrada noutra linha por 1 linha só com toda a expressão. Nesta substituição foi utilizada a função processa_espacos, que aplica uma série de substituições às linhas que fazem macth. A função foi utilizada, pois não era possível  efetuar todas as substituições de uma vez só;

* Substituir as linhas das entradas remissivas que ficam em 2 linhas por 1 linha só com toda a expressão.

Além destas substituições com expressões regulares, foram ainda efetuadas 2 susbtituições manuais, uma vez que apresentavam tão pouca ocorrência no documento (2 vezes cada), não se justificava desenvolver uma expressão regular para isso. Deste modo, no documento "medicina.xml" colocaram-se as expressões 'fertilização' e 'in vitro' na mesma linha, assim como as expressões 'CO' e '2'. 

Nesta etapa, é ainda de realçar que se desenvolveram 2 expressões regulares para fazerem match com os temas e com as abreviaturas e que foram recorrentemente utilizadas em várias expressões regulares ao longo do ficheiro 'tp1.py'.

---
### 4. Identificação das entradas

Nesta 4ª etapa procedeu-se à identificação das entradas do ficheiro. É de realçar que no ficheiro "medicina.pdf" existiam 2 tipos de entradas: as normais e as remissivas. As normais apresentam o índice (1 a 5393), o termo, a abreviatura (opcional), o tema associado, os sinónimos ou variantes existentes desse termo (opcional), as traduções em espanhol, inglês, português e latim, sendo esta última opcional e ainda eventuais notas (também opcional). Dentro dos campos das traduções, das variantes e dos sinónimos podem existir explicações mais detalhadas sobre a que corresponde esse campo. Por exemplo, o aparecimento de [pop.], [arc.]e [col.] indicam que esses campos correspondem a designções populares, arcaicas ou coloquiais, respetivamente. Já as entradas remissivas são entradas às quais o utilizador recorre pois não sabe o nome correto daquilo que procura, e com essas, consegue ser corretamente encaminhado para a entrada que realmente procura. Estas entradas são constituídas por um termo remissivo (que o utilizador usa para pesquisar) e pelo termo a que este corresponde no dicionário. É ainda de realçar que algumas das entradas remissivas possuem um * que indica que esse termo não deve ser utilizado.

Posto isto, foram desenvolvidas expressões regulares com o objetivo de marcarem as entradas normais e as remissivas, sendo que antes do início da cada uma, foi colocado o marcador #@. O facto de se ter colocado #@ e não apenas @, foi porque, para se obter cada uma das entradas, efetuou-se o split do documento por @. E assim, obteve-se uma lista, em que cada elemento era uma entrada e o início da entrada estava marcado com #, um marcador que viria a facilitar o desenvolvimento de expressões regulares, à posteriori.

---
### 5. Procesamento das entradas

Estando todas as entradas delimitadas e contidas numa lista, em que cada elemento da lista era uma entrada, foi possível proceder ao processamento das entradas. Para tal, foi desenvolvido um conjunto de funções auxiliares da função principal processa_entradas. Esta função leva como argumento a lista de entradas e para cada elemento da lista verifica se:

1. A entrada é normal e tem mais de uma abreviatura;

2. A entrada é normal e não tem abreviaturas;

3. A entrada é normal e tem apenas uma abeviatura;

4. A entrada é remissiva e deve-se evitar;

5. A entrada é remissiva mas não é preciso evitá-la.  

Para os casos 1 a 3, foi desenvolvido um conjunto de expressões regulares e de funções auxiliares,com o objetivo de:

* Identificar o índice, o termo e a(s) abreviatura(s) caso existam. Se não existirem abreviaturas, a variável 'abv' toma o valor None. Se apenas existir uma abreviatura, então a variável 'abv' é uma string com a respetiva abreviatura. Se existirem 2 ou mais abreviaturas, então a variável 'abv' é uma lista em que cada elemento é uma abreviatura;

* Identificar o(s) temas associado(s) à entrada e processá-lo através da função processa_tema, que toma como argumento a expressão que fez match, faz algumas eliminações de tags e caso exista mais do que 1 tema, adiciona um ';' entre estes. Nessas situações em que existe mais do que 1 termo, é feito um split por ';' e a variável 'tema' passa a ser uma lista, em que cada elemento é um 'tema'. Caso contrário a variável tema é apenas uma string com o respetivo tema. No fim, a função retorna a variável 'tema';

* Identificar a(s) traduções em espanhol, inglês, português e latim e processá-las através da função processa_trad,que toma como argumento a expressão que fez match, faz algumas eliminações de tags e o split da expressão por ';', de forma a ser possível obter uma lista em que cada elemento é uma das várias traduções existentes. Posteriormente, esta lista de traduções é processada através da função separa, cujo o objetivo é identificar para cada tradução a existência de traduções especiais (como [pop.], [arc.] ou alguma abreviatura) e de traduções normais e adicioná-las a um dicionário. De forma a exemplificar o funcionamento desta expressão, é dado o seguinte exemplo: 

    Considere-se a tradução 
    pt afasia amnésica; afasia anômica [Br.];     afasia anómica [Pt.]; anomia

    Aplicando a função separa, o resultado será um dicionário do tipo:
    "pt: ": {
            "definicao(oes)": [
                "afasia amnésica",
                "anomia"
            ],
            "Br.": "afasia anômica ",
            "Pt.": "afasia anómica "
        }

No fim, a função separa retorna o dicionário que é depois retornado na função processa_trad;

* Identificar a(s) variantes e o(s) sinónimos e processá-los através da função processa_extra,que toma como argumento a expressão que fez match, faz algumas eliminações de tags, limpeza na expressão e o split da expressão por ';', de forma a ser possível obter uma lista em que cada elemento é um(a) dos(as) vários(as) sinónimos (variantes) existentes. Posteriormente, esta lista de sinónimos (ou variantes) é processada através da função separa, sendo retornado um dicionário conforme explicado anteriormente; 

* Identificar a(s) nota(s) e processá-las através da função processa_notas,que toma como argumento a expressão que fez match, faz algumas eliminações de tags, limpeza na expressão e o split da expressão por ';', de forma a ser possível obter uma lista em que cada elemento é uma das várias notas existentes. Posteriormente, esta lista de notas é processada através da função separa, sendo retornado um dicionário conforme explicado anteriormente. É de realçar que apesar das funções processa_trad, processa_notas e processa_extra serem muito parecidas, estas tiveram de ser construídas separadamente, pois ao juntar todas as funcionalidades numa só, os resultados obtidos não eram os pretendidos.

Tendo sido essas expressões desenvolvidas, posteriormente cada um dos campos (índice, termo, abreviatura, tema, traduções, sinónimos, variantes e notas) eram adicionados a um dicionário dic, cuja chave era o índice e os valores os restantes campos. Um exemplo de uma entrada de um termo normal no dicionário dic é:

dic[ent.group(1).strip()] = {
                "termo: " : ent.group(2).strip(),
                "abv: " : abv,
                "tema: " : tem,
                "es: " : es,
                "en: " : en,
                "pt: " : pt,
                "la: " : la,
                "sin: " : sin,
                "var: " : var,
                "notas: " : nots
            }

Para as entradas remissivas, foram desenvolvidas expressões regulares para identificar o termo da entrada que o utilizador usa para procurar (termo remissivo), o termo a que corresponde no dicionário (entrada) e se a entrada se deve ou não utilizar. Foi ainda desenvolvida uma função auxiliar processa_vid que toma como argumentos o termo remissivo e a entrada e cujo objetivo é fazer algumas eliminações de tags e limpeza da expressão. No fim é retornado o termo remissivo e a entrada devidamente processados. Posteriormente, estes campos obtidos são adicionados ao dicionário dic, cuja chave é vidN, em que N é o número do termo remissivo, por ordem de aparecimento no dicionário. É ainda de realçar que se a entrada remissiva deve ser eviatada, então, para essa entrada no dicionário dic, é ainda acrescentado um campo que é uma string com chave "utilizacao" e valor "evitar usar esse termo". Um exemplo de uma entrada remissiva, cuja utilização deve ser evitada no dicionário dic é:

dic["vid "+str(c)] = {
                "termo: " : termo_remissivo,
                "entrada: " : entrada,
                "utilizacao" : "evitar usar esse termo"
            }

E para entradas remissivas que não é preciso evitar é:

dic["vid "+str(c)] = {
                "termo: " : termo_remissivo,
                "entrada: " : entrada
            }

---
### 6. Eliminação dos valores nulos

Nesta 6ª etapa foi desenvolvida uma função cujo objetivo é eliminar os valores nulos existentes no dicionário dic. Isto porque nem todos os termos apresentam temas, abreviaturas, traduções em latim, sinónimos, variantes e notas. Assim sendo, a função elimina_nulos recebe como argumento um dicionário e para cada elemento verifica se o valor é ou não nulo. Se for nulo, elimina-o, se não for, adiciona-o ao dicionário limpo, uma versão do dicionário passado como argumento mas que não tem valores nulos.

---
### 7. Execução do código para criar o dicionário e guardá-lo no ficheiro JSON

Nesta 7ª e última etapa, invocou-se a função processa_entradas que devolve o dicionário dic e de seguida foi invocada a função elimina_nulos para eliminar os valores nulos desse dicionário, obtendo-se o dicionário limpo. Por último, esse dicionário foi passado como argumento na função dump do módulo json, de forma a escrever no ficheiro "dicionario.json" o dicionário limpo.




