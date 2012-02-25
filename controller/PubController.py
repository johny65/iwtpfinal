from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from model import PubModel

class ListadoPrecios(webapp.RequestHandler):
	def get(self):
		p = PubModel.listado_publicaciones()
		template_values = {"publicaciones": p}
		self.response.out.write(template.render("view/lista.htm", template_values))

class Precio(webapp.RequestHandler):
	def post(self):
		key = self.request.get("pubkey")
		p = PubModel.get_publicacion(key)
		template_values = {"pub": p}
		self.response.out.write(template.render("view/precio.htm", template_values))

class Modificacion(webapp.RequestHandler):
	def post(self):
		key = self.request.get("pubkey")
		precio = float(self.request.get("precio"))
		p = PubModel.modificar_precio(key, precio)
		template_values = {"pub": p}
		self.response.out.write(template.render("view/preciook.htm", template_values))
