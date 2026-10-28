# TechStore - Desarrollo de Componente de Negocio (Actividad 4)

Componente backend de comercio electrónico desarrollado bajo los principios de **Domain-Driven Design (DDD)**, utilizando **FastAPI**, **Uvicorn** y **Pytest**. Modela el ciclo de vida completo de un pedido con validación estricta de reglas de negocio, transiciones de estado y eventos de dominio.

---

## 🛠️ Instalación y Configuración del Entorno

Sigue estos pasos para configurar tu entorno local:

1. **Abrir la carpeta del proyecto en la terminal:**
   ```bash
   cd "Logica de Negocios"
   ```

2. **Crear y activar un entorno virtual de Python:**
   * **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   * **Mac / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar las dependencias:**
   Asegúrate de instalar FastAPI, Uvicorn, Pytest y Httpx:
   ```bash
   pip install fastapi uvicorn pytest httpx
   ```

---

## 🚀 Guía de Ejecución

### 1. Carga de Datos Iniciales (CSV)
Para procesar y verificar los registros iniciales desde los archivos de datos (`clientes.csv`, `pedidos.csv`, `productos.csv`, etc.), ejecuta:
```bash
python cargar_csv.py
```

### 2. Ejecutar Pruebas Automatizadas (`Pytest`)
Para comprobar que todas las reglas de negocio, restricciones de límites y excepciones funcionan correctamente, ejecuta la suite de pruebas:
```bash
python -m pytest -q
```

### 3. Ejecutar el Servidor de la API REST
Inicia el servidor de desarrollo con Uvicorn:
```bash
uvicorn app.api:app --reload
```
Una vez iniciado, abre tu navegador e ingresa a la documentación interactiva en Swagger:
`http://127.0.0.1:8000/docs`

---

## 📋 Reglas de Negocio y Máquina de Estados

Los pedidos siguen un ciclo de vida estricto controlado por el dominio:

* **`DRAFT` (Borrador):** Estado inicial de toda orden. Se pueden agregar o modificar artículos. La cantidad total no puede exceder las **20 unidades**.
* **`CONFIRMED` (Confirmado):** Activado mediante `confirm()`. Exige que el pedido contenga al menos un artículo y que el cliente esté activo. Emite el evento `OrderConfirmed`.
* **`SHIPPED` (Enviado):** Activado mediante `ship(tracking_number)`. Requiere que el pedido esté confirmado y que se proporcione obligatoriamente un número de guía válido. Emite el evento `OrderShipped`.
* **`CANCELLED` (Cancelado):** Activado mediante `cancel(reason)`. Permite abortar un pedido confirmado antes de que sea enviado. Emite el evento `OrderCancelled`.
* **`DELIVERED` / `RETURNED`:** Estados finales alcanzados desde `SHIPPED` mediante `deliver()` o `return_order()`. Emiten sus respectivos eventos de dominio.

---

## 🔌 Resumen de Endpoints de la API

| Método | Endpoint | Descripción | Parámetros / Cuerpo de la Petición |
| :--- | :--- | :--- | :--- |
| **GET** | `/orders/{order_id}` | Consulta el estado actual y detalles de un pedido. | `order_id` (Ruta) |
| **POST** | `/orders/{order_id}/confirm` | Confirma el pedido si cumple con las reglas de negocio. | `order_id` (Ruta) |
| **POST** | `/orders/{order_id}/ship` | Cambia el pedido a enviado registrando la guía. | `order_id` (Ruta), `tracking_number` (JSON) |
| **POST** | `/orders/{order_id}/cancel` | Cancela el pedido especificando un motivo. | `order_id` (Ruta), `reason` (JSON) |