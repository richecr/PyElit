import os
import csv
import json
import spacy
import geocoder

import nltk
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from gensim.test.utils import datapath

import truecase
from googletrans import Translator

from utils import string_to_list

class Geoparsing:
    def __init__(self):
        self.translator = Translator()
        self.stemmer = PorterStemmer()
        self.nlp = spacy.load("pt_core_news_sm")
        self.nlp.Defaults.stop_words |= {"vamos", "olha", "pois", "tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui", "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá", "hoje", "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"}
        self.stop_words_spacy = self.nlp.Defaults.stop_words
        self.residential = {}
        self.gazetteer = {}
        ROOT = os.path.abspath(os.path.dirname(__file__))
        fname = ROOT + "/gazetteer/processados"
        self.gazetteer_ln = csv.DictReader(open(fname + "/gazetteer.csv", "r", encoding='utf-8'))
        self.pre_process(self.gazetteer_ln)

    def pre_process(self, gazetteer):
        for row in gazetteer:
            self.gazetteer[row['name'].lower()] = (row['coordenates'], row['fclass'])

    def remove_stop_words(self, text):
        saida = ""
        text = text.lower()
        for palavra in text.split():
            if (palavra not in self.stop_words_spacy and (len(palavra) > 3 or palavra == "rua")):
                saida += palavra + " "
        s = saida.strip()
        return s

    def concantena_end(self, lista_end):
        saida = []
        for i in range(len(lista_end) - 1):
            for j in range(i+1, len(lista_end)):
                temp = str(lista_end[i]) + " " + str(lista_end[j])
                saida.append(temp)
        return saida

    def verifica_endereco(self, end):
        # if (end['address'].lower() in ruas):
        #	return True
        if (end['confidence'] >= 5):
            # ", campina grande" in end['address'].lower() and
            if (", paraíba" in end['address'].lower()):
                return True
            else:
                return False
        else:
            return False

    def verfica(self, ents_loc, limit):
        ends = []
        for loc in ents_loc:
            l = str(loc)
            g = geocoder.arcgis(l)
            end = g.json
            if (end != None):
                ends.append(end)

        ends_corretos = []
        for e in ends:
            if (self.verifica_endereco(e)):
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

    def search_next_index(self, lista):
        for i in range(len(lista)):
            if lista[i]['type_class'] == "geral":
                return i
        
        return len(lista) - 1

    def insert_ordened_to_priority(self, result, address, type_):
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

    def choose_best_addresses(self, adresses):
        """
        Realiza a escolha dos melhores endereços encontrados.

        Parâmetro:
        ----------
        adresses : Dict
            - Dicionário de endereços e suas respectivas coordenadas.

        Retorno:
        ----------
        result : Dict
            - Dicionário de `melhores` endereços e suas respectivas coordenadas.
        """
        # TODO: Implementar algoritmos que escolham os melhores endereços
        # Ex 0: Ordenar por níveis de prioridades.
        # Ex 1: Filtrar por endereços que estejam em um determinado bairro
        # que também esteja nestes endereços.
        # Ex 2: Olhar qual endereço mais se repete no texto.
        # Ex 3: Aplicar os três algoritmos acima. E etc.
        print(adresses.keys())
        result = []
        for loc in adresses.keys():
            coord, type_ = adresses[loc]
            lat, lon = string_to_list(coord)
            loc_= str(lat) + ", " + str(lon)
            g = geocoder.reverse(location=loc_, provider="arcgis")
            g = g.json
            result.append(g)
            self.insert_ordened_to_priority(result, g, type_)
        
        for a in result:
            print(a['address'], a['raw']['address']['District'])
        print("---------------------")
        for i in range(len(result)):
            l = result[i]
            if l['raw']['address']['District'].lower() in adresses.keys():
                result.remove(l)
                result.insert(0, l)

        for a in result:
            print(a['address'], a['raw']['address']['District'])
        return result

    def filterAddressCGText(self, text):
        """
        Realiza a filtragem dos endereços do texto que estão no gazetteer.

        Parâmetro:
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

        result = self.choose_best_addresses(addresses_geral)
        return result

    def geoparsing(self, text, case_correct=None, limit=5, gazetteer_cg=True):
        """
        Realiza o geoparsing do texto.

        Parâmetro:
        ----------
        text : String
            - Texto que para realizar o geoparsing.
        case_correct: Bool
            - Caso o texto já esteja com o case correto, True, caso contrário False.
        limit: Int
            - Limite máximo de endereços retornados.
        gazetteer_cg: Bool
            - Caso deseje utilizar o gazetteer da região de Campina Grande.
            - Assim aumentando a acurácia se os endereços buscados sejam da região.

        Retorno:
        ----------
        result : List
            - Lista de endereços.
        """
        if (case_correct):
            if gazetteer_cg:
                result = self.filterAddressCGText(text.lower())
                # TODO: Usar a biblioteca do GeoCoder para que por meio
                # das coordenadas, seja retornado um objeto representando o
                # endereço.
                if result:
                    return result
                else:
                    raise Exception("não foi possível realizar o geoparsing do texto")        
            else:
                doc = self.nlp(text)
                ents_loc = [entity for entity in doc.ents if entity.label_ == "LOC" or entity.label_ == "GPE"]
                address_found = self.concantena_end(ents_loc)
                result = self.verfica(address_found, limit)

                if (result[0]):
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
            address_found = self.concantena_end(ents_loc)
            result = self.verfica(address_found, limit)

            if (result[0]):
                return result[1]
            else:
                raise Exception("Não foi possivel realizar o geoparsing do texto")

g = Geoparsing()

text = "JPB de hoje começa na Rua Napoleão Crispim bairro de oitizeiro Esse é o endereço do abandono não tem outra definição para quem mora numa rua que é cheia de crateras o calendário vem acompanhando esse problema Desde janeiro já foram 3 visitas a prefeitura até fez um remendo nos buracos mas com as últimas chuvas foi tudo Ladeira abaixo esse buraco aqui é novo foi o que se formou na última chuva se prepara agora para ver como é que tá a situação do restante da rua é buraco e Desmantelo demais só para o pessoal de casa tem uma ideia da força da água quando chove aqui na Rua Napoleão Crispim olha só o que aconteceu com o poste tombou completamente Alexandre eu tô espantado aqui com a situação que a gente encontra essa rua por que na nossa última reportagem também não existe esse buraco que eu tava lá dentro Eu tô observando o que é essa outra cratera maior tá começando a avançar para o lado de cá e vocês estão ficando encurralados nesse monte de Cratera né da última vez que vocês vieram eles fizeram um serviço de terraplanagem que realmente ao menos uma situação era um paliativo a gente sabia disso mas só que infelizmente não pode chover qualquer chuvinha que dá volta aí as cartelas como você tá vendo esse buraco vem cada dia mais aumentando em direção a rua daqui a pouco a rua vai desaparecer vai ser um buraco só o problema piorou porque ele tá avançando para o lado de cá para o lado onde ficam as casas e a rua tá sendo literalmente engolida por esse buraco como se não bastasse existe esse outro aqui que a prefeitura conseguiu colocar um aterro na nossa última reportagem Melhorou a situação não mas olha bastou uma chuva para ele abrir novamente começar engolir não só essa rua mas aquela outra ali porque não pode passar mais nem carro por essas duas ruas aqui entre uma rua e outra e a gente tem que ter cuidado até para caminhar aqui eu vou pedir para o meu cinegrafista me acompanhar vocês também porque existe uma galeria pluvial aqui nessa rua que conduz água da chuva e vem muita água durante a chuva e a gente já tinha mostrado na última reportagem que ela tinha se rompido né a força da água é tão grande que ela havia se rompido vamos ver como é que ela tá agora isso aqui gente foi o que sobrou de uma galeria pluvial ela diz morou aqui completamente e essa área tá cheia de aterro o que acontece quando chove vem muito muita água com força e agora tá entupido né não tá entrando água aqui dentro das casas Por que tem essa mureta aqui mas eu acho que fica perto né Alexandre Com certeza é muita água e esse buraco Aí tá cada dia também aumentando"
a = g.geoparsing(text=text, case_correct=True)
# print(a)
print(len(a))

# text = "hora equipe reportagem conjunto Severino Cabral bairro liberdade Feirinha fizemos reportagem acontecendo asfaltou ruas colocou sinalização preocupados acontecendo acidentes agente sério volta equipe reportagem Severino Cabral volta Damião mostrar circular mostrar feirinha Severino Cabral Bodocongó Severino Cabral continua hein francinaldo' verdade existe vieram setembro aconteceu acidentes grave recente cara chocou moto moto ficou carro preocupado pena verdade tomar providências aconteça objeto sinalização entender deles mostrar presta atenção olhada lisinha asfalto novinho folha sinalização consigo marquinha tinta branca verdade justamente preocupado acidente acidente ônibus carro moto entra asfaltada francinaldo' Providência tomada estamos preocupado namorado daqui localidade difícil comigo tentando atravessar cruzamento faixa pedestre carro passa prioridade carros param causa comércio senhor precisa atravessar medo claro medo perigoso acidente ficou precisa quebra-mola veículos passam muita velocidade ficha asfaltada faixa pedestre faixa pedestre mestre pedestres atravessar segurança placa cruzamentos indicar dona Gerusa contando situação ônibus

# textos_limpos = []
# titulos = []
# arq = csv.DictReader(open("../dados/textos_videos.csv", "r", encoding='utf-8'))

# sucess = 0
# fail = 0
# total = 0
# for p in arq:
#     try:
#         r = g.geoparsing(text=p['texto'], case_correct=True)
#         # print(r)
#         total += 1
#         sucess += 1
#     except Exception as error:
#         total += 1
#         fail += 1
#         # print(error)

# print("Total: ", total)
# print("Sucess: ", sucess)
# print("Fail: ", fail)

# for e in r:
#     print(e['address'])
#     print(e['confidence'])
#     print("----------------------")
# print(r)
