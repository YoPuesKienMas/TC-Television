import urllib.request
import re

# 1. El robot entra a TC Televisión
url = "https://tctelevision.com/en-vivo"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    # 2. Lee todo el código oculto de la página
    html = urllib.request.urlopen(req).read().decode('utf-8')
    
    # 3. Busca el enlace m3u8
    match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8)', html)
    if match:
        enlace = match.group(1)
        
        # 4. Cambiamos la calidad a 720p (HD) si es posible
        enlace_hd = enlace.replace('live-480', 'live-720')
        
        # 5. Crea tu archivo M3U automáticamente
        with open('tc.m3u', 'w') as f:
            f.write("#EXTM3U\n")
            f.write("#EXTINF:-1, TC Television (HD)\n")
            f.write(enlace_hd + "\n")
        print("¡Éxito! Enlace guardado:", enlace_hd)
except Exception as e:
    print("Hubo un error:", e)
