from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import controller

application = webapp.WSGIApplication([
								("/", controller.Principal),
								("/cargar",controller.Carga),
								("/delete", controller.Baja),
								("/info", controller.Detalle),
								("/modificar", controller.Modificacion)
								], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
