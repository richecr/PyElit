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
        self.gazetteer_ln = csv.DictReader(open(fname + "/gazetteer_ln.csv", "r", encoding='utf-8'))
        self.gazetteer_pt = csv.DictReader(open(fname + "/gazetteer_pt.csv", "r", encoding='utf-8'))
        # self.gazetteer.update(self.pre_process(gazetteer_pt))
        self.pre_process(self.gazetteer_ln)
        self.pre_process(self.gazetteer_pt)

    def pre_process(self, gazetteer):
        for row in gazetteer:
            if row['fclass'] == "residential":
                self.residential[row['name'].lower()] = row['coordenates']
            else:
                self.gazetteer[row['name'].lower()] = row['coordenates']

    def remove_stop_words(self, text):
        saida = ""
        for palavra in texto.split():
            if (palavra.lower() not in stop_words_spacy and len(palavra) > 3):
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

    def filterAddressCG(addresses):
        addresses_residentials = {}
        adresses_geral = {}
        for address in addresses:
            if address in self.residential:
                addresses_residentials[address] = self.residential[address]
            elif address in self.gazetteer_ln:
                adresses_geral[address] = self.adresses_geral[address]

        # Pode ser feito uma lógica para capturar os melhores endereços.
        return addresses_residentials, adresses_geral

    def choose_best_addresses(self, addresses_residentials, addresses_geral):
        """
        Realiza a escolha dos melhores endereços encontrados.

        Parâmetro:
        ----------
        addresses_residentials : Dict
            - Dicionário de endereços residenciais e suas respectivas coordenadas.
        addresses_geral : Dict
            - Dicionário de endereços gerais(menos residenciais) e suas respectivas coordenadas.

        Retorno:
        ----------
        result : Dict
            - Dicionário de `melhores` endereços e suas respectivas coordenadas.
        """
        # TODO: Implementar algoritmos que escolham os melhores endereços
        # Ex 1: Filtrar por endereços que estejam em um determinado bairro
        # que também esteja nestes endereços.
        # Ex 2: Olhar qual endereço mais se repete no texto.
        # Ex 3: Aplicar os dois algoritmos acima. E etc.
        result = []
        for loc in addresses_residentials.keys():
            print(type(addresses_residentials[loc][0]))
            print(addresses_residentials[loc][0])

            if type(addresses_residentials[loc][0]) != list:
                loc_ = ", ".join(map(str, [-7.234222, -35.2996532]))
                g = geocoder.reverse(location=loc_, provider="arcgis")
                g = g.json
                result.append(g)
            else:
                x = 0
                y = 0
                for l in loc:
                    x += l[0]
                    y += l[1]
                lat = x / len(loc)
                lon = y / len(loc)
                loc = str(lat) + ", " + str(lon)
                g = geocoder.reverse(location=loc_, provider="arcgis")
                g = g.json
                result.append(g)

        print(result)

        # result.update(addresses_residentials)
        # result.update(addresses_geral)
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
        for address in self.residential.keys():
            address_aux = address.split()
            if address_aux[0] == "rua":
                address_aux = address_aux[1:]
            if len(address_aux) > 1:
                if re.search("\\b" + address + "\\b", text):
                    addresses_residentials[address] = self.residential[address]

        for address in self.gazetteer.keys():
            address_aux = address.split()
            if address_aux[0] == "rua":
                address_aux = address_aux[1:]
            if len(address_aux) > 1:
                if re.search("\\b" + address + "\\b", text):
                    addresses_geral[address] = self.gazetteer[address]

        result = self.choose_best_addresses(addresses_residentials, addresses_geral)
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
                # result[0] = self.filterAddressCG(address_found)

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

a = g.geoparsing(text="hora do calendário dessa vez nossa equipe de reportagem foi até o conjunto rua Severino Cabral ali perto da Feirinha nós já fizemos uma reportagem lá só que tá acontecendo é que a prefeitura asfaltou as ruas local mas não colocou sinalização aí os moradores estão muito preocupados Por que estão acontecendo muitos acidentes agente sabe que um problema tá sério quando a gente volta no local Já é a segunda vez que nossa equipe de reportagem tá aqui no Severino Cabral dá uma volta Damião para mostrar para circular para mostrar para o pessoal onde a gente tá feirinha do Severino Cabral aqui entre Bodocongó Severino Cabral Mas o problema continua não faz muito tempo que a gente teve aqui não hein seu francinaldo' é verdade você existe vieram aqui no dia 19 de setembro para cá tem o que é dois nem dois meses o que aconteceu o terceiro três acidentes O mais grave foi agora recente né cara se chocou com a moto a moto ficou com carro ao mesmo tempo e quer dizer esse preocupado e fazemos uma pena na verdade aí TP para que tomar as providências era para você vai ser que aconteça um objeto para que ele ia fazer isso aí como não tem sinalização aí o que dá entender que cada um deles é a vez mas não é isso que eu ia mostrar presta atenção dá só uma olhada na rua a rua bem lisinha tá com asfalto novinho em folha mas não tem uma sinalização não consigo ver uma marquinha de tinta aqui branca no local é verdade é justamente preocupado que vai ter acidente como é que não vai ter acidente Quem é que sabe quem é a vez do ônibus do carro da moto quem vai quem entra não tem como saber aqui e sim essa rua foi asfaltada a um ano não é isso seu francinaldo' faz mais ou menos um ano só que até então não é Providência foi tomada e estamos preocupado tanto a mim como namorado daqui também como age os demais moradores da localidade olha aqui como é difícil vamos comigo também a gente tá tentando atravessar aqui aqui no meio do cruzamento ela não tem uma faixa de pedestre a gente não sabe qual o carro que que passa que tem prioridade aqui os carros param né Por causa que tem esse comércio aqui senhor quando precisa atravessar tem medo claro com certeza tem medo né muito perigoso acidente aqui já já ele já Olha então a gente ainda a gente ficou que precisa aqui no local um quebra-mola porque os veículos passam e muita velocidade depois que a ficha tá asfaltada uma faixa de pedestre porque não tem nenhuma faixa de pedestre mestre para os pedestres atravessar com segurança que é que também falta a placa nos cruzamentos para indicar qual é quem tem a vez quem não tem e a dona Gerusa tá me contando aqui uma outra situação olha só a gente tá no ponto de ônibus só que como a rua", case_correct=True)

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
