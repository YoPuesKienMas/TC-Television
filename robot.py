import urllib.request

# 1. Usamos el enlace maestro para evitar los bloqueos de JS
url = "https://iptv-org.github.io/iptv/countries/ec.m3u"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    contenido = urllib.request.urlopen(req).read().decode('utf-8')
    lineas = contenido.split('\n')
    enlace_tc = "https://5c21f7ec1999d.streamlock.net/8054/8054/playlist.m3u8" # Enlace de emergencia
    
    # 2. Extraemos ÚNICAMENTE TC Televisión
    for i, linea in enumerate(lineas):
        if "TC" in linea.upper() and "TELEVIS" in linea.upper():
            enlace_tc = lineas[i+1].strip()
            break
            
    # 3. TRUCO PRO: Forzamos la calidad a HD (720) arreglando la imagen
    enlace_hd = enlace_tc.replace('live-480', 'live-720').replace('live-360', 'live-720')
    
    # 4. Creamos el archivo final
    with open('tc.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1, TC Television (HD)\n")
        f.write(enlace_hd + "\n")
        
    print("¡Éxito! Lista creada con:", enlace_hd)
    
except Exception as e:
    print("Error:", e)
    # Salvavidas extremo: Si la web se cae, crea el archivo igual para evitar el Error 128
    with open('tc.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n#EXTINF:-1, TC Television (Backup)\nhttps://5c21f7ec1999d.streamlock.net/8054/8054/playlist.m3u8\n")
