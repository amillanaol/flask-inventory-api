# Flujo de Códigos de Respuesta HTTP — Flask Inventory API

Diagrama de decisión que muestra cómo la API determina el código de respuesta HTTP para cada request, basado en la lógica real de los endpoints.

---

## Diagrama General

```mermaid
flowchart TD
    A([Request Received]) --> B{¿Problema con\nel request?}

    B -->|Sí| C{¿JSON body\npresente?}
    B -->|No| D{¿Error\nen servidor?}

    C -->|No| E[400 Bad Request\nNo data provided]
    C -->|Sí| F{¿Campos\nrequeridos\ncompletos?}

    F -->|No| G[400 Bad Request\nMissing field: &lt;campo&gt;]
    F -->|Sí| H{¿Recurso\nexiste en DB?}

    H -->|No — GET/PUT/DELETE| I[404 Not Found\nProduct / Category not found]
    H -->|No — POST duplicate| J[400 Bad Request\nSKU / Category already exists]
    H -->|Sí| K{¿Regla de\nnegocio OK?}

    K -->|No| L[400 Bad Request\nRegla de negocio violada]
    K -->|Sí — POST| M[201 Created\nRecurso creado]
    K -->|Sí — GET/PUT/DELETE| N[200 OK\nOperación exitosa]

    D -->|Sí| O[500 Internal Server Error\nError no controlado]
    D -->|No| N
```

---

## Reglas de Negocio que Devuelven 400

Cada endpoint tiene validaciones específicas adicionales más allá de los campos requeridos:

| Endpoint | Condición | Mensaje de error |
|---|---|---|
| `POST /api/products` | SKU ya registrado | `SKU already exists` |
| `PUT /api/products/<id>` | Nuevo SKU ya pertenece a otro producto | `SKU already exists` |
| `POST /api/categories` | Nombre de categoría ya registrado | `Category name already exists` |
| `PUT /api/categories/<id>` | Nuevo nombre ya pertenece a otra categoría | `Category name already exists` |
| `DELETE /api/categories/<id>` | Categoría tiene productos asociados | `Cannot delete category with associated products` |
| `POST /api/movements` | `movement_type` no es `entry` ni `exit` | `Invalid movement_type. Must be "entry" or "exit"` |
| `POST /api/movements` | Tipo `exit` con stock insuficiente | `Insufficient stock. Current stock: <n>` |

---

## Flujo por Endpoint

### Products `/api/products`

```mermaid
flowchart TD
    subgraph GET_ALL["GET /api/products"]
        G1([Request]) --> G2[Consulta todos\nlos productos] --> G3[200 OK\nArray JSON]
    end

    subgraph POST["POST /api/products"]
        P1([Request]) --> P2{¿Body JSON?}
        P2 -->|No| P3[400 No data provided]
        P2 -->|Sí| P4{¿Campos requeridos?\nsku, name, price,\nstock, min_stock}
        P4 -->|No| P5[400 Missing field]
        P4 -->|Sí| P6{¿SKU\nduplicado?}
        P6 -->|Sí| P7[400 SKU already exists]
        P6 -->|No| P8[Inserta en DB] --> P9[201 Created]
    end

    subgraph GET_ONE["GET /api/products/:id"]
        G4([Request]) --> G5{¿Producto\nexiste?}
        G5 -->|No| G6[404 Not Found]
        G5 -->|Sí| G7[200 OK\nObjeto JSON]
    end

    subgraph PUT["PUT /api/products/:id"]
        U1([Request]) --> U2{¿Producto\nexiste?}
        U2 -->|No| U3[404 Not Found]
        U2 -->|Sí| U4{¿Body JSON?}
        U4 -->|No| U5[400 No data provided]
        U4 -->|Sí| U6{¿SKU nuevo\nduplicado?}
        U6 -->|Sí| U7[400 SKU already exists]
        U6 -->|No| U8[Actualiza en DB] --> U9[200 OK]
    end

    subgraph DELETE["DELETE /api/products/:id"]
        D1([Request]) --> D2{¿Producto\nexiste?}
        D2 -->|No| D3[404 Not Found]
        D2 -->|Sí| D4[Elimina de DB] --> D5[200 OK\nProduct deleted]
    end
```

---

### Categories `/api/categories`

```mermaid
flowchart TD
    subgraph POST["POST /api/categories"]
        P1([Request]) --> P2{¿Body JSON?}
        P2 -->|No| P3[400 No data provided]
        P2 -->|Sí| P4{¿Campo name\npresente?}
        P4 -->|No| P5[400 Missing field: name]
        P4 -->|Sí| P6{¿Nombre\nduplicado?}
        P6 -->|Sí| P7[400 Category name\nalready exists]
        P6 -->|No| P8[Inserta en DB] --> P9[201 Created]
    end

    subgraph DELETE["DELETE /api/categories/:id"]
        D1([Request]) --> D2{¿Categoría\nexiste?}
        D2 -->|No| D3[404 Not Found]
        D2 -->|Sí| D4{¿Tiene productos\nasociados?}
        D4 -->|Sí| D5[400 Cannot delete\ncategory with products]
        D4 -->|No| D6[Elimina de DB] --> D7[200 OK]
    end
```

---

### Movements `/api/movements`

```mermaid
flowchart TD
    P1([POST /api/movements]) --> P2{¿Body JSON?}
    P2 -->|No| P3[400 No data provided]
    P2 -->|Sí| P4{¿Campos requeridos?\nproduct_id, movement_type,\nquantity}
    P4 -->|No| P5[400 Missing field]
    P4 -->|Sí| P6{¿movement_type es\nentry o exit?}
    P6 -->|No| P7[400 Invalid movement_type]
    P6 -->|Sí| P8{¿Producto\nexiste?}
    P8 -->|No| P9[404 Product not found]
    P8 -->|Sí| P10{¿Es exit con\nstock insuficiente?}
    P10 -->|Sí| P11[400 Insufficient stock]
    P10 -->|No| P12[Registra movimiento\nActualiza stock] --> P13[201 Created]
```

---

## Resumen de Códigos

| Código | Descripción | Cuándo ocurre en esta API |
|---|---|---|
| **200 OK** | Éxito | GET (todos o por ID), PUT, DELETE exitoso |
| **201 Created** | Recurso creado | POST exitoso en products, categories, movements |
| **400 Bad Request** | Error del cliente | Body ausente, campo faltante, duplicado, regla de negocio violada |
| **404 Not Found** | Recurso no encontrado | ID inexistente en products, categories o movements |
| **500 Internal Server Error** | Error del servidor | Excepción no controlada (BD caída, error inesperado) |
