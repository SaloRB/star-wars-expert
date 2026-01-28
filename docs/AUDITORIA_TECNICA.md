# 🛡️ AUDITORÍA TÉCNICA — Star Wars Expert

**Fecha:** 2026-01-28  
**Auditor:** Arquitecto de Software Senior  
**Versión del repositorio:** commit `0d98f9b` (2026-01-27)  
**Clasificación:** Proyecto personal / PoC

---

## Índice

1. [Estructura del Proyecto](#1-estructura-del-proyecto)
2. [Stack Tecnológico](#2-stack-tecnológico)
3. [Arquitectura](#3-arquitectura)
4. [Calidad del Código](#4-calidad-del-código)
5. [Dependencias](#5-dependencias)
6. [DevOps](#6-devops)
7. [Seguridad](#7-seguridad-)
8. [Rendimiento](#8-rendimiento)
9. [Documentación](#9-documentación)
10. [Problemas Encontrados](#10-problemas-encontrados)
11. [Recomendaciones](#11-recomendaciones)
12. [Resumen Ejecutivo](#12-resumen-ejecutivo)

---

## 1. ESTRUCTURA DEL PROYECTO

### 1.1 Árbol de Directorios

```
star-wars-expert/
├── .github/
│   └── copilot-instructions.md    # Instrucciones para AI assistants
├── docs/                          # Documentación técnica completa
│   ├── INDEX.md                   # Índice de documentación
│   ├── ARQUITECTURA_TECNICA.md    # 605 líneas
│   ├── CALIDAD_Y_OPERACION.md     # 385 líneas
│   ├── DOCUMENTACION_FUNCIONAL.md # 381 líneas
│   ├── SUPUESTOS_Y_DECISIONES_TOMADAS.md  # 253 líneas
│   └── support/                   # Knowledge base para soporte
│       ├── AI_SUPPORT_CONTEXT.md
│       ├── AI_SUPPORT_FAQ.md
│       ├── AI_SUPPORT_KNOWLEDGE.md
│       └── AI_SUPPORT_PLAYBOOK.md
├── tests/                         # Tests unitarios e integración
│   ├── __init__.py
│   ├── test_config.py             # 117 líneas - 17 tests
│   ├── test_loader.py             # 133 líneas - 6 tests
│   └── test_rag_integration.py    # 120 líneas - 8 tests
├── qdrant_db/                     # 🔸 Generado (6.1MB) - ignorado por git
├── .venv/                         # 🔸 Generado - ignorado por git
├── __pycache__/                   # 🔸 Generado - ignorado por git
├── .pytest_cache/                 # 🔸 Generado - ignorado por git
│
├── main.py                        # Entry point (76 líneas)
├── config.py                      # Configuración centralizada (103 líneas)
├── loader.py                      # HTTP fetch + parsing (110 líneas)
├── vectorstore.py                 # Qdrant management (107 líneas)
├── chat.py                        # RAG chain + memory (177 líneas)
├── ui.py                          # Progress display (120 líneas)
│
├── pyproject.toml                 # Configuración uv
├── uv.lock                        # Lockfile (1874 líneas)
├── .python-version                # Python 3.10
├── .gitignore                     # Correctamente configurado
├── .env.example                   # Template de variables
├── .env                           # 🔴 Contiene API key (excluido vía .gitignore)
└── README.md                      # Documentación de usuario
```

### 1.2 Estadísticas de Archivos

| Tipo                    | Archivos | Líneas | Propósito                        |
| ----------------------- | -------- | ------ | -------------------------------- |
| **Código fuente** `.py` | 6        | 693    | Lógica de aplicación             |
| **Tests** `.py`         | 4        | 371    | Tests unitarios/integración      |
| **Documentación** `.md` | 12       | ~2,500 | Docs técnicos y de usuario       |
| **Configuración**       | 5        | ~15    | pyproject.toml, .gitignore, etc. |
| **Lockfile**            | 1        | 1,874  | Dependencias fijas               |

**Total código productivo:** ~693 LOC (excluyendo tests)

### 1.3 Clasificación de Archivos

| Categoría              | Archivos                                          |
| ---------------------- | ------------------------------------------------- |
| ✅ Código fuente       | `*.py` (excl. tests)                              |
| ✅ Tests               | `tests/*.py`                                      |
| ✅ Documentación       | `docs/*.md`, `README.md`                          |
| ✅ Configuración       | `pyproject.toml`, `.gitignore`, `.env.example`    |
| 🔸 Generado (ignorado) | `qdrant_db/`, `__pycache__/`, `.venv/`, `uv.lock` |

---

## 2. STACK TECNOLÓGICO

### 2.1 Lenguajes y Runtimes

| Componente | Versión | Estado LTS                  |
| ---------- | ------- | --------------------------- |
| Python     | 3.10+   | ✅ Soportado hasta Oct 2026 |

### 2.2 Frameworks y Librerías Principales

| Dependencia                | Versión | Propósito             | Estado     |
| -------------------------- | ------- | --------------------- | ---------- |
| `langchain`                | 1.2.6   | Framework RAG         | ✅ Actual  |
| `langchain-openai`         | 1.1.7   | Integración OpenAI    | ✅ Actual  |
| `langchain-qdrant`         | 1.1.0   | Integración Qdrant    | ✅ Actual  |
| `langchain-text-splitters` | 1.1.0   | Chunking              | ✅ Actual  |
| `qdrant-client`            | 1.16.2  | Vector store          | ✅ Actual  |
| `openai`                   | 2.15.0  | OpenAI SDK            | ✅ Actual  |
| `beautifulsoup4`           | 4.14.3  | Web scraping          | ✅ Actual  |
| `rich`                     | 14.2.0  | Terminal UI           | ✅ Actual  |
| `colorama`                 | 0.4.6   | Cross-platform colors | ✅ Estable |
| `python-dotenv`            | 1.0.0   | Env management        | ✅ Estable |

### 2.3 Dependencias de Desarrollo

| Dependencia   | Versión | Propósito |
| ------------- | ------- | --------- |
| `pytest`      | 9.0.2   | Testing   |
| `pytest-mock` | 3.15.1  | Mocking   |

### 2.4 APIs Externas

| Servicio   | Uso                                                     | SLA     |
| ---------- | ------------------------------------------------------- | ------- |
| OpenAI API | Embeddings (`text-embedding-3-small`) + Chat (`gpt-4o`) | 99.9%   |
| IMSDB.com  | Fuente de scripts                                       | Sin SLA |

---

## 3. ARQUITECTURA

### 3.1 Diagrama del Sistema

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          STAR WARS EXPERT                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────┐                                                          │
│  │   IMSDB.com    │                                                          │
│  │  (3 scripts)   │                                                          │
│  └───────┬────────┘                                                          │
│          │ HTTP + Retry (3x)                                                 │
│          ▼                                                                   │
│  ┌────────────────┐    ┌─────────────────┐    ┌──────────────────┐          │
│  │  loader.py     │───▶│ BeautifulSoup   │───▶│ RecursiveText    │          │
│  │  (Fetch+Parse) │    │ (Parse <pre>)   │    │ Splitter         │          │
│  └────────────────┘    └─────────────────┘    │ (2500/250 chars) │          │
│                                               └────────┬─────────┘          │
│                                                        │                    │
│                                                        ▼                    │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     vectorstore.py                                    │   │
│  │  ┌──────────────────┐    ┌─────────────────────────────────────────┐ │   │
│  │  │ OpenAI Embeddings│───▶│          Qdrant (Local File)            │ │   │
│  │  │ text-embedding-  │    │          ./qdrant_db/                   │ │   │
│  │  │ 3-small          │    │          Collection: star_wars_scripts  │ │   │
│  │  └──────────────────┘    └───────────────────┬─────────────────────┘ │   │
│  └──────────────────────────────────────────────│───────────────────────┘   │
│                                                 │                            │
│                                                 │ Retriever (k=15)           │
│                                                 ▼                            │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         chat.py                                       │   │
│  │                                                                       │   │
│  │  ┌─────────────┐   ┌─────────────────┐   ┌────────────────────────┐  │   │
│  │  │ Conversation│   │ ChatPrompt      │   │ ChatOpenAI (GPT-4o)    │  │   │
│  │  │ Memory (5)  │──▶│ Template        │──▶│ streaming=True         │  │   │
│  │  └─────────────┘   └─────────────────┘   └───────────┬────────────┘  │   │
│  │                                                      │               │   │
│  └──────────────────────────────────────────────────────│───────────────┘   │
│                                                         │                    │
│                                                         ▼                    │
│  ┌─────────────┐    ┌────────────────┐    ┌────────────────────────────┐    │
│  │   ui.py     │◀───│  Terminal CLI  │◀───│  Typing Effect + Colors    │    │
│  │ StepProgress│    │  (colorama)    │    │  (30ms/char)               │    │
│  └─────────────┘    └────────────────┘    └────────────────────────────┘    │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        config.py                                      │   │
│  │  Todas las constantes configurables (LLM, retriever, UI, HTTP, etc.) │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Patrones de Diseño Identificados

| Patrón                                   | Implementación                        | Evaluación             |
| ---------------------------------------- | ------------------------------------- | ---------------------- |
| **RAG (Retrieval-Augmented Generation)** | Pipeline completo                     | ✅ Bien implementado   |
| **Configuration Object**                 | `config.py` centralizado              | ✅ Excelente práctica  |
| **Retry with Backoff**                   | `loader.py`                           | ✅ Exponential backoff |
| **Separation of Concerns**               | Módulos separados por responsabilidad | ✅ Buena modularidad   |
| **Chain of Responsibility**              | LCEL pipeline en LangChain            | ✅ Idiomático          |
| **Factory Pattern**                      | `get_or_create_vectorstore()`         | ✅ Lazy initialization |

### 3.3 Flujo de Datos

```
1. INICIALIZACIÓN (Cold Start):
   main.py → validate_environment() → get_or_create_vectorstore()
                                              │
                                              ├─ [Si no existe DB]
                                              │   load_and_split_scripts()
                                              │   → HTTP GET (3 URLs)
                                              │   → BeautifulSoup parse
                                              │   → RecursiveCharacterTextSplitter
                                              │   → OpenAI Embeddings
                                              │   → Qdrant persist
                                              │
                                              └─ [Si existe DB]
                                                  Cargar desde ./qdrant_db

2. CHAT LOOP:
   User Input → ConversationMemory.add_user_message()
             → Retriever.invoke(query)  [k=15 chunks]
             → ChatPromptTemplate(context + history + query)
             → ChatOpenAI.stream()
             → StrOutputParser()
             → Typing effect output
             → ConversationMemory.add_ai_message()
```

### 3.4 Acoplamiento y Cohesión

| Módulo           | Cohesión | Acoplamiento | Observaciones                 |
| ---------------- | -------- | ------------ | ----------------------------- |
| `config.py`      | 🟢 Alta  | 🟢 Bajo      | Solo constantes               |
| `loader.py`      | 🟢 Alta  | 🟢 Bajo      | Solo HTTP + parsing           |
| `vectorstore.py` | 🟢 Alta  | 🟡 Medio     | Depende de loader, config, ui |
| `chat.py`        | 🟡 Media | 🟡 Medio     | RAG + Memory + UI en uno      |
| `ui.py`          | 🟢 Alta  | 🟢 Bajo      | Solo componentes visuales     |
| `main.py`        | 🟡 Media | 🟡 Medio     | Orquestación (esperado)       |

---

## 4. CALIDAD DEL CÓDIGO

### 4.1 Métricas

| Métrica                     | Valor                            | Evaluación                 |
| --------------------------- | -------------------------------- | -------------------------- |
| **Total LOC (prod)**        | 693                              | 🟢 Proyecto compacto       |
| **Total LOC (tests)**       | 371                              | 🟢 Ratio 1:0.5 (aceptable) |
| **Archivo más grande**      | chat.py (177 líneas)             | 🟢 Manejable               |
| **Complejidad ciclomática** | Baja                             | 🟢 Funciones simples       |
| **Docstrings**              | Presentes en todas las funciones | 🟢 Buena documentación     |
| **Type hints**              | Presentes (Python 3.10+)         | 🟢 Tipado moderno          |

### 4.2 Tests

| Categoría             | Tests | Cobertura Estimada |
| --------------------- | ----- | ------------------ |
| **Unit tests**        | 23    | ~70%               |
| **Integration tests** | 8     | ~40%               |
| **Total**             | 31    | ~55%               |

**Resultado de ejecución:**

```
23 passed, 8 deselected in 0.78s ✅
```

### 4.3 Gaps de Testing Identificados

| Módulo                         | Cobertura | Prioridad |
| ------------------------------ | --------- | --------- |
| `ui.py`                        | 0%        | 🟡 Media  |
| `main.py`                      | 0%        | 🟡 Media  |
| `ConversationMemory` (chat.py) | Parcial   | 🟠 Alta   |
| Error handling chat.py         | Parcial   | 🟠 Alta   |

### 4.4 Linting/Formatting

| Herramienta | Configurada | Estado         |
| ----------- | ----------- | -------------- |
| Ruff        | ❌          | No configurado |
| Black       | ❌          | No configurado |
| isort       | ❌          | No configurado |
| mypy        | ❌          | No configurado |
| pre-commit  | ❌          | No configurado |

### 4.5 Code Smells

| Tipo             | Ubicación                                  | Severidad | Descripción                                |
| ---------------- | ------------------------------------------ | --------- | ------------------------------------------ |
| Código duplicado | `chat.py:127-140` y `vectorstore.py:15-26` | 🟡 Medio  | Formateo de errores OpenAI duplicado       |
| Función larga    | `run_chat_loop()`                          | 🟢 Bajo   | 60 líneas, aceptable pero podría dividirse |

---

## 5. DEPENDENCIAS

### 5.1 Análisis de Manifiestos

**pyproject.toml:**

- ✅ Formato moderno (PEP 621)
- ✅ Versiones mínimas especificadas
- ✅ Dependencias de desarrollo separadas
- ⚠️ Falta descripción del proyecto

### 5.2 Estado de Dependencias

| Dependencia   | Versión | Última Disponible | Estado    |
| ------------- | ------- | ----------------- | --------- |
| langchain     | 1.2.6   | 1.2.6             | ✅ Actual |
| openai        | 2.15.0  | 2.15.0            | ✅ Actual |
| qdrant-client | 1.16.2  | 1.16.2            | ✅ Actual |

### 5.3 Vulnerabilidades Potenciales

| Dependencia             | Riesgo  | Descripción                                    |
| ----------------------- | ------- | ---------------------------------------------- |
| `requests` (transitiva) | 🟢 Bajo | Revisar periódicamente                         |
| `beautifulsoup4`        | 🟢 Bajo | Web scraping, posible XSS si se renderiza HTML |

### 5.4 Licencias

| Dependencia   | Licencia   |
| ------------- | ---------- |
| LangChain     | MIT        |
| Qdrant        | Apache 2.0 |
| OpenAI SDK    | MIT        |
| BeautifulSoup | MIT        |
| Rich          | MIT        |

✅ **Todas las licencias son compatibles para uso comercial**

---

## 6. DEVOPS

### 6.1 Scripts de Build y Ejecución

| Comando                                     | Propósito             |
| ------------------------------------------- | --------------------- |
| `uv sync`                                   | Instalar dependencias |
| `uv run main.py`                            | Ejecutar aplicación   |
| `uv run pytest tests/ -m "not integration"` | Tests unitarios       |
| `uv run pytest tests/ -m integration`       | Tests de integración  |

### 6.2 CI/CD

| Aspecto          | Estado            |
| ---------------- | ----------------- |
| GitHub Actions   | ❌ No configurado |
| Pipelines        | ❌ No existen     |
| Hooks pre-commit | ❌ No configurado |

### 6.3 Containerización

| Aspecto        | Estado       |
| -------------- | ------------ |
| Dockerfile     | ❌ No existe |
| docker-compose | ❌ No existe |
| Kubernetes     | ❌ No aplica |

### 6.4 Gestión de Entornos

| Aspecto              | Implementación                         |
| -------------------- | -------------------------------------- |
| Variables de entorno | ✅ `.env` con python-dotenv            |
| Template             | ✅ `.env.example`                      |
| Validación           | ✅ `validate_environment()` en main.py |

---

## 7. SEGURIDAD 🔴

### 7.1 Secretos/Credenciales

| Hallazgo                          | Severidad | Estado                 |
| --------------------------------- | --------- | ---------------------- |
| `.env` en `.gitignore`            | ✅        | Correctamente excluido |
| API Key no hardcodeada            | ✅        | Buena práctica         |
| `.env.example` sin valores reales | ✅        | Correcto               |

### 7.2 Hallazgos Críticos

| ID     | Hallazgo                    | Severidad | Descripción                                                                                                                 |
| ------ | --------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------- |
| SEC-01 | API Key expuesta localmente | 🟡 Medio  | El archivo `.env` contiene API key real. Aunque está en gitignore, cualquier persona con acceso al filesystem puede leerla. |

### 7.3 Configuración de .gitignore

```gitignore
# Correctamente configurado:
__pycache__/
*.py[oc]
.venv
qdrant_db
.env  ✅ API key protegida
```

### 7.4 Validación de Input

| Aspecto                     | Estado             | Riesgo                                |
| --------------------------- | ------------------ | ------------------------------------- |
| Sanitización de user input  | ⚠️ No implementada | 🟡 Medio - El input va directo al LLM |
| Límite de longitud de query | ❌ No implementado | 🟡 Medio - Posible token overflow     |
| Rate limiting local         | ❌ No implementado | 🟢 Bajo - Solo uso local              |

### 7.5 Dependencias de Red

| Servicio   | Comunicación                               | Riesgo                                                                 |
| ---------- | ------------------------------------------ | ---------------------------------------------------------------------- |
| IMSDB.com  | Según `STAR_WARS_SCRIPTS` en `config.py`   | Depende del protocolo configurado: usar siempre HTTPS para evitar MITM |
| OpenAI API | HTTPS                                      | 🟢 Bajo                                                                 |

---

## 8. RENDIMIENTO

### 8.1 Estrategias de Caché

| Tipo                    | Implementación          | Eficacia                                 |
| ----------------------- | ----------------------- | ---------------------------------------- |
| Vector store persistido | ✅ `./qdrant_db`        | 🟢 Excelente - Cold start ~60s, warm ~1s |
| Embeddings cacheados    | ✅ En Qdrant            | 🟢 No recalcula                          |
| Conversación en memoria | ✅ `ConversationMemory` | 🟢 In-memory, rápido                     |

### 8.2 Optimizaciones Presentes

| Optimización        | Descripción                            |
| ------------------- | -------------------------------------- |
| Lazy loading        | Vector store solo se crea si no existe |
| Streaming responses | Respuestas en tiempo real              |
| Chunk overlap       | 250 chars para preservar contexto      |
| k=15 retriever      | Balance entre contexto y tokens        |

### 8.3 Cuellos de Botella Potenciales

| Cuello de Botella   | Impacto  | Mitigación                           |
| ------------------- | -------- | ------------------------------------ |
| Cold start (60s)    | 🟡 Medio | Ya implementado: persistencia        |
| Latencia OpenAI API | 🟡 Medio | Streaming mitiga percepción          |
| IMSDB availability  | 🟠 Alto  | Solo afecta primer uso, sin fallback |

---

## 9. DOCUMENTACIÓN

### 9.1 Inventario

| Documento                              | Líneas | Calidad           |
| -------------------------------------- | ------ | ----------------- |
| README.md                              | 107    | 🟢 Completo       |
| docs/ARQUITECTURA_TECNICA.md           | 605    | 🟢 Exhaustivo     |
| docs/CALIDAD_Y_OPERACION.md            | 385    | 🟢 Completo       |
| docs/DOCUMENTACION_FUNCIONAL.md        | 381    | 🟢 Completo       |
| docs/SUPUESTOS_Y_DECISIONES_TOMADAS.md | 253    | 🟢 Valioso        |
| .github/copilot-instructions.md        | 169    | 🟢 Útil para AI   |
| docs/support/\*.md                     | 690    | 🟢 Knowledge base |

### 9.2 Onboarding

| Aspecto         | Estado                            |
| --------------- | --------------------------------- |
| Instalación     | ✅ Documentada en README          |
| Configuración   | ✅ `.env.example` + instrucciones |
| Uso básico      | ✅ Comandos documentados          |
| Arquitectura    | ✅ Diagramas en docs/             |
| Troubleshooting | ✅ Runbooks en docs/              |
| API interna     | ✅ Docstrings completos           |

### 9.3 Evaluación

**Ratio documentación/código:** ~3:1 (2,500 líneas doc : 693 líneas código)

🟢 **Excelente documentación** - Muy por encima del promedio de la industria.

---

## 10. PROBLEMAS ENCONTRADOS

### 10.1 Lista Priorizada

| ID   | Problema                              | Severidad | Impacto                  | Esfuerzo  |
| ---- | ------------------------------------- | --------- | ------------------------ | --------- |
| P-01 | Sin CI/CD pipeline                    | 🟠 Alto   | Riesgo de regresiones    | 2-4 horas |
| P-02 | Sin linting/formatting configurado    | 🟡 Medio  | Inconsistencia de estilo | 1 hora    |
| P-03 | Falta validación de input del usuario | 🟡 Medio  | Posible token overflow   | 2 horas   |
| P-04 | Código duplicado en manejo de errores | 🟡 Medio  | Mantenibilidad           | 1 hora    |
| P-05 | Sin tests para `ui.py` y `main.py`    | 🟡 Medio  | Cobertura incompleta     | 3 horas   |
| P-06 | Sin Dockerfile                        | 🟢 Bajo   | Portabilidad limitada    | 1 hora    |
| P-07 | IMSDB sin fallback/cache local        | 🟢 Bajo   | Single point of failure  | 2 horas   |
| P-08 | Description vacía en pyproject.toml   | 🟢 Bajo   | Metadata incompleta      | 5 min     |

### 10.2 Detalles

#### 🟠 P-01: Sin CI/CD Pipeline

**Ubicación:** `.github/` solo tiene copilot-instructions.md  
**Riesgo:** Commits pueden romper tests sin que nadie se entere  
**Solución:** Agregar GitHub Actions workflow

#### 🟡 P-02: Sin Linting Configurado

**Ubicación:** pyproject.toml  
**Riesgo:** Inconsistencia de estilo entre contribuidores  
**Solución:** Agregar ruff + pre-commit

#### 🟡 P-03: Sin Validación de Input

**Ubicación:** chat.py línea 94  
**Riesgo:** Queries muy largas pueden causar errores de tokens  
**Solución:** Agregar límite de caracteres + sanitización

---

## 11. RECOMENDACIONES

### 11.1 Inmediatas (Esta Semana)

#### R-01: Agregar GitHub Actions CI

Crear archivo `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run pytest tests/ -m "not integration" -v
```

#### R-02: Configurar Ruff

Agregar a `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
```

Comandos:

```bash
# Instalar y ejecutar
uv add --dev ruff
uv run ruff check .
uv run ruff format .
```

### 11.2 Corto Plazo (1 Mes)

#### R-03: Agregar Validación de Input

En `chat.py`, agregar en `run_chat_loop()`:

```python
MAX_QUERY_LENGTH = 2000

query = input(...)
if len(query) > MAX_QUERY_LENGTH:
    print(f"Query too long ({len(query)} chars). Max: {MAX_QUERY_LENGTH}")
    continue
```

#### R-04: Extraer Manejo de Errores

Crear nuevo archivo `errors.py`:

```python
def format_openai_error(error_str: str) -> tuple[str, str]:
    """Format OpenAI errors with title and description."""
    if "insufficient_quota" in error_str:
        return ("OpenAI API Quota Exceeded",
                "Check billing at: https://platform.openai.com/account/billing")
    # ... etc
```

#### R-05: Agregar Tests Faltantes

```bash
# Crear tests/test_ui.py
# Crear tests/test_main.py
# Objetivo: subir cobertura a 80%+
```

### 11.3 Mediano Plazo (3 Meses)

#### R-06: Agregar Dockerfile

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
CMD ["uv", "run", "main.py"]
```

#### R-07: Cache Local de Scripts

En `loader.py`, agregar fallback:

```python
CACHE_PATH = "./script_cache/"

def load_star_wars_script(url, title, console=None):
    cache_file = Path(CACHE_PATH) / f"{title.replace(' ', '_')}.txt"
    if cache_file.exists():
        return Document(page_content=cache_file.read_text(), ...)
    # ... fetch from network
    cache_file.write_text(script_raw)  # Save to cache
```

---

## 12. RESUMEN EJECUTIVO

### 12.1 Scorecard por Categoría

| Categoría             | Score      | Comentario                               |
| --------------------- | ---------- | ---------------------------------------- |
| **Estructura**        | 9/10       | Organización ejemplar                    |
| **Arquitectura**      | 9/10       | Patrones RAG bien aplicados              |
| **Calidad de Código** | 8/10       | Falta linting, código duplicado menor    |
| **Tests**             | 7/10       | Buenos tests, gaps en ui.py/main.py      |
| **Dependencias**      | 9/10       | Actualizadas, bien gestionadas           |
| **DevOps**            | 5/10       | Sin CI/CD ni containerización            |
| **Seguridad**         | 7/10       | Buenas prácticas, falta validación input |
| **Performance**       | 8/10       | Caché efectiva, streaming                |
| **Documentación**     | 10/10      | Excepcional                              |
| **PROMEDIO**          | **8.0/10** |                                          |

### 12.2 Roadmap Visual

```
Semana 1-2 (Inmediato)         Mes 1 (Corto)              Mes 2-3 (Mediano)
────────────────────────────────────────────────────────────────────────────
┌─────────────────┐     ┌──────────────────┐     ┌────────────────────────┐
│ ✓ GitHub Actions│────▶│ ✓ Input validation│────▶│ ✓ Dockerfile           │
│ ✓ Ruff config   │     │ ✓ Error handling │     │ ✓ Script cache fallback│
│ ✓ pyproject fix │     │ ✓ Tests ui/main  │     │ ✓ Integration tests++  │
└─────────────────┘     └──────────────────┘     └────────────────────────┘
     Priority: 🟠              Priority: 🟡              Priority: 🟢
```

### 12.3 Fortalezas y Debilidades

| ✅ Fortalezas                      | ❌ Debilidades               |
| ---------------------------------- | ---------------------------- |
| Documentación excepcional (10/10)  | Sin CI/CD pipeline           |
| Arquitectura RAG bien implementada | Sin linting/formatting       |
| Código modular y bien organizado   | Tests incompletos (ui, main) |
| Configuración centralizada         | Sin containerización         |
| Manejo de errores descriptivo      | Código duplicado menor       |
| Dependencias actualizadas          | Sin validación de input      |

### 12.4 Conclusión

**Star Wars Expert** es un proyecto de alta calidad para su propósito (PoC/personal). La arquitectura RAG está bien implementada siguiendo patrones idiomáticos de LangChain, y la documentación es excepcional.

Las áreas de mejora principales son la infraestructura de DevOps (CI/CD) y la configuración de herramientas de calidad de código (linting). Para un proyecto productivo, se recomienda priorizar P-01 (CI/CD) y P-02 (linting) esta semana.

**Calificación global: 8.0/10** — Listo para demo/PoC, requiere mejoras de DevOps para producción.

---

## Apéndice: Comandos de Verificación

```bash
# Ejecutar tests unitarios
uv run pytest tests/ -m "not integration" -v

# Ejecutar tests de integración (requiere OPENAI_API_KEY)
uv run pytest tests/ -m integration -v

# Verificar estado del repositorio
git status

# Contar líneas de código
wc -l *.py tests/*.py

# Ver dependencias
cat pyproject.toml
```

---

_Documento generado el 2026-01-28 como resultado de auditoría técnica exhaustiva._
