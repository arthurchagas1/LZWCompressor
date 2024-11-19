import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from lzw import LZWCompressor, LZWDecompressor 
import random
import string
from collections import Counter
from math import log2

# Função para gerar texto aleatório
def generate_random_text(size):
    caracteres = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(caracteres) for _ in range(size))

# Função para calcular a entropia de um texto
def calculate_entropy(text):
    # Contagem de ocorrências de cada caractere
    freq = Counter(text)
    total_chars = len(text)
    
    # Cálculo da entropia de Shannon
    entropy = 0
    for count in freq.values():
        probability = count / total_chars
        entropy -= probability * log2(probability)
    
    return entropy

# Página Relatório - Testes manuais e explicações
def show_report():
    st.title("Relatório de Comportamento do Algoritmo LZW")
    st.markdown("""
    ## Testes e Exemplos
    Nesta seção, descrevo os testes realizados manualmente para observar o comportamento do algoritmo de compressão LZW.
    
    ### Teste 1: Compressão de Texto com Repetição
    O algoritmo LZW é muito eficiente quando os dados de entrada contêm sequências repetitivas. Por exemplo, ao comprimir o texto:
    `ABABABABABAABABABABABA`
    o algoritmo identifica padrões e os codifica eficientemente. A expectativa é que o arquivo comprimido seja significativamente menor.
    
    ### Teste 2: Compressão de Texto Aleatório
    Quando o texto é aleatório e não contém padrões, o algoritmo pode não ser tão eficiente, pois não há repetições a serem exploradas. Um exemplo seria a string gerada aleatoriamente:
    `g7d!@#$%uY7*sdfse&*^%&&U`.
    
    ### Teste 3: Compressão de Texto com Diversidade
    O comportamento do algoritmo também é interessante em textos como: 
    `Lorem ipsum dolor sit amet, consectetur adipiscing elit.`
    Este tipo de entrada contém tanto repetições quanto diversidade, e o algoritmo deve equilibrar esses fatores para otimizar a compressão.
    
    ## Conclusões
    Os testes realizados demonstram que o LZW é eficiente em lidar com dados repetitivos, mas pode não oferecer grandes vantagens em dados aleatórios. A análise da entropia do texto também foi uma ferramenta útil para entender o comportamento da compressão.
    """)

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

