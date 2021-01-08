import database as db

def query():
    cursor = db.execute_query("SELECT tags->'highway', ST_Transform(linestring,4326) FROM ways WHERE tags?->'highway' AND ST_Within(ST_Transform(bbox,4326), ST_GeomFromText('POLYGON((5.7 45.1, 5.7 45.2, 5.8 45.2, 5.8 45.1, 5.7 45.1))', 4326));")
    for row in cursor:
        name = row[0]
        polygon = row[1]
        print(name,polygon)
    cursor.close()
    db.close_connection()

query()
