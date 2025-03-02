# sgil-monitoreo-service
Sistema de Gestión Integral de Logística y Comercio (SGIL) , monitoreo service


### Crear y activar el entorno virtual
```
make venv
```

### Instalar dependencias

```
make install
```

### Ejecutar el proyecto desde el folder raiz `sgil-monitoreo-service`
```
make run
```

### Ejecutar pruebas
```
make test
```

### Formatear el codigo con Black
```
make format
```

### Revisar errores de linting con Flake8:
```
make lint
```

### Eliminar entorno virtual y reinstalar todo 
```
make reset
```

### Estructura del proyecto


```
📂 sgil-monitoreo-service/       # Folder raiz
│
│── 📂 app/                    # Contiene los archivos principales del proyecto
│   │── 📂 models/             # Modelos SQLAlchemy
│   │── 📂 repositories/       # Lógica de acceso a BD
│   │── 📂 routers/            # Endpoints de la API
│   │── 📂 schemas/            # Esquemas Pydantic
│   │── 📂 services/           # Lógica de negocio
│   │── main.py                # Punto de entrada de FastAPI
│── 📂 postman                 # Colección del servicio de monitoreo
│── docker-compose.yml          # Archivo de configuración de Docker Compose
│── Dockerfile                  # Archivo de creación de imagen del contenedor
│── requirements.txt           # Dependencias del proyecto
│── .env                       # Variables de entorno (si usas PostgreSQL, MySQL, etc.)
│── alembic/                   # Migraciones de base de datos (opcional)
```


### Correr contenedor
 - ### Construir image de docker
    ```
        docker build --no-cache -t sgil-monitoreo-service .
    ```

 - ### Correr conteedor
    ```
        docker run -it --name sgil-monitoreo-service  sgil-monitoreo-service
    ```


## Docker compose

### 🚀 Ejecutar el proyecto desde docker-compose
```
docker-compose up --build
```

### Eliminar volúmenes y contenedores antiguos 
```
docker system prune
```

### Eliminar los contenedores & volumenes
```
docker-compose down -v
```
