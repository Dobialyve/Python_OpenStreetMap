from drawer import Image
import database as db
import cairo

def create_highway_map(bbox, width, height):
    
    x1, y1, x2, y2 = bbox.split(",")
   
    cursor = db.execute_query("SELECT ST_Transform(linestring,3857), tags->'highway' FROM ways WHERE tags?'highway' AND ST_Xmin(ST_Transform(bbox,3857))>"+x1+" AND ST_Xmax(ST_Transform(bbox,3857))<"+x2+" AND ST_Ymin(ST_Transform(bbox,3857))>"+y1+" AND ST_Ymax(ST_Transform(bbox,3857))<"+y2+";")
   
    highway = []
    coordinates = []
    highway_color = {}
    
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)    
    width, height = int(width), int(height)
    for row in cursor:
        highway.append(row[1])
        coord_ajout = row[0]
        normalize = [(width-(x2-point.x)*width/(x2-x1), ((y2-point.y)*height/(y2-y1))) for point in coord_ajout]
        coordinates.append(normalize)


    image_highway = Image(width,height)

    for x, i in enumerate(coordinates):
        image_highway.draw_linestring(i, (0,0,0,1))

    image_highway.save("tuiles/"+bbox+".png")
    cursor.close()
    db.close_connection()
