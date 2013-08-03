"""
Carga los datos de los archivos *.csv al almacenamiento de datos (autores,
publicaciones y sus relaciones).
"""

import model
import csv

from google.appengine.ext import webapp

class importdb(webapp.RequestHandler):
    def get(self):
        #cargar autores:
        with open('_utilidades_/authors.csv', 'r') as f:
            reader = csv.reader(f)
            for r in reader:
                a = model.AutorModel.Autor(au_id=r[0], apellido=r[1],
                nombre=r[2], ciudad=r[5], cp=int(r[7]), tel=r[3])
                a.put()

        #for a in model.AutorModel.Autor.all():
            #print a.nombre

        #cargar publicaciones:
        with open('_utilidades_/titles.csv', 'r') as f:
            reader = csv.reader(f)
            for r in reader:
                p = model.PubModel.Publicacion(pub_id=r[0], titulo=r[1],
                year=int(r[3]), precio=float(r[2]), editorial="Editorial")
                p.put()

        #for p in model.PubModel.Publicacion.all():
            #print p.pub_id, p.titulo

        #asociar publicaciones con autores:
        with open('_utilidades_/rel.csv', 'r') as f:
            reader = csv.reader(f)
            for r in reader:
                ps = model.PubModel.Publicacion.gql("WHERE pub_id = :1", r[1])
                ps.run()
                #for i in ps:
                    #print i.titulo
                p = ps[0]
                aa = model.AutorModel.Autor.gql("WHERE au_id = :1", r[0])
                aa.run()
                a = aa[0]
                p.autor = a
                p.put()

        self.response.out.write("Ok")
