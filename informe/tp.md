Caso de Estudio usando el patrón MVC con Google App Engine y Python
===================================================================

[TOC]

# 1. Introducción:

{: style="page-break-before: always" }

Al decidir un tema para este trabajo mi intención era mostrar alguna otra tecnología para hacer aplicaciones web que las enseñadas en clases (*Servlets Java*, *JSP*, *JavaBeans*, *JavaServer Faces*, etc.). Me llamó la atención ***Google App Engine***, un servicio de alojamiento para aplicaciones web que nos ofrece Google de forma gratuita, ya que nos permite desarrollar nuestras aplicaciones en **Python** y dejarlas disponibles en la Web con muchísima facilidad y usando toda la infraestructura de Google, por lo que decidí introducirme en el tema y tratar de llevar lo aprendido en clases a esta plataforma.

Google App Engine nos permite desarrollar nuestras aplicaciones web en Java o en Python, y más recientemente en Go (el lenguaje de programación de Google) y en PHP. En este trabajo decidí optar por Python para mostrar una alternativa al desarrollo de aplicaciones web (donde generalmente las tecnologías más comunes son Java, PHP, ASP/ASP.NET, etc.), y lo sencillo que es trabajar usando este lenguaje y este servicio.

Por lo tanto este trabajo tiene como objetivo presentar Google App Engine y la manera en que podemos desarrollar aplicaciones web para esta plataforma. Más específicamente, mostrar un caso de estudio implementado usando estas herramientas, en donde teniendo una base de datos con publicaciones guardadas, podemos modificar el precio de una publicación a elección, aplicando el patrón MVC (Modelo-Vista-Controlador).

Cuando sea posible voy a mostrar las equivalencias con la API de Servlets Java aprendida en clases.


# 2. Instalación del entorno:

## 2.1 Conseguir las herramientas:

Para desarrollar aplicaciones para Google App Engine debemos descargarnos el kit de desarrollo (SDK) el cual es gratuito y libre. En este momento la última versión es la **1.8.2**.

Podemos descargarlo de la siguiente página:

<https://developers.google.com/appengine/downloads?hl=es-AR>

en la cual disponemos de varias opciones según nuestras preferencias:

* el SDK para Python (que incluye una versión para Windows, para Mac OS X, y para Linux y otras plataformas)
* el SDK para Java
* el SDK para Go y una versión experimental del SDK para PHP

En este trabajo haremos uso de la primera opción (SDK para Python), por lo tanto descargamos el archivo **google_appengine_1.8.2.zip** (pesa alrededor de unos 50 MB) si estamos en Linux o el instalador **GoogleAppEngine-1.8.2.msi** (unos 40 MB) si estamos en Windows.

También necesitamos el intérprete de Python. Se puede conseguir en su sitio oficial ([www.python.org](http://www.python.org)) o desde los repositorios de la distribución de Linux que usemos. Necesitamos la versión 2 y no la 3, ya que App Engine está diseñado para trabajar con la versión 2 de Python (recomiendan la 2.7).

Para escribir nuestras aplicaciones podemos hacer uso de cualquier editor de programación de nuestra preferencia, no hace falta disponer de ningún IDE especial. Sin embargo, se encuentra disponible un [plugin] que integra el SDK (para Java) con Eclipse.

[plugin]: https://developers.google.com/eclipse/?hl=es-AR
[Eclipse]: http://www.eclipse.org/

## 2.2 Instalación:

### 2.2.1 Python:

Python viene instalado por defecto en muchas distribuciones Linux. Sino podemos instalarlo desde los repositorios (esto depende de la distribución). Por ejemplo:

    sudo apt-get install python

En Windows ejecutamos el instalador descargado (archivo .msi) y esperamos que nos instale todo automáticamente.

### 2.2.2 El kit de desarrollo:

Una vez descargado el SDK, la instalación es muy sencilla.
En Linux, solamente descomprimimos el archivo ZIP a alguna carpeta y ya estamos listos para trabajar (por ejemplo en la carpeta google_appengine).
En Windows, el archivo de instalación nos instala todo automáticamente. La versión para Windows incluye además un lanzador gráfico, que tenemos que configurar para poder trabajar:

Vamos a Edit/Preferences y configuramos los distintos elementos:

En "Python Path" buscamos la ruta del ejecutable "pythonw.exe" en donde instalamos Python.
En "App Engine SDK" ponemos la ruta de la carpeta donde instalamos el SDK de App Engine.
En "Editor" ponemos algún editor de texto de nuestra preferencia.
Dejamos en blanco "Deployment Server".

### 2.2.3 El servidor de pruebas:

El SDK trae un servidor de pruebas que emula todos los servicios de App Engine con el que podemos probar nuestras aplicaciones localmente y que no requiere ninguna configuración adicional para trabajar con él. Más adelante voy a mostrar cómo usarlo.


# 3. Pequeña guía sobre Google App Engine:

## 3.1 Qué es Google App Engine:

Google App Engine es una plataforma que permite alojar y ejecutar nuestras aplicaciones web en la infraestructura de Google, brindándonos una serie de servicios y herramientas para que sean fáciles de crear, de mantener y de ampliar al ir aumentando el tráfico y las necesidades de almacenamiento de datos.

App Engine puede empezar a usarse de forma totalmente gratuita, y luego pagar los recursos que utiliza nuestra aplicación (como almacenamiento y ancho de banda) que superen los niveles gratuitos. Todas las aplicaciones pueden utilizar sin costo alguno hasta 500 MB de almacenamiento y suficiente CPU y ancho de banda como para permitir un servicio eficaz de alrededor de cinco millones de visitas a la página al mes.

Algunos de los servicios que nos brinda son:

* Google Accounts:

App Engine permite que nuestra aplicación tenga autenticación de usuarios a través de Google Accounts, permitiéndolos acceder con su cuenta de Google.

* Extracción de URL:

Permite que las aplicaciones puedan acceder a recursos en Internet, mediante la infraestructura de alta velocidad de Google, y trabajar con ellos.

* Correo:

Nuestras aplicaciones pueden enviar mensajes de correo electrónico.

* Memcache:

Servicio de memoria caché de valores-claves de alto rendimiento, accesible desde varias instancias de nuestra aplicación.

* Manipulación de imágenes:

Este servicio permite a nuestra aplicación manipular imágenes, como recortar, girar, dar la vuelta o ajustar el tamaño. 

* Tareas programadas y colas de tareas:

Podemos configurar la programación de tareas para que nuestra aplicación ejecute, así como también ella misma puede añadir tareas a una cola.

Además de estos servicios, tenemos a disposición muchas herramientas y recursos útiles para trabajar en App Engine, que podemos consultar en la siguiente página: <https://developers.google.com/appengine/tools_tips?hl=es-AR>.

Información más detallada sobre App Engine se puede ver en este enlace: <http://code.google.com/intl/es-AR/appengine/docs/whatisgoogleappengine.html>. La página web de la plataforma es muy rica en documentación e información relacionada, incluyendo ejemplos, tutoriales, preguntas frecuentes, etc. Es recomendable darle un vistazo.

## 3.2 Estructura de una aplicación web:

Una aplicación web creada para App Engine consiste básicamente en uno o varios archivos .py (código fuente en Python) ordenados a gusto en subdirectorios o no, y un archivo de configuración llamado **app.yaml** ubicado en la raíz y que es obligatorio. Sería el equivalente al archivo **web.xml** ubicado en el directorio **WEB-INF** que usamos en nuestras aplicaciones con servlets Java en el sentido de que es quien describe a nuestra aplicación y donde se configuran sus opciones de despliegue.
La sintaxis de este archivo es YAML[^yaml], y una configuración básica sería la siguiente:

    application: nombre
    version: 1
    runtime: python
    api_version: 1
    
    handlers:
    - url: /.*
      script: modulo.py

En él se configura el nombre y versión de nuestra aplicación, runtime y versión de la API (siempre 1), y los handlers: todas las solicitudes enviadas a una URL cuya ruta coincida con la expresión url se deben procesar con el módulo indicado por script. En este caso, /.* significa todas las URL's.
Con estos datos ya alcanza para tener nuestra aplicación funcionando. Es recomendable configurar que todas las URL's sean procesadas por un único módulo, y este módulo se encargará luego de redirigir cada petición a otro módulo específico.
Por lo tanto para tener una aplicación sencilla nos alcanza con tener la siguiente estructura:

[^yaml]: YAML Ain't Markup Language (www.yaml.org)

Si tenemos un directorio con archivos estáticos (es decir que puedan ser accedidos al invocarse su URL) debemos definir una nueva entrada en handlers:

    handlers:
    - url: /img
      static_dir: img
    
    - url: /.*
      script: modulo.py

De esta forma en el ejemplo podemos acceder a cualquier archivo ubicado en la carpeta img a través de la URL /img/nombre_del_archivo.

## 3.3 Uso de `webapp`:

Las aplicaciones Python de App Engine se comunican con el servidor web mediante el estándar CGI. Aunque el estándar CGI es sencillo, escribir manualmente todo el código que utiliza sería muy laborioso. Es por esto que App Engine permite el uso de frameworks (o marcos) creados enteramente en Python que usen CGI con el fin de esconder sus detalles y permitir a los programadores concentrarse en las funciones de su aplicación. Algunos frameworks que se pueden usar son Django, CherryPy, Pylons y web.py.

Sin embargo, App Engine ya incluye un framework sencillo que viene con el kit de desarrollo y que es muy fácil de usar, llamado webapp. En este trabajo voy a usar webapp para mantener las cosas simples.
Un ejemplo de aplicación web usando este marco es la siguiente (éste sería el archivo modulo.py indicado en el archivo app.yaml):


    #!python
    from google.appengine.ext import webapp
    from google.appengine.ext.webapp.util import run_wsgi_app
     
    class MainPage(webapp.RequestHandler):
        def get(self):
            self.response.out.write('Hola mundo!')

    application = webapp.WSGIApplication([('/', MainPage)],
     							debug=True)
    
    def main():
        run_wsgi_app(application)
    
    if __name__ == "__main__":
        main()


Podemos analizar lo siguiente:

Nuestra aplicación consiste de un objeto `webapp.WSGIApplication` (la variable `application`) que posee una lista de rutas y la clase que manejará cada ruta (en este ejemplo la raíz "/" será manejada por la clase `MainPage`). Esto es lo que explicaba anteriormente donde decía que un único módulo será el encargado de redirigir las peticiones al módulo correspondiente (en este caso la clase manejadora se encuentra en el mismo archivo pero podemos ponerla en otro distinto).

La clase manejadora (`MainPage`) es una clase que hereda de `webapp.RequestHandler`. Este tipo de clase sería el equivalente a la clase `HttpServlet` que usamos en Java, donde definimos el comportamiento para el método GET (en este caso con la función `get(self)`). Podemos también definir el comportamiento para el método POST con la función `post(self)`.

La clase `webapp.RequestHandler` nos provee el objeto `self.response`, equivalente al `HttpServletResponse` que usamos en Java y que nos permite armar la respuesta a la solicitud. En este ejemplo simplemente escribimos "Hola Mundo!" en el objeto `self.response.out` equivalente al brindado por `HttpServletResponse.getWriter()` en Java.

Como vamos a ver en el caso de estudio, `webapp.RequestHandler` también nos provee el objeto `self.request` para obtener datos de la petición, equivalente al objeto `HttpServletRequest` que usamos en Java.

Al ejecutarse este módulo, se llama a la función `main()` quien llama a la función `run_wsgi_app()` con nuestro objeto aplicación (línea 12). De esta forma la aplicación queda corriendo.

Con eso ya podemos tener una aplicación web sencilla corriendo en App Engine. 
Más adelante cuando desarrolle el caso de estudio, será necesario dar unas explicaciones sobre el almacén de datos usado por App Engine (una base de datos no relacional) y el sistema de plantillas, para poder implementar el patrón MVC.


# 4. Caso de estudio:

## 4.1 Presentación:

Xxxxxxxxxx

Por lo tanto voy a dividir la aplicación en los siguientes elementos:
El Modelo:
Será el encargado de todo lo relacionado con la base de datos. A él le pedimos los datos y le brindamos la información nueva que debe guardar.
La vista:
La vista (o las vistas) van a ser los archivos HTML en donde presentemos la información al usuario (las publicaciones disponibles por ejemplo) y en donde él va a poder introducir un nuevo valor para el precio.
El controlador:
Será la conexión entre el modelo y la vista. Recibe datos del modelo y se los pasa a la vista, y viceversa.

El controlador estará dividido en 3 “servicios”: p1, p2 y p3 (la “p” de “precio”). Al invocar a p1 vamos a obtener la primera pantalla donde podemos elegir una publicación a editar. De esta vista se invoca a p2 con una publicación en particular, y vamos a obtener la pantalla en donde vemos el precio que tiene esa publicación y donde podemos modificarlo. Por último se invoca a p3 quien será el encargado de guardar este valor y mostrarnos una pantalla de confirmación.

Dicho esto comencemos a escribir la aplicación.

4.2 Iniciar una nueva aplicación:

En Linux empezamos creando una carpeta dentro del directorio google_appengine donde extrajimos el SDK. Por ejemplo podemos llamarla “iw”. En esta carpeta voy a ir poniendo todos los archivos de la aplicación web.
El primer archivo que voy a crear va a ser el descriptor app.yaml, con el siguiente contenido:

application: iw-tpfinal
version: 1
runtime: python
api_version: 1

handlers:
- url: /.*
  script: main.py

Como se ve el nombre de la aplicación por ahora va a ser “iw-tpfinal”. Este nombre después hay que cambiarlo por el que usemos al registrar la aplicación en Google App Engine (o el mismo si está libre al momento de registrarla).
Después creo el archivo main.py, por ahora con el siguiente contenido:

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

application = webapp.WSGIApplication([], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

Por ahora no tenemos ninguna clase manejadora, si probamos esto vamos a obtener una página en blanco. Guardamos los 2 archivos en nuestra carpeta “iw”:


La forma de ir probando nuestro trabajo es con el servidor de pruebas. Abrimos una terminal en la carpeta google_appengine y ejecutamos:

$ ./dev_appserver.py iw

Con esto tenemos el servidor corriendo en localhost en el puerto 8080. Si probamos la URL http://localhost:8080/ obtenemos la página en blanco como mencioné anteriormente:



En Windows empezar una aplicación nueva es más sencillo. Abrimos el lanzador (Google App Engine Launcher), y elegimos File/Add New Application (o el botón “+” en la parte inferior). En el cuadro configuramos el nombre, una ruta donde guardarla (automáticamente se crea una carpeta con el nombre de la aplicación en esta ruta) y un puerto para el servidor (dejamos 8080):


Al presionar Create obtenemos ya los archivos app.yaml y main.py genéricos (una aplicación que muestra “Hello world”). Si presionamos el botón Run, el servidor se ejecuta y podemos probar la aplicación con el botón Browse:



En este caso modificamos los archivos app.yaml y main.py con los mostrados en este trabajo.

Algunos datos sobre el servidor de pruebas:

Cualquier cambio que hagamos en los archivos de la aplicación es automáticamente reflejado en el servidor web, sin necesidad de reiniciarlo o de indicárselo manualmente. Solamente hay que refrescar la página en el navegador y siempre veremos la última versión.
Además en http://localhost:8080/_ah/admin tenemos una consola de administración que nos ofrece algunas herramientas útiles para el desarrollo pero no voy a hacer uso de ellas ya que no es necesario.



4.3 Consideraciones antes de seguir:

4.3.1 El almacén de datos de App Engine:



4.3.2 El sistema de plantillas de App Engine:





4.4 El modelo:


Como ya fije anteriormente, el modelo será el encargado de todo lo relacionado con la base de datos. A él le vamos a pedir la lista de p    ublicaciones guardadas, 