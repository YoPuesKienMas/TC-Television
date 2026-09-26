from playwright.sync_api import sync_playwright
import random

def extraer_senal():
    enlace_m3u8 = ""
    # Inventamos una IP de Ecuador al azar para engañar al sistema
    ip_ecuador = f"186.101.{random.randint(1,255)}.{random.randint(1,255)}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Aquí está la magia: Disfrazamos completamente el navegador
        context = browser.new_context(
            geolocation={"latitude": -2.19616, "longitude": -79.88621}, # Coordenadas de Guayaquil
            permissions=["geolocation"],
            locale="es-EC", # Idioma Español Ecuador
            timezone_id="America/Guayaquil", # Zona horaria
            extra_http_headers={
                "X-Forwarded-For": ip_ecuador,
                "X-Originating-IP": ip_ecuador,
                "X-Remote-IP": ip_ecuador,
                "X-Remote-Addr": ip_ecuador,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        page = context.new_page()

        def interceptar_red(respuesta):
            nonlocal enlace_m3u8
            if ".m3u8" in respuesta.url and "live" in respuesta.url:
                enlace_m3u8 = respuesta.url

        page.on("response", interceptar_red)
        
        print(f"Entrando a TC disfrazado con la IP falsa: {ip_ecuador}")
        try:
            page.goto("https://tctelevision.com/en-vivo", timeout=60000)
            page.wait_for_timeout(10000) # Espera a que el video suelte el enlace
        except Exception as e:
            print("Error al cargar:", e)
            
        browser.close()
        
    return enlace_m3u8

enlace = extraer_senal()

if enlace:
    print("¡Engaño exitoso! Enlace HD capturado:", enlace)
    with open('tc.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        f.write('#EXTINF:-1 aspect-ratio="16:9", TC Television (HD Real)\n')
        f.write(enlace + "\n")
else:
    print("El sistema detectó el engaño. No soltó el enlace.")
    # Si falla, dejamos un enlace de respaldo
    with open('tc.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n#EXTINF:-1, TC Television (Fallo)\nhttps://5c21f7ec1999d.streamlock.net/8054/8054/playlist.m3u8\n")
