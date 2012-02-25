# -*- coding: iso-8859-1 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from model import PubModel
from model import AutorModel

def armar_datos(request):
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

class Principal(webapp.RequestHandler):
	def get(self):
		p = PubModel.listado_publicaciones()
		a = AutorModel.listado_autores()
		template_values = {"publicaciones": p, "autores": a}
		self.response.out.write(template.render("view/abm_main.htm", template_values))

class Carga(webapp.RequestHandler):
	def post(self):
		datos = armar_datos(self.request)
		PubModel.nueva_publicacion(datos)
		self.redirect("/abm")

class Baja(webapp.RequestHandler):
	def get(self):
		pubkey = self.request.get("key")
		PubModel.eliminar_publicacion(pubkey)
		self.redirect("/abm")

class Detalle(webapp.RequestHandler):
	def get(self):
		pubkey = self.request.get("key")
		autor, pub = PubModel.detalles_publicacion(pubkey)
		template_values = {"aut": autor, "pub": pub}
		self.response.out.write(template.render("view/abm_detalles.htm", template_values))

class Modificacion(webapp.RequestHandler):
	def post(self):
		datos = armar_datos(self.request)
		pubkey = self.request.get("key")
		PubModel.modificar_publicacion(pubkey, datos)
		pub = datos["titulo"]
		template_values = {"titulo": pub}
		self.response.out.write(template.render("view/abm_ok.htm", template_values))
