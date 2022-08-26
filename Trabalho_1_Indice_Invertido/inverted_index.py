# Autores: Matheus Nascimento Silva, Christian Menezes e João Carlos
# Universidade Estadual de Santa Cruz - 2021
# Disciplina: ORI
# Primeiro trabalho: Indice Invertido

import sys

# from nltk.tokenize import word_tokenize
# import nltk
# from nltk.corpus import stopwords
# nltk.download('stopwords')

class Inverted_Index():
    '''Indice invertido.
    \n Parametros:
    \n texts - lista contendo caminhos para os arquivos de texto que serão lidos.
    \n unconsidered - lista com as palavras que não serão consideradas na criação do indice invertido.
    '''
    def __init__(self, texts, unconsidered):
        super().__init__()

        self.texts_path = texts  # Endereços originais dos arquivos de texto considerados
        self.texts = []  # Lista que guardará as palavras de cada arquivo de texto

        # Separa as palavras de cada texto e salva na lista
        for i in range(len(self.texts_path)):
            self.texts.append(self.split_text(self.texts_path[i]))

        self.unconsidered = unconsidered  # Palavras desconsideradas
        self.vocabulary = set()  # Conjunto com o vocabulário

        # Define o vocabulário do indice invertido
        for text in self.texts:
            self.define_vocabulary(text)

        # Organiza o vocabulário em ordem alfabética
        self.vocabulary = sorted(self.vocabulary)  

        # Dicionário que guardará os indices de cada ocorrência da palavra
        self.index = {word: [] for word in self.vocabulary}

        # Define os indices
        for i in range(len(self.texts)):
            self.define_indexes(self.texts[i], i+1)

        # Gera o arquivo de indice invertido
        self.generate_index_file()  

    def split_text(self, path):
        '''Separa as palavras do texto, considerando como separadores os símbolos:\n
        '\\n - ? - ! - . - ,'
        \nParametros:
        \npath - caminho do arquivo de texto que será separado
        '''
        with open(path, 'r') as file:
            # Cria um arquivo temporário com o texto
            temp = file.read()  

            # Cria um conjunto com os delimitadores
            delimiters = {'\n', '?', '!', '.', ','}

            # Para cada delimitador, troca o delimitador por um espaço em branco
            for delimiter in delimiters:
                temp = temp.replace(delimiter, ' ')

            # Aplica um split para separar todos os espaços em branco
            temp = temp.split()

        return temp

    def define_vocabulary(self, words):
        '''Define o vocabulário do indice invertido, excluindo as palavras desconsideradas.
        \nParametros:
        \nwords - lista de palavras que serão adicionadas no vocabulário.
        '''

        # Para cada palavra passada como parâmetro, verifica se faz parte da lista de
        # desconsideradas, se não fizer, a adiciona no vocabulário
        for word in words:
            if word not in self.unconsidered:
                self.vocabulary.add(word)

    def define_indexes(self, text, index):
        '''Define os indices.
        \n Parametros:
        \n text - texto que será considerado para ser adicionado no indice invertido.
        \n index - indice do arquivo que foi passado como parâmetro.
        '''

        # Para cada palavra do vocabulário, conta quantas vezes a palavra aparece no texto
        # caso apareça pelo menos uma vez, a adiciona no indice invertido
        for word in self.vocabulary:
            count = text.count(word)
            if count > 0:
                self.index[word].append((index, count))

    def generate_index_file(self):
        '''
            Gera o arquivo de saída com o indice invertido.
        '''
        with open('indice.txt', 'w') as file:

            # Para cada palavra do vocabulário, escreve os dados no arquivo de indice
            # idx variável que vai registrar no arquivo os resultados das ocorrências
            for word in self.vocabulary:
                """idx, idx2 e separator servem para organizar o registro no arquivo
                Eles ficam de forma organizada e mais fácil de entender"""
                idx = '|'
                idx2 = '|'
                separator = '|'
                for value in self.index[word]:
                    idx += f'{value[0]}, {value[1]}'+separator

                file.write(f'{word}: {str(idx+idx2)}\n')

    def query(self, words):
        '''Realiza uma consulta com as palavras de consulta.
        \n Parametros:
        \n words - palavras que serão consultadas
        '''

        # Cria um conjunto com os valores possíveis
        fileID = set(range(1, len(self.texts) + 1))

        # Cria um segundo conjunto com os valores possíveis
        fileID2 = set(range(1, len(self.texts) + 1))
        
        # contador de ocorrências
        firstOcurrence = 0

        # função que faz o tratamento nas consultas
        """Verifica na consulta os caracteres ',' e ,';'"""

        wordsSanitized = list()
        temp = []
        chars = []

        keys = ''';, '''
        for elem in words:
            for i in range(0, len(elem)):
                if elem[i] not in keys:
                    chars.append(elem[i])
                else:
                    chars.append(' ')
                    
        temp = ''.join(chars).split()
        
        for word in temp:
            wordsSanitized.append(word)

        # Funciona como um forEach
        for word in wordsSanitized:
        
            # print("word: ", word)

            # Verifica se a palavra está no vocabulário para cada palavra consultada
            # caso não esteja, para o loop
            if word not in self.vocabulary:
                # print("entrei aqui, deu merda -> ok")
                fileID = {}
                fileID2 = {}
                break

            # Caso a palavra esteja no vocabulário, cria um conjunto com os indices em
            # que ela aparece, e realiza a intersercção com o conjunto de possibilidades
            # salvando assim os indices em que todas as palavras consultadas aparecem

            if word in self.vocabulary:
                temp = set()
                for index in self.index[word]:
                    temp.add(index[0])

                if fileID and firstOcurrence == 0:
                    fileID = fileID.intersection(temp)
                    firstOcurrence = firstOcurrence + 1

                    # metodo intersection faz as comparações se as duas palavras fazem parte do mesmo grupo 
                

            if word in self.vocabulary:
                temp2 = set()
                for index in self.index[word]:
                    temp2.add(index[0])
                
                if fileID2:
                    fileID2 = fileID.union(temp2)
                    firstOcurrence = firstOcurrence + 1

                    # método union faz a união de todos os regitros das palavras que encontrar
        
        # Conta o número de textos em que as palavras aparecem no operador E
        count = len(fileID)
        
        # conta o número de textos que as palavras aparecem no operador OU
        count2 = len(fileID2)

        # Para cada indice salvo no conjunto da intersecção, o salva no arquivo de resposta1
        with open('resposta1.txt', 'w') as file:
            file.write(f'{str(count)}\n')
            for i in fileID:
                file.write(f'{self.texts_path[i-1]}\n')

        # Para cada indice salvo no conjunto da união, o salva no arquivo de resposta2
        with open('resposta2.txt', 'w') as file:
            file.write(f'{str(count2)}\n')
            for i in fileID2:
                file.write(f'{self.texts_path[i-1]}\n')


if __name__ == '__main__':
    # Pega os arquivos passados como argumento pelo terminal
    files = sys.argv[1:]

    # Separa os endereços dos arquivos de conjunto do primeiro argumento
    with open(files[0], 'r') as file:
        conjunto = [line.strip() for line in file.readlines()]
        # print(conjunto)

    # Separa as palavras que serão desconsideradas do segundo argumento
    with open(files[1], 'r') as file:
        desconsiderados = [line.strip() for line in file.readlines()]
        # print(desconsiderados)

    # Separa as palavras que serão consultadas do terceiro argumento
    with open(files[2], 'r') as file:
        consulta1 = [line.strip(',').split() for line in file.readlines()]
        consulta1 = consulta1[0]

    # Separa as palavras que serão consultadas do quarto argumento
    with open(files[3], 'r') as file:
        consulta2 = [line.strip(';').split() for line in file.readlines()]
        consulta2 = consulta2[0]

    # Cria a instancia do indice invertido passando o conjunto e as palavras desconsideradas
    # invertded é um objeto do tipo Inverted_Index
    inverted = Inverted_Index(conjunto, desconsiderados)

    # Faz as consultas com as palavras dos arquivos de consulta1 e consulta2
    inverted.query(consulta1)
    inverted.query(consulta2)
