import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from math import log2
from lzw import LZWCompressor, LZWDecompressor
import random
import string
import time

# Função para carregar os dados do CSV automaticamente
@st.cache
def load_data(csv_file):
    return pd.read_csv(csv_file)

# Função para gerar texto aleatório
def generate_random_text(size):
    caracteres = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(caracteres) for _ in range(size))

# Função para calcular a entropia de um texto
def calculate_entropy(text):
    freq = Counter(text)
    total_chars = len(text)
    entropy = 0
    for count in freq.values():
        probability = count / total_chars
        entropy -= probability * log2(probability)
    return entropy

# Página Introdução
def show_introduction():
    st.title("Trabalho Prático 1 de Algoritmos II - LZW")
    st.markdown("""
    ### Arthur Rodrigues Chagas - 2022069417
    ### Lucas Dayrell de Andrade Machado - 2020035329

    #Introdução
    O Trabalho Prático 1 de Algoritmos II visa colocar em prática os conhecimentos trabalhados em sala, especialmente se referindo a uma aplicação da árovre Trie. A tarefa a ser realizada é a compressão e descompressão de arquivos utilizando o algoritmo Lempel-Ziv-Welch (LZW), que utiliza essa estrutura. Nas seções ao lado, discutiremos as implementações e alguns experimentos realizados, a fim de analisar a utilidade e aplicabilidade do algoritmo em questão.      
    """)

# Página Implementações
def show_implementations():
    st.title("Implementações")
    st.markdown("""
    ##Trie
        Para representar a árvore trie, foram criadas duas classes: uma correspondente ao nó e a outra à estrutura da árvore.
        ###Classe TrieNode
            O objetivo dessa classe é representar o nó de uma Trie direcionado para o objetivo de compressão de arquivos. Cada nó possui dois atributos:
            - `children` : um dicionário que mapeia caracteres para seus respectivos nós filhos
            - `code`: um campo que armazena o código associado a uma sequência de caracteres
        ###Classe Trie
            Essa classe implementa a estrutura da Trie compacta. Seus atributos são: 
            - `root`: o nó raiz da árvore
            - `next_code`: o próximo código disponível para ser atribuído a uma nova sequência de caracteres.
        ###Métodos
            -`insert(self, string, code)`: insere uma sequência de caracteres (string) na trie e associa a sequência com um código (code). Se nós correspondentes não existirem, eles são criados.
            -`search(self, string)`: Pesquisa se uma sequência de caracteres está inserida na árvore. Se sim, retorna o código associado. Caso contrário, retorna None.
            Ambos os métodos possuem complexidade $O(m)$, onde $m$ é o comprimento da sequência de caracteres. Isso ocorre porque, em cada operação, o código percorre cada caractere da sequência por vez.
    ##LZW Padrão
        O compressor LZW é o componente responsável por comprimir dados da entrada utilizando a trie
        ###Classe LZWCompressor
            -`__init__(self, max_bits=12)` (construtor): inicializa uma instância de compressor, configurando o número máximo de bits para o código, criando uma trie e inserindo os caracteres ASCII nela com seus respectivos códigos.
            -`compress(self, input_data)`: Realiza a compressão do texto fornecido. Para cada caractere da entrada: (1): Tenta combiná-lo com o restante da sequência já processada; (2):Se a sequência combinada já estiver na trie, o caractere é adicionado à sequência atual. (3): Caso contrário, o código da sequência existente é armazenado no resultado, e a sequência combinada é adicionada à trie com um novo código; (4): No final, o último código da sequência é adicionado ao resultado.
            A compressão possui complexidade $O(m * n)$, onde $n$ é o número de caracteres da entrada e $m$ é o comprimento da sequência inserida ou pesquisada na trie. Esse comportamento assintótico decorre da necessidade de verificar ou inserir sequências na trie, que é uma operação de tempo linear com relação ao comprimento da sequência.          
        ###Classe LZWDecompressor
            -`__init__(self, max_bits=12)` (construtor): inicializa o descompressor, criando um dicionário com os primeiros 256 códigos ASCII.
            -`decompress(self, compressed_data)`: Descomprime os dados. Para cada código: (1): Recupera a sequência correspondente ao código; (2):Se o código é o próximo disponível, a sequência é formada pelo último caractere da sequência anterior repetido; (3):Insere novas sequências no dicionário à medida que o processo avança.
            A descompressão possui a mesma complexidade assintótica da compressão, pois envolve a reconstrução das sequências a partir de código e as constantes inserções de novos pares no dicionário.
    ##Métodos de leitura e escrita de arquivos
            -`write_compressed_file(output_path, compressed_data)`: Grava os códigos comprimidos em um arquivo binário, usando 2 bytes por código.
            -`read_compressed_file(input_path)`: Lê os códigos comprimidos de um arquivo binário e os retorna como uma lista de inteiros.
            Ambos possuem complexidade $O(n)$, com $n$ sendo o número de códigos, evidentemente. Isso se deve ao fato dos métodos iterarem sobre os códigos.
                
    ##LZW Dinâmico
        ###Classe LZWCompressorDynamic
        - `__init__(self, max_bits=12)` (construtor): Inicializa o compressor. O número máximo de bits (max_bits) é configurado para o tamanho máximo de código permitido. O compressor começa com códigos de 9 bits (até 511 códigos possíveis), e a tabela de prefixos é preenchida com os códigos ASCII (0-255). O próximo código disponível (next_code) começa em 256, já que os códigos ASCII são usados inicialmente.
        - `compress(self, input_data)`: Realiza a compressão do texto de entrada, com os seguintes passos:(1)Percorre os caracteres da entrada e tenta expandir a sequência (current_string) com o próximo caractere (char).(2)Se a sequência já existe no dicionário, continua a expandir a sequência.(3)Caso contrário, armazena o código da sequência atual no resultado e insere a nova sequência no dicionário.(4)Se o dicionário atinge o limite de códigos (determinado pelo número de bits), o número de bits usados para os códigos é aumentado, ajustando a variável current_bits. (5)Ao final, o código adiciona o código da última sequência ao resultado.
        ###Classe LZWDecompressorDynamic
        - `__init__(self, max_bits=12)` (construtor): Inicializa o compressor. Os parâmetros e fucnionamento da inicialização são análogos ao do compressor.
        -`decompress(self, input_data)`: Descomprime a entrada da seguinte forma: (1)Recupera a sequência correspondente ao primeiro código da entrada; (2)Para cada código subsequente: Se o código estiver no dicionário, recupera a sequência correspondente; Se o código for igual ao próximo código esperado, a sequência é formada pelo caractere repetido da sequência anterior; Caso contrário, lança um erro; (3)Insere as novas sequências no dicionário à medida que são processadas; (4)Se o número de códigos exceder o limite, o número de bits usados para os códigos é incrementado; (5)O resultado final é reconstruído e retornado como uma string;
        
        ###Funções de leitura e escrita: 
        São análogas às anteriores. `write_compressed_file(output_path, compressed_data, max_bits)` Grava os dados comprimidos em um arquivo binário, salvando também o número de bits usado para os códigos. `read_compressed_file(input_path)` faz o mesmo do anterior, levando em conta o número de bits utilizados.
    ##Considerações
        Podemos afirmar que a implementação dinâmica tem a vantagem de ajustar automaticamente o número de bits conforme necessário (até um máximo), enquanto a implementação estática usa um número fixo de bits para representar os códigos. Isso torna o algoritmo dinâmico mais flexível, especialmente lidando com dados de tamanho variado. Cabe frisar, no entanto, que essa implementação pode ser mais lenta dependendo do caso pela presença do custo de atualizar o número de bits e verificar a necessidade de ajustar.
    """)

# Página Relatório - Testes e Gráficos (LZW Padrão)
def show_report():
    st.title("Relatório de Comportamento do Algoritmo LZW (Padrão)")
    st.markdown("""
    ## Testes e Gráficos
    Nesta seção, apresentamos os dados coletados a partir dos testes automáticos do algoritmo de compressão LZW.
    """)

    # Carrega os dados do CSV automaticamente
    csv_file = "lzw_analysis.csv"  # Nome do arquivo no diretório
    try:
        data = load_data(csv_file)
        
        # Exibe o DataFrame
        st.write("### Dados do CSV")
        st.write(data)
        
        # Gráfico 1: Tamanho Original x Taxa de Compressão
        st.write("### Tamanho Original vs. Taxa de Compressão")
        fig, ax = plt.subplots()
        ax.plot(data["Input Size"], label="Tamanho Original", marker="o", linestyle="--")
        ax.plot(data["Compression Rate"], label="Taxa de Compressão", marker="x")
        ax.set_xlabel("Casos")
        ax.set_ylabel("Tamanho / Taxa")
        ax.set_title("Comparação de Tamanho e Taxa de Compressão")
        ax.legend()
        st.pyplot(fig)
        
        # Gráfico 2: Tempo de Compressão
        st.write("### Tempo de Compressão por Caso")
        fig, ax = plt.subplots()
        ax.plot(data["Compression Time (s)"], label="Tempo de Compressão (s)", color="green", marker="o")
        ax.set_xlabel("Casos")
        ax.set_ylabel("Tempo (s)")
        ax.set_title("Tempo de Compressão por Caso")
        st.pyplot(fig)
        
        # Gráfico 3: Entropia
        st.write("### Entropia por Nível de Entrada")
        fig, ax = plt.subplots()
        ax.scatter(data["Entropy Level"], data["Entropy"], label="Entropia", color="blue")
        ax.set_xlabel("Nível de Entropia")
        ax.set_ylabel("Entropia")
        ax.set_title("Entropia por Nível de Entrada")
        st.pyplot(fig)

        # Calcular a eficiência da compressão em porcentagens
        data["Compression Efficiency (%)"] = (1 - data["Compression Rate"]) * 100

        # Gráfico: Entropia x Eficiência de Compressão (%)
        st.write("### Relação entre Entropia e Eficiência de Compressão (%)")
        fig, ax = plt.subplots()
        ax.scatter(data["Entropy"], data["Compression Efficiency (%)"], c='green', alpha=0.7, edgecolors='w', s=80)
        ax.set_xlabel("Entropia")
        ax.set_ylabel("Eficiência de Compressão (%)")
        ax.set_title("Relação entre Entropia e Eficiência de Compressão (%)")
        ax.grid(True)
        st.pyplot(fig)

        # Gráfico Interativo (Streamlit Native)
        st.write("### Gráfico Interativo: Input Size vs. Compression Rate")
        st.line_chart(data[["Input Size", "Compression Rate"]])
        
        # Estatísticas Descritivas
        st.write("### Estatísticas Descritivas dos Dados")
        st.write(data.describe())
        
    except FileNotFoundError:
        st.error(f"O arquivo '{csv_file}' não foi encontrado no diretório do aplicativo.")

# Página Relatório - Testes e Gráficos (LZW Dinâmico)
def show_dynamic_report():
    st.title("Relatório de Comportamento do Algoritmo LZW (Dinâmico)")
    st.markdown("""
    ## Testes e Gráficos
    Nesta seção, apresentamos os dados coletados a partir dos testes automáticos do algoritmo de compressão LZW Dinâmico.
    """)

    # Carrega os dados do CSV automaticamente
    csv_file = "lzw_dynamic_analysis.csv"  # Nome do arquivo dinâmico no diretório
    try:
        data = load_data(csv_file)
        
        # Exibe o DataFrame
        st.write("### Dados do CSV")
        st.write(data)
        
        # Gráfico 1: Tamanho Original x Taxa de Compressão
        st.write("### Tamanho Original vs. Taxa de Compressão")
        fig, ax = plt.subplots()
        ax.plot(data["Input Size"], label="Tamanho Original", marker="o", linestyle="--")
        ax.plot(data["Compression Rate"], label="Taxa de Compressão", marker="x")
        ax.set_xlabel("Casos")
        ax.set_ylabel("Tamanho / Taxa")
        ax.set_title("Comparação de Tamanho e Taxa de Compressão")
        ax.legend()
        st.pyplot(fig)
        
        # Gráfico 2: Tempo de Compressão
        st.write("### Tempo de Compressão por Caso")
        fig, ax = plt.subplots()
        ax.plot(data["Compression Time (s)"], label="Tempo de Compressão (s)", color="green", marker="o")
        ax.set_xlabel("Casos")
        ax.set_ylabel("Tempo (s)")
        ax.set_title("Tempo de Compressão por Caso")
        st.pyplot(fig)
        
        # Gráfico 3: Entropia
        st.write("### Entropia por Nível de Entrada")
        fig, ax = plt.subplots()
        ax.scatter(data["Entropy Level"], data["Entropy"], label="Entropia", color="blue")
        ax.set_xlabel("Nível de Entropia")
        ax.set_ylabel("Entropia")
        ax.set_title("Entropia por Nível de Entrada")
        st.pyplot(fig)

        # Calcular a eficiência da compressão em porcentagens
        data["Compression Efficiency (%)"] = (1 - data["Compression Rate"]) * 100

        # Gráfico: Entropia x Eficiência de Compressão (%)
        st.write("### Relação entre Entropia e Eficiência de Compressão (%)")
        fig, ax = plt.subplots()
        ax.scatter(data["Entropy"], data["Compression Efficiency (%)"], c='blue', alpha=0.7, edgecolors='w', s=80)
        ax.set_xlabel("Entropia")
        ax.set_ylabel("Eficiência de Compressão (%)")
        ax.set_title("Relação entre Entropia e Eficiência de Compressão (%)")
        ax.grid(True)
        st.pyplot(fig)

        # Gráfico Interativo (Streamlit Native)
        st.write("### Gráfico Interativo: Input Size vs. Compression Rate")
        st.line_chart(data[["Input Size", "Compression Rate"]])
        
        # Estatísticas Descritivas
        st.write("### Estatísticas Descritivas dos Dados")
        st.write(data.describe())
        
    except FileNotFoundError:
        st.error(f"O arquivo '{csv_file}' não foi encontrado no diretório do aplicativo.")

# Página Interativa - Teste de Compressão e Descompressão
def show_interactive_page():
    st.title("Documentação Interativa do Algoritmo de Compressão LZW")
    st.markdown("""
    ## Introdução
    Este site interativo apresenta a documentação do algoritmo Lempel-Ziv-Welch (LZW), explorando seu funcionamento, 
    etapas de compressão e descompressão, e exemplos de uso.
    """)

    # Inicializar variáveis de sessão
    if 'attempts' not in st.session_state:
        st.session_state['attempts'] = []
    if 'compressed_data' not in st.session_state:
        st.session_state['compressed_data'] = None
    if 'generated_text' not in st.session_state:
        st.session_state['generated_text'] = ""

    # Parâmetros de Configuração
    st.markdown("### Parâmetros de Configuração")
    max_bits = st.slider("Número máximo de bits", min_value=9, max_value=16, value=12)

    st.markdown("### Gerador de Texto Aleatório")
    text_size = st.slider("Tamanho do Texto Aleatório", min_value=100, max_value=5000, value=1000)
    if st.button("Gerar Texto Aleatório"):
        # Gerar o texto aleatório com o tamanho especificado
        generated_text = generate_random_text(text_size)
        st.session_state['generated_text'] = generated_text
        st.text_area("Texto Gerado", generated_text, height=200)
        
        # Calcular a entropia do texto gerado
        entropy_value = calculate_entropy(generated_text)
        st.write(f"**Entropia do Texto Gerado:** {entropy_value:.4f} bits")

    st.markdown("### Teste Interativo de Compressão e Descompressão")
    input_text = st.text_area("Digite o texto para compressão", st.session_state['generated_text'] if st.session_state['generated_text'] else "ABABABABAABABABABABA")

    # Inicialize o compressor e o decompressor antes dos botões
    compressor = LZWCompressor(max_bits=max_bits)
    decompressor = LZWDecompressor(max_bits=max_bits)

    # Botão de compressão
    if st.button("Comprimir"):
        start_time = time.time()
        compressed_data = compressor.compress(input_text)
        end_time = time.time()
        
        # Calcular métricas
        input_size = len(input_text)
        compressed_size = len(compressed_data)
        compression_ratio = compressed_size / input_size if input_size > 0 else 0
        execution_time = end_time - start_time
        
        # Calcular a entropia do texto comprimido
        entropy_value = calculate_entropy(input_text)
        
        # Exibir resultados
        st.write("**Dados Comprimidos:**", compressed_data)
        st.write(f"**Taxa de Compressão:** {compression_ratio:.2f}")
        st.write(f"**Tempo de Execução:** {execution_time:.4f} segundos")
        st.write(f"**Entropia do Texto:** {entropy_value:.4f} bits")
        
        # Armazenar dados na sessão
        st.session_state['attempts'].append({
            'operation': 'Compressão',
            'input_size': input_size,
            'output_size': compressed_size,
            'compression_ratio': compression_ratio,
            'execution_time': execution_time,
            'entropy': entropy_value
        })
        
        # Salva o texto comprimido na sessão para permitir descompressão
        st.session_state['compressed_data'] = compressed_data

    # Botão de descompressão
    if st.button("Descomprimir") and st.session_state['compressed_data'] is not None:
        start_time = time.time()
        decompressed_data = decompressor.decompress(st.session_state['compressed_data'])
        end_time = time.time()
        
        execution_time = end_time - start_time
        output_size = len(decompressed_data)
        input_size = len(st.session_state['compressed_data'])
        
        # Calcular a entropia do texto descomprimido
        entropy_value = calculate_entropy(decompressed_data)
        
        st.write("**Texto Descomprimido:**", decompressed_data)
        st.write(f"**Tamanho do Texto Descomprimido:** {output_size}")
        st.write(f"**Tempo de Execução:** {execution_time:.4f} segundos")
        st.write(f"**Entropia do Texto Descomprimido:** {entropy_value:.4f} bits")
        
        # Armazenar dados na sessão
        st.session_state['attempts'].append({
            'operation': 'Descompressão',
            'input_size': input_size,
            'output_size': output_size,
            'execution_time': execution_time,
            'entropy': entropy_value
        })

    st.markdown("### Histórico de Tentativas e Estatísticas")

    if st.session_state['attempts']:
        # Converter a lista de tentativas em um DataFrame
        df = pd.DataFrame(st.session_state['attempts'])
        
        # Exibir tabela com todas as tentativas
        st.write("#### Tabela de Tentativas")
        st.write(df)
# Página Conclusões
def show_conclusions():
    st.title("Conclusões")
    st.markdown("""
    **Preencha esta seção com suas conclusões e análises finais.**
    """)

# Configuração do menu lateral para navegação
page = st.sidebar.radio("Escolha uma página", ("Introdução", "Implementações","Testes do LZW Padrão", "Testes do LZW Dinâmico", "Teste Interativo", "Conclusões"))

if page == "Introdução":
    show_introduction()
elif page == "Implementações":
    show_implementations()
elif page == "Relatório LZW Padrão":
    show_report()
elif page == "Relatório LZW Dinâmico":
    show_dynamic_report()
elif page == "Teste Interativo":
    show_interactive_page()
elif page == "Conclusões":
    show_conclusions()
    

