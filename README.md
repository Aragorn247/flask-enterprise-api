# Enterprise Python REST API Boilerplate

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Flask-3.1-green.svg)](https://flask.palletsprojects.com/)
[![ORM](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![Tests](https://img.shields.io/badge/Tests-Pytest%20Passed-brightgreen.svg)]()

Producción-ready RESTful API diseñada bajo arquitectura modular en capas, autenticación sin estado mediante JWT, validación de esquemas estricta y suite de pruebas automatizadas.

## 🏗️ Arquitectura y Patrones

- **Application Factory Pattern**: Desacoplamiento de la instanciación de la app para facilitar entornos de testing e integración continua.
- **Stateless Authentication**: Firma y verificación de tokens JWT (HS256) mediante decoradores personalizados.
- **ORM & Migrations**: Persistence Layer gestionado con SQLAlchemy 2.0 y control de versiones de esquema mediante Flask-Migrate (Alembic).
- **Data Validation**: Marshmallow Schemas para sanitización y serialización estricta de JSONs de entrada/salida.
- **Global Error Handling**: Intercepción centralizada de excepciones para respuestas HTTP uniformes en formato JSON.

## 🚀 Endpoints de la API

| Método | Endpoint | Protección | Descripción |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Pública | Registro de nuevos usuarios con hash seguro |
| `POST` | `/api/v1/auth/login` | Pública | Autenticación y emisión del Bearer Token JWT |
| `GET` | `/api/v1/resources` | JWT | Lista de recursos del usuario autenticado |
| `POST` | `/api/v1/resources` | JWT | Creación de recurso con validación Marshmallow |

## 🧪 Pruebas Automatizadas (Testing)

El proyecto incluye una suite de pruebas de integración con `pytest` que utiliza una base de datos SQLite en memoria isolated per-test:

```bash
python -m pytest