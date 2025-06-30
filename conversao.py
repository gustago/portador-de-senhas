import csv
import re

def adicionar_protocolo_https(url):
    """
    Adiciona https:// no início da URL se não houver protocolo
    """
    if not url:
        return url
    
    # Remove espaços em branco
    url = url.strip()
    
    # Verifica se já tem http:// ou https://
    if url.startswith('http://') or url.startswith('https://'):
        return url
    
    # Adiciona https:// no início
    return f'https://{url}'

def converter_txt_para_csv(arquivo_txt, arquivo_csv):
    """
    Converte senhas do formato txt para o formato csv
    """
    senhas = []
    
    # Ler o arquivo txt
    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Dividir por entradas (separadas por "---")
    entradas = conteudo.split('---')
    
    for entrada in entradas:
        entrada = entrada.strip()
        if not entrada or entrada == 'Websites':
            continue
            
        # Extrair informações usando regex
        nome_match = re.search(r'Website name:\s*(.+)', entrada)
        url_match = re.search(r'Website URL:\s*(.+)', entrada)
        login_match = re.search(r'Login:\s*(.+)', entrada)
        senha_match = re.search(r'Password:\s*(.+)', entrada)
        comentario_match = re.search(r'Comment:\s*(.+)', entrada)
        
        # Extrair valores
        nome = nome_match.group(1).strip() if nome_match else ''
        url = url_match.group(1).strip() if url_match else ''
        login = login_match.group(1).strip() if login_match else ''
        senha = senha_match.group(1).strip() if senha_match else ''
        comentario = comentario_match.group(1).strip() if comentario_match else ''
        
        # Adicionar https:// se necessário
        url = adicionar_protocolo_https(url)
        
        # Adicionar à lista se tiver pelo menos nome e URL
        if nome and url:
            senhas.append({
                'name': nome,
                'url': url,
                'username': login,
                'password': senha,
                'note': comentario
            })
    
    # Escrever no arquivo csv
    with open(arquivo_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'url', 'username', 'password', 'note']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Escrever cabeçalho
        writer.writeheader()
        
        # Escrever dados
        for senha in senhas:
            writer.writerow(senha)
    
    print(f"Conversão concluída! {len(senhas)} senhas foram convertidas.")
    print(f"Arquivo salvo como: {arquivo_csv}")
