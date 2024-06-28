import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import openpyxl

# URL da página base
url_base = "https://www.pcisecuritystandards.org/faqs/all/"

# Função para remover duplicatas e URLs inválidas
def remove_duplicates(l):
    links = set()  # Usamos um set para garantir que não haja duplicatas
    for item in l:
        match = re.search(r"(?P<url>https?://[^\s]+)", item)
        if match:
            links.add(match.group("url"))
    return list(links)

# Função para verificar se um link corresponde ao padrão desejado
def is_valid_link(link):
    return re.match(r"https://www\.pcisecuritystandards\.org/faq/articles/Frequently_Asked_Question/.+", link)

# Inicializa a lista de links com a página base
links = [url_base]
all_links = []
visited_links = set()

# Loop para buscar links em todas as páginas
while links:
    link = links.pop(0)
    if link in visited_links:
        continue
    visited_links.add(link)
    
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        for a_tag in tqdm(soup.find_all("a", href=True), desc=f"Processando {link}", unit="link"):
            href = a_tag["href"]
            if is_valid_link(href):
                links.append(href)
                all_links.append(href)
    except Exception as e:
        print(f"Erro ao acessar {link}: {e}")

# Remove duplicatas e URLs inválidas
all_links = remove_duplicates(all_links)

# Função para extrair informações desejadas de uma página
def extract_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.find("h3", class_="single-faq-title")
        if title:
            title_text = title.get_text(strip=True)
            description_div = soup.find("div", class_="single-faq-description")
            if description_div:
                spans = description_div.find_all("span")
                if len(spans) >= 2:
                    content = spans[1].decode_contents()  # Pegando o conteúdo entre o segundo <span> e o primeiro </span>
                    return {"url": url, "title": title_text, "content": content}
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
    return None

# Extraindo informações de todos os links
data = []
for link in tqdm(all_links, desc="Extraindo informações dos links", unit="link"):
    info = extract_info(link)
    if info:
        data.append(info)

# Criando um arquivo Excel e salvando os dados
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "FAQ Info"
sheet.append(["URL", "Title", "Content"])

for item in data:
    sheet.append([item["url"], item["title"], item["content"]])

workbook.save("faq_info.xlsx")

print(f"Total de {len(data)} registros salvos em faq_info.xlsx")
