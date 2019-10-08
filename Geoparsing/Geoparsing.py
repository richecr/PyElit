import csv
import nltk
import spacy
import pandas as pd

import requests
import json
import geocoder

import gensim
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer

from googletrans import Translator

import truecase

class Geoparsing:
    def __init__(self):
        self.translator = Translator()
        self.stemmer = PorterStemmer()
        self.nlp = spacy.load("pt_core_news_sm")
        self.nlp.Defaults.stop_words |= {"vamos", "olha", "pois", "tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui", "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá", "hoje", "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"}
        self.stop_words_spacy = nlp.Defaults.stop_words

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

    def verfica(self, ents_loc):
        ends = []
        for loc in ents_loc:
            l = str(loc)
            g = geocoder.arcgis(l)
            end = g.json
            if (end != None):
                ends.append(end)
        # print("1: ", json.dumps(ends, indent=4))

        ends_corretos = []
        for e in ends:
            if (verifica_endereco(e)):
                ends_corretos.append(e)
        # print("2: ", json.dumps(ends_corretos, indent=4))

        if (len(ends_corretos)):
            end_final = ends_corretos[0]
            end_final_confidence = ends_corretos[0]
            for ed in ends_corretos:
                if (ed['confidence'] > end_final_confidence['confidence']):
                    end_final = ed
            print("3: ", end_final['address'])
            return (True, end_final)
        else:
            return (False, [])

    def geoparsing(self, text, case_correct=None):
        if (case_correct):
            pass
            # TODO
        else:
            text_en = self.translator.translate(text, src="pt", dest="en")
            text_en = text_en.text
            text_true_case = truecase.caser.get_true_case(text_en)

            text_pt = self.translator.translate(text_true_case, src="en", dest="pt")
            text = text_pt.text
            doc = self.nlp(text)
            ents_loc = [entity for entity in doc.ents if entity.label_ == "LOC" or entity.label_ == "GPE"]
            address_found = self.concantena_end(ents_loc)
            result = self.verfica(end_encontrados)
            
            if (result[0]):
                return result[1]
            else:
                raise Exception("Não foi possivel realizar o geoparsing do texto")

g = Geoparsing()
r = g.geoparsing("eu moro na rua joão sergio de almeida no bairro de bodocongo", case_correct=False)

print(r)
