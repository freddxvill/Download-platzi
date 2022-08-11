# Descarga automática de Platzi

Descarga automática mediante un script de Python utilizando Playwright y FFmpeg.

🎭 [Playwright](https://playwright.dev/python/) es un framework para web testing y automatizacion. Tambien se lo utiliza para realizar web scraping y esta disponible en varios lenguajes, por lo que el codigo podria ser traducido a [Node.js](https://playwright.dev/docs/intro), [.NET](https://playwright.dev/dotnet/docs/intro) o [Java](https://playwright.dev/java/docs/intro).

En este caso es utilizado junto con la herramienta [FFmpeg](https://ffmpeg.org/) para realizar descargas automatizadas de videos de `Platzi`pertenecientes a un curso.


## Instalación
- Instalar [Python](https://www.python.org/downloads/).
- Descargar o clonar el codigo en una carpeta con git.

```bash
git clone https://github.com/freddxvill/Download-platzi.git
```
- Crear un **entorno virtual** de python dentro de la carpeta. Con [virtualenv](https://virtualenv.pypa.io/en/latest/) utilizar el siguiente comando:

```bash
virtualenv venv
```
- **Activa** el entorno. En Windows - Powershell:

```bash
.\venv\Scripts\activate
```
- Instalar las dependencias del archivo **requirements.txt** en el entorno.

```bash
pip install -r requirements.txt
```

- Despues de tener Playwright instalado. Instalar los navegadores, que seran controlados por Playwright.

```bash
playwright install
```

### Instalacion de FFmepg

Descargar FFmepg desde (https://ffmpeg.org/) para windows.
**En Windows descomprimir el .zip en el disco C y añadir su ruta a las variables del sistema, en path.**

Esta herramienta permite descargar videos no solo de links directos, sino tambien de videos tipo streaming en tiempo real tipo (M-DASH y HLS).

M-DASH y HLS son protocolos que se ejecutan a través de HTTP, utilizan TCP como protocolo de transporte, dividen el vídeo en segmentos con un archivo de índice adjunto y ofrecen transmisión de velocidad de bits adaptable.

Para saber mas ver : [Qué es M-DASH y HLS](https://www.cloudflare.com/es-es/learning/video/what-is-mpeg-dash/) 

## Instrucciones

Crear un cuenta en Platzi.

Ejecutar el archivo platzi.py (entorno activado)

```bash
python platzi.py
```
En la consola se mostrara lo siguiente:

```notepad
Descargador de cursos [colocar los datos correctamente]
volver a ejecutar si falla el login o algun dato
--------------------------------------------------------------------------------------
Curso [nombre completo]: Curso de Fundamentos de Web Scraping con Python y Xpath
Email: tuemail@gmail.com
Password: password
Path [direccion de la carpeta donde sera descargado][ejm:'D:/cursos_programacion/'][debe terminar con un / ]
Path: D:/dir1/dir2/
--------------------------------------------------------------------------------------
```
y comenzara la descarga del curso.

```notepad
Path ----> D:/dir1/dir2/curso de fundamentos de web scraping con python y xpath

comenzando ...
link: ok
--------- Descargando clase: 1_Qué es el web scraping ---------
frame=3629 fps=88 q=-1.0 Lsize= 10901kB time=00:02:06.97 bitrate= 795 kbits/s speed=3.09x

link: ok
--------- Descargando clase: 2_Por qué aprender webscraping hoy ---------
frame=5575 fps=88 q=-1.0 Lsize= 10901kB time=00:03:05.97 bitrate= 735 kbits/s speed=3.5x

link: ok
--------- Descargando clase: 3_Python- el lenguaje mas poderoso para extraer datos ---------
frame=6032 fps=88 q=-1.0 Lsize= 10901kB time=00:03:21.97 bitrate= 735 kbits/s speed=3.5x
    .
    .
    .
    .

secciones: 5
clases: 21
Descarga terminada: curso de fundamentos de web scraping con python y xpath
```
Una vez finalizado, ir al carpeta para ver los videos descargados.

[![Captura2.png](https://i.postimg.cc/gj3m1zY1/Captura2.png)](https://postimg.cc/n9VyDt91)

### Funcionamiento del script

Al ejecutar el script con los datos del usuario de platzi, Playwright abrirá un navegador (en este caso Chrome) para insertar los datos en el login. Posteriormente se realiza una busqueda del curso dentro de la pagina.
Una vez encontrado el curso, se dirige a la primera clase del curso y con Playwright se [intercepta](https://playwright.dev/python/docs/network#network-events) todas las requests que hace la pagina. Se captura el link del video en streaming y se lo pasa a ffmpeg para que realize la descarga y lo convierta directamente a .mp4.

## Notas importantes

- El script abrirá y cerrará un navegador para hallar el link de cada video, esto sucederá debido a que se intentó usar el modo `headless=True`el cual permite navegar en una página sin tener que mostrar el navegador. Este parámetro funciona muy bien en otras páginas, pero no funciono en el caso de Platzi. Por lo tanto, hasta este momento, para que el script funcione, debe abrir y cerrar la interfaz al encontrar el link.
- Si el script se detiene en la página del **Login**, solo debe detener el cript y volverlo a correr. El script detectará los archivos ya descargados, para no volverlos a descargar.
- El script descargará videos con resolución 1080x720, pero puede cambiarlo a 1920x1080 modificando dentro del script, en la funcion download, después de `'-map'` en vez de `'0:1'` colocar `'0:3'`. Esto seleccionará el video stream a 1080p, el cual tendrá un mayor tamaño, por lo cual la descarga tomará un poco más de tiempo.

## Referencias

* [Playwright](https://playwright.dev/docs/intro)
* [FFmpeg](https://ffmpeg.org/)
* [FFmpeg- streaming](https://trac.ffmpeg.org/wiki/StreamingGuide)
* [Selecting streams with the -map option](https://trac.ffmpeg.org/wiki/Map)
* [How Download Videos Or Live Streaming From Azure Media Service Content](https://hoohoo.top/blog/20210627214233-how_download_azure_media_service_video_and_live_streaming_to_local/)
* [Deliver content to customers](https://docs.microsoft.com/en-us/azure/media-services/previous/media-services-deliver-content-overview)