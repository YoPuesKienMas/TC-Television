from playwright.sync_api import sync_playwright

def extraer_senal():
    enlace_m3u8 = ""
    
    # Abrimos un Chrome invisible
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Esta función actúa como el "F12" (Network tab)
        def interceptar_red(respuesta):
            nonlocal enlace_m3u8
            # Filtramos buscando el archivo de video en vivo
            if ".m3u8" in respuesta.url and "live" in respuesta.url:
                enlace_m3u8 = respuesta.url

        # Le decimos al navegador que escuche todo el tráfico
        page.on("response", interceptar_red)
        
        print("Entrando a la página de TC Televisión...")
        # Entramos a la web
        page.goto("https://tctelevision.com/en-vivo", timeout=60000)
        # Esperamos 10 segundos para darle tiempo al reproductor de cargar y soltar el enlace
        page.wait_for_timeout(10000) 
        browser.close()
        
    return enlace_m3u8

enlace = extraer_senal()

if enlace:
    # Forzamos la calidad más alta (HD)
    enlace_hd = enlace.replace('live-480', 'live-720').replace('live-360', 'live-720')
    print("¡Enlace interceptado con éxito!", enlace_hd)
    
    with open('tc.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        # Le añadimos la orden aspect-ratio="16:9" para obligar a la TV a estirar la imagen
        f.write('#EXTINF:-1 aspect-ratio="16:9", TC Television (Web HD)\n')
        f.write(enlace_hd + "\n")
else:
    print("No se pudo interceptar el enlace.")
    # Salvavidas en caso de que la página no cargue ese día
    with open('tc.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n#EXTINF:-1, TC Television (Backup)\nhttps://5c21f7ec1999d.streamlock.net/8054/8054/playlist.m3u8\n")
