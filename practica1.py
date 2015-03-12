#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp


class acortadorApp(webapp.webApp):

    def devolverUrls(self):
        html = "</br><strong>Ya acortadas:</strong><ul>"
        for numero, url in enumerate(self.acortadas):
            html += "<li>http://" + self.hostname + ":" + str(self.port) + "/" + str(numero) + " <strong>--------------</strong> " + url + "</li>"
        return html


    def parse(self, request):
        metodo = request.split(' ', 2)[0]
        recurso = request.split(' ',2)[1]
        #EL CUERPO DEL POST DEL FORMULARIO VENDRA DE LA FORMA DE campo=valor1&campo2=valor2....
        if metodo == "POST":
            cuerpo = request.split('\r\n\r\n', 1)[1]
        else:
            cuerpo = ""
        return (metodo, recurso, cuerpo)


    def process(self, (metodo, recurso, cuerpo)):

        #CONSTRUCCION DEL FORMULARIO QUE VA A IR SIEMPRE DESPUES DE LA PAGINA
        formulario = "<form method='post' enctype='text/plain'>Introduce url:<input type='text' name='url' value='' /><button type='submit'>Acortar!</button></form>"

        if metodo == "GET":
            if recurso == "/":
                urlsYaAcortadas = self.devolverUrls()
                httpCode = "200 OK"
                htmlBody = "<html><body><h1>Acortador de URLs</h1>" + formulario + urlsYaAcortadas + "</body></html>"
                return (httpCode, htmlBody)
            else:
                try:
                    numero = int(recurso[1:])
                    return ("307 Temporary Redirect" + "\n" +  "Location: " + self.acortadas[numero], "")
                except IndexError:
                    return ("404 Not Found", "<h3>Recurso no disponible</h3>")
                except ValueError:
                    return ("404 Not Found", "<h3>Recurso no numerico</h3>")
                    
        #CON POST ACORTO URL O DEVUELVO SI YA EXISTE
        elif metodo == "POST":
            contenido = cuerpo.split("=")[1]

            #pongo el http o https si hace falta
            if not contenido.startswith("http"):
                contenido = "http://" + contenido

            #Miro a ver si ya la tenia o guardo en mi lista de urls acortadas
            if contenido in self.acortadas:
                urlAcortadaExistente = "http://" + self.hostname + ":" + str(self.port) + "/" + str(self.acortadas.index(contenido))
                return ("404 Not Found", "<html><body>Lo siento, ya esta acortada en: <strong>" + urlAcortadaExistente)
            else:
                self.acortadas.append(contenido)
                return ("200 OK", "<html><body>URL acortada para '" + contenido + "': <strong>http://" + self.hostname + ":" + str(self.port) + "/" + str(len(self.acortadas)-1) + "</body></html>")

    def __init__(self, hostname, port):
        self.acortadas = []
        self.hostname = hostname
        self.port = port
        webapp.webApp.__init__(self, hostname, port)


if __name__ == "__main__":
    acortadorurls = acortadorApp("localhost", 1234)
