"""Publica en Instagram el carrusel que toca hoy (según calendario.json).

Variables de entorno (en GitHub: Settings → Secrets and variables → Actions):
  IG_TOKEN    token de larga duración de Instagram (Instagram Login)
  IG_USER_ID  ID de la cuenta de Instagram profesional
Opcionales:
  ORDEN       publica un post específico (prueba manual), p. ej. "1"
  DRY_RUN     "1" para solo mostrar qué haría, sin publicar
"""
import json, os, sys, time, datetime, urllib.request, urllib.parse, urllib.error
from zoneinfo import ZoneInfo

API = "https://graph.instagram.com/" + os.environ.get("API_VERSION", "v23.0")
TOKEN, USER = os.environ.get("IG_TOKEN", ""), os.environ.get("IG_USER_ID", "")
REPO = os.environ["GITHUB_REPOSITORY"] if "GITHUB_REPOSITORY" in os.environ else "USUARIO/REPO"
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/posts"
DRY = os.environ.get("DRY_RUN") == "1"

def api(method, path, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    req = urllib.request.Request(url + ("?" + data.decode() if method == "GET" else ""), data=None if method == "GET" else data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Error de la API ({e.code}) en {path}: {e.read().decode()}")

def esperar(cid):  # Meta descarga y procesa la imagen; esperar a FINISHED
    for _ in range(30):
        st = api("GET", cid, fields="status_code").get("status_code")
        if st == "FINISHED": return
        if st in ("ERROR", "EXPIRED"): sys.exit(f"El contenedor {cid} quedó en {st}")
        time.sleep(5)
    sys.exit(f"Tiempo de espera agotado para {cid}")

cal = json.load(open("calendario.json", encoding="utf-8"))
hechos = json.load(open("publicados.json", encoding="utf-8"))
hoy = datetime.datetime.now(ZoneInfo("America/Mexico_City")).date().isoformat()
orden = os.environ.get("ORDEN", "").strip()
post = next((p for p in cal if (str(p["orden"]) == orden if orden else p["fecha"] == hoy)), None)
if not post:
    print(f"Nada que publicar hoy ({hoy})."); sys.exit(0)
if any(h["orden"] == post["orden"] for h in hechos) and not orden:
    print(f"El post {post['orden']} ya se publicó."); sys.exit(0)

slides = sorted(f for f in os.listdir(f"posts/{post['carpeta']}") if f.endswith(".jpg"))
urls = [f"{RAW}/{post['carpeta']}/{f}" for f in slides]
print(f"Post {post['orden']} · {post['id']} · {post['universidad']} · {len(urls)} slides")
if DRY:
    print("\n".join(urls)); print("---\n" + post["caption"]); sys.exit(0)
if not TOKEN or not USER:
    sys.exit("Faltan IG_TOKEN o IG_USER_ID.")

hijos = []
for u in urls:  # 1) un contenedor por imagen
    c = api("POST", f"{USER}/media", image_url=u, is_carousel_item="true")["id"]
    esperar(c); hijos.append(c)
car = api("POST", f"{USER}/media", media_type="CAROUSEL", children=",".join(hijos), caption=post["caption"])["id"]  # 2) carrusel
esperar(car)
pub = api("POST", f"{USER}/media_publish", creation_id=car)["id"]  # 3) publicar
print(f"Publicado ✔ media_id={pub}")

hechos.append({"orden": post["orden"], "id": post["id"], "media_id": pub,
               "publicado": datetime.datetime.now(ZoneInfo("America/Mexico_City")).isoformat(timespec="minutes")})
json.dump(hechos, open("publicados.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
