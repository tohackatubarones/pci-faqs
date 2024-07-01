import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import openpyxl
import csv
import os
import concurrent.futures

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

# Função para processar links em paralelo usando múltiplas threads
def process_links(links):
    data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(extract_info, url): url for url in links}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                info = future.result()
                if info:
                    data.append(info)
            except Exception as e:
                print(f"Erro ao processar {url}: {e}")
    return data

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

# Extraindo informações de todos os links em paralelo
data = process_links(all_links)

# Obtendo o diretório atual do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Criando um arquivo Excel e salvando os dados
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "FAQ Info"
sheet.append(["URL", "Title", "Content"])

for item in data:
    sheet.append([item["url"], item["title"], item["content"]])

excel_file = os.path.join(script_dir, "faq_info.xlsx")
workbook.save(excel_file)

# Salvando os dados em um arquivo CSV
csv_file = os.path.join(script_dir, "faq_info.csv")
with open(csv_file, "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["url", "title", "content"])
    writer.writeheader()
    writer.writerows(data)

# Criando arquivos de texto para cada FAQ
faqs_dir = os.path.join(script_dir, "faqs")
if not os.path.exists(faqs_dir):
    os.makedirs(faqs_dir)

# Salvando os dados em arquivos de texto com nomes sequenciais
for index, item in enumerate(data, start=1):
    filename = f"{index:04}.txt"  # Formato para salvar como 0001.txt, 0002.txt, etc.
    txt_file = os.path.join(faqs_dir, filename)
    with open(txt_file, "w", encoding='utf-8') as f:
        f.write(item["content"])

print(f"Total de {len(data)} registros salvos em {excel_file}, {csv_file}, e arquivos de texto na pasta 'faqs'")
