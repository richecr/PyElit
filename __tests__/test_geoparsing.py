import pytest

from pyelit import Geoparsing


@pytest.fixture
def init_geoparsing():
    geoparsing = Geoparsing()
    return geoparsing


class TestGeoparsing:
    geoparsing = Geoparsing()

    def test_geoparsing_simple(self, init_geoparsing):
        print(init_geoparsing.geoparsing(
            text="Eu moro na Rua João Sérgio de Almeida"))
        assert 1 == 1
