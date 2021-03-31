import requests
from bs4 import BeautifulSoup
import re
import math
import csv

# Recebe o endereço da página principal (previamente preparado como 
# descrito no README).
# Retorna o número de páginas que a pesquisa retornou, através 
# da divisão do total de unidades / unidades por página.
def Get_Num_Of_Pages(mainpageurl):
    page = requests.get(mainpageurl)
    soup = BeautifulSoup(page.content, 'html.parser')
    num_of_properties = int(soup.find('p', class_='titulo_res_busca').find('strong').get_text())
    num_of_pages = math.ceil(num_of_properties / 16)
    return num_of_pages

# Realiza uma série de loops básicos para coletar dados exibidos para
# cada unidade das 16 unidades exibidas no resultado para aquela página.
def Get_all_properties_from_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    property_listing = soup.find('div', id='property-listing')
    properties = property_listing.find_all('div', class_='item col-sm-6 col-md-4 col-lg-3')
    properties_list = []

    for property in properties:
        image_class = property.find('div', class_='image')
        price_class = property.find('div', class_='price')
        info_class = property.find('div', class_='info')

        category = image_class.find('a')['title']
        image = image_class.find('img')['src']
        price = re.sub('[^0-9\,]', '', price_class.find_all('span')[0].get_text())

        location = info_class.find('small')['title']
        description = info_class.find('p', class_='corta_desc').get_text()
        amenities = info_class.find('ul', class_='amenities').find_all('li')

        # Valores default em caso de ausência de dado
        area = 'NULL'
        bedrooms = 'NULL'
        bathrooms = 'NULL'

        # Coleta os dados sobre área, banheiros e quartos
        for amenity in amenities:
            amenity_type = amenity.find('i')['class'][0]

            if amenity_type == 'icon-area':
                area = amenity.get_text()

            if amenity_type == 'icon-bathrooms':
                bathrooms = amenity.get_text()

            if amenity_type == 'icon-bedrooms':
                bedrooms = amenity.get_text()

        properties_dict = {'category':    category.strip(),
                        'location':    location.strip(),
                        'description': description.strip(),
                        'price':       price.strip(),
                        'area':        area.strip(),
                        'bathrooms':   bathrooms.strip(),
                        'bedrooms':    bedrooms.strip()}

        properties_list.append(properties_dict)

    return properties_list

# Essa função faz um loop sobre todas as páginas retornadas na pesquisa,
# executando a função acima para cada página.
def Loop_Over_All_Pages(url):
    num_of_pages = Get_Num_Of_Pages(url)
    all_properties = []

    for i in range(num_of_pages):
        print('Current page: ' + str(i+1))
        page_url = 'https://www.cardinali.com.br/pesquisa-de-imoveis/locacao_venda=L&id_cidade[]=190&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma=&&pag=' + str(i+1)
        properties_from_i_page = Get_all_properties_from_page(page_url)
        all_properties.extend(properties_from_i_page)

    return all_properties

# Main (executa o seu propósito)
if (__name__ == '__main__'):
    mainpage = 'https://www.cardinali.com.br/pesquisa-de-imoveis/?locacao_venda=L&id_cidade%5B%5D=190&finalidade=residencial&dormitorio=0&garagem=0&vmi=&vma='
    properties_list = Loop_Over_All_Pages(mainpage)   
    keys = properties_list[0].keys()
    with open('unidades.csv', 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys, delimiter = ';')
        dict_writer.writeheader()
        dict_writer.writerows(properties_list)




