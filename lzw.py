import argparse
import os

# definicao do no da trie
class TrieNode:
    def __init__(self):
        self.children = {}
        self.code = None


class Trie:
    
    # inicializa a trie para armazenar as sequencias de caracteres
    def __init__(self):
        self.root = TrieNode()
        # armazena o proximo codigo disponivel para novas entradas
        self.next_code = 256  
    
    # insere uma string na trie atribuindo o codigo a ultima letra
    # complexidade O(m), onde m e o tamanho da sequencia inserida
    def insert(self, string, code):
        node = self.root
        for char in string:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.code = code
    
    # pesquisa uma string na trie e retorna o codigo associado, se encontrado. retorna None se nao existir
    # complexidade O(m), onde m e o tamanho da sequencia pesquisada
    def search(self, string):
        node = self.root
        for char in string:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node.code

class LZWCompressor:
    
    # configura o compressor e insere todos os caracteres ASCII no dicionario
    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.max_code = (1 << max_bits) - 1
        self.trie = Trie()
        # Initialize dictionary with ASCII
        for i in range(256):
            self.trie.insert(chr(i), i)
    
    # itera pelo arquivo de entrada para gerar uma lista de codigos comprimidos
    # complexidade O(n.m), onde n e o numero de caracteres no texto e m o comprimento medio da sequencia pesquisada ou inserida
    def compress(self, input_data):
        result = []
        current_string = ""
        for char in input_data:
            combined_string = current_string + char
            if self.trie.search(combined_string) is not None:
                current_string = combined_string
            else:
                # Verificação adicionada
                code = self.trie.search(current_string)
                if code is None:
                    raise ValueError(f"Erro: Sequência inválida encontrada: {current_string}")
                
                result.append(code)
                if self.trie.next_code <= self.max_code:
                    self.trie.insert(combined_string, self.trie.next_code)
                    self.trie.next_code += 1
                current_string = char

        # Append last code
        if current_string:
            code = self.trie.search(current_string)
            if code is None:
                raise ValueError(f"Erro: Sequência inválida encontrada no final: {current_string}")
            result.append(code)
        return result

class LZWDecompressor:
    
    # inicializa o descompressor com o dicionario ASCII inicial
    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.max_code = (1 << max_bits) - 1
        self.dictionary = {i: chr(i) for i in range(256)}  # Initialize with ASCII
        self.next_code = 256

    # le os codigos comprimidos e reconstroi o texto original
    # complexidade O(n.m), onde n e o numero de codigos e m e o comprimento medio da sequencia reconstruida
    def decompress(self, compressed_data):
        current_string = self.dictionary[compressed_data[0]]
        decompressed_data = [current_string]
        for code in compressed_data[1:]:
            if code in self.dictionary:
                entry = self.dictionary[code]
            elif code == self.next_code:
                entry = current_string + current_string[0]
            else:
                raise ValueError("Invalid LZW code")

            decompressed_data.append(entry)
            if self.next_code <= self.max_code:
                self.dictionary[self.next_code] = current_string + entry[0]
                self.next_code += 1
            current_string = entry

        return ''.join(decompressed_data)

# salva os codigos comprimidos em um arquivo binario
# complexidade O(n), onde n e o numero de codigos
def write_compressed_file(output_path, compressed_data):
    with open(output_path, 'wb') as f:
        for code in compressed_data:
            f.write(code.to_bytes(2, byteorder='big'))

# le codigos comprimidos de um arquivo binario e os retorna como inteiros
# complexidade O(n), onde n e o numero de codigos no arquivo
def read_compressed_file(input_path):
    compressed_data = []
    with open(input_path, 'rb') as f:
        while byte := f.read(2):
            (code,) = int.from_bytes(byte, byteorder='big'),
            compressed_data.append(code)
    return compressed_data

def main():
    
    # recebe os argumentos de entrada para a execucao do codigo
    parser = argparse.ArgumentParser(description="LZW Compression/Decompression Tool")
    parser.add_argument("operation", choices=["compress", "decompress"], help="Operation to perform")
    parser.add_argument("input_file", type=str, help="Path to input file")
    parser.add_argument("output_file", type=str, help="Path to output file")
    parser.add_argument("--max_bits", type=int, default=12, help="Maximum number of bits (default: 12)")

    args = parser.parse_args()
    
    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        return

    if args.operation == "compress":
        
        # leitura do arquivo de entrada para compressão
        with open(args.input_file, 'rb') as f:
            input_data = f.read().decode('latin1')  # suporte para dados binários

        compressor = LZWCompressor(max_bits=args.max_bits)
        compressed_data = compressor.compress(input_data)
        write_compressed_file(args.output_file, compressed_data)
        print(f"Arquivo comprimido salvo em: {args.output_file}")

    elif args.operation == "decompress":
        
        # leitura do arquivo comprimido
        compressed_data = read_compressed_file(args.input_file)
        
        decompressor = LZWDecompressor(max_bits=args.max_bits)
        decompressed_data = decompressor.decompress(compressed_data)
        
        # salva o conteúdo descomprimido no arquivo de saída
        with open(args.output_file, 'w', encoding="latin1") as f:
            f.write(decompressed_data)
        print(f"Arquivo descomprimido salvo em: {args.output_file}")

if __name__ == "__main__":
    main()

