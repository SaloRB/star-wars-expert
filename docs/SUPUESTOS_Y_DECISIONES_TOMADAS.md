# SUPUESTOS Y DECISIONES TOMADAS

## Fase 0 — Revisión de Insumos

**Fecha de generación:** 2026-01-27  
**Repositorio analizado:** `star-wars-expert`  
**Stack tecnológico real:** Python 3.10+ | LangChain | Qdrant | OpenAI | Rich/Colorama | pytest

---

## Resumen Ejecutivo

Este documento registra los supuestos, decisiones y vacíos identificados tras analizar el repositorio completo de **Star Wars Expert**, una aplicación RAG (Retrieval-Augmented Generation) que responde preguntas sobre los scripts de la trilogía original de Star Wars (Episodios IV-VI).

La aplicación está **desarrollada y funcional**, con documentación técnica existente en:
- [README.md](file:///Users/salo/dev/langchain/star-wars-expert/README.md)
- [.github/copilot-instructions.md](file:///Users/salo/dev/langchain/star-wars-expert/.github/copilot-instructions.md)

---

## 1. Elementos Claramente Definidos por el Producto Real

### 1.1 Arquitectura Técnica ✅

| Componente | Implementación | Archivo Fuente |
|------------|----------------|----------------|
| Entry Point | Validación de env + orquestación | [main.py](file:///Users/salo/dev/langchain/star-wars-expert/main.py) |
| Cargador de Scripts | HTTP con retry + BeautifulSoup | [loader.py](file:///Users/salo/dev/langchain/star-wars-expert/loader.py) |
| Vector Store | Qdrant file-based persistente | [vectorstore.py](file:///Users/salo/dev/langchain/star-wars-expert/vectorstore.py) |
| RAG Chain | LCEL pipeline con memoria | [chat.py](file:///Users/salo/dev/langchain/star-wars-expert/chat.py) |
| UI/UX | Rich + Colorama + typing effect | [ui.py](file:///Users/salo/dev/langchain/star-wars-expert/ui.py) |
| Configuración | Constantes centralizadas | [config.py](file:///Users/salo/dev/langchain/star-wars-expert/config.py) |

### 1.2 Flujo de Datos Principal ✅

```
Scripts IMSDB → HTTP Fetch → BeautifulSoup Parse → Chunk (2500/250)
    → OpenAI Embeddings → Qdrant Storage → Retriever (k=15)
    → ChatPromptTemplate + Memory → GPT-4o → Streaming Response
```

### 1.3 Configuración Documentada ✅

| Parámetro | Valor | Ubicación |
|-----------|-------|-----------|
| `LLM_MODEL` | gpt-4o | config.py:12 |
| `EMBEDDING_MODEL` | text-embedding-3-small | config.py:14 |
| `RETRIEVER_K` | 15 chunks | config.py:25 |
| `MEMORY_K` | 5 turnos | config.py:30 |
| `CHUNK_SIZE` | 2500 caracteres | config.py:35 |
| `CHUNK_OVERLAP` | 250 caracteres | config.py:36 |
| `TYPING_DELAY` | 0.03s/caracter | config.py:19 |
| `REQUEST_TIMEOUT` | 30s | config.py:41 |
| `MAX_RETRIES` | 3 intentos | config.py:42 |

### 1.4 Fuentes de Datos Externas ✅

| Script | URL |
|--------|-----|
| A New Hope | https://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html |
| The Empire Strikes Back | https://www.imsdb.com/scripts/Star-Wars-The-Empire-Strikes-Back.html |
| Return of the Jedi | https://www.imsdb.com/scripts/Star-Wars-Return-of-the-Jedi.html |

### 1.5 Testing Existente ✅

| Archivo | Tipo | Cobertura |
|---------|------|-----------|
| [test_config.py](file:///Users/salo/dev/langchain/star-wars-expert/tests/test_config.py) | Unit | Validación de constantes |
| [test_loader.py](file:///Users/salo/dev/langchain/star-wars-expert/tests/test_loader.py) | Unit | HTTP + parsing (mocks) |
| [test_rag_integration.py](file:///Users/salo/dev/langchain/star-wars-expert/tests/test_rag_integration.py) | Integration | RAG E2E con API real |

---

## 2. Elementos Inferidos (No Documentados Explícitamente)

### 2.1 Tipo de Usuario

> **Asunción:** La aplicación está diseñada para un **único tipo de usuario (End User)** sin roles ni permisos diferenciados.

**Evidencia:**
- No existe sistema de autenticación
- No hay RBAC ni control de acceso
- Interface CLI interactiva directa

### 2.2 Modo de Despliegue

> **Asunción:** Aplicación de uso **local/personal**, no productiva ni web-exposed.

**Evidencia:**
- Usa Qdrant file-based (`./qdrant_db`), no cliente remoto
- Sin servidor HTTP/API externa
- Sin configuración de CI/CD para deploy (solo estructura `.github`)
- Sin Dockerfile ni configuración de cloud

### 2.3 Manejo de Sesiones

> **Asunción:** Sesión única por ejecución, sin persistencia entre ejecuciones.

**Evidencia:**
- `ConversationMemory` es in-memory
- No hay serialización de historial a disco
- Comando `clear` solo limpia memoria actual

### 2.4 Límites de Uso

> **Asunción:** Sin rate limiting interno; depende de límites de OpenAI API.

**Evidencia:**
- No hay throttling implementado
- Retry logic solo para errores de red (no 429)
- Sin queue de requests

---

## 3. Puntos Ambiguos / Inconsistentes

### 3.1 Manejo de Errores de API OpenAI

| Área | Descripción | Nivel |
|------|-------------|-------|
| Rate Limits | No hay manejo explícito de HTTP 429 de OpenAI | ⚠️ Medio |
| Token Limits | No hay validación de longitud de contexto antes de enviar | ⚠️ Medio |
| API Key Inválida | Valida existencia pero no validez de key | ⚠️ Bajo |

**Decisión tomada:** Documentaré como limitación conocida en "Riesgos".

### 3.2 Parámetro `show_progress` No Utilizado

En [loader.py:85](file:///Users/salo/dev/langchain/star-wars-expert/loader.py#L85), el parámetro `show_progress` existe pero nunca se utiliza:

```python
def load_and_split_scripts(console: Console, show_progress: bool = False) -> list[Document]:
```

**Decisión tomada:** Lo mencionaré como debt técnico menor.

### 3.3 Separación de Sugerencias en Respuesta

El chat separa respuesta principal de sugerencias usando un separador hardcoded:

```python
separator = "─────────────────────────────────────────"
if separator in full_response:
    main_answer, suggestions = full_response.split(separator, 1)
```

**Ambigüedad:** Si el LLM no genera el separador exacto, las sugerencias no se parsean correctamente.

**Decisión tomada:** Documentaré como comportamiento esperado que depende del prompt engineering.

---

## 4. Vacíos Identificados

### 4.1 Documentación Faltante

| Área | Estado | Impacto |
|------|--------|---------|
| API Reference | No existe | Bajo (no es librería) |
| Changelog | No existe | Medio |
| User Guide detallada | Solo README básico | Medio |
| Arquitectura diagramada | No existe | Bajo |
| FAQ de usuario | No existe | Alto para soporte |

### 4.2 Testing Gaps

| Área | Estado |
|------|--------|
| Tests para `ui.py` | No existen |
| Tests para `vectorstore.py` | No existen |
| Tests para `chat.py` (unit) | No existen |
| Tests de error handling de OpenAI | No existen |
| Tests de memoria conversacional | No existen |

### 4.3 Operación / Observabilidad

| Área | Estado |
|------|--------|
| Logging estructurado | No implementado |
| Métricas | No implementado |
| Tracing | No implementado |
| Health checks | No aplica (local) |

### 4.4 Seguridad

| Área | Estado |
|------|--------|
| Validación de input usuario | No existe (se asume benigno) |
| Sanitización de URLs | No existe |
| Rotación de API keys | No documentado |

---

## 5. Decisiones de Documentación Tomadas

### 5.1 Alcance de Documentación

| Decisión | Justificación |
|----------|---------------|
| Asumir usuario técnico | App CLI requiere `uv`, API key, terminal |
| No documentar deployment web | No es parte del producto actual |
| Documentar como "personal tool" | Arquitectura indica uso individual |
| Incluir NFRs observados | Basados en código, no inventados |

### 5.2 Lenguaje de Documentación

| Decisión | Justificación |
|----------|---------------|
| **Español** para documentación interna | El usuario se comunica en español |
| **Inglés** para código y docs técnicas | Consistencia con codebase existente |

### 5.3 Estructura de `/docs`

```
docs/
├── SUPUESTOS_Y_DECISIONES_TOMADAS.md    ← Este documento (Fase 0)
├── DOCUMENTACION_FUNCIONAL.md           ← Fase 1
├── ARQUITECTURA_TECNICA.md              ← Fase 2
├── CALIDAD_Y_OPERACION.md               ← Fase 3
└── support/                              ← Fase 4
    ├── AI_SUPPORT_CONTEXT.md
    ├── AI_SUPPORT_PLAYBOOK.md
    ├── AI_SUPPORT_FAQ.md
    └── AI_SUPPORT_KNOWLEDGE.md
```

---

## 6. Preguntas Bloqueantes

> **Ninguna pregunta bloqueante identificada.**

La aplicación es suficientemente simple y autodescriptiva para inferir todo el comportamiento necesario del código fuente.

---

## 7. Próximos Pasos

Proceder con **FASE 1 — Documentación Funcional y de Producto** que incluirá:

1. Resumen ejecutivo
2. Visión del producto
3. Tipos de usuario
4. Análisis funcional (módulos, comandos, flujos)
5. User Stories
6. Criterios de aceptación
7. Reglas de negocio
8. Glosario de términos

---

> [!NOTE]
> Este documento se actualizará si durante las fases posteriores se descubren nuevas asunciones o inconsistencias.
