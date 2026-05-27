# TFG informática 2025-2026

## Descripción
Este repositorio contiene los *datasets* y el código necesario para realizar un análisis predictivo de la generación de startups en España. 

La totalidad de las fuentes consultadas se encuentran resumidas en el archivo [fuentes.yaml](./data/fuentes.yaml). 

El código se organiza en módulos de Python y notebooks de Jupyter.

## Requisitos

- Python 3.12
- [uv](https://github.com/astral-sh/uv), como gestor de dependencias y entorno virtual.
- [google-chrome-canary](https://www.google.com/chrome/canary/), versiones superiores a la 148.
- [vscode](https://code.visualstudio.com/) o cualquier otro editor de texto que soporte las extensiones del archivo [extensions.json](./.vscode/extensions.json)
- API key de [google maps](https://developers.google.com/maps/documentation), el coste será 0 porque no se excederá el límite gratuito, pero es necesaria para obtener coordenadas geográficas a partir de direcciones.
- VPN (Opcional, pero recomendado para evitar bloqueos al scrapear datos)

### Instalación de dependencias

```bash
uv sync && uv pip install -e .
```
## Datos

Los datos del proyecto se organizan en tres capas:

```yaml
datos:
  - capa: bronze
    descripcion: Datos brutos descargados de las fuentes originales, sin apenas transformación.
  - capa: silver
    descripcion: Datos limpios, normalizados y preparados para análisis intermedio.
  - capa: gold
    descripcion: Tablas finales agregadas y listas para análisis, visualización o modelado.
  - inventario: data/fuentes.yaml
    descripcion: Catálogo de fuentes, formatos y correspondencia con los archivos del repositorio.
```


## Modulos custom

Resumen de los módulos propios del proyecto y su responsabilidad principal.

```yaml
modulos:
  - ruta: src/shared
    descripcion: Utilidades comunes del proyecto, como normalización de texto, `slugify`, persistencia de archivos y helpers reutilizables.
  - ruta: src/geocoders
    descripcion: Integraciones para geocodificación y obtención de coordenadas, polígonos y metadatos geográficos.
  - ruta: src/scrapers
    descripcion: Scrapers y adaptadores para extraer datos de las fuentes externas consultadas.
  - ruta: src/processing
    descripcion: Parsers y transformaciones para limpiar, normalizar y reestructurar los ficheros de `data/`.
  - ruta: src/analysis
    descripcion: Consultas SQL, métricas agregadas y funciones de visualización para el análisis exploratorio.
```

## Notebooks
Los notebooks de Jupyter se encuentran en `notebooks/` y reflejan el flujo principal del proyecto: extracción, transformación, análisis exploratorio, modelado y cartografía.

```yaml
notebooks:
  - ruta: notebooks/01_extract.ipynb
    descripcion: Extracción de datos desde las fuentes originales y carga inicial de los ficheros en `data/bronze`.
  - ruta: notebooks/02_transform.ipynb
    descripcion: Limpieza, normalización y generación de tablas intermedias en `data/silver`.
  - ruta: notebooks/03_01_sample.ipynb
    descripcion: Exploración inicial de las muestras de empresas y validación de la estructura de los datos.
  - ruta: notebooks/03_02_workforce.ipynb
    descripcion: Análisis de afiliación a la seguridad social por territorio.
  - ruta: notebooks/03_03_graduates.ipynb
    descripcion: Análisis de egresados universitarios y su relación territorial.
  - ruta: notebooks/03_04_network.ipynb
    descripcion: Análisis de red y relaciones entre entidades, centros y nodos del ecosistema.
  - ruta: notebooks/03_05_RECIDI.ipynb
    descripcion: Exploración de datos de la RECIDI y su distribución territorial.
  - ruta: notebooks/04_model.ipynb
    descripcion: Construcción y evaluación de modelos predictivos para estimar la generación de startups.
  - ruta: notebooks/05_map.ipynb
    descripcion: Visualización cartográfica de resultados territoriales y capas geográficas.

```

## Detalles técnicos

### Clase `Scraper`
- Patrón: `Template Method`.
- Responsabilidad: Inicializar el WebDriver con `undetected-chromedriver`, registrar la ejecución y orquestar la construcción de URL, la navegación y el parseo del html.
- La clase base centraliza esperas explícitas, control de errores, `skip` de targets y exportación de datos.

### Clase `CorreosApi`
- Patrón: cliente de API con caché en disco y decoradores de persistencia.
- Responsabilidad: Unificar el acceso a la API de Correos para obtener sugerencias, detalles y polígonos a partir de códigos postales, además de derivar municipio, provincia y CCAA.
- Las respuestas se pueden almacenar en JSON para evitar consultas repetidas y mejorar el rendimiento.

### Función `fuzzy_match_dict`
- Función de coincidencia difusa basada en `RapidFuzz` para mapear una clave contra un diccionario de candidatos.
- Genera varias consultas a partir de la clave original y de prefijos opcionales (`key_modifiers`) para mejorar el match.
- Devuelve el valor asociado a la mejor coincidencia que supere el umbral (`threshold`); si no hay match válido, devuelve `None`.
- Se usa principalmente para normalizar nombres o categorías con variantes de escritura.

### Submódulo `src.scrapers.powerbi`
- Submódulo especializado en extraer datos de paneles incrustados en Power BI.
- `src.scrapers.powerbi.queries` almacena consultas y cabeceras de la petición HTTP necesarias para reproducir la extracción desde el navegador.
- La función `src.scrapers.powerbi.queries.get_json_from_powerbi()` ejecuta la petición y devuelve la respuesta JSON cruda.
- La función `src.scrapers.powerbi.powerbi_parser.pbi_json_to_df()` convierte la respuesta JSON de Power BI en un `DataFrame` plano, resolviendo diccionarios, valores repetidos, nulos y fechas codificadas.

### Archivo .env
- El archivo `.env.example` contiene variables de entorno necesarias para la ejecución del proyecto, como la API key de Google Maps.
- Se recomienda crear un archivo `.env` a partir del ejemplo y completar los valores correspondientes antes de ejecutar los notebooks.