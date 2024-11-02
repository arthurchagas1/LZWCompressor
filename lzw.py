import argparse
import os

class TrieNode:
    def __init__(self):
        self.children = {}
        self.code = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.next_code = 256  # ASCII range for initial dictionary entries

    def insert(self, string, code):
        node = self.root
        for char in string:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.code = code

    def search(self, string):
        node = self.root
        for char in string:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node.code

class LZWCompressor:
    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.max_code = (1 << max_bits) - 1
        self.trie = Trie()
        # Initialize dictionary with ASCII
        for i in range(256):
            self.trie.insert(chr(i), i)

    def compress(self, input_data):
        result = []
        current_string = ""
        for char in input_data:
            combined_string = current_string + char
            if self.trie.search(combined_string) is not None:
                current_string = combined_string
            else:
                result.append(self.trie.search(current_string))
                if self.trie.next_code <= self.max_code:
                    self.trie.insert(combined_string, self.trie.next_code)
                    self.trie.next_code += 1
                current_string = char

        # Append last code
        if current_string:
            result.append(self.trie.search(current_string))
        return result

class LZWDecompressor:
    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.max_code = (1 << max_bits) - 1
        self.dictionary = {i: chr(i) for i in range(256)}  # Initialize with ASCII
        self.next_code = 256

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

def write_compressed_file(output_path, compressed_data):
    with open(output_path, 'wb') as f:
        for code in compressed_data:
            f.write(code.to_bytes(2, byteorder='big'))

def read_compressed_file(input_path):
    compressed_data = []
    with open(input_path, 'rb') as f:
        while byte := f.read(2):
            (code,) = int.from_bytes(byte, byteorder='big'),
            compressed_data.append(code)
    return compressed_data

def main():
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
        # Leitura do arquivo de entrada para compressão
        with open(args.input_file, 'r', encoding="utf-8") as f:
            input_data = f.read()

        compressor = LZWCompressor(max_bits=args.max_bits)
        compressed_data = compressor.compress(input_data)
        write_compressed_file(args.output_file, compressed_data)
        print(f"Arquivo comprimido salvo em: {args.output_file}")

    elif args.operation == "decompress":
        # Leitura do arquivo comprimido
        compressed_data = read_compressed_file(args.input_file)
        
        decompressor = LZWDecompressor(max_bits=args.max_bits)
        decompressed_data = decompressor.decompress(compressed_data)
        
        # Salva o conteúdo descomprimido no arquivo de saída
        with open(args.output_file, 'w', encoding="utf-8") as f:
            f.write(decompressed_data)
        print(f"Arquivo descomprimido salvo em: {args.output_file}")

if __name__ == "__main__":
    main()


