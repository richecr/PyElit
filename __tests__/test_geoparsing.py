import pytest

from pyelit import Geoparsing


@pytest.fixture
def init_geoparsing():
    geoparsing = Geoparsing()
    return geoparsing


class TestGeoparsing:
    geoparsing = Geoparsing()

    def test_geoparsing_simple(self, init_geoparsing):
        result = init_geoparsing.geoparsing(
            text="Eu moro na rua joão sérgio de almeida")

        address_correct = "Rua João Sérgio de Almeida, " + \
            "Malvinas, Campina Grande, Paraíba, 58433-395"
        assert type(result) == list
        assert result[0]['address'] == address_correct

    def test_geoparsing_case_correct(self, init_geoparsing):
        result = init_geoparsing.geoparsing(
            text="Eu moro na Rua João Sérgio de Almeida", case_correct=True)

        address_correct = "Rua João Sérgio de Almeida, " + \
            "Malvinas, Campina Grande, Paraíba, 58433-395"
        assert type(result) == list
        assert result[0]['address'] == address_correct

    def test_geoparsing_case_using_gazetteer(self, init_geoparsing):
        result = init_geoparsing.geoparsing(
            text="Eu moro na Rua João Sérgio de Almeida", gazetteer_cg=True)

        address_correct = "Rua João Sérgio de Almeida 1015-1015, " + \
            "Bodocongó, Campina Grande, Paraíba, 58433-395"
        assert type(result) == list
        assert result[0]['address'] == address_correct
        assert result[0]['city'] == "Campina Grande"
        assert result[0]['occurrences_in_text'] == 1

    def test_geoparsing_simple_exception(self, init_geoparsing):
        with pytest.raises(Exception):
            init_geoparsing.geoparsing(
                text="Eu moro na rua joão sérgio em campina grande")

    def test_geoparsing_case_correct_exception(self, init_geoparsing):
        with pytest.raises(Exception):
            init_geoparsing.geoparsing(
                text="Eu moro na rua joão sérgio de almeida",
                case_correct=True)

    def test_geoparsing_case_using_gazetteer_exception(self, init_geoparsing):
        with pytest.raises(Exception):
            init_geoparsing.geoparsing(
                text="Eu moro na rua joão sérgio", gazetteer_cg=True)
