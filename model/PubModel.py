from google.appengine.ext import db
from AutorModel import Autor

class Publicacion(db.Model):
	pub_id = db.StringProperty(required=True)
	titulo = db.StringProperty()
	year = db.IntegerProperty()
	precio = db.FloatProperty()
	editorial = db.StringProperty()
	autor = db.ReferenceProperty(Autor)

def listado_publicaciones():
	"""Devuelve una lista con las publicaciones guardadas."""
	q = Publicacion.all()
	q.order("titulo")
	#q = Publicacion.gql("ORDER BY titulo")
	l = []
	for p in q:
		p.pub_key = str(p.key()) #le meto su key de la bd
		l.append(p)
	return l

def get_publicacion(pubkey):
	p = Publicacion.get(db.Key(pubkey))
	p.pub_key = pubkey
	return p

def modificar_precio(pubkey, nuevo_precio):
	p = Publicacion.get(db.Key(pubkey))
	p.precio = nuevo_precio
	p.put()
	p.pub_key = pubkey
	return p



#-----------------------------------------------------------------------------

#Metodos para el ABM:

def nueva_publicacion(d):
	keyautor = d["autor"]
	a = Autor.get(keyautor)
	p = Publicacion(pub_id=d["id"], titulo=d["titulo"], year=d["year"],
					precio=d["precio"], editorial=d["editorial"], autor=a)
	p.put()

def eliminar_publicacion(pubkey):
	#no elimina el autor
	p = Publicacion.get(db.Key(pubkey))
	p.delete()

def modificar_publicacion(pubkey, d):
	p = get_publicacion(pubkey)
	a = p.autor
	a.nombre = d["nombre"]
	a.apellido = d["apellido"]
	a.ciudad = d["ciudad"]
	a.cp = d["cp"]
	a.tel = d["telefono"]
	a.put()
	p.titulo = d["titulo"]
	p.year = d["year"]
	p.precio = d["precio"]
	p.editorial = d["editorial"]
	p.put()
