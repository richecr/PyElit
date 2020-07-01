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
    Topic Modeling Class with a coherence score of 0.52.
    As an unsupervised learning approach is used, no accuracy tests
    were performed, but those that were performed manually
    obtained good results.

    It allows from a text to be able to describe which topic that
    text belongs to with a good probability.
    """

    def __init__(self):
        """
        Class constructor. Starts the main objects/attributes
        for its operation.
        """
        self.stemmer = PorterStemmer()
        self.nlp = spacy.load("pt_core_news_sm")
        self.nlp.Defaults.stop_words |= {
            "tudo", "coisa", "toda", "tava", "pessoal", "dessa", "resolvido",
            "aqui", "gente", "tá", "né", "calendário", "jpb", "agora",
            "voltar", "lá", "hoje", "aí", "ainda", "então", "vai", "porque",
            "moradores", "fazer", "rua", "bairro", "prefeitura", "todo",
            "vamos", "problema", "fica", "ver", "tô"
        }
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
        doc = self.nlp(text)
        location_entities = [
            entity for entity in doc.ents if entity.label_ == "LOC"]
        for token in doc:
            if (token.text not in self.stop_words_spacy and
                len(token.text) > 3 and
                token.pos_ in self.allowed_postags and not
                    self.is_entities_loc(token.text, location_entities)):
                doc_out.append(self.lemmatization(token.text))

        return doc_out

    def lemmatization(self, word):
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
        return self.stemmer.stem(WordNetLemmatizer().lemmatize(word, pos="v"))

    def is_entities_loc(self, word, location_entities):
        """
        Method that check if the word is entity of location.

        Params:
        ----------
        word : String
            - Word.
        location_entities : List
            - List of location entities recognized by spacy.

        Return:
        ----------
        True: If the word is a location entity.\n
        False: Othwerwise..
        """
        for entity in location_entities:
            if (entity.text.lower() == word.lower()):
                return True

        return False

    def print_keywords(self, max_number_words=None):
        """
        Method that will print the keywords for each of topics in the model.

        Params:
        ----------
        max_number_words: Int
            - Maximum number of words that representing a topic to be returned

        Return:
        ----------
        topics : List
            - List of keywords for topics in the model.
        """
        if max_number_words is None:
            max_number_words = 5
        topics = []
        for topic in self.model.print_topics(-1, max_number_words):
            topics.append(topic)
        return topics

    def print_topics(self):
        """
        Method that will print each of topics in the model.

        Return:
        ----------
        topics : List
            - List of topics in the model.
        """
        return self.topics

    def represent_topics(self, ids_topics, names_topics):
        """
        Method that will set the values to the topics.

        NOTE: The two must come in the same order, name in position 0
        is from id in position 0.


        Params:
        ----------
        ids_topics: List
            - List of ids in the topics.
        names_topics: List
            - List of names of topics.
        """
        for id_topic, name in zip(ids_topics, names_topics):
            self.topics[id_topic] = name

    def get_topic(self, id_topic):
        """
        Method that returns the representation of the topic.

        Params:
        ----------
        id_topic: Int
            - Integer that represent the topic.

        Return:
        ----------
        topics: String
            - The name that represent the topic with the `id_topic`.
        """
        return self.topics[id_topic]

    def rate_text(self, text):
        """
        Method that will return from which topic the text is more
        likely to belong to.

        Params:
        ----------
        text : String
            - Text that will to be evaluate.

        Return:
        ----------
        result : List
            - List of tuples with id of topic that the text belongs
            and probability.
        """
        bow_vector = self.model.id2word.doc2bow(self.pre_processing(text))
        result = self.model.get_document_topics(bow_vector)
        result = sorted(result, reverse=True, key=lambda t: t[1])
        return result
