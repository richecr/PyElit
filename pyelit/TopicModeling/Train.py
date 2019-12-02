import nltk
import random
import spacy
import gensim
import numpy as np
import pandas as pd
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel

from sklearn.model_selection import train_test_split

def main_cross_val():
	# Configurando bibliotecas para ter um melhor resultado.
	np.random.seed(2018)
	nltk.download('wordnet')
	nlp = spacy.load('pt_core_news_sm')

	# PREPARANDO ARQUIVOS.
	dados = pd.read_csv("../../dados/textos_limpos.csv")
	dados.drop_duplicates(['texto'], inplace=True)
	textos = dados['texto']
	textos = [str(texto) for texto in textos]
	cross = kfoldcv(textos)
	print("Total: ", len(textos))
	print(len(cross))

	for train_tests in cross:
		print(len(train_tests))
		train = train_tests[0]
		test = train_tests[1]

		# print(train)
		processed_docs = [t1.split() for t in train for t1 in t]
		processed_test = [t.split() for t in test]

		print("Train: ", len(processed_docs))
		print("Tests: ", len(processed_test))

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

		coherence_model(lda_model_tfidf, processed_test, corpus_tfidf, dictionary)


def coherence_model(lda_model_, tests, corpus, dictionary):
	coherence_model_lda = CoherenceModel(model=lda_model_, texts=tests, corpus=corpus, dictionary=dictionary, coherence='c_v')
	coherence_lda = coherence_model_lda.get_coherence()
	print('\nCoherence Score LDAModelTfIdf: ', coherence_lda)

def kfoldcv(dados, k = 6, seed = 42):
	size = len(dados)
	subset_size = round(size / k)
	random.Random(seed).shuffle(dados)
	subsets = [dados[x:x+subset_size] for x in range(0, len(dados), subset_size)]
	kfolds = []
	for i in range(k):
		test = subsets[i]
		train = []
		for subset in subsets:
			if subset != test:
				train.append(subset)
		kfolds.append((train,test))
	
	return kfolds

main_cross_val()

# def main():
# 	# Configurando bibliotecas para ter um melhor resultado.
# 	np.random.seed(2018)
# 	nltk.download('wordnet')
# 	nlp = spacy.load('pt_core_news_sm')

# 	# PREPARANDO ARQUIVOS.
# 	dados = pd.read_csv("../../dados/textos_limpos.csv")
# 	dados.drop_duplicates(['texto'], inplace=True)
# 	textos = dados['texto']

# 	processed_docs = dados['texto'].map(lambda texto: texto.split())
# 	print(processed_docs[:10])

# 	# Criando dicionário de palavras.
# 	dictionary = gensim.corpora.Dictionary(processed_docs)

# 	# Gensim Filter Extremes
# 	# Filtrar tokens que aparecem em menos de 15 documentos
# 	# ou em mais de 0.5 documentos(fração do tamanho total do corpus)
# 	# Após essas duas etapas, mantenha apenas os 100000
# 	dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

# 	# Bag of Words(Saco de Palavras).
# 	bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

# 	# Usando TF-IDF.
# 	tfidf = models.TfidfModel(bow_corpus)
# 	corpus_tfidf = tfidf[bow_corpus]

# 	# Criando e treinando o modelo.
# 	lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=4, id2word=dictionary, passes=10, workers=4, alpha=0.01, eta=0.9)
# 	# lda_model_tfidf.save("./modelo/meu_lda_model")

# 	def coherence_model(lda_model_, processed_docs, corpus_tfidf, dictionary):
# 		coherence_model_lda = CoherenceModel(model=lda_model_, texts=processed_docs, corpus=corpus_tfidf, dictionary=dictionary, coherence='c_v')
# 		coherence_lda = coherence_model_lda.get_coherence()
# 		print('\nCoherence Score LDAModelTfIdf: ', coherence_lda)

# 	coherence_model(lda_model_tfidf, processed_docs, corpus_tfidf, dictionary)
# main()
