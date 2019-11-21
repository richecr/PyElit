import os
import csv
import unicodedata

import truecase
from googletrans import Translator

import spacy
import geocoder

import nltk
from nltk.stem.porter import *

from .utils.utils import string_to_list

class Geoparsing:
    """
    Classe responsável por realizar o Geoparsing.
    """
    def __init__(self):
        """
        Construtor da classe. Onde todos os atributos são iniciandos e sofrem pré-processamento.
        """
        self.translator = Translator()
        self.stemmer = PorterStemmer()
        self.nlp = spacy.load("pt_core_news_sm")
        self.nlp.Defaults.stop_words |= {"vamos", "olha", "pois", "tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui", "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá", "hoje", "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"}
        self.stop_words_spacy = self.nlp.Defaults.stop_words
        self.residential = {}
        self.gazetteer = {}
        ROOT = os.path.abspath(os.path.dirname(__file__))
        fname = ROOT + "/gazetteer/processados"
        self.gazetteer_ln = csv.DictReader(open(fname + "/gazetteerpb.csv", "r", encoding='utf-8'))
        self.pre_process(self.gazetteer_ln)

    def pre_process(self, gazetteer):
        """
        Método que realiza o pré-processamento do gazetteer.
        Carrega as informações do gazetteer em um dicionário.

        Parâmetros:
        ----------
        gazetteer: DictReader
            - Objeto da biblioteca nativa do python: `CSV`.
        """
        for row in gazetteer:
            self.gazetteer[self.remove_accents(row['name'].lower())] = (row['coordenates'], row['fclass'])

    def remove_accents(self, input_str):
        """
        Método que remove acentos das palavras.

        Parâmetros:
        ----------
        input_str: String
            - Entrada a ser removido os acentos
        """
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii.decode('utf-8')

    def remove_stop_words(self, text):
        """
        Método que remove stop words do texto.

        Parâmetros:
        ----------
        text: String
            - Texto que esta passando pelo processo do geoparsing.
        
        Retorno:
        ----------
        out : String
            - Texto pré-processado, sem conter palavras de stop words.
        """
        out = ""
        text = text.lower()
        for palavra in text.split():
            if (palavra not in self.stop_words_spacy and (len(palavra) > 3 or palavra == "rua")):
                out += palavra + " "
        out = out.strip()
        return out

    def __concatena_end(self, list_end):
        """
        Método que concatena os endereços.

        Parâmetros:
        ----------
        list_end: List
            - Lista contendo todos os endereços encontrados.
        
        Retorno:
        ----------
        out : List
             - Lista de endereços concatenados.
        """
        out = [e for e in list_end]
        for i in range(len(list_end) - 1):
            for j in range(i+1, len(list_end)):
                temp = str(list_end[i]) + " " + str(list_end[j])
                out.append(temp)
        return out

    def __verifica_endereco(self, end):
        """
        Método que verifica se um endereço é da Paraíba 
        e se sua confiabilidade é maior ou igual a 5.

        Parâmetros:
        ----------
        end: Dict
            - Dicionário contendo todas as informações do endereço.
        
        Retorno:
        ----------
        True: Caso o endereço obedeça aos requisitos.
        False: Caso contrário.
        """
        if (end['confidence'] >= 5):
            # ", campina grande" in end['address'].lower() and
            if (", paraíba" in end['address'].lower()):
                return True
            else:
                return False
        else:
            return False

    def verfica(self, ents_loc, limit):
        """
        Método que verifica se os endereços estão corretos. 
            - Encontra as localizações das entidades de localizações(Geocoder com arcgis).
            - Verifica se é da PB e sua confiabilidade(`verifica_endereco`).
            - Concatena os endereços.
            - Ordena endereços pela confiabilidade.

        Parâmetros:
        ----------
        ents_loc : List
            - Lista de entidades de localizações.
        limit : Integer
            - Quantidade de endereços que desejar retornar.

        Retorno:
        ----------
        out : Tuple
            - Uma tupla do tipo (Boolean, List).
            Caso tenha encontrado pelo menos um endereço nesses requisitos.
            Lista de endereços(len = limit)
        """
        ends = []
        for loc in ents_loc:
            l = str(loc)
            g = geocoder.arcgis(l)
            end = g.json
            if (end != None):
                ends.append(end)

        ends_corretos = []
        for e in ends:
            if (self.__verifica_endereco(e)):
                ends_corretos.append(e)

        if (len(ends_corretos)):
            end_final = ends_corretos[0]
            for ed in ends_corretos:
                if (ed['confidence'] > end_final['confidence']):
                    end_final = ed
            end_ = sorted(ends_corretos, key=lambda end: end['confidence'])
            return (True, end_[0:limit])
        else:
            return (False, [])

    def search_next_index(self, list_best_address):
        """
        Método que busca uma nova posição a ser adicionado na lista de melhores endereços.

        Parâmetros:
        ----------
        list_best_address : List
            - Lista contendo todos os endereços encontrados.
        
        Retorno:
        ----------
        out : Integer
            - Posição onde o novo endereço deve ser adicionado.
        """
        for i in range(len(list_best_address)):
            if list_best_address[i]['type_class'] == "geral":
                return i
        
        return len(list_best_address) - 1

    def insert_ordened_to_priority(self, result, address, type_):
        """
        Método que insere na lista de melhores endereços ordenando por prioridades.

        Parâmetros:
        ----------
        result : List
            - Lista de melhores endereços.
        address : Dict
            - Endereço a ser inserido na lista.
        type_ : String
            - Tipo do endereço.
        """
        if address not in result:
            if type_ == "school":
                address['type_class'] = "school"
                result.insert(0, address)
            elif type_ == "residential":
                address['type_class'] = "residential"
                result.insert(self.search_next_index(result), address)
            else:
                address['type_class'] = "geral"
                result.append(address)

    def choose_best_addresses(self, adresses, text):
        """
        Realiza a escolha dos melhores endereços encontrados.

        Algoritmos implementados:
            - Ordenar por níveis de prioridades
            - Filtrar por endereços que estejam em um determinado bairro 
            que também esteja nestes endereços filtrados.
            - Endereços que mais se repetem no texto.

        Parâmetros:
        ----------
        adresses : Dict
            - Dicionário de endereços e suas respectivas coordenadas.
        text : String
            - Texto que esta passando pelo geoparsing.

        Retorno:
        ----------
        result : List
            - Lista de objetos de `melhores` endereços.
        """
        print(adresses.keys())
        result = []
        # Adicionar os endereços por ordem de prioridades.
        # Ocorrências dos endereços no texto.
        for loc in adresses.keys():
            coord, type_ = adresses[loc]
            lat, lon = string_to_list(coord)
            loc_= str(lat) + ", " + str(lon)
            g = geocoder.reverse(location=loc_, provider="arcgis")
            g = g.json
            g['occurrences_in_text'] = text.count(loc)
            if g != None:
                result.append(g)
                self.insert_ordened_to_priority(result, g, type_)

        # Ordenando por endereços que também foram encontrados seus bairros na filtragem, 
        # assim possuindo uma chance maior de ser o endereço correto.
        new_result = []
        for i in range(len(result) - 1, -1, -1):
            l = result[i]
            if l['raw']['address']['District'].lower() in adresses.keys():
                new_result.insert(0, l)
            else:
                new_result.append(l)

        # Ordenando por quantidade de ocorrências no texto.
        sorted(new_result, key=lambda e: e['occurrences_in_text'])

        return result

    def filterAddressCGText(self, text):
        """
        Realiza a filtragem dos endereços do texto que estão no gazetteer.

        Parâmetros:
        ----------
        text : String
            - Texto que para realizar o geoparsing.

        Retorno:
        ----------
        result : Dict
            - Dicionário de endereços e suas respectivas coordenadas.
        """
        addresses_residentials = {}
        addresses_geral = {}
        text = self.remove_accents(text)

        for address in self.gazetteer.keys():
            address_aux = address.split()
            if address_aux[0] == "rua":
                address_aux = address_aux[1:]
            if len(address_aux) > 1 or self.gazetteer[address][1] == "suburb":
                address = address.replace("(", "")
                address = address.replace(")", "")
                if re.search("\\b" + address + "\\b", text):
                    print(address)
                    addresses_geral[address] = self.gazetteer[address]

        result = self.choose_best_addresses(addresses_geral, text)
        return result

    def geoparsing(self, text, case_correct=None, limit=5, gazetteer_cg=False):
        """
        Realiza o geoparsing do texto.

        OBS: Utilizar o geoparsing sem o case correct e sem o gazetteer
        fará com que você tenha resultados ruins. 

        Parâmetros:
        ----------
        text : String
            - Texto que para realizar o geoparsing.
        case_correct: Bool
            - Caso o texto já esteja com o case correto, True, caso contrário False.
        limit: Int
            - Limite máximo de endereços retornados.
        gazetteer_cg: Bool
            - Caso deseje utilizar o gazetteer com localidades do estado da Paraíba.

        Retorno:
        ----------
        result : List
            - Lista de endereços.
        """
        if gazetteer_cg:
            result = self.filterAddressCGText(text.lower())
            if result:
                return result
            else:
                raise Exception("Não foi possível realizar o geoparsing do texto") 
        else:
            if case_correct:
                doc = self.nlp(text)
                ents_loc = [entity for entity in doc.ents if entity.label_ == "LOC" or entity.label_ == "GPE"]
                address_found = self.__concatena_end(ents_loc)
                result = self.verfica(address_found, limit)
                if result[0]:
                    return result[1]
                else:
                    raise Exception("Não foi possivel realizar o geoparsing do texto")
            else:
                text_en = self.translator.translate(text, src="pt", dest="en")
                text_en = text_en.text
                text_true_case = truecase.caser.get_true_case(text_en)

                text_pt = self.translator.translate(text_true_case, src="en", dest="pt")
                text = text_pt.text

                doc = self.nlp(text)

                ents_loc = [entity for entity in doc.ents if entity.label_ == "LOC" or entity.label_ == "GPE"]
                address_found = self.__concatena_end(ents_loc)
                result = self.verfica(address_found, limit)
                if result[0]:
                    return result[1]
                else:
                    raise Exception("Não foi possivel realizar o geoparsing do texto")
