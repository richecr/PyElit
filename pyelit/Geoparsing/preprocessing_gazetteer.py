from plpygis import Geometry
import csv
import sys

# Increasing the limit size of the CSV.
maxInt = sys.maxsize
csv.field_size_limit(maxInt)


def convert_geometry_point(geometry):
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
    coord = g.geojson["coordinates"]
    coord.reverse()
    return coord


def convert_geometry_polygon(geometry):
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
    coord = g.geojson["coordinates"]
    saida = []
    for c in coord[0]:
        c.reverse()
        saida.append(c)
    return saida


def convert_feature(geometry):
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
    coord = g.geojson["coordinates"][0][0]
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
    if localidade == "cg":
        arq = csv.DictReader(
            open("./gazetteer/features_campina_ln.csv", "r", encoding="utf-8")
        )
    elif localidade == "jp":
        arq = csv.DictReader(
            open("./gazetteer/features_jp_ln.csv", "r", encoding="utf-8")
        )
    elif localidade == "pb":
        arq = csv.DictReader(
            open("./gazetteer/features_paraiba_ln.csv", "r", encoding="utf-8")
        )

    fields = ["osm_id", "fclass", "name", "type", "coordenates"]
    f = csv.writer(
        open("./gazetteer/processados/" + localidade + "_ln.csv", "w", encoding="utf-8")
    )
    f.writerow(fields)

    for p in arq:
        coord = convert_geometry_polygon(p["geometry"])
        t = [
            p["osm_id"].__str__(),
            p["fclass"].__str__(),
            p["name"].__str__(),
            p["type"].__str__(),
            coord,
        ]
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
    if localidade == "cg":
        arq = csv.DictReader(
            open("./gazetteer/features_campina_pt.csv", "r", encoding="utf-8")
        )
    elif localidade == "jp":
        arq = csv.DictReader(
            open("./gazetteer/features_jp_pt.csv", "r", encoding="utf-8")
        )
    elif localidade == "pb":
        arq = csv.DictReader(
            open("./gazetteer/features_paraiba_pt.csv", "r", encoding="utf-8")
        )

    fields = ["osm_id", "fclass", "name", "type", "coordenates"]
    f = csv.writer(
        open("./gazetteer/processados/" + localidade + "_pt.csv", "w", encoding="utf-8")
    )
    f.writerow(fields)

    for p in arq:
        coord = convert_geometry_point(p["geometry"])
        t = [
            p["osm_id"].__str__(),
            p["fclass"].__str__(),
            p["name"].__str__(),
            p["type"].__str__(),
            coord,
        ]
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
    if localidade == "cg":
        arq = csv.DictReader(open("./gazetteer/features_campina.csv", mode="r"))
    elif localidade == "jp":
        arq = csv.DictReader(open("./gazetteer/features_jp.csv", mode="r"))
    elif localidade == "pb":
        arq = csv.DictReader(open("./gazetteer/features_paraiba.csv", mode="r"))

    fields = ["osm_id", "fclass", "name", "type", "coordenates"]
    f = csv.writer(
        open("./gazetteer/processados/" + localidade + ".csv", "w", encoding="utf-8")
    )
    f.writerow(fields)

    for p in arq:
        coord = convert_feature(p["geometry"])
        t = [
            p["osm_id"].__str__(),
            p["fclass"].__str__(),
            p["name"].__str__(),
            p["type"].__str__(),
            coord,
        ]
        f.writerow(t)


def main():
    locs = ["cg", "jp", "pb"]

    for loc in locs:
        points(localidade=loc)

    for loc in locs:
        polygons(localidade=loc)

    for loc in locs:
        features(localidade=loc)


# main()
