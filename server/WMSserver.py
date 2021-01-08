#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
from generation_image_12 import create_highway_map
import drawer
from os import path

PORT_NUMBER = 4242


class WMSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/wms"):
            # Ici on récupère les valeurs de paramètres GET
            params = urlparse.parse_qs(urlparse.urlparse(self.path).query)

            check_params = ['request', 'layers', 'height', 'width', 'srs', 'bbox']
            for x in check_params:
                if not params.get(x):
                    self.send_error(404, "Le paramètre n'as pas été retrouvé : \"%s\" " %x)

            if (params['request'][0] != "GetMap"):
                self.send_error(404, "La valeur pour le paramètre request est incorrecte, elle doit valoir GetMap.")
            elif (params['srs'][0] != "EPSG:3857"):
                self.send_error(404, "La valeur pour le paramètre srs est incorrecte, nous nous plaçons dans le système référentiel EPSG:3857.")
            else :
                bbox = params["bbox"][0]
                height, width = params["height"][0], params["width"][0]
                if not path.exists("tuiles/"+bbox+".png"):
                    create_highway_map(bbox, height, width)
                
                self.send_png_image("tuiles/"+bbox+".png")
            return 0
        
        else:
            self.send_error(404, 'Fichier non trouvé : %s' % self.path)


    def send_plain_text(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

    def send_png_image(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename):
        self.send_response(200)
        self.end_headers()
        self.serveFile(filename)


if __name__ == "__main__":
    try:
        # Ici on crée un serveur web HTTP, et on affecte le traitement
        # des requêtes à notre releaseHandler ci-dessus.
        server = HTTPServer(('', PORT_NUMBER), WMSHandler)
        print('Serveur démarré sur le port ', PORT_NUMBER)
        print('Ouvrez un navigateur et tapez dans la barre d\'url :'
              + ' http://localhost:%d/' % PORT_NUMBER)

        # Ici, on demande au serveur d'attendre jusqu'à la fin des temps...
        server.serve_forever()

    # ...sauf si l'utilisateur l'interrompt avec ^C par exemple
    except KeyboardInterrupt:
        print('^C reçu, je ferme le serveur. Merci.')
        server.socket.close()
