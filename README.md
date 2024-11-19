## LZW Compressor

## Index
[English](#english)
[Português](#portugues)

# English

# Português

## Descrição

Este projeto implementa o algoritmo de compressão LZW com suporte para tamanho de código dinâmico e um gerador de casos para análise de desempenho, entropia e eficiência da compressão.

O projeto consiste em:

• Implementação do LZW com tamanho de código dinâmico.
• Geradores de strings com diferentes níveis de entropia para análise.
• Ferramentas para medir tempo de compressão, taxa de compressão e entropia.
• Resultados salvos automaticamente em arquivos CSV para análise posterior.

## Uso Remoto (site)

• Acesse [Este Link](inserir link)

## Instalação Local

• Clone o repositório: 
git clone github.com/arthurchagas1/LZWCompressor/

• Instale os requisitos, se necessário:
pip install requisito

## Uso Local

• Execute o arquivo:
python (lzw.py ou dynamic.py) (compress ou decompress) (arquivo de entrada) (arquivo de saida) (max_bits *opcional)

• Para usar o gerador automatico de testes, execute:
python (cases.py ou cases_dynamic.py)
O arquivo com os testes será um CSV e estará no diretório do programa

