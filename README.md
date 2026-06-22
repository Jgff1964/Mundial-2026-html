# Mundial 2026 · HTML/CSS/JS + backend

Versión reestructurada: HTML, CSS y JavaScript separados del backend Flask.

## Archivos

```txt
app.py
promiedos_client.py
bracket_logic.py
flags.py
renderer.py
templates/index.html
static/app.js
static/style.css
requirements.txt
Procfile
render.yaml
zonas_validadas.json
```

## Render

Build Command:

```txt
pip install -r requirements.txt
```

Start Command:

```txt
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 120
```

Usar `Manual Deploy → Clear build cache & deploy`.
