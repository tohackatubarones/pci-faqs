import os

# Obtém o diretório atual do script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Nome do arquivo de saída
output_filename = "faqs.txt"

# Caminho completo para o arquivo de saída
output_file = os.path.join(current_directory, output_filename)

# Lista para armazenar o conteúdo de todos os arquivos .txt
all_text = []

# Lista todos os arquivos .txt no diretório atual
txt_files = [f for f in os.listdir(current_directory) if f.endswith('.txt')]

# Itera sobre cada arquivo .txt encontrado
for txt_file in txt_files:
    file_path = os.path.join(current_directory, txt_file)
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        all_text.append(file_content.strip())  # Adiciona o conteúdo do arquivo à lista, removendo espaços em branco extras

# Escreve todos os conteúdos dos arquivos .txt em um único arquivo "faqs.txt"
with open(output_file, 'w', encoding='utf-8') as f_out:
    for text in all_text:
        f_out.write(text + '\n\n')  # Adiciona duas quebras de linha entre os conteúdos de diferentes arquivos

print(f"Arquivo 'faqs.txt' criado com sucesso contendo o conteúdo de {len(txt_files)} arquivos.")
