class GeoparsingException(Exception):
    """
    Geoparsing Exception
    """

    def __init__(self, msg="Text geoparsing could not be performed"):
        self.msg = msg

    def __str__(self):
        return "Erro: {}".format(self.msg)