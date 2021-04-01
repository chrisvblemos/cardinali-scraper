# Introdução
Isto não é uma análise de dados das casas e apartamentos residenciais disponíveis para locação na imobiliária Cardinalli de São Carlos. No entanto, alguns gráficos mediamente bonitos estão disponíveis.

# Principal

## Pacotes Utilizados

### Código:
- BeautifulSoap
- requests

### Análise dos dados (Jupyter):
- pandas
- seaborn
- matplotlib

## Ideia do código

Basicamente, o código acessa [essa página da imobiliária Cardinalli](https://www.cardinali.com.br/pesquisa-de-imoveis/?locacao_venda=L&id_cidade%5B%5D=190&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma=). Note que ela já vem preparada com alguns filtros para a pesquisa (a saber, Cidade: São Carlos, Operação:Locação, Finalidade:Residencial) e com a primeira página da pesquisa já retornada. O código consulta quantos imóveis foram retornados (é exibido na própria página), e sabendo que são exibidos 16 imóveis por página, ele calcula o número total de páginas disponíveis para percorrer.

Com essas informações em mente, o código faz alguns loops básicos coletando as informações visíveis de cada imóvei e acessando a próxima página, até atingir o número de páginas calculado no passo anterior. Um pequeno aviso, eu não me responsabilizo se o provedor da Cardinalli detectar seu IP como a origem de um ataque DDoS caso você utilize o número máximo de threads por muitas vezes seguidas, use com responsabilidade! Uma explicação mais detalhada pode ser consultada diretamente nos comentários do código em `main.py`, na função `threads_controller`.

Para otimização, eu quebro a busca das páginas em intervalos que são executadas por threads. O número de threads é escolhido pelo usuário, desde que seja um número entre 1 e o número total de páginas a ser buscado (isso garante que o tamanho do intervalo que cada thread varrerá é >= 1).

Os dados são salvos em dicionários, que então são inserios em uma lista final. Essa lista então é escrita em um arquivo `unidades.csv` é gerado com todos os dados de todos os imóveis.

Em seguida, eu faço uma análise desses dados utilizando o jupyter com a biblioteca pandas. Nada muito a fundo.

## Execução

Para rodar, primeiro instale todos os requirements com o seguinte comando:

`pip install -r requirements.txt`

Para executar a extração de dados, basta rodar:

`python main.py`

O programa irá coletar o número de páginas que serão buscadas, e perguntará para você quantas threads você deseja utilizar para a extração de dados.
Você deve informar um número entre 1 e o número total de páginas que serão buscadas.

Se desejar, pode ativar o modo verboso utilizando

`python main.py -v`

## Notebok (Jupyter)

Disponibilizei um notebook onde faço uma exploração dos dados obtidos utilizando o pandas e o seaborn para plotagem. Ele está no notebook incluso no repo.

Para executar ele, basta executar:

`jupyter notebook`

Se quiser, você pode consultar o notebook diretamente aqui pelo github também.

## Modificações

Fique a vontade para utilizar o arquivo CSV com os dados, ou mesmo fazer suas alterações no código para extrair outros dados, ou mesmo aplicar em outros sites.

# TODO

- Implementar um código que verifica a localização do imóvel por coordenadas e calcula a distância até uma das duas universidades da cidade. A ideia é verificar como o preço varia em função dessa distância. Uma ideia é utilizar alguma API como a do OpenStreetMaps para fazer o geocoding (conversão de endereço para coordenadas), mas ele não consegue encontrar alguns bairros ou nomes de condomínios.
- Melhorar a análise dos dados.
- Melhorar esse README.
- Melhorar os comentários do código.