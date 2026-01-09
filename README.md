# Repo para EU - DevOps & Cloud – UNIR

Este repositorio incluye un proyecto sencillo para demostrar los conceptos de **pruebas unitarias**, **pruebas de servicio**, **uso de WireMock** y **ejecución de pipelines con Jenkins**.

El objetivo es que el alumno entienda estos conceptos, por lo que el código y la estructura del proyecto son **deliberadamente simples**. Este proyecto sirve también como **fuente de código para el pipeline de Jenkins** utilizado en la práctica.

---

## Entorno virtual

Se utiliza un **entorno virtual de Python** para evitar instalar dependencias de forma global en el sistema y mantener el proyecto **aislado** de otros desarrollos.

Esto permite:

* No contaminar el Python del sistema
* Reproducir el entorno de forma consistente
* Eliminar el entorno sin efectos colaterales

### Crear el entorno virtual

```bash
python3 -m venv .venv
```

### Activar el entorno virtual

```bash
source .venv/bin/activate
```

---

## Variables de entorno (.envrc)

Para evitar exportar variables manualmente en cada sesión, se utiliza un fichero **.envrc** (con `direnv`) donde se definen las variables necesarias para el proyecto.

Este fichero **solo aplica dentro del directorio del proyecto** y no afecta a otros entornos.

### Crear el fichero `.envrc`

```bash
cat <<EOF > .envrc
source .venv/bin/activate
export PYTHONPATH=$(pwd)
export FLASK_APP=app/api.py
EOF
```

A continuación, permitir su uso:

```bash
direnv allow
```

---

## Instalación de dependencias

Las dependencias del proyecto están definidas en el fichero **requirements.txt**.

El flujo correcto es:

1. Clonar el repositorio
2. Crear el entorno virtual
3. Activar el entorno virtual
4. Instalar dependencias desde `requirements.txt`

```bash
pip install -r requirements.txt
```

---

## Ejecución del código

Ejecutar la aplicación de ejemplo:

```bash
python3 ./app/calc.py
```

---

## Ejecución de tests

### Tests unitarios

```bash
pytest ./test/unit/
```

### Tests de integración / servicio

Para los tests de integración es necesario tener el servicio Flask levantado:

```bash
flask run
```

Una vez levantado el servicio:

```bash
pytest ./test/rest/
```
