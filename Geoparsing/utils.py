from plpygis import Geometry

def converterGeometryPoint(geometry):
    g = Geometry(geometry)
    coord = g.geojson['coordinates']
    return [coord[1], coord[0]]

print(converterGeometryPoint("0101000000A46C36FBA8F241C0C3E1BB838EF41CC0"))