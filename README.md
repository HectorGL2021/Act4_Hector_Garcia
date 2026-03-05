# Actividad 4 - Aplicación Flask con Docker y CI/CD

**Autor:** Héctor García  
**Universidad:** UNIR

Aplicación web simple en Python con Flask, contenerizada con Docker y configurada con un pipeline de integración continua usando GitHub Actions.

---

## Estructura del Proyecto

```
Act4_Hector_Garcia/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline CI/CD con GitHub Actions
├── app.py                      # Aplicación Flask
├── test_app.py                 # Tests unitarios con pytest
├── requirements.txt            # Dependencias de Python
├── Dockerfile                  # Configuración del contenedor
├── .dockerignore               # Archivos excluidos del build Docker
└── README.md                   # Este archivo
```

---

## Requisitos Previos

- **Python 3.11+** instalado
- **Docker** instalado y en ejecución
- **Cuenta en Docker Hub** (para subir imágenes)
- **Cuenta en GitHub** (para CI/CD)

---

## Ejecución Local (sin Docker)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

---

## Ejecutar Tests

```bash
pip install -r requirements.txt
pytest test_app.py -v
```

---

## Uso con Docker

### Construir la imagen

```bash
docker build -t act4-flask-app .
```

### Ejecutar el contenedor

```bash
docker run -p 5000:5000 act4-flask-app
```

La aplicación estará disponible en: **http://localhost:5000**

### Detener el contenedor

```bash
docker ps                    # Obtener el CONTAINER ID
docker stop <CONTAINER_ID>   # Detener el contenedor
```

---

## Pipeline CI/CD con GitHub Actions

El pipeline (`.github/workflows/ci.yml`) se ejecuta automáticamente en cada push o pull request a la rama `main` y consta de 3 etapas:

| Etapa     | Descripción                                                   |
| --------- | ------------------------------------------------------------- |
| **Test**  | Instala dependencias y ejecuta los tests unitarios con pytest |
| **Build** | Construye la imagen Docker a partir del Dockerfile            |
| **Push**  | Sube la imagen a Docker Hub (solo en push a `main`)           |

### Configurar Secretos en GitHub

Para que el pipeline pueda subir imágenes a Docker Hub, hay que configurar los siguientes secretos en el repositorio:

1. Ve a **Settings** → **Secrets and variables** → **Actions** en tu repositorio de GitHub.
2. Añade los siguientes secretos:

| Secreto           | Valor                                         |
| ----------------- | --------------------------------------------- |
| `DOCKER_USERNAME` | Tu nombre de usuario de Docker Hub            |
| `DOCKER_PASSWORD` | Tu contraseña o token de acceso de Docker Hub |

### Verificar el Pipeline

1. Haz push del código a tu repositorio en GitHub.
2. Ve a la pestaña **Actions** del repositorio.
3. Verifica que las 3 etapas (Test, Build, Push) se completan correctamente.
4. Comprueba en **Docker Hub** que la imagen `act4-flask-app` se ha subido correctamente.

---

## Endpoints Disponibles

| Ruta      | Método | Descripción                       |
| --------- | ------ | --------------------------------- |
| `/`       | GET    | Mensaje de saludo en formato JSON |
| `/health` | GET    | Health check del servicio         |

### Ejemplo de respuesta en `/`

```json
{
  "mensaje": "¡Hola! Bienvenido a la aplicación Flask - Actividad 4",
  "autor": "Héctor García",
  "universidad": "UNIR",
  "status": "ok"
}
```
