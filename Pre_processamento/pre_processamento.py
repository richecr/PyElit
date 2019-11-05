import csv
import json
import numpy as np
import pandas as pd
import nltk
import spacy
import gensim
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer

# Objetivo é colocar todos os textos(dados) em um arquivo CSV, pré-processados.
# Resultado é ter um arquivo com todos os textos(dados) pré-processados.

# Configurando bibliotecas para ter um melhor resultado.
np.random.seed(2018)
nltk.download('wordnet')
nlp = spacy.load('pt_core_news_sm')

def verificar_palavra_entidade_loc(palavra, entidades_loc):
	"""
	Verifica se a palavra é uma entidade de localização.

	Parâmetros:
	----------
	palavra : String
		- Palavra a ser verificada.
	entidades_loc : List
		- Lista de entidades de localizações reconhecidas pelo Spacy.

	Retorno:
	----------
	True : Caso a palavra seja uma entidade de localização.\n
	False : Caso a palavra não seja uma entidade de localização.
	"""
    
	for e in entidades_loc:
		if (e.text.lower() == palavra.lower()):
			return True

	return False

def lista_para_texto(lista):
    """
	Transforma uma lista de palavras em texto.

	Parâmetros:
	----------
	lista : List
		- Lista de palavras.

	Retorno:
	----------
	texto : String
		- O texto contento todas as palavras da lista.
	"""
    texto = ""
    for palavra in lista:
        texto += palavra + " "

    return texto.strip()

# Configurando bibliotecas e variaveis globais.
stemmer = PorterStemmer()
nlp = spacy.load("pt_core_news_sm")

nlp.Defaults.stop_words |= {"tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui", "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá", "hoje", "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "rua", "bairro", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"}
stop_words_spacy = nlp.Defaults.stop_words

def lematizacao(palavra):
    """
	Realiza a lematização de uma palavra.

	Parâmetro:
	----------
	palavra : String
		- Palavra que irá sofrer a lematização.

	Retorno:
	----------
	palavra : String
		- Palavra lematizada.
	"""
    return stemmer.stem(WordNetLemmatizer().lemmatize(palavra, pos="v"))

allowed_postags = ['NOUN', 'ADJ', 'PRON']
def pre_processamento(texto, titulo):
    """
	Realiza o pré-processamento de um texto:
		- Remove Stop Words.
		- Remove palavras que são entidades de localizações.
		- Colocar as palavras para caixa baixa.
		- Realiza a lematização das palavras.
		- Apenas palavras que são: substantivos, adjetivos e pronomes.

	Parâmetro:
	----------
	texto : String
		- Texto que irá sofrer o pré-processamento.
	titulo: String
		- Titulo do texto.

	Retorno:
	----------
	doc_out : List
		- Lista de palavras que passaram pelo pré-processamento.
	"""
    doc_out = []
    doc = nlp(texto)
    entidades_loc = [entidade for entidade in doc.ents if entidade.label_ == "LOC"]
    for token in doc:
        if (token.text not in stop_words_spacy and len(token.text) > 3 and token.pos_ in allowed_postags and not verificar_palavra_entidade_loc(token.text, entidades_loc)):
            doc_out.append(lematizacao(token.text))

    texto = lista_para_texto(doc_out)
    return texto

# PREPARANDO ARQUIVOS.

fields = ["titulo", "texto"]
f = csv.writer(open('../dados/textos_limpos.csv', 'w', encoding='utf-8'))
f.writerow(fields)

# Carregando dados.
dados = csv.DictReader(open("../dados/textos_videos.csv", encoding='utf-8'))
textos = []
titulo_textos = []

for arq in dados:
    textos.append(arq['texto'])
    titulo_textos.append(arq['titulo'])

for texto, titulo in zip(textos, titulo_textos):
	t = pre_processamento(texto, titulo)
	f.writerow([titulo, t])