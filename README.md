# Generador de Documentación Administrativa - DPA-SsFyCP-MP

App en Streamlit para generar Notas, Memorándums y Pases con formato oficial (vista previa + exportación a PDF).

## Archivos
- `generador_documentos.py` — archivo principal de la app
- `requirements.txt` — dependencias (`streamlit`, `fpdf2`)
- `.gitignore` — archivos a excluir del repo

## Deploy en Streamlit Cloud

1. Creá un repositorio en GitHub (por ejemplo `generador-documentos-chubut`) y subí estos 3 archivos a la rama `main`.
   - Si preferís hacerlo desde la terminal:
     ```
     git init
     git add generador_documentos.py requirements.txt .gitignore README.md
     git commit -m "Primera versión del generador de documentos"
     git branch -M main
     git remote add origin https://github.com/TU_USUARIO/generador-documentos-chubut.git
     git push -u origin main
     ```
2. Andá a [share.streamlit.io](https://share.streamlit.io) e iniciá sesión con tu cuenta de GitHub.
3. Click en **"New app"**.
4. Elegí el repositorio, la rama `main` y como **Main file path** poné `generador_documentos.py`.
5. Click en **Deploy**. Streamlit Cloud instala `requirements.txt` automáticamente y te da una URL tipo `tu-app.streamlit.app`.

## Actualizaciones
Cada `git push` a `main` redeploya la app automáticamente.
