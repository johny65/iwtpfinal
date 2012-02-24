# -*- coding: iso-8859-1 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import model

def armar_datos(request):
	datos = {}
	datos["nombre"] = request.get("nombre")
	datos["apellido"] = request.get("apellido")
	datos["ciudad"] = request.get("ciudad")
	datos["cp"] = int(request.get("cp"))
	datos["email"] = request.get("email")
	datos["titulo"] = request.get("titulo")
	datos["year"] = int(request.get("year"))
	datos["precio"] = float(request.get("precio"))
	datos["editorial"] = request.get("editorial")
	return datos

class Principal(webapp.RequestHandler):
	def get(self):
		p = model.listado_publicaciones()
		template_values = {"publicaciones": p}
		self.response.out.write(template.render("main.htm", template_values))

class Carga(webapp.RequestHandler):
	def post(self):
		datos = armar_datos(self.request)
		model.nueva_publicacion(datos)
		self.redirect("/")

class Baja(webapp.RequestHandler):
	def get(self):
		pubid = self.request.get("id")
		model.eliminar_publicacion(pubid)
		self.redirect("/")

class Detalle(webapp.RequestHandler):
	def get(self):
		pubid = self.request.get("id")
		autor, pub = model.detalles_publicacion(pubid)
		template_values = {"aut": autor, "pub": pub, "pubid": pubid}
		self.response.out.write(template.render("detalles.htm", template_values))

class Modificacion(webapp.RequestHandler):
	def post(self):
		datos = armar_datos(self.request)
		pubid = self.request.get("id")
		model.modificar_publicacion(pubid, datos)
		pub = datos["titulo"]
		template_values = {"titulo": pub}
		self.response.out.write(template.render("ok.htm", template_values))
