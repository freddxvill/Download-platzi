from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import os
import subprocess

print('Descargador de cursos [colocar los datos correctamente]')
print('volver a ejecutar si falla el login o algun dato')
print('-'*80)
curso = str(input('Curso [nombre completo]: '))
email = str(input('Email [@gmail.com]: '))
password = str(input('Password: '))
print('Path [direccion de la carpeta donde sera descargado][ejem: D:/cursos_programacion/ ][debe terminar con un /]')
print('[ Se creara una carpeta dentro del Path con el nombre del curso ]')
path = str(input('Path: '))
print('-'*80)

video_link = ''

curso = curso.lower()
name_folder = curso.replace(':', '-')
complet_path = path + name_folder
print('Path ----> ',complet_path)
print('')
print('Iniciando ...')
print('')

if not os.path.exists(complet_path):
    os.makedirs(complet_path)


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



def download_video(video_link: str, path: str, clas_title: str):
    try:
        if os.path.exists(path):
            print('Archivo ya descargado en: ', path)
            print('')

        else:
            if video_link:
                print(f'--------  Descargando clase: {clas_title} -----------' )
                subprocess.run(['ffmpeg','-loglevel' ,'quiet', '-stats', '-i', video_link, '-map', '0:0', '-map', '0:1', '-c', 'copy', path])
                print('')
            else:
                print('Link no encontrado')

    except Exception as e:
        print('Error en la descarga: clase no descargada')
        print(e)
        pass

# ---------
log = True
bloc = True
num_clases = 0
b = 1
while bloc:
    i = 1
    cont_clas = True
    while True:
        with sync_playwright() as p:
            
            try:
                browser = p.chromium.launch(channel="chrome",headless=False) 
                page = browser.new_page(viewport= {"width": 800, "height": 600}) # user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')
                stealth_sync(page)
                page.goto('https://platzi.com/login/')
                page.fill("//input[@type='email']", email)
                page.fill("//input[@type='password']", password)
                page.wait_for_timeout(2*1000)
                page.click("button[type='submit']")
                page.is_visible('div.NewSearch-box')
                page.wait_for_selector(selector= 'div.NewSearch-box', timeout=6000)
                page.fill("//input[@class='NewSearch-input']",curso)
                print('Login: succesfully')
            except:
                print('Login: error, volviendo a ingresar ...')
                log = False
                break



            page.wait_for_timeout(2*1000)
            page.keyboard.press('Enter')
            page.is_visible('div.CourseList')
            # click al primer resultado para el curso solicitado
            page.click("//div[@class='CourseList']/article[1]//a[@class='CourseCard-content-title']") 
            try:
                selector = f"//div[@class='ContentBlock'][{b}]"
                page.wait_for_selector(selector= selector, timeout=6000)
            except:
                bloc = False
                browser.close()

            try:
                selector_2 = f"//div[@class='ContentBlock'][{b}]//li[{i}]/div/div/a"
                page.wait_for_selector(selector= selector_2, timeout=6000)
                # click al curso n
                # prueba del primero
                page.wait_for_timeout(2*1000)
                page.on("request", handle_requests)
                page.click(f"//div[@class='ContentBlock'][{b}]//li[{i}]/div/div/a")
                page.wait_for_timeout(3*1000)
                title = page.title()
                i += 1
                num_clases += 1
            except:
                cont_clas = False
                browser.close()

        if bloc == False:
            print('secciones: ', b)
            break

        if cont_clas == False:
            break

        try:
            clas_title = process_text(title)
            clas_title = f'{num_clases}_{clas_title}'
            path_dir = complet_path + f'/{clas_title}.mp4'
            
            download_video(video_link=video_link, path=path_dir, clas_title=clas_title)
        except:
            break

    if log == True:
        b += 1

print('clases: ', num_clases)
print('Descarga terminada: ', curso)