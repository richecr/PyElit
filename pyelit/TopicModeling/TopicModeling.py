import os
import nltk
import spacy
import gensim
import numpy as np
import pyLDAvis.gensim
from nltk.stem import *
from nltk.stem.porter import *
from nltk.corpus import stopwords
from gensim import corpora, models
from gensim.test.utils import datapath
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess, deaccent
from gensim.models.coherencemodel import CoherenceModel


class TopicModeling:
    """
    Classe de Modelagem de tópicos com um score de coherence de 0.52.
    Como é usado uma abordagem de aprendizado não-supervisionado não foi
    feito testes de acurácia, mas os que foram realizados manualmente 
    obteram bons resultados.
    Descreve textos que tratam sobre problemas urbanos.

    Permite que a partir de um texto seja possível descrever qual tópico aquele texto pertence, com uma boa probabilidade.
    """

    def __init__(self):
        """
        Construtor da classe. Inicia os principais objetos/atributos para o funcionamento do mesmo.
        """
        self.stemmer = PorterStemmer()
        self.nlp = spacy.load("pt_core_news_sm")
        self.nlp.Defaults.stop_words |= {"tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui", "gente", "tá", "né", "calendário", "jpb", "agora", "voltar",
                                         "lá", "hoje", "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "rua", "bairro", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"}
        self.stop_words_spacy = self.nlp.Defaults.stop_words
        np.random.seed(2018)
        nltk.download('wordnet')
        self.allowed_postags = ['NOUN', 'ADJ', 'PRON']
        # Carrega o modelo.
        ROOT = os.path.abspath(os.path.dirname(__file__))
        fname = datapath(ROOT + "/modelo/meu_lda_model")
        self.model = gensim.models.LdaMulticore.load(fname=fname)
        self.topics = {}
        self.represent_topics(
            [0, 1, 2, 3], ['saneamento', 'trânsito', 'obras', 'diversos'])

    def pre_processing(self, text):
        """
        Realiza o pré-processamento de um texto:
            - Remove Stop Words.
            - Remove palavras que são entidades de localizações.
            - Coloca todo o texto para caixa baixa.
            - Realiza a lematização das palavras.
            - Deixa apenas palavras que são: substantivos, adjetivos e pronomes.

        Parâmetro:
        ----------
        text : String
            - Texto que irá sofrer o pré-processamento.

        Retorno:
        ----------
        doc_out : List
            - Lista de palavras que passaram pelo pré-processamento.
        """
        doc_out = []
        doc = self.nlp(text)
        entidades_loc = [
            entidade for entidade in doc.ents if entidade.label_ == "LOC"]
        for token in doc:
            if (token.text not in self.stop_words_spacy and len(token.text) > 3 and token.pos_ in self.allowed_postags and not self.is_entities_loc(token.text, entidades_loc)):
                doc_out.append(self.lemmatization(token.text))

        return doc_out

    def lemmatization(self, word):
        """
        Realiza a lematização de uma palavra.

        Parâmetro:
        ----------
        word : String
            - Palavra que irá sofrer a lematização.

        Retorno:
        ----------
        word : String
            - Palavra lematizada.
        """
        return self.stemmer.stem(WordNetLemmatizer().lemmatize(word, pos="v"))

    def is_entities_loc(self, word, entities_loc):
        """
        Verifica se a palavra é uma entidade de localização.

        Parâmetros:
        ----------
        word : String
            - Palavra a ser verificada.
        entities_loc : List
            - Lista de entidades de localizações reconhecidas pelo Spacy.

        Retorno:
        ----------
        True : Caso a palavra seja uma entidade de localização.\n
        False : Caso a palavra não seja uma entidade de localização.
            """
        for e in entities_loc:
            if (e.text.lower() == word.lower()):
                return True

        return False

    def print_keywords(self, quant_max_palavras=None):
        """
        Método que irá imprimir as palavras chaves de cada tópicos do modelo.

        Parâmetros:
        ----------
        quant_max_palavras: Int
            - Quantidade máxima de palavras que representam um tópico a serem retornadas.

        Retorno:
        ----------
        topics : List
            - Lista de palavras chaves por tópicos do modelo.
        """
        if quant_max_palavras == None:
            quant_max_palavras = 5
        topics = []
        for topic in self.model.print_topics(-1, quant_max_palavras):
            topics.append(topic)
        return topics

    def print_topics(self):
        return self.topics

    def represent_topics(self, ids_topics, names_topics):
        """
        Método que irá setar os valores para os tópicos, dando nomes.

        Parâmetros:
        ----------
        ids_topics: List
            - Lista de ids dos tópicos.
        names_topics: List
            - Lista de nomes dos tópicos.
        Os dois devem vim na mesma ordem, nome na posição 0 é do id na posição 0.
        """
        for id_topic, name in zip(ids_topics, names_topics):
            self.topics[id_topic] = name

    def get_topic(self, id_topic):
        """
        Método que retorna a representação de um tópico.

        Parâmetro:
        ----------
        id_topic: Int
            - Inteiro que representa o tópico.
        """
        return self.topics[id_topic]

    def rate_text(self, text):
        """
        Método que irá retorna de qual tópico o texto, passado como parametro, tem mais probabilidade de pertencer.

        Parâmetro:
        ----------
        text : String
            - Texto que irá ser avaliado.

        Retorno:
        ----------
        result : List
            - Uma lista de tuplass com o id do tópico que esse texto pertence e também a probabilidade.
        """
        bow_vector = self.model.id2word.doc2bow(self.pre_processing(text))
        result = self.model.get_document_topics(bow_vector)
        result = sorted(result, reverse=True, key=lambda t: t[1])
        return result
