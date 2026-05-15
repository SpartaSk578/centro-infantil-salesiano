# Centro Infantil Don Bosquito - Sistema de Gestión

Sistema web Django para la gestión del Centro Infantil Salesiano.

## Estructura del Proyecto

```
centro_infantil_limpio/
├── centro_infantil_config/   # Configuración principal Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── usuarios/                 # App: autenticación y roles
├── beneficiarios/            # App: tutores y pre-inscripciones
├── ninos/                    # App: niños + exportar Excel/PDF
├── grupos/                   # App: salas/grupos
├── asistencia/               # App: control de asistencia
├── evaluaciones/             # App: evaluaciones
├── templates/                # Plantillas HTML
├── static/                   # Archivos estáticos (imágenes, etc.)
├── manage.py
├── requirements.txt
└── render.yaml               # Configuración para Render
```

## Despliegue en Render

### Paso a Paso

1. **Subir a GitHub**
   ```bash
   git init
   git add .
   git commit -m "Proyecto limpio y ordenado"
   git remote add origin https://github.com/TU_USUARIO/centro-infantil-salesiano.git
   git push -u origin main
   ```

2. **En Render (render.com)**
   - Ir a Dashboard → New → Web Service
   - Conectar tu repositorio de GitHub
   - Render detecta automáticamente el `render.yaml`
   - Si no usa render.yaml, configurar manualmente:
     - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
     - **Start Command:** `gunicorn centro_infantil_config.wsgi:application`
     - **Root Directory:** *(dejar vacío, el manage.py está en la raíz)*

3. **Variables de entorno en Render**
   - `DATABASE_URL` → URL de tu base de datos PostgreSQL (Render la genera automáticamente si usas render.yaml)
   - `SECRET_KEY` → Clave secreta segura (Render puede generarla automáticamente)
   - `DEBUG` → `False`

4. **Base de datos**
   - Render crea la base de datos PostgreSQL gratuita automáticamente con el render.yaml
   - Las migraciones se ejecutan en el Build Command

## Ejecución Local

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Funcionalidades

- ✅ Gestión de niños (CRUD)
- ✅ Exportar lista a **Excel** (formato OFPROBOL)
- ✅ Exportar lista a **PDF** (requiere weasyprint)
- ✅ Gestión de tutores/beneficiarios
- ✅ Pre-inscripción pública
- ✅ Control de asistencia
- ✅ Evaluaciones
- ✅ Roles de usuario (Admin, Director, etc.)
