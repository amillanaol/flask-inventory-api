# Flask Inventory API

Sistema de gestión de inventario desarrollado con Flask, PostgreSQL y Bootstrap 5.

## Características

- **Gestión de Productos**: CRUD completo con SKU único, precios, stock y alertas de bajo inventario
- **Gestión de Categorías**: Organización de productos por categorías
- **Movimientos de Inventario**: Registro de entradas y salidas con actualización automática de stock
- **Panel de Dashboard**: Métricas en tiempo real del inventario
- **API REST**: Endpoints JSON para integración externa
- **Autenticación**: Sistema de login/registro con Flask-Login

## Stack Tecnológico

- **Backend**: Flask 3.0 + Python 3.11
- **Base de Datos**: PostgreSQL + SQLAlchemy + Flask-Migrate
- **Autenticación**: Flask-Login + Flask-WTF
- **Frontend**: Bootstrap 5 (CDN) + Jinja2
- **Contenedores**: Docker Compose

## Estructura del Proyecto

```
flask-inventory-api/
├── app/
│   ├── blueprints/        # Blueprints de la aplicación
│   │   ├── api/          # API REST JSON
│   │   ├── auth/         # Autenticación
│   │   ├── categories/   # Gestión de categorías
│   │   ├── dashboard/    # Panel principal
│   │   ├── movements/    # Movimientos de inventario
│   │   └── products/     # Gestión de productos
│   ├── forms/            # Formularios WTForms
│   ├── models/           # Modelos SQLAlchemy
│   ├── templates/        # Plantillas Jinja2
│   ├── config.py         # Configuración
│   ├── extensions.py     # Extensiones Flask
│   └── __init__.py       # Factory de la app
├── docker-compose.yml    # Orquestación de servicios
├── Dockerfile            # Imagen de la aplicación
├── requirements.txt      # Dependencias Python
├── run.py               # Punto de entrada
└── .env.example         # Variables de entorno ejemplo
```

## Modelos de Datos

### User
- `id`: Integer (PK)
- `username`: String (unique)
- `email`: String (unique)
- `password_hash`: String
- `created_at`: DateTime

### Category
- `id`: Integer (PK)
- `name`: String (unique)
- `description`: Text
- `created_at`: DateTime

### Product
- `id`: Integer (PK)
- `sku`: String (unique)
- `name`: String
- `description`: Text
- `price`: Numeric(10,2)
- `stock`: Integer
- `min_stock`: Integer
- `category_id`: Integer (FK)
- `is_active`: Boolean
- `created_at`: DateTime
- `updated_at`: DateTime

### Movement
- `id`: Integer (PK)
- `product_id`: Integer (FK)
- `user_id`: Integer (FK)
- `movement_type`: String ('entry'/'exit')
- `quantity`: Integer
- `notes`: Text
- `created_at`: DateTime

## Endpoints Web (HTML)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Dashboard |
| GET/POST | `/auth/login` | Iniciar sesión |
| GET/POST | `/auth/register` | Registrarse |
| GET | `/auth/logout` | Cerrar sesión |
| GET | `/products` | Listar productos |
| GET/POST | `/products/create` | Crear producto |
| GET/POST | `/products/<id>/edit` | Editar producto |
| POST | `/products/<id>/delete` | Eliminar producto |
| GET | `/categories` | Listar categorías |
| GET/POST | `/categories/create` | Crear categoría |
| GET/POST | `/categories/<id>/edit` | Editar categoría |
| POST | `/categories/<id>/delete` | Eliminar categoría |
| GET | `/movements` | Listar movimientos |
| GET/POST | `/movements/create` | Registrar movimiento |

## Endpoints API REST (JSON)

### Productos
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/products` | Listar todos los productos |
| POST | `/api/products` | Crear producto |
| GET | `/api/products/<id>` | Obtener producto |
| PUT | `/api/products/<id>` | Actualizar producto |
| DELETE | `/api/products/<id>` | Eliminar producto |

### Categorías
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/categories` | Listar todas las categorías |
| POST | `/api/categories` | Crear categoría |
| GET | `/api/categories/<id>` | Obtener categoría |
| PUT | `/api/categories/<id>` | Actualizar categoría |
| DELETE | `/api/categories/<id>` | Eliminar categoría |

### Movimientos
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/movements` | Listar todos los movimientos |
| POST | `/api/movements` | Crear movimiento |

## Configuración

Copiar `.env.example` a `.env` y configurar:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/inventory_db
```

## Setup Local (Sin Docker)

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tu configuración
```

4. Crear base de datos:
```bash
flask create-db
```

5. Cargar datos de ejemplo:
```bash
flask seed-db
```

6. Ejecutar servidor:
```bash
python run.py
```

## Setup con Docker Compose

1. Construir y ejecutar:
```bash
docker-compose up --build
```

2. La aplicación estará disponible en `http://localhost:5000`

3. Para populate la base de datos:
```bash
docker-compose exec app flask seed-db
```

## Usuario de Prueba

- **Usuario**: admin
- **Contraseña**: admin123

## Comandos CLI

```bash
flask seed-db    # Cargar datos de ejemplo
flask create-db  # Crear tablas de la base de datos
```

## Validaciones

- Productos: SKU único, precio y stock no negativos
- Categorías: Nombre único
- Movimientos: No permiten salidas mayores al stock disponible
- Alertas: Productos con stock <= min_stock se marcan visualmente

## Licencia

MIT
