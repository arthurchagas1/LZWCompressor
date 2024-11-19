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

# Página Relatório - Testes e Gráficos
def show_report():
    st.title("Relatório de Comportamento do Algoritmo LZW")
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

# Configuração do menu lateral para navegação
page = st.sidebar.radio("Escolha uma página", ("Relatório", "Teste Interativo"))

if page == "Relatório":
    show_report()
else:
    show_interactive_page()

