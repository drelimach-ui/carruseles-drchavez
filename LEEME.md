# Publicador automático de carruseles · Dr. Chávez

Cada día a las 19:00 (hora de CDMX), GitHub Actions publica en Instagram el carrusel que toca según `calendario.json`. Es gratis y no necesita que tu computadora esté encendida.

## Contenido
- `publicar.py`: el script que publica (crea las 4 imágenes, arma el carrusel y lo publica con su caption).
- `.github/workflows/publicar.yml`: el horario (todos los días a las 01:00 UTC = 19:00 CDMX) y el botón de prueba manual.
- `calendario.json`: los 100 posts con fecha (del 28-oct-2026 al 4-feb-2027), carpeta y caption.
- `publicados.json`: registro de lo ya publicado (se actualiza solo; evita publicar dos veces).
- `posts/`: aquí van las 100 carpetas `001_…` a `100_…` (descomprime ahí los 4 .zip de carruseles).

## Paso 1 · Instagram profesional
En la app de Instagram: Configuración → Tipo de cuenta y herramientas → Cambiar a cuenta profesional (Creador o Empresa).

## Paso 2 · App de Meta y token
1. Entra a developers.facebook.com → Mis apps → Crear app → tipo **Empresa**.
2. Agrega el producto **Instagram** → "API con inicio de sesión de Instagram".
3. En "Generar tokens de acceso", agrega tu cuenta @drchavezmx (te pedirá iniciar sesión y aceptar permisos).
4. Copia el **token** y el **ID de la cuenta de Instagram** que aparecen ahí. El token dura 60 días.
5. Permisos que debe tener: `instagram_business_basic` e `instagram_business_content_publish`.

## Paso 3 · Repositorio en GitHub
1. Crea una cuenta en github.com (si no tienes) y un repositorio **público** llamado, por ejemplo, `carruseles-drchavez`.
   Debe ser público porque Instagram descarga las imágenes desde un enlace público.
2. Instala **GitHub Desktop**, clona el repositorio y copia dentro todo el contenido de esta carpeta (incluida la carpeta oculta `.github`) y las 100 carpetas en `posts/`.
3. Commit → Push.

## Paso 4 · Secretos
En el repositorio: Settings → Secrets and variables → Actions → New repository secret:
- `IG_TOKEN` = el token del paso 2
- `IG_USER_ID` = el ID de la cuenta del paso 2

## Paso 5 · Prueba
Actions → "Publicar carrusel del día" → Run workflow:
- Deja `dry_run = 1` y `orden = 1` → solo simula y muestra los enlaces y el caption.
- Si todo sale bien, corre con `dry_run = 0` y `orden = 1` para publicar el primero de verdad.
Después ya no tienes que hacer nada: se publica uno cada día a las 19:00.

## Mantenimiento
- **Token:** vence a los 60 días. Genera uno nuevo en el panel de Meta (paso 2) antes del día ~55 y reemplaza el secreto `IG_TOKEN`.
- **Pausar:** Actions → el workflow → "…" → Disable workflow.
- **Cambiar fechas u horario:** edita `fecha` en `calendario.json` o el `cron` en el workflow.
- GitHub puede retrasar la ejecución programada unos minutos en horas de alta demanda.
