import database as db

query = "SELECT DISTINCT tags->'highway' FROM ways WHERE tags?'highway'"

cursor = db.execute_query(query)

with open("list_highway.text", "w") as file:
    for row in cursor:
        file.write(row[0]+"\n")
        
        
    cursor.close()
    db.close_connection()