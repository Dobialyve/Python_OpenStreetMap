from drawer import Image
import database as db
import cairo

def create_highway_map(xmin, ymin, xmax, ymax, width, height):
    cursor = db.execute_query("SELECT tags->'highway', ST_Transform(linestring,4326) FROM ways WHERE tags?'highway' AND ST_Within(ST_Transform(bbox,4326), ST_GeomFromText('POLYGON((5.7 45.1, 5.7 45.2, 5.8 45.2, 5.8 45.1, 5.7 45.1))', 4326));")
    highway = []
    coordinates = []
    highway_color = {}
    for row in cursor:
        highway.append(row[0])
        coord_ajout = row[1]
        normalize = [(width-(xmax-point.x)*width/(xmax-xmin), ((ymax-point.y)*height/(ymax-ymin))) for point in coord_ajout]
        coordinates.append(normalize)

    image_highway = Image(width,height)

    for x, i in enumerate(coordinates):
        image_highway.draw_linestring(i, (0,0,0,1))

    image_highway.save("image_highway")
    cursor.close()
    db.close_connection()
