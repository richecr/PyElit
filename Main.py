from pyelit import Geoparsing
from pyelit import TopicModeling

# Geoparsing
g = Geoparsing()
result = g.geoparsing(text="Eu moro na rua joão sérgio em campina grande")

address_correct = (
    "Rua João Sérgio de Almeida, " + "Malvinas, Campina Grande, Paraíba, 58433-395"
)
print(result)
print(type(result) == list)
print(result[0]["address"] == address_correct)

# Topic Modeling
# t = TopicModeling()
# text = "Minha rua esta cheia de lixo, as pessoas não respeitam nada"
# r = t.rate_text(text)

# print(t.print_keywords(max_number_words=5))

# print(r)
