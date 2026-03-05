# Actividad 4 - Aplicación Flask con Docker y CI/CD

**Autor:** Héctor García  
**Universidad:** UNIR  
**Asignatura:** DevOps  
**Fecha:** Marzo 2026

---

## 1. Descripción del Proyecto

Este proyecto consiste en el desarrollo de una aplicación web simple utilizando el framework Flask de Python, contenerizada mediante Docker y automatizada con un pipeline de integración continua (CI/CD) mediante GitHub Actions.

La aplicación ofrece un endpoint principal que responde con un mensaje de saludo en formato JSON cuando se accede a la ruta raíz (`/`). Además, se incluye un endpoint de health check (`/health`) que permite verificar el estado del servicio de forma rápida y automatizada.

El objetivo principal de esta actividad es demostrar el uso de tecnologías de contenerización y automatización de despliegues, integrando buenas prácticas de desarrollo como las pruebas unitarias automatizadas con pytest y la integración continua mediante GitHub Actions.

---

## 2. Estructura del Proyecto

```
Act4_Hector_Garcia/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline CI/CD con GitHub Actions
├── app.py                      # Aplicación Flask (código principal)
├── test_app.py                 # Tests unitarios con pytest
├── requirements.txt            # Dependencias de Python
├── Dockerfile                  # Configuración del contenedor Docker
├── .dockerignore               # Archivos excluidos del build Docker
├── .gitignore                  # Archivos excluidos del control de versiones
└── README.md                   # Documentación del proyecto (este archivo)
```

---

## 3. Tecnologías Utilizadas

| Tecnología     | Versión | Propósito                                |
| -------------- | ------- | ---------------------------------------- |
| Python         | 3.11    | Lenguaje de programación principal       |
| Flask          | 3.1.0   | Framework web para crear la API          |
| pytest         | 8.3.4   | Framework de pruebas unitarias           |
| Docker         | Latest  | Contenerización de la aplicación         |
| GitHub Actions | N/A     | Pipeline de integración continua (CI/CD) |
| Docker Hub     | N/A     | Registro de imágenes Docker              |

---

## 4. Requisitos Previos

Para ejecutar este proyecto correctamente, es necesario tener instalados los siguientes componentes:

- **Python 3.11 o superior**: Necesario para ejecutar la aplicación de forma local.
- **pip**: Gestor de paquetes de Python para instalar las dependencias.
- **Docker**: Necesario para construir y ejecutar el contenedor de la aplicación.
- **Cuenta en Docker Hub**: Para subir las imágenes Docker generadas por el pipeline.
- **Cuenta en GitHub**: Para alojar el repositorio y ejecutar el pipeline de CI/CD.

---

## 5. Instalación y Ejecución Local (sin Docker)

### 5.1 Clonar el repositorio

```bash
git clone https://github.com/HectorGL2021/Act4_Hector_Garcia.git
cd Act4_Hector_Garcia
```

### 5.2 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5.3 Ejecutar la aplicación

```bash
python app.py
```

La aplicación se iniciará y estará disponible en la dirección: **http://localhost:5000**

### 5.4 Verificar el funcionamiento

Abre un navegador o utiliza curl para comprobar que la aplicación responde correctamente:

```bash
curl http://localhost:5000
```

La respuesta esperada será:

```json
{
  "mensaje": "¡Hola! Bienvenido a la aplicación Flask - Actividad 4",
  "autor": "Héctor García",
  "universidad": "UNIR",
  "status": "ok"
}
```

---

## 6. Ejecución de Pruebas Unitarias

El proyecto incluye un conjunto completo de pruebas unitarias escritas con pytest que verifican el correcto funcionamiento de la aplicación. Las pruebas cubren los siguientes aspectos:

| Test                      | Descripción                                          |
| ------------------------- | ---------------------------------------------------- |
| `test_index_status_code`  | Verifica que la ruta `/` devuelve HTTP 200           |
| `test_index_content_type` | Verifica que la respuesta es de tipo JSON            |
| `test_index_message`      | Verifica que el cuerpo contiene el mensaje de saludo |
| `test_index_autor`        | Verifica que el campo `autor` es correcto            |
| `test_index_status_field` | Verifica que el campo `status` es `ok`               |
| `test_health_endpoint`    | Verifica que `/health` responde correctamente        |
| `test_not_found`          | Verifica que rutas inexistentes devuelven 404        |

### Ejecutar los tests localmente

```bash
pytest test_app.py -v
```

Salida esperada:

```
test_app.py::test_index_status_code   PASSED
test_app.py::test_index_content_type  PASSED
test_app.py::test_index_message       PASSED
test_app.py::test_index_autor         PASSED
test_app.py::test_index_status_field  PASSED
test_app.py::test_health_endpoint     PASSED
test_app.py::test_not_found           PASSED

==================== 7 passed ====================
```

---

## 7. Uso con Docker

### 7.1 Descripción del Dockerfile

El archivo `Dockerfile` define cómo se construye la imagen del contenedor. A continuación se describe cada instrucción:

| Instrucción               | Descripción                                                        |
| ------------------------- | ------------------------------------------------------------------ |
| `FROM python:3.11-slim`   | Utiliza la imagen oficial de Python 3.11 en su versión slim        |
| `WORKDIR /app`            | Establece `/app` como directorio de trabajo dentro del contenedor  |
| `COPY requirements.txt`   | Copia el archivo de dependencias al contenedor                     |
| `RUN pip install`         | Instala las dependencias de Python sin caché para optimizar tamaño |
| `COPY . .`                | Copia todo el código fuente de la aplicación al contenedor         |
| `EXPOSE 5000`             | Expone el puerto 5000, que es donde Flask escucha las peticiones   |
| `CMD ["python","app.py"]` | Define el comando que se ejecuta al iniciar el contenedor          |

### 7.2 Construir la imagen

```bash
docker build -t act4-flask-app .
```

### 7.3 Ejecutar el contenedor

```bash
docker run -p 5000:5000 act4-flask-app
```

La aplicación estará disponible en: **http://localhost:5000**

### 7.4 Ejecutar los tests dentro del contenedor

```bash
docker run --rm act4-flask-app python -m pytest test_app.py -v
```

### 7.5 Detener el contenedor

```bash
docker ps                    # Obtener el CONTAINER ID
docker stop <CONTAINER_ID>   # Detener el contenedor
```

---

## 8. Pipeline CI/CD con GitHub Actions

### 8.1 Descripción General

El pipeline de integración continua se define en el archivo `.github/workflows/ci.yml` y se ejecuta automáticamente en cada push o pull request a la rama `main`. El pipeline consta de tres etapas secuenciales que garantizan la calidad del código antes de subir la imagen al registro de contenedores.

### 8.2 Etapas del Pipeline

| Etapa     | Nombre del Job                  | Descripción                                                            |
| --------- | ------------------------------- | ---------------------------------------------------------------------- |
| **Test**  | Ejecutar Tests                  | Instala Python 3.11, las dependencias y ejecuta pytest                 |
| **Build** | Construir Imagen Docker y Tests | Construye la imagen Docker y ejecuta las pruebas dentro del contenedor |
| **Push**  | Subir Imagen a Docker Hub       | Inicia sesión en Docker Hub, construye, etiqueta y sube la imagen      |

Las etapas se ejecutan de forma secuencial: la etapa de **Build** solo se ejecuta si la etapa de **Test** finaliza con éxito, y la etapa de **Push** solo se ejecuta si la etapa de **Build** finaliza correctamente. Además, la etapa de **Push** solo se activa en pushes directos a la rama `main`, no en pull requests.

### 8.3 Configuración de Secretos en GitHub

Para que la etapa de Push funcione correctamente, es necesario configurar los siguientes secretos en el repositorio de GitHub:

1. Navega a tu repositorio en GitHub.
2. Ve a **Settings** → **Secrets and variables** → **Actions**.
3. Haz clic en **New repository secret** y añade los siguientes secretos:

| Nombre del Secreto | Valor                                         |
| ------------------ | --------------------------------------------- |
| `DOCKER_USERNAME`  | Tu nombre de usuario de Docker Hub            |
| `DOCKER_PASSWORD`  | Tu contraseña o token de acceso de Docker Hub |

Es recomendable utilizar un **Access Token** de Docker Hub en lugar de la contraseña directa. Para generar un token, accede a Docker Hub → **Account Settings** → **Security** → **New Access Token**.

### 8.4 Verificación del Pipeline

Una vez configurados los secretos y subido el código al repositorio:

1. Ve a la pestaña **Actions** del repositorio en GitHub.
2. Verifica que el workflow **CI/CD Pipeline - Flask Docker** se ejecuta correctamente.
3. Confirma que las tres etapas (Test, Build, Push) se completan con un check verde.
4. Accede a **Docker Hub** y comprueba que la imagen `act4-flask-app` está disponible con las etiquetas `latest` y el hash del commit correspondiente.

---

## 9. Endpoints Disponibles

| Ruta      | Método | Descripción                                    |
| --------- | ------ | ---------------------------------------------- |
| `/`       | GET    | Devuelve un mensaje de saludo en formato JSON  |
| `/health` | GET    | Devuelve el estado del servicio (health check) |

### Ejemplo de respuesta en `/`

```json
{
  "mensaje": "¡Hola! Bienvenido a la aplicación Flask - Actividad 4",
  "autor": "Héctor García",
  "universidad": "UNIR",
  "status": "ok"
}
```

### Ejemplo de respuesta en `/health`

```json
{
  "status": "healthy"
}
```

---

## 10. Imagen en Docker Hub

Una vez que el pipeline se ejecuta correctamente, la imagen Docker estará disponible en Docker Hub. Para descargarla y ejecutarla desde cualquier máquina con Docker instalado:

```bash
docker pull <tu-usuario>/act4-flask-app:latest
docker run -p 5000:5000 <tu-usuario>/act4-flask-app:latest
```

Esto permite desplegar la aplicación en cualquier entorno que disponga de Docker, sin necesidad de instalar Python ni las dependencias de forma manual, demostrando una de las principales ventajas de la contenerización.
