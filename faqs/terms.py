import os
import re

# Função para ler e modificar um arquivo
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define os padrões a serem removidos
    patterns = [r'<br>', r'</br>', r'<span>', r'</span>']

    # Substitui os padrões por uma string vazia
    for pattern in patterns:
        content = re.sub(pattern, '', content)

    # Escreve o conteúdo modificado de volta no arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Obtém o diretório atual do script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Lista todos os arquivos .txt no diretório atual
txt_files = [f for f in os.listdir(current_directory) if f.endswith('.txt')]

# Processa cada arquivo .txt encontrado
for txt_file in txt_files:
    file_path = os.path.join(current_directory, txt_file)
    process_file(file_path)

print("Termos removidos com sucesso de todos os arquivos .txt no diretório atual.")
