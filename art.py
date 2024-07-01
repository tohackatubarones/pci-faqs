import requests
from bs4 import BeautifulSoup

# URL da página a ser analisada
url = "https://www.pcisecuritystandards.org/faqs/all/"

try:
    # Fazendo a requisição GET
    response = requests.get(url)
    response.raise_for_status()  # Lança um erro para códigos de status HTTP diferentes de 200
    
    # Criando o objeto BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Encontrando todos os elementos com a classe 'featured-faq-list-item'
    faq_items = soup.find_all(class_="featured-faq-list-item")
    
    # Inicializando uma lista para armazenar os números encontrados
    numbers = []
    
    # Iterando sobre os elementos encontrados
    for item in faq_items:
        # Encontrando todos os elementos <span> dentro de cada item
        spans = item.find_all("span")
        for span in spans:
            # Verificando se o conteúdo do span é um número
            try:
                number = int(span.text.strip())  # Convertendo o texto do span para inteiro
                numbers.append(number)  # Adicionando o número à lista
            except ValueError:
                pass  # Ignorando se o conteúdo do span não puder ser convertido para inteiro
    
    # Contando o número de itens encontrados
    total_items = len(numbers)
    
    # Imprimindo os números encontrados e o total de itens
    print(f"Números encontrados: {numbers}")
    print(f"Total de itens encontrados: {total_items}")
    
except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
