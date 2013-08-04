# -*- coding: utf-8 -*-

"""
Modelo de publicaciones.
"""

from google.appengine.ext import db
from AutorModel import Autor

class Publicacion(db.Model):
    """Modelo de la entidad Publicación."""
    pub_id = db.StringProperty(required=True)
    titulo = db.StringProperty(required=True)
    year = db.IntegerProperty()
    precio = db.FloatProperty(required=True)
    editorial = db.StringProperty()
    autor = db.ReferenceProperty(Autor)

def listado_publicaciones():
    """Devuelve una lista con las publicaciones guardadas."""
    q = Publicacion.all()
    q.order("titulo")
    #q = Publicacion.gql("ORDER BY titulo") #otra forma de obtener el listado
    resultados = []
    for p in q:
        p.pub_key = str(p.key()) #le meto su key de la bd para el ABM, ahí las identifico por su key y no por su pub_id (más eficiente)
        resultados.append(p)
    return resultados

def get_publicacion(pub_id):
    """Devuelve una publicación en particular según su ID de publicación."""
    q = Publicacion.gql("WHERE pub_id = :1", pub_id)
    return q.get()

def modificar_precio(pub_id, nuevo_precio):
    """Asigna el nuevo precio a una publicación en particular."""
    p = get_publicacion(pub_id)
    p.precio = nuevo_precio
    p.put() #persiste los cambios
    return p



#-----------------------------------------------------------------------------
#Métodos para el ABM:

def get_publicacion_por_key(pubkey):
    """Recupera y devuelve una publicación según su key en la base de datos.
    Se usa en el ABM, donde identifico a las publicaciones según esta key ya
    que es más eficiente la búsqueda."""
    p = Publicacion.get(db.Key(pubkey))
    p.pub_key = pubkey
    return p

def nueva_publicacion(d):
    """Guarda una nueva publicación en la base de datos."""
    keyautor = d["autor"]
    a = Autor.get(keyautor)
    p = Publicacion(pub_id=d["id"], titulo=d["titulo"], year=d["year"],
                    precio=d["precio"], editorial=d["editorial"], autor=a)
    p.put()

def eliminar_publicacion(pubkey):
    """Elimina una publicación de la base de datos."""
    p = get_publicacion_por_key(pubkey)
    p.delete()

def modificar_publicacion(pubkey, d):
    """Modifica los datos guardados de una publicación."""
    p = get_publicacion_por_key(pubkey)
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
