import streamlit as st
import time
from io import StringIO
from lzw import LZWCompressor, LZWDecompressor  # Certifique-se de que o módulo está no mesmo diretório ou ajuste o caminho

st.title("Documentação Interativa do Algoritmo de Compressão LZW")
st.markdown("""
## Introdução
Este site interativo apresenta a documentação do algoritmo Lempel-Ziv-Welch (LZW), explorando seu funcionamento, 
etapas de compressão e descompressão, e exemplos de uso.

### Como o LZW Funciona
O algoritmo LZW é uma técnica de compressão baseada em dicionário que substitui sequências repetitivas por códigos 
mais compactos, reduzindo o espaço necessário para armazenar dados.
""")

st.markdown("### Parâmetros de Configuração")
max_bits = st.slider("Número máximo de bits", min_value=9, max_value=16, value=12)

st.markdown("### Teste Interativo de Compressão e Descompressão")
input_text = st.text_area("Digite o texto para compressão", "ABABABABAABABABABABA")

if st.button("Comprimir"):
    compressor = LZWCompressor(max_bits=max_bits)
    compressed_data = compressor.compress(input_text)
    st.write("Dados Comprimidos:", compressed_data)

    # Salva o texto comprimido para possível descompressão
    st.session_state['compressed_data'] = compressed_data

if st.button("Descomprimir") and 'compressed_data' in st.session_state:
    decompressor = LZWDecompressor(max_bits=max_bits)
    decompressed_data = decompressor.decompress(st.session_state['compressed_data'])
    st.write("Texto Descomprimido:", decompressed_data)

st.markdown("### Análise de Estatísticas de Compressão")

if st.button("Analisar Compressão"):
    start_time = time.time()
    compressed_data = compressor.compress(input_text)
    end_time = time.time()
    
    compression_ratio = len(compressed_data) / len(input_text) if len(input_text) > 0 else 0
    st.write("Taxa de Compressão:", compression_ratio)
    st.write("Tempo de Execução:", end_time - start_time, "segundos")
