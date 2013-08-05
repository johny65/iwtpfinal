# -*- coding: utf-8 -*-

"""
Controlador para la modificación del precio de una publicación (caso de estudio).
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from model import PubModel

class ListadoPrecios(webapp.RequestHandler):
    """Muestra la página principal para la modificación de precios (contiene el
    listado de publicaciones disponibles) (Servicio 1)."""
    def get(self):
        p = PubModel.listado_publicaciones()
        template_values = {"publicaciones": p}
        self.response.out.write(template.render("view/listado.htm", template_values))

class Precio(webapp.RequestHandler):
    """Muestra la página donde se permite ingresar el nuevo precio (Servicio 2)."""
    def post(self):
        pid = self.request.get("pub_id_seleccionada")
        p = PubModel.get_publicacion(pid)
        template_values = {"pub": p}
        self.response.out.write(template.render("view/input_precio.htm", template_values))

class Modificacion(webapp.RequestHandler):
    """Modifica el precio de una publicación (Servicio 3)."""
    def post(self):
        try:
            pid = self.request.get("pub_id_actual")
            precio = float(self.request.get("precio"))
            p = PubModel.modificar_precio(pid, precio)
            template_values = {"pub": p}
            self.response.out.write(template.render("view/precio_ok.htm", template_values))
        except Exception:
            self.response.out.write("El precio ingresado es inv&aacute;lido.")
