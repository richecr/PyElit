import pytest

from pyelit import TopicModeling


@pytest.fixture
def init_topic_modeling():
    tModeling = TopicModeling()
    return tModeling


class TestTopicModeling:
    tModeling = TopicModeling()

    def test_topic_modeling_simple(self, init_topic_modeling):
        result = init_topic_modeling.rate_text(
            "Tem um buraco na minha rua e a prefeitura não faz nada")

        assert result[0][0] == 0  # Saneamento

    def test_topic_modeling_print_keywords(self, init_topic_modeling):
        print(init_topic_modeling.print_keywords())
        assert init_topic_modeling.print_keywords(
        )[0] == (0, '0.016*"água" + 0.015*"esgoto" + 0.010*"calçamento" + ' +
                 '0.010*"casa" + 0.009*"buraco"')

    def test_topic_modeling_print_topics(self, init_topic_modeling):
        assert init_topic_modeling.print_topics(
        ) == {0: 'saneamento', 1: 'trânsito', 2: 'obras', 3: 'diversos'}

    def test_topic_modeling_get_topic(self, init_topic_modeling):
        assert init_topic_modeling.get_topic(0) == "saneamento"
        assert init_topic_modeling.get_topic(1) == "trânsito"
        assert init_topic_modeling.get_topic(2) == "obras"
        assert init_topic_modeling.get_topic(3) == "diversos"

    def test_topic_modeling_represent_topics(self, init_topic_modeling):
        ids = [0, 1, 2, 3]
        names = ['SANEAMENTO', 'TRÂNSITO', 'OBRAS', 'DIVERSOS']
        init_topic_modeling.represent_topics(ids, names)

        assert init_topic_modeling.get_topic(0) == "SANEAMENTO"
        assert init_topic_modeling.get_topic(1) == "TRÂNSITO"
        assert init_topic_modeling.get_topic(2) == "OBRAS"
        assert init_topic_modeling.get_topic(3) == "DIVERSOS"
