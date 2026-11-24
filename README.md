# Evaluación 3 – Programación Web (Flask)

Aplicación web en Python con Flask que tiene un menú principal con dos botones:

- **Ejercicio 1:** recibe 3 notas (10 a 70) y una asistencia (0 a 100 %), calcula el promedio y muestra **APROBADO** si el promedio es ≥ 40 y la asistencia es ≥ 75 %; en caso contrario, **REPROBADO**.
- **Ejercicio 2:** recibe 3 nombres diferentes y muestra el nombre con más caracteres y su cantidad de caracteres.

## Estructura del proyecto

```
EV3_Flask/
├── main.py               # Rutas y lógica en Python
├── requirements.txt      # Dependencias (pip)
├── static/
│   └── css/
│       └── estilos.css   # Estilos cargados en base.html
└── templates/
    ├── base.html         # Plantilla base con bloques
    ├── index.html        # Menú principal
    ├── ejercicio1.html   # Formulario de notas
    ├── ejercicio2.html   # Formulario de nombres
    └── 404.html          # Página de error
```

## Rutas

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Menú principal |
| `/inicio` | GET | Redirige al menú principal |
| `/ejercicio1` | GET, POST | Formulario de notas |
| `/ejercicio2` | GET, POST | Formulario de nombres |
| `/ejercicio/<numero>` | GET | Ruta con parámetro: redirige al ejercicio 1 o 2; otro número aborta con 404 |
| `/historial/limpiar` | POST | Borra los registros guardados en memoria |

## Cómo ejecutar (Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Luego abrir en el navegador: http://127.0.0.1:5000
