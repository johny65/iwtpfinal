from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from controller import PubController
from controller import ABMController

class Index(webapp.RequestHandler):
	def get(self):
		html = open("index.htm").read()
		self.response.out.write(html)

application = webapp.WSGIApplication([
								("/", Index),
								("/p1", PubController.ListadoPrecios),
								("/p2", PubController.Precio),
								("/p3", PubController.Modificacion),
								("/abm", ABMController.Principal),
								("/cargar",ABMController.Carga),
								("/delete", ABMController.Baja),
								("/info", ABMController.Detalle),
								#("/db", importdb.importdb),
								("/modificar", ABMController.Modificacion)
								], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
