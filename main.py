# -*- coding: utf-8 -*-

from google.appengine.ext import webapp

from controller import PubController
from controller import ABMController
from _utilidades_ import importdb

class Index(webapp.RequestHandler):
    def get(self):
        html = open("index.htm").read()
        self.response.out.write(html)

application = webapp.WSGIApplication([
                                #página principal:
                                ("/", Index),

                                #caso de estudio:
                                ("/s1", PubController.ListadoPrecios),
                                ("/s2", PubController.Precio),
                                ("/s3", PubController.Modificacion),

                                #abm completo:
                                ("/abm", ABMController.Principal),
                                ("/cargar",ABMController.Carga),
                                ("/delete", ABMController.Baja),
                                ("/info", ABMController.Detalle),
                                ("/modificar", ABMController.Modificacion),

                                #carga inicial de la base de datos:
                                ("/db", importdb.importdb)
                                ], debug=True)
