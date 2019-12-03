from pyelit.Geoparsing import Geoparsing

g = Geoparsing()
r = g.geoparsing("Eu moro na Rua Treze de Maio no centro de campina grande", gazetteer_cg=True)

print(r[:3])

print(len(r))