import nltk
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer

import json
import spacy
import geocoder

import truecase
from googletrans import Translator

class Geoparsing:
    def __init__(self):
        self.translator = Translator()
        self.stemmer = PorterStemmer()
        self.nlp = spacy.load("pt_core_news_sm")
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp.Defaults.stop_words |= {"vamos", "olha", "pois", "tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui", "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá", "hoje", "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"}
        self.stop_words_spacy = self.nlp.Defaults.stop_words

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
            print(end_final)
            end_ = sorted(ends_corretos, key=lambda end: end['confidence'])
            return (True, end_[0:limit])
        else:
            return (False, [])

    def geoparsing(self, text, case_correct=None, limit=5):
        if (case_correct):
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
r = g.geoparsing(text="quem está de volta agora com o calendário JPB hoje tem Missão Nova para nossa equipe uma praça abandonada no Ernani Sátiro aqui na capital Na verdade eu nem sei se a gente pode chamar de Praça sim viu Plínio Almeida foi até lá para conferir de um lado a Rua Abílio Paiva desse outro aqui a Auta de Luna Freire no bairro Ernani Sátiro E no meio tem algo que um dia já pode ser chamado de Praça mas do jeito que tá hoje com tudo quebrado esquecido abandonado mato lixo e sem condições nenhuma de uso Se tem uma coisa que isso aqui não é mais é uma praça os moradores dizem que faz mais ou menos uns 10 anos da última vez que alguém chegou aqui para fazer algum tipo de conserto manutenção nessa praça né Ficar Com certeza isso aqui assim eu eu eu tenho 41 anos aqui como ele tem como você já tá vendo aqui que as pessoas lhe darem a gente precisa de uma praça a gente precisa de um lazer a gente tem criança a gente precisa disso as crianças já se furaram aqui as crianças já pegaram o germe de cachorro aqui ali ó ferro enfiado para cavalo para animal aqui só serve para isso que não tem condições de andar eu mesmo vou fazer uma caminhada de Zezinho saiu daqui na rua aí rodeio e venho Quando estivesse pronto eu sou uma pracinha aqui tá certo é pequeno mas a gente aumentar o número de volta né Não só sou eu sou muito idosa que tem aqui temos a prefeitura ela tem aí uma creche em frente à praça das crianças aí vem para aí que eu já vi que ia subir aí e desceu aí pode se acidentar aí tudo rasgado tudo quebrado brincando do jeito que tá aí no jeito que tá aí criança vem amanhã à tarde para pegar porque tá vendo a hora que acidentado que a gente não pagamos também no nosso IPTU né não pagamos temos direito como colocar o outro cidadão exatamente nesse local aqui que tá cheio de mato tem Metralha também tem vários buracos era uma quadra não é isso Léo como era que antes antes de uma quadra de areia Aqui é onde a comunidade se divertir né Tem várias crianças aqui no bairro e a gente joga futebol a gente praticava vôlei não é isso para comunidade isso é muito importante queria que ele viesse reformar fazer uma quadra não colocaria novamente mas fazer uma quadra fazer um espaço que o pessoal fazer caminhada colocar ali os aparelhos para prática também de musculação isso que nós precisamos a gente que é o mesmo direito que as outros bairros tem que as outras praças tem dona Eronildes é uma das pessoas que mora aqui pertinho da praça e que tem muita vontade de fazer caminhada né mas nessas condições olha ali buraco não dá não tem não tem condições porque", case_correct=True)

for e in r:
    print(e['address'])
    print(e['confidence'])
    print("----------------------")
# print(r)
