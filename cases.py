import numpy as np
from collections import Counter
import math

def calculate_shannon_entropy(string):
    # Calcula a entropia de Shannon para uma string
    frequency = Counter(string)
    probabilities = [freq / len(string) for freq in frequency.values()]
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy

def generate_entropy_level_1(length):
    # Nível 1: Muito baixa entropia (um único caractere diferente entre vários iguais)
    string1 = 'A' * int(length/2) + 'B' + 'A' * int((length/2) - 1)
    return string1

def generate_entropy_level_2(length):
    # Nível 2: Baixa entropia (dois caracteres)
    chars = ['A', 'B']
    return ''.join(np.random.choice(chars) for _ in range(length))

def generate_entropy_level_3(length):
    # Nível 3: Média-baixa entropia (quatro caracteres com padrão)
    chars = ['A', 'B', 'C', 'D']
    pattern = ''.join(np.random.choice(chars) for _ in range(length // 4))
    return pattern * 4

def generate_entropy_level_4(length):
    # Nível 4: Média entropia (seis caracteres com mistura de repetição e aleatoriedade)
    chars = ['A', 'B', 'C', 'D', 'E', 'F']
    pattern = ''.join(np.random.choice(chars) for _ in range(length // 2))
    random_segment = ''.join(np.random.choice(chars) for _ in range(length // 2))
    return pattern + random_segment

def generate_entropy_level_5(length):
    # Nível 5: Média-alta entropia (grande diversidade com alguns caracteres mais frequentes)
    chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    probs = [0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05]  # Distribuição não uniforme
    return ''.join(np.random.choice(chars, p=probs) for _ in range(length))

def generate_entropy_level_6(length):
    # Nível 6: Entropia moderadamente alta, alvo entre 4 e 5 (ASCII limitado, não uniforme)
    chars = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]  # Letras maiúsculas e minúsculas
    probs = np.random.dirichlet(np.ones(len(chars)) * 0.3)  # Distribuição levemente não uniforme
    return ''.join(np.random.choice(chars, p=probs) for _ in range(length))

def generate_entropy_level_7(length):
    # Nível 7: Alta entropia (letras, dígitos, e símbolos ASCII com leve distribuição não uniforme)
    chars = [chr(i) for i in range(32, 126)]  # Conjunto ASCII imprimível
    probs = np.random.dirichlet(np.ones(len(chars)) * 0.5)  # Distribuição não uniforme leve
    return ''.join(np.random.choice(chars, p=probs) for _ in range(length))

def generate_entropy_level_8(length):
    # Nível 8: Alta entropia (ASCII imprimível com probabilidade quase uniforme)
    chars = [chr(i) for i in range(32, 126)]
    probs = np.full(len(chars), 1 / len(chars))  # Probabilidade uniforme aproximada
    return ''.join(np.random.choice(chars, p=probs) for _ in range(length))

def generate_entropy_level_9(length):
    # Nível 9: Muito alta entropia (ASCII imprimível com probabilidade uniforme)
    ascii_chars = [chr(i) for i in range(32, 126)]
    return ''.join(np.random.choice(ascii_chars) for _ in range(length))

# Parâmetros
length = 100  # Tamanho da string

# Gera strings para cada nível de entropia e calcula suas entropias
levels = [
    generate_entropy_level_1,
    generate_entropy_level_2,
    generate_entropy_level_3,
    generate_entropy_level_4,
    generate_entropy_level_5,
    generate_entropy_level_6,
    generate_entropy_level_7,
    generate_entropy_level_8,
    generate_entropy_level_9
]

for i, level_func in enumerate(levels, start=1):
    string = level_func(length)
    entropy = calculate_shannon_entropy(string)
    print(f"String de entropia nível {i}: {string}")
    print(f"Entropia de Shannon (Nível {i}): {entropy}\n")
