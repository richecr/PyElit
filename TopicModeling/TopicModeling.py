import nltk
import spacy
import gensim
import numpy as np
import pandas as pd
from nltk.stem import *
from nltk.stem.porter import *
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from gensim import corpora, models
from gensim.test.utils import datapath
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess, deaccent
from gensim.models.coherencemodel import CoherenceModel
import pyLDAvis.gensim

class TopicModeling:
    """
        Classe de Modelagem de tópicos com um score de coherence de 0.52. Descreve textos que tratam sobre problemas urbanos.
        
        Permite que a partir de um texto eu consiga descrever qual tópico esse texto pertence com uma boa probabilidade.
    """
    def __init__(self):
        """
            Construtor da classe. Inicia os principais objetos/variaveis para o funcionamento do mesmo.
        """
        self.stemmer = PorterStemmer()
        self.nlp = spacy.load("pt_core_news_sm")
        self.nlp.Defaults.stop_words |= {"tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui", "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá", "hoje", "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "rua", "bairro", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"}
        self.stop_words_spacy = self.nlp.Defaults.stop_words
        np.random.seed(2018)
        nltk.download('wordnet')
        self.allowed_postags = ['NOUN', 'ADJ', 'PRON']
        # Carrega o modelo.
        fname = datapath("./modelo/meu_lda_model")
        self.model = gensim.models.LdaMulticore.load(fname="./modelo/meu_lda_model")

    def pre_processing(self, text):
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
        doc = self.nlp(text)
        entidades_loc = [entidade for entidade in doc.ents if entidade.label_ == "LOC"]
        for token in doc:
            if (token.text not in self.stop_words_spacy and len(token.text) > 3 and token.pos_ in self.allowed_postags and not self.remove_entities_loc(token.text, entidades_loc)):
                doc_out.append(self.lemmatization(token.text))

        return doc_out

    def lemmatization(self, palavra):
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
        return self.stemmer.stem(WordNetLemmatizer().lemmatize(palavra, pos="v"))

    def remove_entities_loc(self, word, entities_loc):
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

    def check_entity_word_loc(self, palavra, entities_loc):
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

    def print_topics(self):
        """
            Método que irá imprimir os tópicos do modelo.
            Retorno:
            ----------
            topics : List
                - Lista de tópicos do modelo.
        """
        topics = []
        for topic in model.print_topics(-1, 15):
            topics.append(topic)

    def rate_text(self, text):
        """
            Método que irá retorna de qual tópico o texto passado como parametro tem mais probabilidade de pertencer.
            
            Parâmetro:
            ----------
            texto : String
                - Texto que irá ser avaliado.

            Retorno:
            ----------
            Topico : List
                - Uma lista contento o tópico que esse texto pertence e também sua probabilidade.
        """
        bow_vector = self.model.id2word.doc2bow(self.pre_processing(text))
        result = self.model.get_document_topics(bow_vector)
        return result

m = TopicModeling()
r = m.rate_text('calendário JPB aqui nas nossas telas nós vamos agora até o bairro Jardim Paulistano zona sul de Campinas Você lembra que nossa equipe ouviu os moradores da Rua Riachuelo que reclamavam da falta de calçamento no local então o problema foi resolvido só que na época a prefeitura também se comprometeu e fazer o calçamento da Rua Ariel que fica bem pertinho essa parte foi feita mas só que pela metade Laisa grisi foi conferido calendário JPB desembarcou aqui no Jardim Paulistano E olha que maravilha hoje é possível andar na rua com calçamento sem tanta poeira sem pisar em lama Quando chove essa foi uma conquista dos moradores junto com calendário Desde o ano passado em 2015 quando a prefeitura calçou essa rua calça com a Rua Riachuelo também mas presta atenção dois passos seguintes e rua de terra essa rua que esse trechinho não foi calçado vou aqui conversar com os moradores já tá todo mundo reunido Por que me explica como é que pode só esse trechinho não foi calçada só esse trecho você imagina que fizeram as duas por duas partes né fizeram aquela parte de lá aí ficou a metade depois fizeram essa daqui aí deixar essa parte aqui sem sem tá feita né nessa parte de baixo é pior ainda porque quando chove a água invade a Casa dos moradores e olha só aqui nessa casa foi colocado um monte de pedra bem na frente para impedir que a água entre vamos lá falar com ela é dona Severina é dona Bill Olá tudo bom com a senhora como é que tá aqui essa situação a senhora Teve que colocar pedra aqui né é chover em entrar aqui sozinha imagina aperreio Aí tem que dar um jeito aqui é pior difícil hein dona Bill quanto tempo já que a senhora mora aqui nessa rua 8 anos viu o resultado de vergonha né a gente não tem né É porque se ele tivesse vergonha ele já tinha feito isso todos vocês moram aqui nessa rua aí o que que acontece nessas ruas aqui né aí o que que acontece a Rua Areal lá em cima Foi calçada a Rua Riachuelo também E vocês ficaram só um gostinho só na saudade e o pior que não se desviar da Lama dos buracos e ele prometeu Então olha você tá vendo aquela cerâmica Vale Aí depois ele dá o que é o povo que bota para que ele possa passar infelizmente é uma situação difícil a gente já pediu muitas vezes recado dado essa essa rua que já é assunto do calendário a gente conseguiu algumas ruas outras não voltamos em 2016 em 2016 o secretário André agra secretário de obras de Campina Grande e disse que ia voltar aqui não foi então vamos lá calendário novo quem é o representante')

print(r)