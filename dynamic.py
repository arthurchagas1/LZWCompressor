class LZWCompressorDynamic:
    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.current_bits = 9  # Tamanho inicial do código
        self.max_code = (1 << self.current_bits) - 1
        self.trie = {}
        for i in range(256):  # Inicializa a tabela com códigos ASCII
            self.trie[chr(i)] = i
        self.next_code = 256  # Primeiro código disponível após ASCII

    def compress(self, input_data):
        result = []
        current_string = ""
        
        for char in input_data:
            combined_string = current_string + char
            if combined_string in self.trie:
                current_string = combined_string
            else:
                # Salva o código do padrão atual
                result.append(self.trie[current_string])

                # Insere o novo padrão no dicionário
                if self.next_code <= self.max_code:
                    self.trie[combined_string] = self.next_code
                    self.next_code += 1

                # Atualiza o número de bits se necessário
                if self.next_code > self.max_code and self.current_bits < self.max_bits:
                    self.current_bits += 1
                    self.max_code = (1 << self.current_bits) - 1

                current_string = char

        # Salva o último padrão
        if current_string:
            result.append(self.trie[current_string])

        return result, self.current_bits


class LZWDecompressorDynamic:
    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.current_bits = 9  # Tamanho inicial do código
        self.max_code = (1 << self.current_bits) - 1
        self.dictionary = {i: chr(i) for i in range(256)}  # Inicializa a tabela com códigos ASCII
        self.next_code = 256

    def decompress(self, compressed_data):
        result = []
        current_string = self.dictionary[compressed_data[0]]
        result.append(current_string)

        for code in compressed_data[1:]:
            if code in self.dictionary:
                entry = self.dictionary[code]
            elif code == self.next_code:
                entry = current_string + current_string[0]
            else:
                raise ValueError("Código inválido durante a descompressão.")

            result.append(entry)

            # Adiciona a nova entrada no dicionário
            if self.next_code <= self.max_code:
                self.dictionary[self.next_code] = current_string + entry[0]
                self.next_code += 1

            # Atualiza o número de bits se necessário
            if self.next_code > self.max_code and self.current_bits < self.max_bits:
                self.current_bits += 1
                self.max_code = (1 << self.current_bits) - 1

            current_string = entry

        return ''.join(result)


# Funções auxiliares para salvar e carregar arquivos comprimidos
def write_compressed_file(output_path, compressed_data, max_bits):
    with open(output_path, 'wb') as f:
        f.write(max_bits.to_bytes(1, byteorder='big'))  # Salva o número máximo de bits usado
        for code in compressed_data:
            f.write(code.to_bytes((max_bits + 7) // 8, byteorder='big'))


def read_compressed_file(input_path):
    with open(input_path, 'rb') as f:
        max_bits = int.from_bytes(f.read(1), byteorder='big')  # Lê o número máximo de bits usado
        code_size = (max_bits + 7) // 8
        compressed_data = []
        while chunk := f.read(code_size):
            compressed_data.append(int.from_bytes(chunk, byteorder='big'))
    return compressed_data, max_bits


# Exemplo de uso
if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="LZW Compression/Decompression Tool with Dynamic Code Size")
    parser.add_argument("operation", choices=["compress", "decompress"], help="Operation to perform")
    parser.add_argument("input_file", type=str, help="Path to input file")
    parser.add_argument("output_file", type=str, help="Path to output file")
    parser.add_argument("--max_bits", type=int, default=12, help="Maximum number of bits (default: 12)")

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' does not exist.")
        exit(1)

    if args.operation == "compress":
        # Leitura do arquivo de entrada
        with open(args.input_file, 'r', encoding='latin1') as f:
            input_data = f.read()

        # Compressão
        compressor = LZWCompressorDynamic(max_bits=args.max_bits)
        compressed_data, final_bits = compressor.compress(input_data)

        # Salva o arquivo comprimido
        write_compressed_file(args.output_file, compressed_data, final_bits)
        print(f"Arquivo comprimido salvo em: {args.output_file}")

    elif args.operation == "decompress":
        # Leitura do arquivo comprimido
        compressed_data, max_bits = read_compressed_file(args.input_file)

        # Descompressão
        decompressor = LZWDecompressorDynamic(max_bits=max_bits)
        decompressed_data = decompressor.decompress(compressed_data)

        # Salva o arquivo descomprimido
        with open(args.output_file, 'w', encoding='latin1') as f:
            f.write(decompressed_data)
        print(f"Arquivo descomprimido salvo em: {args.output_file}")

