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
        # TODO: Implementar algoritmos que escolham os melhores endereços
        # Ex 1: Filtrar por endereços que estejam em um determinado bairro
        # que também esteja entre esses endereços.
        # Ex 2: Olhar qual endereço mais se repete no texto.
        # Ex 3: Aplicar os dois algoritmos acima. E etc.
        result = {}
        result.update(addresses_residentials)
        result.update(addresses_geral)
        return result

    def filterAddressCGText(self, text):
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

    def geoparsing(self, text, case_correct=None, limit=5, gazettteer_cg=True):
        if (case_correct):
            if gazettteer_cg:
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
r = g.geoparsing(text="quem está de volta agora com o calendário JPB hoje tem Missão Nova para nossa equipe uma praça abandonada no Ernani Sátyro aqui na capital Na verdade eu nem sei se a gente pode chamar de Praça sim viu Plínio Almeida foi até lá para conferir de um lado a Rua Abílio Paiva desse outro aqui a Auta de Luna Freire no bairro Ernani Sátyro E no meio tem algo que um dia já pode ser chamado de Praça mas do jeito que tá hoje com tudo quebrado esquecido abandonado mato lixo e sem condições nenhuma de uso Se tem uma coisa que isso aqui não é mais é uma praça os moradores dizem que faz mais ou menos uns 10 anos da última vez que alguém chegou aqui para fazer algum tipo de conserto manutenção nessa praça né Ficar Com certeza isso aqui assim eu eu eu tenho 41 anos aqui como ele tem como você já tá vendo aqui que as pessoas lhe darem a gente precisa de uma praça a gente precisa de um lazer a gente tem criança a gente precisa disso as crianças já se furaram aqui as crianças já pegaram o germe de cachorro aqui ali ó ferro enfiado para cavalo para animal aqui só serve para isso que não tem condições de andar eu mesmo vou fazer uma caminhada de Zezinho saiu daqui na rua aí rodeio e venho Quando estivesse pronto eu sou uma pracinha aqui tá certo é pequeno mas a gente aumentar o número de volta né Não só sou eu sou muito idosa que tem aqui temos a prefeitura ela tem aí uma creche em frente à praça das crianças aí vem para aí que eu já vi que ia subir aí e desceu aí pode se acidentar aí tudo rasgado tudo quebrado brincando do jeito que tá aí no jeito que tá aí criança vem amanhã à tarde para pegar porque tá vendo a hora que acidentado que a gente não pagamos também no nosso IPTU né não pagamos temos direito como colocar o outro cidadão exatamente nesse local aqui que tá cheio de mato tem Metralha também tem vários buracos era uma quadra não é isso Léo como era que antes antes de uma quadra de areia Aqui é onde a comunidade se divertir né Tem várias crianças aqui no bairro e a gente joga futebol a gente praticava vôlei não é isso para comunidade isso é muito importante queria que ele viesse reformar fazer uma quadra não colocaria novamente mas fazer uma quadra fazer um espaço que o pessoal fazer caminhada colocar ali os aparelhos para prática também de musculação isso que nós precisamos a gente que é o mesmo direito que as outros bairros tem que as outras praças tem dona Eronildes é uma das pessoas que mora aqui pertinho da praça e que tem muita vontade de fazer caminhada né mas nessas condições olha ali buraco não dá não tem não tem condições porque", case_correct=True)
print(r)

# for e in r:
#     print(e['address'])
#     print(e['confidence'])
#     print("----------------------")
# print(r)
