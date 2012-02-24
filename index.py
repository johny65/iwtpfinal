# -*- coding: utf8 -*-

import cgi
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext import db

class TablaUsuarios(db.Model):
  nombre=db.StringProperty()
  clave=db.StringProperty()

class Listado(webapp.RequestHandler):
  def get(self):
    self.response.out.write("<html><head></head><body>")
    self.response.out.write("<table border=\"1\">")
    self.response.out.write("<tr>")


    self.response.out.write("<td>Usuario</td><td>Clave</td><td>Borrar</td><td>Modificar</td>")
    self.response.out.write("</tr>")
    usuarios=db.GqlQuery("select * from TablaUsuarios")
    for usu in usuarios:
      self.response.out.write("<tr>")
      self.response.out.write("<td>" + usu.nombre +"</td>")
      self.response.out.write("<td>" + usu.clave +"</td>")
      self.response.out.write("<td><a href=\"baja?nombre="+usu.nombre+"\">Borra?</a>"+"</td>")
      self.response.out.write("<td><a href=\"formulariomodificacion?nombre="+usu.nombre+"\">Modifica?</a>"+"</td>")
      self.response.out.write("</tr>")
    self.response.out.write("<tr>")
    self.response.out.write("<td colspan=\"4\"><a href=\"formularioalta\">Alta</a></td>")
    self.response.out.write("</tr>")
    self.response.out.write("</table>")
    self.response.out.write("</body></html>")

class FormularioAlta(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
<html>
<head></head>
<body>
<form action="alta" method="post">
Ingrese su nombre:
<input type="text" name="nombre"><br>
Ingrese su clave:
<input type="password" name="clave"><br>
<input type="submit" value="Alta"><br>
</form>
</body>
</html>
""")

class Alta(webapp.RequestHandler):
  def post(self):
    nom=cgi.escape(self.request.get('nombre'))
    cla=cgi.escape(self.request.get('clave'))
    usuario=TablaUsuarios()
    usuario.nombre=nom
    usuario.clave=cla
    usuario.put()
    self.redirect("/")

class Baja(webapp.RequestHandler):
  def get(self):
    nom=cgi.escape(self.request.get('nombre'))
    usuario=db.GqlQuery("select * from TablaUsuarios where nombre=:1",nom)
    usu=usuario.fetch(1)
    if len(usu)>0:
      usu[0].delete()
    self.redirect("/")

class FormularioModificacion(webapp.RequestHandler):
  def get(self):
    self.response.out.write("<html><head></head><body>")
    nom=cgi.escape(self.request.get('nombre'))
    usuario=db.GqlQuery("select * from TablaUsuarios where nombre=:1",nom)
    usu=usuario.fetch(1)
    if len(usu)>0:
      self.response.out.write("""
<html>
<head></head>
<body>
<form action="modificacion" method="post">
Nombre actual:
""")
      self.response.out.write("<input type=\"text\" name=\"nombre\" value=\""+usu[0].nombre+"\"><br>")
      self.response.out.write("Clave actual:")
      self.response.out.write("<input type=\"text\" name=\"clave\" value=\""+usu[0].clave+"\"><br>")
      self.response.out.write("<input type=\"hidden\" name=\"nombreoculto\" value=\""+usu[0].nombre+"\">")
      self.response.out.write("""
<input type="submit" value="Modificar"><br>
</form>
</body>
</html>
""")
    else:
      self.response.out.write("No existe un usuario con dicho nombre<br>")
    self.response.out.write("</body></body>")

class Modificacion(webapp.RequestHandler):
  def post(self):
    nomoculto=cgi.escape(self.request.get('nombreoculto'))
    nom=cgi.escape(self.request.get('nombre'))
    cla=cgi.escape(self.request.get('clave'))
    usuario=db.GqlQuery("select * from TablaUsuarios where nombre=:1",nomoculto)
    usu=usuario.fetch(1)
    if len(usu)>0:
      usu[0].nombre=nom
      usu[0].clave=cla
      usu[0].put()
    self.redirect("/")


def main():
  application = webapp.WSGIApplication([('/', Listado),
                                        ('/formularioalta',FormularioAlta ),
                                        ('/alta',Alta ),
                                        ('/baja', Baja),
                                        ('/formulariomodificacion', FormularioModificacion),
                                        ('/modificacion', Modificacion),
                                       ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
