# cardinalli-scrapper
Isto não é uma análise de dados das casas e apartamentos residenciais disponíveis para locação na imobiliária Cardinalli de São Carlos. No entanto, alguns gráficos mediamente bonitos estão disponíveis.

# Principal
## Ideia

Basicamente, o código acessa [essa página da imobiliária Cardinalli](https://www.cardinali.com.br/pesquisa-de-imoveis/?locacao_venda=L&id_cidade%5B%5D=190&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma=). Note que ela já vem preparada com alguns filtros para a pesquisa (a saber, Cidade: São Carlos, Operação:Locação, Finalidade:Residencial) e com a primeira página da pesquisa já retornada. O código consulta quantos imóveis foram retornados (é exibido na própria página), e sabendo que são exibidos 16 imóveis por página, ele calcula o número total de páginas disponíveis para percorrer.

Com essas informações em mente, o código faz alguns loops básicos coletando as informações visíveis de cada imóvei e acessando a próxima página, até atingir o número de páginas calculado no passo anterior.

Os dados são salvos em dicionários, que então são inserios em uma lista final. Essa lista então é lida e um arquivo `unidades.csv` é gerado com todos os dados de todos os imóveis.

Em seguida, eu faço uma análise desses dados utilizando o jupyter com a biblioteca pandas. Nada muito a fundo.

## Run

Para rodar, primeiro instale todos os requirements com o seguinte comando:

`pip install -r requirements.txt`

Para executar a extração de dados, basta rodar:

`python main.py`

## Jupyter

Disponibilizei um arquivo onde faço uma exploração dos dados obtidos utilizando o pandas e o seaborn para plotagem. Ele está no notebook incluso no repo.

Para executar ele, basta executar:

`jupyter notebook`

Se quiser, você pode consultar o notebook diretamente aqui pelo github também.

## Modificações

Fique a vontade para utilizar o arquivo CSV com os dados, ou mesmo fazer suas alterações no código para extrair outros dados, ou mesmo aplicar em outros sites.

# TODO

- Implementar um código que verifica a localização do imóvel por coordenadas e calcula a distância até uma das duas universidades da cidade. A ideia é verificar como o preço varia em função dessa distância. Uma ideia é utilizar alguma API como a do OpenStreetMaps para fazer o geocoding (conversão de endereço para coordenadas), mas ele não consegue encontrar alguns bairros ou nomes de condomínios.
- Melhorar a análise dos dados.
- Melhorar esse README.