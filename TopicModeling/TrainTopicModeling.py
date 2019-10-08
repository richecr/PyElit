import nltk
import spacy
import gensim
import numpy as np
import pandas as pd
import pyLDAvis.gensim
from nltk.stem import *
from nltk.stem.porter import *
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from gensim import corpora, models
from nltk import word_tokenize, pos_tag
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess, deaccent
from gensim.models.coherencemodel import CoherenceModel

# Configurando bibliotecas e variaveis globais.
stemmer = PorterStemmer()
nlp = spacy.load("pt_core_news_sm")

nlp.Defaults.stop_words |= {"tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui", "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá", "hoje", "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "rua", "bairro", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"}
stop_words_spacy = nlp.Defaults.stop_words

# CONFIGURAÇÕES DE BIBLIOTECAS.
np.random.seed(2018)
nltk.download('wordnet')
nlp = spacy.load('pt_core_news_sm')

allowed_postags = ['NOUN', 'ADJ', 'PRON']

# CARREGANDO OS DADOS.
dados = pd.read_csv("../dados/textos_videos.csv")
dados.drop_duplicates(['texto'], inplace=True)
textos = dados['texto']
# print(textos[:5])

# PRÉ-PROCESSAMENTO DOS DADOS.

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

def pre_processamento(texto):
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

def init():
    # Chamando a função de pré-processamento para cada texto.
    processed_docs = dados['texto'].map(lambda texto: pre_processamento(texto).split())
    print(processed_docs[:10])

    # Criando dicionário de palavras.
    dictionary = gensim.corpora.Dictionary(processed_docs)

    # Gensim Filter Extremes
    # Filtrar tokens que aparecem em menos de 15 documentos
    # ou em mais de 0.5 documentos(fração do tamanho total do corpus)
    # Após essas duas etapas, mantenha apenas os 100000
    dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

    # Bag of Words(Saco de Palavras).
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    # Usando TF-IDF.
    tfidf = models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]

    # Criando e treinando o modelo.
    lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=4, id2word=dictionary, passes=10, workers=4)
    # lda_model_tfidf.save("./modelo/meu_lda_model")
    return lda_model_tfidf

lda_model_tfidf = init()

# Imprimir os tópicos do modelo.
topics = lda_model_tfidf.show_topics()
print(topics)

# Verificando o 'coherence score' para avaliar a qualidade dos tópicos aprendidos.
def coherence_model(lda_model_, processed_docs, corpus_tfidf, dictionary):
	coherence_model_lda = CoherenceModel(model=lda_model_, texts=processed_docs, corpus=corpus_tfidf, dictionary=dictionary, coherence='c_v')
	coherence_lda = coherence_model_lda.get_coherence()
	print('\nCoherence Score LDAModelTfIdf: ', coherence_lda)
coherence_model(lda_model_tfidf, processed_docs, corpus_tfidf, dictionary)