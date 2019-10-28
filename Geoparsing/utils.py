import csv
import pandas as pd
from plpygis import Geometry

def converterGeometryPoint(geometry):
    g = Geometry(geometry)
    coord = g.geojson['coordinates']
    return [coord[1], coord[0]]

# print(converterGeometryPoint("0101000000A46C36FBA8F241C0C3E1BB838EF41CC0"))

#gazetteer_ln = csv.reader(open("./gazetteer/processados/gazetteer_ln.csv", "r", encoding='utf-8'))
gazetteer_ln = pd.read_csv(open("./gazetteer/processados/gazetteer_ln.csv"))
a = "[[-7.2283327, -35.8862199], [-7.228354, -35.8860804], [-7.228354, -35.8860804], [-7.228354, -35.8860804]]"
b = a.replace("[", "")
b = b.replace("]", "")

a = b.split(", ")
print(a)

lat = []
lon = []
for i in range(len(a)):
    if i % 2 == 0:
        lat.append(float(a[i]))
    else:
        lon.append(float(a[i]))

print("Lat: ", sum(lat) / len(lat))
print("Lon: ", sum(lon) / len(lon))

# print(gazetteer_ln.values[10][4])
# c = 0
# for i in a:
#     print(type(i[4]))
#     if c == 1:
#         break
#     else:
#         c = 1
