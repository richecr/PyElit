from plpygis import Geometry
import csv
import sys

# Aumentando o tamanho limite do csv.
maxInt = sys.maxsize
csv.field_size_limit(maxInt)

def convertGeometryPoint(geometry):
	"""
	Função de pré-processamento que transformar um código em geometria para uma lista de floats.

	Parâmetros:
	----------
	geometry : String
		- String que representa um coordenada geometrica de um ponto.

	Retorno:
	----------
	coord : List
		- Lista de coordenadas.
	"""
	g = Geometry(geometry)
	coord = g.geojson['coordinates']
	coord.reverse()
	return coord

def convertGeometryPolygon(geometry):
	"""
	Função de pré-processamento que transformar um código em geometria para uma lista de floats.

	Parâmetros:
	----------
	geometry : String
		- String que representa um coordenada geometrica de um polígono.

	Retorno:
	----------
	coord : List
		- Lista de coordenadas.
	"""
	g = Geometry(geometry)
	coord = g.geojson['coordinates']
	saida = []
	for c in coord[0]:
		c.reverse()
		saida.append(c)
	return saida

def convertFeature(geometry):
	"""
	Função de pré-processamento que transformar um código em geometria para uma lista de floats.

	Parâmetros:
	----------
	geometry : String
		- String que representa um coordenada geometrica de uma feature.

	Retorno:
	----------
	coord : List
		- Lista de coordenadas.
	"""
	g = Geometry(geometry)
	coord = g.geojson['coordinates'][0][0]
	saida = []
	for c in coord:
		c.reverse()
		saida.append(c)
	return saida

def polygons(localidade="cg"):
	"""
	Função de pré-processamento escreve dados dos endereços de poligonos em outro arquivo
	com as coordenadas normalizadas.

	Parâmetros:
	----------
	localidade : String
		- String que representa a cidade/estado("cg", "jp" ou "pb").
	"""
	if (localidade == "cg"):
		arq = csv.DictReader(open("./gazetteer/features_campina_ln.csv", "r", encoding='utf-8'))
	elif (localidade == "jp"):
		arq = csv.DictReader(open("./gazetteer/features_jp_ln.csv", "r", encoding='utf-8'))
	elif (localidade == "pb"):
		arq = csv.DictReader(open("./gazetteer/features_paraiba_ln.csv", "r", encoding='utf-8'))
	
	fields = ["osm_id", "fclass", "name", "type", "coordenates"]
	f = csv.writer(open('./gazetteer/processados/' + localidade + '_ln.csv', 'w', encoding='utf-8'))
	f.writerow(fields)

	for p in arq:
		coord = convertGeometryPolygon(p['geometry'])
		t = [ p['osm_id'].__str__(), p["fclass"].__str__(), p["name"].__str__(), p["type"].__str__(), coord ]
		f.writerow(t)

def points(localidade="cg"):
	"""
	Função de pré-processamento escreve dados dos endereços de pontos em outro arquivo
	com as coordenadas normalizadas.

	Parâmetros:
	----------
	localidade : String
		- String que representa a cidade/estado("cg", "jp" ou "pb").
	"""
	if (localidade == "cg"):
		arq = csv.DictReader(open("./gazetteer/features_campina_pt.csv", "r", encoding='utf-8'))
	elif (localidade == "jp"):
		arq = csv.DictReader(open("./gazetteer/features_jp_pt.csv", "r", encoding='utf-8'))
	elif (localidade == "pb"):
		arq = csv.DictReader(open("./gazetteer/features_paraiba_pt.csv", "r", encoding='utf-8'))

	fields = ["osm_id", "fclass", "name", "type", "coordenates"]
	f = csv.writer(open('./gazetteer/processados/' + localidade + '_pt.csv', 'w', encoding='utf-8'))
	f.writerow(fields)

	for p in arq:
		coord = convertGeometryPoint(p['geometry'])
		t = [ p['osm_id'].__str__(), p["fclass"].__str__(), p["name"].__str__(), p["type"].__str__(), coord ]
		f.writerow(t)

def features(localidade="cg"):
	"""
	Função de pré-processamento escreve dados dos endereços de features em outro arquivo
	com as coordenadas normalizadas.

	Parâmetros:
	----------
	localidade : String
		- String que representa a cidade/estado("cg", "jp" ou "pb").
	"""
	if (localidade == "cg"):
		arq = csv.DictReader(open("./gazetteer/features_campina.csv", mode="r"))
	elif (localidade == "jp"):
		arq = csv.DictReader(open("./gazetteer/features_jp.csv", mode="r"))
	elif (localidade == "pb"):
		arq = csv.DictReader(open("./gazetteer/features_paraiba.csv", mode="r"))
	
	fields = ["osm_id", "fclass", "name", "type", "coordenates"]
	f = csv.writer(open('./gazetteer/processados/' + localidade + '.csv', 'w', encoding='utf-8'))
	f.writerow(fields)

	for p in arq:
		coord = convertFeature(p['geometry'])
		t = [ p['osm_id'].__str__(), p["fclass"].__str__(), p["name"].__str__(), p["type"].__str__(), coord ]
		f.writerow(t)

def main():
	"""
	Função principal, onde tudo será executado.
	"""
    locs = ['cg', 'jp', 'pb']

    for loc in locs:
        points(localidade=loc)

    for loc in locs:
        polygons(localidade=loc)

    for loc in locs:
        features(localidade=loc)

# main()