import os
import nltk
import spacy
import gensim
import numpy as np
import pyLDAvis.gensim
from nltk.stem import *
from nltk.stem.porter import *
import matplotlib.pyplot as plt
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
        self.nlp.Defaults.stop_words |= {"tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido", "aqui", "gente", "tá", "né", "calendário", "jpb", "agora", "voltar", "lá", "hoje", "aí", "ainda", "então", "vai", "porque", "moradores", "fazer", "rua", "bairro", "prefeitura", "todo", "vamos", "problema", "fica", "ver", "tô"}
        self.stop_words_spacy = self.nlp.Defaults.stop_words
        np.random.seed(2018)
        nltk.download('wordnet')
        self.allowed_postags = ['NOUN', 'ADJ', 'PRON']
        # Carrega o modelo.
        ROOT = os.path.abspath(os.path.dirname(__file__))
        fname = datapath(ROOT + "/modelo/meu_lda_model")
        self.model = gensim.models.LdaMulticore.load(fname=fname)
        self.topics = {}
        self.represent_topics([0, 1, 2, 3], ['saneamento', 'trânsito', 'obras', 'diversos'])

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
        entidades_loc = [entidade for entidade in doc.ents if entidade.label_ == "LOC"]
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

    def print_topics(self, quant_max_palavras=None):
        """
        Método que irá imprimir os tópicos do modelo.

        Parâmetros:
        ----------
        quant_max_palavras: Int
            - Quantidade máxima de palavras que representam um tópico a serem retornadas.

        Retorno:
        ----------
        topics : List
            - Lista de tópicos do modelo.
        """
        if quant_max_palavras == None:
            quant_max_palavras = 5
        topics = []
        for topic in self.model.print_topics(-1, quant_max_palavras):
            topics.append(topic)
        return topics

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
        reult : List
            - Uma lista de tuplass com o id do tópico que esse texto pertence e também a probabilidade.
        """
        bow_vector = self.model.id2word.doc2bow(self.pre_processing(text))
        result = self.model.get_document_topics(bow_vector)
        return result

# m = TopicModeling()
# # print(m.print_topics())
# # m.represent_topics([0, 1, 2, 3], ['saneamento', 'trânsito', 'obras', 'diversos'])
# r = m.rate_text('a gente chegou o Ginásio da Escola Maria honorina Santiago lá em Santa Rita a gente não passava de um depósito teve luta Teve muita insistência diga logo que não vamos carimbar o resolvido hoje ainda mais a sensação é quase essa Quem esteve aqui em outubro do ano passado e entra agora na escola só percebe muita diferença por exemplo nessa rampa aqui o piso era outro inadequado mas o nosso objetivo mesmo tá lá dentro o Ginásio da escola bota o capacete porque ainda é um ambiente obra né Se bem que a gente olha e já é outra escola daquela que a gente chegou aqui com certeza a escola está praticamente pronto tá faltando alguns detalhes de pintura por fora precisa secar parar de chover para secar para que as paredes ficam resistente a minha curiosidade hoje é o vinagre Bora lá chega aqui que eu não tô reconhecendo bem o ambiente porque esse caminho aqui com cobertura não existia rei da escola e pré-escola errada porque tá completamente diferente eu lembro que na primeira vez que o calendário teve aqui uma amiga de vocês que é cadeirante nem pode ir até o ginásio porque não tinha como ir hoje ela já teria condições de Com certeza a gente fez tudo isso mas pensando mais né Olha só o suspense abrindo a porta do ginásio Olha o colorido gente olha só que coisa linda que tá esse ginásio o chão chega brilha Pois é é lindo de ver isso eu tô vendo que tá tudo pintado já esse piso que era uma das fases mais complicadas da obra também já tá pronto é a área mais demorada era esse piso né tá pronto já está pronto como foi a primeira solicitação dos alunos do ginásio está concluído e Inclusive a parte de vestiário a parte de banheiro toda concluída a pintura concluída o piso concluído e a partir da escola está sendo concluída também dá para lembrar aí na edição como era antes e como tá agora é diferente porque antigamente não tinha nem o piso não tinha nada a infraestrutura mudou bastante banheiro e vestiário masculino também com acessibilidade aqui dá para cadeira de rodas passar e aqui atrás os chuveiros calendário JPB E hoje vai marcar o carimbo em andamento mas é um em andamento assim um sabor de Resolvido e aqui eu coloco o carinho em andamento qual seria um prazo bom para a gente voltar aqui testa segurança que os alunos querem festa vamos fazer')

# print(r)
# print(m.get_topic(r[0][0]))

