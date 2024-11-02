import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from lzw import LZWCompressor, LZWDecompressor  # Ajuste o caminho conforme necessário

# Inicializar variáveis de sessão
if 'attempts' not in st.session_state:
    st.session_state['attempts'] = []
if 'compressed_data' not in st.session_state:
    st.session_state['compressed_data'] = None

st.title("Documentação Interativa do Algoritmo de Compressão LZW")
st.markdown("""
## Introdução
Este site interativo apresenta a documentação do algoritmo Lempel-Ziv-Welch (LZW), explorando seu funcionamento, 
etapas de compressão e descompressão, e exemplos de uso.
""")

st.markdown("### Parâmetros de Configuração")
max_bits = st.slider("Número máximo de bits", min_value=9, max_value=16, value=12)

st.markdown("### Teste Interativo de Compressão e Descompressão")
input_text = st.text_area("Digite o texto para compressão", "ABABABABAABABABABABA")

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
    
    # Exibir resultados
    st.write("**Dados Comprimidos:**", compressed_data)
    st.write(f"**Taxa de Compressão:** {compression_ratio:.2f}")
    st.write(f"**Tempo de Execução:** {execution_time:.4f} segundos")
    
    # Armazenar dados na sessão
    st.session_state['attempts'].append({
        'operation': 'Compressão',
        'input_size': input_size,
        'output_size': compressed_size,
        'compression_ratio': compression_ratio,
        'execution_time': execution_time
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
    
    st.write("**Texto Descomprimido:**", decompressed_data)
    st.write(f"**Tamanho do Texto Descomprimido:** {output_size}")
    st.write(f"**Tempo de Execução:** {execution_time:.4f} segundos")
    
    # Armazenar dados na sessão
    st.session_state['attempts'].append({
        'operation': 'Descompressão',
        'input_size': input_size,
        'output_size': output_size,
        'execution_time': execution_time
    })

st.markdown("### Histórico de Tentativas e Estatísticas")

if st.session_state['attempts']:
    # Converter a lista de tentativas em um DataFrame
    df = pd.DataFrame(st.session_state['attempts'])
    
    # Exibir tabela com todas as tentativas
    st.write("#### Tabela de Tentativas")
    st.write(df)
    
    # Função para plotar gráficos personalizados com regressão linear e cor dos pontos
    def plot_with_regression(x, y, color, x_label, y_label, title):
        plt.figure(figsize=(10, 5))
        
        # Scatter plot com cor representando o tamanho da entrada
        scatter = plt.scatter(x, y, c=color, cmap="viridis", alpha=0.6, edgecolors="w", s=50, label=y_label)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.colorbar(scatter, label="Tamanho da Entrada")
        
        # Ajuste da regressão linear
        x = np.array(x).reshape(-1, 1)
        y = np.array(y)
        model = LinearRegression()
        model.fit(x, y)
        y_pred = model.predict(x)
        
        plt.plot(x, y_pred, color="red", linewidth=2, label="Regressão Linear")  # Linha de regressão em vermelho
        plt.legend()
        st.pyplot(plt)

    # Análise 1: Taxa de Compressão vs. Tamanho de Entrada
    st.write("#### Análise: Taxa de Compressão vs. Tamanho de Entrada")
    plot_with_regression(
        x=df['input_size'],
        y=df['compression_ratio'],
        color=df['input_size'],
        x_label="Tamanho da Entrada",
        y_label="Taxa de Compressão",
        title="Taxa de Compressão vs. Tamanho de Entrada"
    )

    # Análise 2: Tempo de Execução vs. Tamanho de Entrada
    st.write("#### Análise: Tempo de Execução vs. Tamanho de Entrada")
    plot_with_regression(
        x=df['input_size'],
        y=df['execution_time'],
        color=df['input_size'],
        x_label="Tamanho da Entrada",
        y_label="Tempo de Execução (s)",
        title="Tempo de Execução vs. Tamanho de Entrada"
    )
    
    # Análise 3: Comparação entre Compressão e Descompressão
    df_compress = df[df['operation'] == 'Compressão']
    df_decompress = df[df['operation'] == 'Descompressão']
    if not df_compress.empty and not df_decompress.empty:
        st.write("#### Comparação: Tempo de Execução entre Compressão e Descompressão")
        
        plt.figure(figsize=(10, 5))
        plt.scatter(df_compress['input_size'], df_compress['execution_time'], color="blue", label="Compressão")
        plt.scatter(df_decompress['input_size'], df_decompress['execution_time'], color="green", label="Descompressão")
        plt.xlabel("Tamanho da Entrada")
        plt.ylabel("Tempo de Execução (s)")
        plt.title("Comparação do Tempo de Execução entre Compressão e Descompressão")
        plt.legend()
        st.pyplot(plt)
    
    # Análise 4: Evolução da Taxa de Compressão por Tentativa
    st.write("#### Análise: Evolução da Taxa de Compressão ao Longo das Tentativas")
    plot_with_regression(
        x=df.index + 1,
        y=df['compression_ratio'],
        color=df['input_size'],
        x_label="Tentativa",
        y_label="Taxa de Compressão",
        title="Evolução da Taxa de Compressão"
    )

    # Cálculo das médias e exibição
    avg_compression_ratio = df_compress['compression_ratio'].mean()
    avg_execution_time_compress = df_compress['execution_time'].mean()
    avg_execution_time_decompress = df_decompress['execution_time'].mean() if not df_decompress.empty else None
    
    st.write("### Médias das Análises")
    st.write(f"**Taxa de Compressão Média (Compressão):** {avg_compression_ratio:.2f}")
    st.write(f"**Tempo de Execução Médio (Compressão):** {avg_execution_time_compress:.4f} segundos")
    if avg_execution_time_decompress:
        st.write(f"**Tempo de Execução Médio (Descompressão):** {avg_execution_time_decompress:.4f} segundos")
