# -*- coding: iso-8859-1 -*-

"""
Controlador para el ABM de publicaciones.

NOTA:
La demora entre una operación (alta, baja o modificación) y su reflejo en la
vista (los cambios no aparecen al instante, hay que refrescar manualmente la
página) es debido al almacenamiento de datos High Replication Datastore (HRD)
usado por App Engine, resultando en una **consistencia eventual** de datos.

Más información:
http://en.wikipedia.org/wiki/Eventual_consistency
https://developers.google.com/appengine/docs/python/gettingstartedpython27/usingdatastore

Para emular la consistencia fuerte, ejecutar el servidor de pruebas con la
opción --datastore_consistency_policy=consistent

"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from model import PubModel
from model import AutorModel

class Principal(webapp.RequestHandler):
    """Muestra la página principal del ABM (contiene el listado de publicaciones
    y el formulario de carga)."""
    def get(self):
        p = PubModel.listado_publicaciones()
        a = AutorModel.listado_autores()
        template_values = {"publicaciones": p, "autores": a}
        self.response.out.write(template.render("view/abm_main.htm", template_values))

class Carga(webapp.RequestHandler):
    """Carga una nueva publicación."""
    def post(self):
        try:
            datos = armar_datos(self.request)
            PubModel.nueva_publicacion(datos)
            self.redirect("/abm")
        except Exception:
            self.response.out.write("Datos inv&aacute;lidos.")

class Baja(webapp.RequestHandler):
    """Elimina una publicación."""
    def get(self):
        pubkey = self.request.get("key")
        PubModel.eliminar_publicacion(pubkey)
        self.redirect("/abm")

class Detalle(webapp.RequestHandler):
    """Muestra los detalles de una publicación."""
    def get(self):
        pubkey = self.request.get("key")
        pub = PubModel.get_publicacion_por_key(pubkey)
        autor = pub.autor
        template_values = {"aut": autor, "pub": pub}
        self.response.out.write(template.render("view/abm_detalles.htm", template_values))

class Modificacion(webapp.RequestHandler):
    """Modifica los datos de una publicación."""
    def post(self):
        try:
            datos = armar_datos(self.request)
            pubkey = self.request.get("key")
            PubModel.modificar_publicacion(pubkey, datos)
            pub = datos["titulo"]
            template_values = {"titulo": pub}
            self.response.out.write(template.render("view/abm_ok.htm", template_values))
        except Exception, e:
            print(e)
            self.response.out.write("Datos inv&aacute;lidos.")

def armar_datos(request):
    """Función privada que a partir de un request arma una estructura de datos
    con la cual trabaja el modelo."""
    datos = {}
    datos["autor"] = request.get("autor")
    datos["nombre"] = request.get("nombre")
    datos["apellido"] = request.get("apellido")
    datos["ciudad"] = request.get("ciudad")
    datos["cp"] = int(request.get("cp")) if request.get("cp") else None
    datos["telefono"] = request.get("telefono")
    datos["id"] = request.get("id")
    datos["titulo"] = request.get("titulo")
    datos["year"] = int(request.get("year")) if request.get("year") else None
    datos["precio"] = float(request.get("precio")) if request.get("precio") else None
    datos["editorial"] = request.get("editorial")
    return datos
