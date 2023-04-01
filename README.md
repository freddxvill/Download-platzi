# Descarga automática de Platzi

Descarga automática y rapida mediante un script de Python utilizando Playwright y yt-dlp.

🎭 [Playwright](https://playwright.dev/python/) es un framework para web testing y automatizacion. Tambien se lo utiliza para realizar web scraping y esta disponible en varios lenguajes, por lo que el codigo podria ser traducido a [Node.js](https://playwright.dev/docs/intro), [.NET](https://playwright.dev/dotnet/docs/intro) o [Java](https://playwright.dev/java/docs/intro).

En este caso es utilizado junto con la herramienta [yt-dlp](https://github.com/yt-dlp/yt-dlp) para realizar descargas automatizadas de videos de `Platzi`pertenecientes a un curso.


## Instalación
- Instalar [Python](https://www.python.org/downloads/). La version utilizada fue python 3.10.5
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

- Instalar yt-dlp, este ejecuta por debajo a ffmpeg.

```bash
pip install yt-dlp
```

### Instalacion de la version de FFmepg estable para yt-dlp

Descargar la version estable de FFmepg para yt-dlp desde (https://github.com/yt-dlp/FFmpeg-Builds) para windows.
**En Windows descomprimir el .zip en el disco C y añadir la ruta de la carpeta FFmpeg a las variables del sistema, en path.**

Esta herramienta permite descargar videos no solo de links directos, sino tambien de videos tipo streaming en tiempo real tipo (M-DASH y HLS).

M-DASH y HLS son protocolos que se ejecutan a través de HTTP, utilizan TCP como protocolo de transporte, dividen el vídeo en segmentos con un archivo de índice adjunto y ofrecen transmisión de velocidad de bits adaptable.

Para saber mas ver : [Qué es M-DASH y HLS](https://www.cloudflare.com/es-es/learning/video/what-is-mpeg-dash/) 

## Instrucciones

Crear un cuenta en Platzi, entrar en la pagina, realizar el login y despues cerrar el navegador.

Modificar en el script de python los datos de su navegador.
Para ver las direcciones, escribir arriba del navegador en url: chrome://version .
Para el user agent debe ir a [what is my user agent](https://www.whatismybrowser.com/es/detect/what-is-my-user-agent/) y copiarlo.

```bash
user_data = 'C:/Users/.../AppData/Local/Google/Chrome/User Data' # Debe terminar en User Data
chrome_path = 'C:/Users/.../AppData/Local/Google/Chrome/Application/chrome.exe'
user_agent_nav = """ Mozilla/5.0 (Windows NT 10.0; Win64; x64)
                 AppleWebKit/537.36 (KHTML, like Gecko)
                 Chrome/107.0.0.0 Safari/537.36 """   # version de chrome 107, coloque la version de su navegador
```
Esto con el fin de que el navegador este autenticado en la pagina y no abrir el navegador mientras descarga.

Ejecutar el archivo platzi.py (con el entorno activado)

```bash
python platzi.py
```
En la consola se mostrara lo siguiente:

```notepad
Descargador de cursos [colocar los datos correctamente]
Importante: Debe estar ya logeado con su navegador Chrome
--------------------------------------------------------------------------------------
Curso [copiar el link de la portada del curso][La pagina donde se muestra el contenido]
Ejm: https://platzi.com/cursos/notacion-matematica/
Link curso: https://platzi.com/cursos/web-scraping/

Path [direccion de la carpeta donde sera descargado][ejm:'D:/cursos_programacion/'][debe terminar con un / ]
[ Se creara una carpeta dentro del Path con el nombre del curso ]
Path: D:/dir1/dir2/

Curso [Nombre del curso][se colocara ese nombre a la carpeta]
Curso: Curso de fundamentos de web scraping con python y xpath
--------------------------------------------------------------------------------------
```
y comenzara la descarga del curso.

```notepad
Path ----> D:/dir1/dir2/curso de fundamentos de web scraping con python y xpath

Iniciando ...

link: ok
Clase ok
--------- Descargando clase: 1_Qué es el web scraping ---------
frame=3629 fps=88 q=-1.0 Lsize= 10901kB time=00:02:06.97 bitrate= 795 kbits/s speed=3.09x

link: ok
Clase ok
--------- Descargando clase: 2_Por qué aprender webscraping hoy ---------
frame=5575 fps=88 q=-1.0 Lsize= 10901kB time=00:03:05.97 bitrate= 735 kbits/s speed=3.5x

link: ok
Clase ok
--------- Descargando clase: 3_Python- el lenguaje mas poderoso para extraer datos ---------
frame=6032 fps=88 q=-1.0 Lsize= 10901kB time=00:03:21.97 bitrate= 735 kbits/s speed=3.5x
    .
    .
    .
    .
    .
    .

clases: 21
Descarga terminada: curso de fundamentos de web scraping con python y xpath
```
Una vez finalizado, ir al carpeta para ver los videos descargados.

[![Captura2.png](https://i.postimg.cc/gj3m1zY1/Captura2.png)](https://postimg.cc/n9VyDt91)

### Funcionamiento del script

El script tomara el control del navegador Chrome (puede ser cambiado a otro tipo de navegadores), Playwright abrirá un navegador (en este caso Chrome), pero este sera el navegador de uso habitual con el que estamos autenticados en la pagina. Posteriormente se obtine los links de cada clase utilizando BeautifulSoup.
Una vez obtenido los links de las clases, se dirige a la primera clase del curso y con Playwright se [intercepta](https://playwright.dev/python/docs/network#network-events) todas las requests que hace la pagina. Se captura el link del video en streaming y se lo pasa a yt-dlp que maneja por debajo a ffmpeg para que realize la descarga y lo convierta directamente a .mp4.

Nuevo:  `yt-dlp` realiza una descarga mas rapida y sin perdida de frames de video y audio.

## Notas importantes

- Si el script se detiene en la página, solo debe detener el script y volverlo a correr. El script detectará los archivos ya descargados, para no volverlos a descargar.
- Si aperece el error 403, es debido a que la pagina le solicita autenticarse manualmente una vez, por lo tanto vuelva a la pagina de su curso y complete la autenticación manual. Vuelva a ejecutar el script.

- **AVISO**: Otro motivo sobre para el error 403 es debido a que la plataforma hizo cambios en el protocolo de streaming de video, si continua con el error puede usar otros programas de descarga como IDM dowloader o XDM dowloader, ya que estos si soportan otros tipos de protocolos.

## Referencias

* [Playwright](https://playwright.dev/docs/intro)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [FFmpeg stable](https://github.com/yt-dlp/FFmpeg-Builds)
* [FFmpeg- streaming](https://trac.ffmpeg.org/wiki/StreamingGuide)
* [Selecting streams with the -map option](https://trac.ffmpeg.org/wiki/Map)
* [How Download Videos Or Live Streaming From Azure Media Service Content](https://hoohoo.top/blog/20210627214233-how_download_azure_media_service_video_and_live_streaming_to_local/)
* [Deliver content to customers](https://docs.microsoft.com/en-us/azure/media-services/previous/media-services-deliver-content-overview)
