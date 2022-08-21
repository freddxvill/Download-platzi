# Librerias
import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
#from playwright_stealth import stealth_sync
import os
import subprocess


#--------------- Ruta propia del navegador Chrome----------------
user_data = 'C:/Users/HP/AppData/Local/Google/Chrome/User Data'
chrome_path = 'C:/Users/HP/AppData/Local/Google/Chrome/Application/chrome.exe'
user_agent_nav = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'

# -----------------------------------
delay = 2 # seg
url_pag = 'https://platzi.com'
video_link = ''

# -------------------------------------------------------------------------------------------------------------
def list_links(url_curso: str, url_pag: str):
    r_curso = requests.get(url_curso)
    s_curso = BeautifulSoup(r_curso.text, 'lxml')
    links = s_curso.find('div', attrs={'class':'Content-feed'}).find_all('div', attrs={'class':'ContentClass'})
    list_links = []
    for link in links:
        if link.a:
            list_links.append(url_pag + link.a.get('href'))
    return list_links


def handle_requests(request):
    global video_link
    
    if request.url:
        if 'manifest' in request.url or '//mdstrm.com/video/' in request.url:
            video_link = request.url
            print('link: ok')
        else:
            pass


def process_text(text: str):
    text = text.replace(' - Platzi', '')
    text = text.replace(':', '-')
    text = text.replace('?', '')
    text = text.replace('¿', '')
    return text


def download_video(path: str, clas_title: str):
    global video_link
    try:
        if os.path.exists(path):
            print('Archivo ya descargado:', clas_title)
            print('')
            video_link=''

        else:
            if video_link:
                print(f'--------  Descargando clase: {clas_title} -----------' )
                subprocess.run(['ffmpeg','-loglevel' ,'quiet', '-stats', '-i', video_link, '-map', '0:0', '-map', '0:1', '-c', 'copy', path])
                print('')
                video_link = ''

            else:
                print('Link no encontrado')
                print('Si este problema persiste:')
                print('--> Abrir el navegador e ir a clase donde se detuvo, y si le muestra un Captcha debe solo resolverlo')
                print('--> Ejecutar de nuevo el script')
                print('')
                video_link = ''

    except Exception as e:
        print('Error en la descarga: clase no descargada')
        print(e)
        pass


# ----------------- Datos --------------------------------------------------------

print('Descargador de cursos [colocar los datos correctamente]')
print('Importante: Debe estar ya logeado con su navegador Chrome')
print('-'*80)
print('Curso [copiar el link de la portada del curso][La pagina donde se muestra el contenido]')
print('Ejm: https://platzi.com/cursos/notacion-matematica/')
url_curso = str(input('Link curso: '))
print('')
print('Path [direccion de la carpeta donde sera descargado][Ejem: D:/cursos_programacion/ ][debe terminar con un /]')
print('[ Se creara una carpeta dentro del Path con el nombre del curso ]')
path = str(input('Path: '))
print('')
print('Curso [Nombre del curso][se colocara ese nombre a la carpeta]')
curso = str(input('Curso: '))
print('-'*80)

# --------- Creacion de la carpeta ------------------

curso = curso.lower()
name_folder = curso.replace(':', '-')
complet_path = path + name_folder
print('Path ----> ',complet_path)
print('')
print('Iniciando ...')
print('')

if not os.path.exists(complet_path):
    os.makedirs(complet_path)
# ----------------------------------------------------


links = list_links(url_curso, url_pag)
print('n clases: ',len(links))
num_clases = 0
    
for link in links:
    tries = 1
    while tries < 3:
        with sync_playwright() as p:
            time.sleep(delay)
            browser = p.chromium.launch_persistent_context(
                user_data_dir= user_data,
                #channel="chrome",
                executable_path= chrome_path,
                headless=True,
                user_agent= user_agent_nav
                )                                   
            page = browser.new_page()
            #stealth_sync(page)
            page.on("request", handle_requests)
            page.goto(link, wait_until='networkidle')
            page.wait_for_timeout(3*1000)
            title = page.title()

        if video_link:
            print('Clase ok')
            tries = 3
        else:
            tries += 1


    if video_link and title:
        num_clases += 1
        print('clase: ',num_clases)
        clas_title = process_text(title)
        clas_title = f'{num_clases}_{clas_title}'
        path_dir = complet_path + f'/{clas_title}.mp4'
        download_video(path=path_dir, clas_title=clas_title)
        title = ''

    if tries > 1 and video_link == '' and title:
        num_clases += 1
        clas_title = process_text(title)
        print(f'clase: {num_clases}_{clas_title}')
        print('-- > Sin link: posiblemente es una pagina')
        print('')
        title = ''


print('clases: ', num_clases)
print('Descarga terminada: ', curso)
