from pyelit import Geoparsing
from pyelit import TopicModeling

# Geoparsing
g = Geoparsing()
r = g.geoparsing(
    "Eu moro na Rua Treze de Maio no centro de campina grande", gazetteer_cg=True)

print(r[:3])

print(len(r))

# Topic Modeling
# t = TopicModeling()
# r = t.rate_text("Minha rua esta cheia de lixo, as pessoas não respeitam nada")

# print(t.print_keywords(quant_max_palavras=5))

# print(r)
