class LZWCompressorDynamic:
    # classe para compressao lzw com tamanho de codigo dinamico
    def __init__(self, max_bits=12):
        # inicializa o compressor com um tamanho maximo de codigo
        self.max_bits = max_bits  # numero maximo de bits permitido
        self.current_bits = 9  # tamanho inicial do codigo
        self.max_code = (1 << self.current_bits) - 1  # maior codigo permitido com os bits atuais
        self.trie = {}  # dicionario para armazenar padroes de sequencia
        for i in range(256):  # preenche a tabela com os codigos ascii
            self.trie[chr(i)] = i
        self.next_code = 256  # primeiro codigo disponivel apos os codigos ascii

    def compress(self, input_data):
        # realiza a compressao dos dados de entrada
        result = []  # lista de codigos comprimidos
        current_string = ""  # sequencia atual sendo processada
        
        for char in input_data:
            combined_string = current_string + char
            if combined_string in self.trie:
                # continua expandindo a sequencia se ja existe no dicionario
                current_string = combined_string
            else:
                # adiciona o codigo da sequencia atual a saida
                result.append(self.trie[current_string])

                # insere o novo padrao no dicionario, se o limite ainda nao foi atingido
                if self.next_code <= self.max_code:
                    self.trie[combined_string] = self.next_code
                    self.next_code += 1

                # ajusta o numero de bits por codigo caso seja necessario
                if self.next_code > self.max_code and self.current_bits < self.max_bits:
                    self.current_bits += 1
                    self.max_code = (1 << self.current_bits) - 1

                # reinicia a sequencia atual com o caractere atual
                current_string = char

        # adiciona o codigo da ultima sequencia, se existir
        if current_string:
            result.append(self.trie[current_string])

        return result, self.current_bits


class LZWDecompressorDynamic:
    # classe para descompressao lzw com tamanho de codigo dinamico
    def __init__(self, max_bits=12):
        # inicializa o descompressor com um tamanho maximo de codigo
        self.max_bits = max_bits  # numero maximo de bits permitido
        self.current_bits = 9  # tamanho inicial do codigo
        self.max_code = (1 << self.current_bits) - 1  # maior codigo permitido com os bits atuais
        self.dictionary = {i: chr(i) for i in range(256)}  # inicializa a tabela com codigos ascii
        self.next_code = 256  # proximo codigo disponivel

    def decompress(self, compressed_data):
        # realiza a descompressao dos dados comprimidos
        result = []  # lista de dados descomprimidos
        current_string = self.dictionary[compressed_data[0]]
        result.append(current_string)

        for code in compressed_data[1:]:
            if code in self.dictionary:
                # recupera a entrada do dicionario
                entry = self.dictionary[code]
            elif code == self.next_code:
                # gera nova entrada se o codigo for igual ao proximo codigo disponivel
                entry = current_string + current_string[0]
            else:
                # lanca erro se o codigo nao for valido
                raise ValueError("codigo invalido durante a descompressao")

            result.append(entry)

            # adiciona a nova entrada no dicionario
            if self.next_code <= self.max_code:
                self.dictionary[self.next_code] = current_string + entry[0]
                self.next_code += 1

            # ajusta o numero de bits por codigo caso seja necessario
            if self.next_code > self.max_code and self.current_bits < self.max_bits:
                self.current_bits += 1
                self.max_code = (1 << self.current_bits) - 1

            current_string = entry

        return ''.join(result)


# funcoes auxiliares para salvar e carregar arquivos comprimidos
def write_compressed_file(output_path, compressed_data, max_bits):
    # escreve os dados comprimidos em um arquivo binario
    with open(output_path, 'wb') as f:
        f.write(max_bits.to_bytes(1, byteorder='big'))  # salva o numero maximo de bits usado
        for code in compressed_data:
            f.write(code.to_bytes((max_bits + 7) // 8, byteorder='big'))


def read_compressed_file(input_path):
    # le os dados comprimidos de um arquivo binario
    with open(input_path, 'rb') as f:
        max_bits = int.from_bytes(f.read(1), byteorder='big')  # le o numero maximo de bits usado
        code_size = (max_bits + 7) // 8  # calcula o tamanho de cada codigo
        compressed_data = []
        while chunk := f.read(code_size):
            compressed_data.append(int.from_bytes(chunk, byteorder='big'))
    return compressed_data, max_bits


# exemplo de uso
if __name__ == "__main__":
    import argparse
    import os

    # define os argumentos da linha de comando
    parser = argparse.ArgumentParser(description="lzw compression/decompression tool with dynamic code size")
    parser.add_argument("operation", choices=["compress", "decompress"], help="operation to perform")
    parser.add_argument("input_file", type=str, help="path to input file")
    parser.add_argument("output_file", type=str, help="path to output file")
    parser.add_argument("--max_bits", type=int, default=12, help="maximum number of bits (default: 12)")

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        # verifica se o arquivo de entrada existe
        print(f"error: file '{args.input_file}' does not exist")
        exit(1)

    if args.operation == "compress":
        # leitura do arquivo de entrada
        with open(args.input_file, 'r', encoding='latin1') as f:
            input_data = f.read()

        # realiza a compressao
        compressor = LZWCompressorDynamic(max_bits=args.max_bits)
        compressed_data, final_bits = compressor.compress(input_data)

        # salva o arquivo comprimido
        write_compressed_file(args.output_file, compressed_data, final_bits)
        print(f"arquivo comprimido salvo em: {args.output_file}")

    elif args.operation == "decompress":
        # leitura do arquivo comprimido
        compressed_data, max_bits = read_compressed_file(args.input_file)

        # realiza a descompressao
        decompressor = LZWDecompressorDynamic(max_bits=max_bits)
        decompressed_data = decompressor.decompress(compressed_data)

        # salva o arquivo descomprimido
        with open(args.output_file, 'w', encoding='latin1') as f:
            f.write(decompressed_data)
        print(f"arquivo descomprimido salvo em: {args.output_file}")
