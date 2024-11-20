import numpy as np
from collections import Counter
import math
import csv
import time
import random
from lzw import LZWCompressor 

# funcao para calcular a entropia de shannon
def calculate_shannon_entropy(string):
    frequency = Counter(string)
    probabilities = [freq / len(string) for freq in frequency.values()]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

# geradores de strings com diferentes niveis de entropia
def generate_entropy_level_1(length):
    string1 = 'A' * int(length / 2) + 'B' + 'A' * int((length / 2) - 1)
    return string1

def generate_entropy_level_2(length):
    chars = ['A', 'B']
    return ''.join(np.random.choice(chars) for _ in range(length))

def generate_entropy_level_3(length):
    chars = ['A', 'B', 'C', 'D']
    pattern = ''.join(np.random.choice(chars) for _ in range(length // 4))
    return pattern * 4

def generate_entropy_level_4(length):
    chars = ['A', 'B', 'C', 'D', 'E', 'F']
    pattern = ''.join(np.random.choice(chars) for _ in range(length // 2))
    random_segment = ''.join(np.random.choice(chars) for _ in range(length // 2))
    return pattern + random_segment

def generate_entropy_level_5(length):
    chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    probs = [0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05]
    return ''.join(np.random.choice(chars, p=probs) for _ in range(length))

def generate_entropy_level_6(length):
    chars = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
    probs = np.random.dirichlet(np.ones(len(chars)) * 0.3)
    return ''.join(np.random.choice(chars, p=probs) for _ in range(length))

def generate_entropy_level_7(length):
    chars = [chr(i) for i in range(32, 126)]
    probs = np.random.dirichlet(np.ones(len(chars)) * 0.5)
    return ''.join(np.random.choice(chars, p=probs) for _ in range(length))

def generate_entropy_level_8(length):
    chars = [chr(i) for i in range(32, 126)]
    probs = np.full(len(chars), 1 / len(chars))
    return ''.join(np.random.choice(chars, p=probs) for _ in range(length))

def generate_entropy_level_9(length):
    ascii_chars = [chr(i) for i in range(32, 126)]
    return ''.join(np.random.choice(ascii_chars) for _ in range(length))

# lista de geradores de strings
generators = [
    generate_entropy_level_1,
    generate_entropy_level_2,
    generate_entropy_level_3,
    generate_entropy_level_4,
    generate_entropy_level_5,
    generate_entropy_level_6,
    generate_entropy_level_7,
    generate_entropy_level_8,
    generate_entropy_level_9,
]

# configuracao para salvar resultados no CSV
output_file = "lzw_analysis.csv"
fields = ["Iteration", "Entropy Level", "Input Size", "Entropy", "Compression Time (s)", "Compression Rate"]

# inicializa o arquivo CSV
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(fields)

# loop de geracao de casos e analise
iteration = 1
try:
    while True:
        # selecao do nivel de entropia e tamanho da string
        level = random.randint(1, len(generators))
        length = random.randint(100, 1000000)  # comprimento aleatorio entre 100 e 1.000.000
        generator = generators[level - 1]
        
        # gera a string e calcula a entropia
        input_string = generator(length)
        entropy = calculate_shannon_entropy(input_string)

        # compressão com LZW
        compressor = LZWCompressor()
        start_time = time.time()
        compressed_data = compressor.compress(input_string)
        end_time = time.time()
        compression_time = end_time - start_time

        # calcula a taxa de compressão
        original_size = len(input_string) * 8  # tamanho original em bits
        compressed_size = len(compressed_data) * 12  # tamanho comprimido (12 bits por codigo)
        compression_rate = compressed_size / original_size

        # salva os resultados no CSV
        with open(output_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([iteration, level, length, entropy, compression_time, compression_rate])

        # exibe no terminal
        print(f"Iteração {iteration}: Nível {level}, Tamanho {length}, Entropia {entropy:.4f}, "
              f"Tempo {compression_time:.4f}s, Taxa {compression_rate:.4f}")
        iteration += 1

except KeyboardInterrupt:
    print("\nExecução interrompida pelo usuário.")

