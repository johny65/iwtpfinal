from google.appengine.ext import db

class Autor(db.Model):
	nombre = db.StringProperty(required=True)
	apellido = db.StringProperty(required=True)
	ciudad = db.StringProperty()
	cp = db.IntegerProperty()
	email = db.EmailProperty()

class Publicacion(db.Model):
	titulo = db.StringProperty(required=True)
	year = db.IntegerProperty(required=True)
	precio = db.FloatProperty(required=True)
	editorial = db.StringProperty(required=True)
	autor = db.ReferenceProperty(Autor, required=True)

def listado_publicaciones():
	"""Devuelve una lista con las publicaciones guardadas."""
	q = Publicacion.all()
	q.order("-year")
	#q = Publicacion.gql("ORDER BY year DESC")
	l = []
	for p in q:
		p.pubid = str(p.key())
		l.append(p)
	return l

def nueva_publicacion(d):

	a = Autor(nombre=d["nombre"], apellido=d["apellido"])
	a.ciudad = d["ciudad"]
	a.cp = d["cp"]
	a.email = d["email"]
	a.put()

	p = Publicacion(titulo=d["titulo"], year=d["year"], precio=d["precio"],
					editorial=d["editorial"], autor=a)
	p.put()

def eliminar_publicacion(pubid):
	p = Publicacion.get(db.Key(pubid))
	a = p.autor
	p.delete()
	a.delete()

def detalles_publicacion(pubid):
	p = Publicacion.get(db.Key(pubid))
	a = p.autor
	return (a, p)

def modificar_publicacion(pubid, d):
	a, p = detalles_publicacion(pubid)
	a.nombre = d["nombre"]
	a.apellido = d["apellido"]
	a.ciudad = d["ciudad"]
	a.cp = d["cp"]
	a.email = d["email"]
	a.put()
	p.titulo = d["titulo"]
	p.year = d["year"]
	p.precio = d["precio"]
	p.editorial = d["editorial"]
	p.put()
