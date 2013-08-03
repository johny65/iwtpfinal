# -*- coding: utf-8 -*-

"""
Modelo de autores.
"""

from google.appengine.ext import db

class Autor(db.Model):
    """Modelo de la entidad Autor."""
    au_id = db.StringProperty(required=True)
    nombre = db.StringProperty()
    apellido = db.StringProperty()
    ciudad = db.StringProperty()
    cp = db.IntegerProperty()
    tel = db.StringProperty()

def listado_autores():
    """Consulta y devuelve el listado de autores guardados."""
    q = Autor.all()
    q.order("apellido")
    l = []
    for a in q:
        a.au_key = str(a.key()) #le meto su key de la bd
        l.append(a)
    return l
