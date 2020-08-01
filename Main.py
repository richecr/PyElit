from pyelit import Geoparsing
from pyelit import TopicModeling

# Geoparsing
g = Geoparsing()
r = g.geoparsing(
    "Eu moro na Rua Treze de Maio no centro de campina grande",
    gazetteer_cg=True)

print(r[:3])

# Topic Modeling
# t = TopicModeling()
# text = "Minha rua esta cheia de lixo, as pessoas não respeitam nada"
# r = t.rate_text(text)

# print(t.print_keywords(max_number_words=5))

# print(r)
