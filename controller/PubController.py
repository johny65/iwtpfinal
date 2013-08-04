# -*- coding: utf-8 -*-

"""
Controlador para la modificación del precio de una publicación (caso de estudio).
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from model import PubModel

class ListadoPrecios(webapp.RequestHandler):
    """Muestra la página principal para la modificación de precios (contiene el
    listado de publicaciones disponibles)."""
    def get(self):
        p = PubModel.listado_publicaciones()
        template_values = {"publicaciones": p}
        self.response.out.write(template.render("view/lista.htm", template_values))

class Precio(webapp.RequestHandler):
    """Muestra la página donde se permite ingresar el nuevo precio."""
    def post(self):
        key = self.request.get("pubkey")
        p = PubModel.get_publicacion(key)
        template_values = {"pub": p}
        self.response.out.write(template.render("view/precio.htm", template_values))

class Modificacion(webapp.RequestHandler):
    """Modifica el precio de una publicación."""
    def post(self):
        try:
            key = self.request.get("pubkey")
            precio = float(self.request.get("precio"))
            p = PubModel.modificar_precio(key, precio)
            template_values = {"pub": p}
            self.response.out.write(template.render("view/preciook.htm", template_values))
        except Exception:
            self.response.out.write("El precio ingresado es inv&aacute;lido.")
