import csv
import json
import numpy as np
import pandas as pd
import nltk
import spacy
import gensim
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer

# Objective is to place all texts (data) in a CSV file, pre-processed.
# The result is to have a file with all texts (data) pre-processed.

# Configuring libraries
np.random.seed(2018)
nltk.download('wordnet')
nlp = spacy.load('pt_core_news_sm')
stemmer = PorterStemmer()
nlp = spacy.load("pt_core_news_sm")
nlp.Defaults.stop_words |= {
    "tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui",
    "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá", "hoje",
    "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "rua",
    "bairro", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"
}
stop_words_spacy = nlp.Defaults.stop_words
allowed_postags = ['NOUN', 'ADJ', 'PRON']


def verificar_palavra_entidade_loc(palavra, entidades_loc):
    """
    Method that check if the word is entity of location.

    Params:
    ----------
    word : String
        - Word.
    entities_loc : List
        - List of location entities recognized by spacy.

    Return:
    ----------
    True: If the word is a location entity.\n
    False: Othwerwise..
    """
    for e in entidades_loc:
        if (e.text.lower() == palavra.lower()):
            return True

    return False


def lista_para_texto(lista):
    """
    method that transforms a list of words into text.

    Params:
    ----------
    lista : List
        - List of words.

    Return:
    ----------
    texto : String
        - The text containing all the words in the list.
    """
    texto = ""
    for palavra in lista:
        texto += palavra + " "

    return texto.strip()


def lematizacao(palavra):
    """
    Method that performs the lemmatization of a word.

    Paramso:
    ----------
    word : String
        - Word that will surffer from stemming.

    Return:
    ----------
    word : String
        - Word lemmatization.
    """
    return stemmer.stem(WordNetLemmatizer().lemmatize(palavra, pos="v"))


def pre_processamento(texto, titulo):
    """
    Method that performs the pre-processing of a text:
        - Remove stop words.
        - Remove words that are of location entities.
        - Put all text in lower case.
        - Performs the lemmatization of the words.
        - Removes words that are not: substantivos, adjetivos
            e pronomes.

    Params:
    ----------
    text : String
        - Text that will undergo pre-processing.

    Return:
    ----------
    doc_out : List
        - List of words that have gone through pre-processing.
    """
    doc_out = []
    doc = nlp(texto)
    entidades_loc = [
        entidade for entidade in doc.ents if entidade.label_ == "LOC"]
    for token in doc:
        if (token.text not in stop_words_spacy and
            len(token.text) > 3 and
            token.pos_ in allowed_postags and not
                verificar_palavra_entidade_loc(token.text, entidades_loc)):
            doc_out.append(lematizacao(token.text))

    texto = lista_para_texto(doc_out)
    return texto


def main():
    # PREPARING FILES.

    fields = ["titulo", "texto"]
    f = csv.writer(open('../dados/textos_limpos.csv', 'w', encoding='utf-8'))
    f.writerow(fields)

    # Load data.
    dados = csv.DictReader(
        open("../dados/textos_videos.csv", encoding='utf-8'))
    textos = []
    titulo_textos = []

    for arq in dados:
        textos.append(arq['texto'])
        titulo_textos.append(arq['titulo'])

    for texto, titulo in zip(textos, titulo_textos):
        t = pre_processamento(texto, titulo)
        f.writerow([titulo, t])

# main()
