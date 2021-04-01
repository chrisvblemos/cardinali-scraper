import requests
from bs4 import BeautifulSoup
import re
import math
import csv
import threading
import argparse

# Algumas constantes
DEFAULT_VALUE = 'NULL'

# Recebe o endereço da página principal (previamente preparado como 
# descrito no README).
# Retorna o número de páginas que a pesquisa retornou, através 
# da divisão do total de unidades / unidades por página.
def get_num_pages(mainpageurl):

    # Acesso a url informada
    page = requests.get(mainpageurl)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Busco pela informação a respeito do número de unidades retornadas pela pesquisa no site
    num_of_properties = int(soup.find('p', class_='titulo_res_busca').find('strong').get_text())

    # Calculo o número total de páginas sabendo que cada página exibe 16 unidades
    # Portanto, o número de páginas é igual ao número total de unidades / 16 (arredondado para cima)
    num_of_pages = math.ceil(num_of_properties / 16)
    return num_of_pages

# Realiza uma série de loops básicos para coletar dados exibidos para
# cada unidade das 16 unidades exibidas no resultado para aquela página.
def extract_unities_from_page(url):

    # Acesso a url informada
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Busco pelo frame que contém as unidades
    property_listing = soup.find('div', id='property-listing')
    properties = property_listing.find_all('div', class_='item col-sm-6 col-md-4 col-lg-3')
    
    # Preparo uma lista que guardará todas as unidades encontradas naquela página
    properties_list = []

    # Para cada item de uma unidade, realiza as buscas pelos dados contidos nas classes image, price e info
    # image -> contém a imagem da unidade
    # price -> contém o preço da locação
    # info -> contém uma breve descrição da unidade e a quantidade de quartos, banheiros e área da unidade
    for property in properties:
        image_class = property.find('div', class_='image')
        price_class = property.find('div', class_='price')
        info_class = property.find('div', class_='info')

        # Coleto algumas informações mais granulares, como categoria, preço, localização, etc
        category = image_class.find('a')['title']
        # image = image_class.find('img')['src'] # TODO talvez no futuro incluir os dados sobre a imagem?
        price = re.sub('[^0-9\,]', '', price_class.find_all('span')[0].get_text())
        location = info_class.find('small')['title']
        description = info_class.find('p', class_='corta_desc').get_text()
        amenities = info_class.find('ul', class_='amenities').find_all('li')

        # Valores default inicializados em caso de ausência de dado
        area = DEFAULT_VALUE
        bedrooms = DEFAULT_VALUE
        bathrooms = DEFAULT_VALUE

        # Coleta os dados sobre área, banheiros e quartos (amenities)
        for amenity in amenities:
            amenity_type = amenity.find('i')['class'][0]

            # Área
            if amenity_type == 'icon-area':
                area = amenity.get_text()

            # Banheiros
            if amenity_type == 'icon-bathrooms':
                bathrooms = amenity.get_text()

            # Quartos
            if amenity_type == 'icon-bedrooms':
                bedrooms = amenity.get_text()

        # Gera o dict com informações a respeito daquela unidade {categoria, location, description, price, area, bathrooms, bedrooms}
        properties_dict = {'category':    category.strip(),
                           'location':    location.strip(),
                           'description': description.strip(),
                           'price':       price.strip(),
                           'area':        area.strip(),
                           'bathrooms':   bathrooms.strip(),
                           'bedrooms':    bedrooms.strip()}

        # Adiciono o dict dessa unidade à lista de unidades
        properties_list.append(properties_dict)

    return properties_list

# Busca a i-ésima página e adiciona as unidades encontradas na lista 'result' (global)
def scan_page_range(mainpageurl, start_page, end_page):

    # A ideia aqui é realizar a busca pelas unidades para cada página entre [start_page, end_page]
    # O resultado dessa busca é appended na lista 'result', que representa todos os dados finais
    for i in range(start_page, end_page):
        page = i
        page_url = 'https://www.cardinali.com.br/pesquisa-de-imoveis/locacao_venda=L&id_cidade[]=190&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma=&&pag=' + str(page)
        
        if verbose: # DEBUG
            print('DEBUG[scan_page_range]: Current page: %d' % page)

        properties_from_i_page = extract_unities_from_page(page_url)
        result.extend(properties_from_i_page) # global

# Controlador das threads, para executar a extração com vários threads em paralelo
def threads_controller():
    
    # Inicializa lista de controle das threads
    threads = []

    # Coleta o número total de páginas a serem analisadas
    total_num_of_pages = get_num_pages(mainpage)

    # 4Fun
    print('\n')
    print('----------------------------------------')
    print('------- Cardinalli Scrapper Tool -------')
    print('-------- Originally by: lemos10 --------')
    print('----------------------------------------')
    print('\n')
    # 4Fun

    print('Detected %d pages to be scanned.' % total_num_of_pages)

    # Coleta o número de threads que o usuário deseja
    print('Please, enter the number N of threads you wish to use, from 1 to %d:' % total_num_of_pages)
    n_of_threads = int(input())
    while (type(n_of_threads) != int) or n_of_threads > total_num_of_pages:
        print('Please, enter a valid number N of threads, an integer from 1 to %d:' % total_num_of_pages)
        n_of_threads = int(input())

    # Calcula o tamanho do step (quantas páginas cada thread irá olhar)
    step = math.floor(total_num_of_pages / n_of_threads)

    print('\n')
    print('Initializing...')
    print('- N of threads: %d'     % n_of_threads)
    print('- Pages to scan: %d'    % total_num_of_pages)
    print('- Pages per thread: %d' % step)
    print('\n')

    print('Preparing threads...')
    for i in range(1, n_of_threads+1):

        # Cada thread vai fazer uma busca da página (i * step) até a página (i + 1) * step
        start = i * step
        end = (i + 1) * step

        # Lidando com casos especiais
        # 1. a divisão saiu torta e o número total de páginas foi atingido antes da hora, nesse caso, não cria mais threads
        # 2. ainda restaram algumas páginas de 'sobra' após o último thread, nesse caso, adiciona a sobra na faixa de busca daquele thread
        # TODO existe uma maneira melhor de lidar com esses casos?
        if i == n_of_threads:
            end = total_num_of_pages + 1

        # Forçando a condição inicial quando i = 1 para setar start = 1 (primeira página é 1 e não 0)
        # TODO existe uma maneira melhor de lidar com esse caso?
        if i == 1:
            start = 1

        # Prepara as threads
        t = threading.Thread(target=scan_page_range, args = (mainpage, start, end))
        t.daemon = True
        threads.append(t)

        if (verbose): # DEBUG
            print('DEBUG [threads_controller]: Worker %d responsible for interval (%d, %d).' % (i, start, end - 1))

    # Inicializa todas as threads
    print('Starting threads...')
    for i in range(len(threads)):
        threads[i].start()

    # Aguarda a execução de todas as threads
    print('Waiting for threads to finish...')
    for i in range(len(threads)):
        threads[i].join()

    print('Extraction completed, creating new csv file...')

# Args parser para o comando de execução (por enquanto, somente uma variável para ativar o modo verboso)
# TODO talvez no futuro incrementar
def argparser_controller():
    parser = argparse.ArgumentParser(description = 'Extract data from the Cardinalli website.')
    parser.add_argument('-v', dest = 'verbose', default = False, action = 'store_true', help = 'Enables verbose mode when present.')
    args = parser.parse_args()
    return args

# Escreve a lista 'result' com todos os dados extraídos para um arquivo CSV
def output_file(results):
    keys = result[0].keys()
    with open('unidades.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys, delimiter = ';')
        dict_writer.writeheader()
        dict_writer.writerows(result)
    print('File unidades.csv with %d rows of data created successfully!' % len(result))

# Main (executa o seu propósito)
if (__name__ == '__main__'):
    mainpage = 'https://www.cardinali.com.br/pesquisa-de-imoveis/?locacao_venda=L&id_cidade%5B%5D=190&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma='
    result = []
    args = argparser_controller()
    verbose = args.verbose

    threads_controller()
    output_file(result)
    print('Exiting...')
    
    




