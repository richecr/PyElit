import sys
import csv
import pandas as pd
from plpygis import Geometry
import geocoder

# Increasing the limit size of the CSV.
maxInt = sys.maxsize
csv.field_size_limit(maxInt)


def to_convert_geometry_point(geometry):
    """
    Pre-processing function that turns a code into geometry(Point)
    for a list of floats.

    Params:
    ----------
    geometry : String
      - String that represents a geometric coordinate of a point.

    Return:
    ----------
    coord : List
      - List of cordenates.
    """
    g = Geometry(geometry)
    coord = g.geojson['coordinates']
    coord.reverse()
    return coord


def to_convert_geometry_polygon(geometry):
    """
    Pre-processing function that turns a code into geometry(polygon)
    for a list of floats.

    Params:
    ----------
    geometry : String
      - String that represents a geometric coordinate of a polygon.

    Return:
    ----------
    coord : List
      - List of cordenates.
    """
    g = Geometry(geometry)
    coord = g.geojson['coordinates']
    saida = []
    for c in coord[0]:
        c.reverse()
        saida.append(c)
    return saida


def to_convert_feature(geometry):
    """
    Pre-processing function that turns a code into geometry(Feature)
    for a list of floats.

    Params:
    ----------
    geometry : String
      - String that represents a geometric coordinate of a feature.

    Return:
    ----------
    coord : List
      - List of cordenates.
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
    Pre-processing function that writes polygon address data to another
    file with normalized coordinates.

    Params:
    ----------
    localidade : String
      - String representing the city/state("cg", "jp" ou "pb").
    """
    if (localidade == "cg"):
        arq = csv.DictReader(
            open("./dados/features_campina_ln.csv", "r", encoding='utf-8'))
    elif (localidade == "jp"):
        arq = csv.DictReader(
            open("./dados/features_jp_ln.csv", "r", encoding='utf-8'))
    elif (localidade == "pb"):
        arq = csv.DictReader(
            open("./dados/features_paraiba_ln.csv", "r", encoding='utf-8'))

    fields = ["osm_id", "fclass", "name", "type", "coordenates"]
    f = csv.writer(open('./processamento/gazetteer/' +
                        localidade + '_ln.csv', 'w', encoding='utf-8'))
    f.writerow(fields)

    for p in arq:
        coord = converterGeometryPolygon(p['geometry'])
        t = [p['osm_id'].__str__(), p["fclass"].__str__(
        ), p["name"].__str__(), p["type"].__str__(), coord]
        f.writerow(t)


def points(localidade="cg"):
    """
    Pre-processing function that writes point address data to another
    file with normalized coordinates.

    Params:
    ----------
    localidade : String
      - String representing the city/state("cg", "jp" ou "pb").
    """
    if (localidade == "cg"):
        arq = csv.DictReader(
            open("./dados/features_campina_pt.csv", "r", encoding='utf-8'))
    elif (localidade == "jp"):
        arq = csv.DictReader(
            open("./dados/features_jp_pt.csv", "r", encoding='utf-8'))
    elif (localidade == "pb"):
        arq = csv.DictReader(
            open("./dados/features_paraiba_pt.csv", "r", encoding='utf-8'))

    fields = ["osm_id", "fclass", "name", "type", "coordenates"]
    f = csv.writer(open('./processamento/gazetteer/' +
                        localidade + '_pt.csv', 'w', encoding='utf-8'))
    f.writerow(fields)

    for p in arq:
        coord = converterGeometryPoint(p['geometry'])
        t = [p['osm_id'].__str__(), p["fclass"].__str__(
        ), p["name"].__str__(), p["type"].__str__(), coord]
        f.writerow(t)


def features(localidade="cg"):
    """
    Pre-processing function that writes feature address data to another
    file with normalized coordinates.

    Params:
    ----------
    localidade : String
      - String representing the city/state("cg", "jp" ou "pb").
    """
    if (localidade == "cg"):
        arq = csv.DictReader(open("./dados/features_campina.csv", mode="r"))
    elif (localidade == "jp"):
        arq = csv.DictReader(open("./dados/features_jp.csv", mode="r"))
    elif (localidade == "pb"):
        arq = csv.DictReader(open("./dados/features_paraiba.csv", mode="r"))

    fields = ["osm_id", "fclass", "name", "type", "coordenates"]
    f = csv.writer(open('./processamento/gazetteer/' +
                        localidade + '.csv', 'w', encoding='utf-8'))
    f.writerow(fields)

    for p in arq:
        coord = to_convert_feature(p['geometry'])
        t = [p['osm_id'].__str__(), p["fclass"].__str__(
        ), p["name"].__str__(), p["type"].__str__(), coord]
        f.writerow(t)


def string_to_list(coor_str):
    """
    Method that transforms a list of coordinate lists into a tuple
    with latitude and longitude values.

    Params:
    ----------
    coord_str: String
        - List of coordinate lists

    Return:
    ----------
    coord: Tuple
        - Latitude and longitude values.
    """
    b = coor_str.replace("[", "")
    b = b.replace("]", "")

    coor_str = b.split(", ")
    # print(coor_str)

    lat = []
    lon = []
    for i in range(len(coor_str)):
        if i % 2 == 0:
            lat.append(float(coor_str[i]))
        else:
            lon.append(float(coor_str[i]))

    # print("Lat: ", sum(lat) / len(lat))
    # print("Lon: ", sum(lon) / len(lon))
    return (lat, lon)


def clear_gazetteer():
    """
    Cleaning the data of the gazetteer, leaving only addresses
    from the state of Paraíba.
    """
    arq = csv.DictReader(
        open("./gazetteer/processados/gazetteer.csv", "r", encoding='utf-8'))
    arq1 = csv.writer(
        open("./gazetteer/processados/gazetteer1.csv", "w", encoding='utf-8'))
    arq1.writerow(["osm_id", "fclass", "name", "type", "coordenates"])
    for row in arq:
        lat, lon = string_to_list(row['coordenates'])
        loc_ = str(lat) + ", " + str(lon)
        g = geocoder.reverse(location=loc_, provider="arcgis")
        g = g.json

        try:
            if (g['state'] == "Paraíba"):
                t = [
                    row['osm_id'].__str__(),
                    row["fclass"].__str__(),
                    row["name"].__str__(),
                    row["type"].__str__(),
                    row['coordenates']
                ]
                arq1.writerow(t)
        except Exception as e:
            continue


def main():
    locs = ['cg', 'jp', 'pb']

    for loc in locs:
        points(localidade=loc)

    for loc in locs:
        polygons(localidade=loc)

    for loc in locs:
        features(localidade=loc)

# clear_gazetteer()
# main()
