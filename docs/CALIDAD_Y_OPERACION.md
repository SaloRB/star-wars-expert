# Calidad, Operación y Roadmap — Star Wars Expert

**Versión:** 1.0  
**Última actualización:** 2026-01-27  
**Stack:** Python 3.10+ | pytest | uv

---

## 1. Requerimientos No Funcionales (NFRs)

### 1.1 Performance

| Métrica | Objetivo | Estado Actual |
|---------|----------|---------------|
| Tiempo de inicio (cold) | < 90s | ✅ ~30-60s |
| Tiempo de inicio (warm) | < 3s | ✅ ~1s |
| Tiempo primera respuesta | < 5s | ✅ ~2-3s |
| Throughput | Single user | ✅ Diseño actual |

### 1.2 Disponibilidad

| Aspecto | Requisito |
|---------|-----------|
| Dependencias externas | OpenAI API (99.9% SLA) |
| Modo offline | ❌ No soportado |
| Recuperación ante fallo | Retry automático (3x) para errores de red |

### 1.3 Seguridad

| Aspecto | Estado |
|---------|--------|
| API Key storage | `.env` file (gitignored) |
| Input validation | ⚠️ No implementado |
| Data encryption | N/A (local storage) |

### 1.4 Usabilidad

| Aspecto | Implementación |
|---------|----------------|
| Feedback visual | ✅ Progress spinner, typing effect |
| Mensajes de error | ✅ Descriptivos con sugerencias |
| Comandos de ayuda | ⚠️ No documentados en runtime |

---

## 2. Plan de Testing

### 2.1 Estrategia por Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                    Pirámide de Testing                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                         ▲                                    │
│                        /E\      E2E/Integration              │
│                       /2E \     (test_rag_integration.py)    │
│                      /─────\                                 │
│                     /       \                                │
│                    / Unit    \   Unit Tests                  │
│                   / Tests     \  (test_config.py,            │
│                  /─────────────\  test_loader.py)            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Cobertura Actual

| Módulo | Unit Tests | Integration | Cobertura |
|--------|------------|-------------|-----------|
| `config.py` | ✅ 18 tests | N/A | ~90% |
| `loader.py` | ✅ 6 tests | N/A | ~70% |
| `vectorstore.py` | ❌ | ✅ (indirecto) | ~30% |
| `chat.py` | ❌ | ✅ 8 tests | ~40% |
| `ui.py` | ❌ | ❌ | 0% |
| `main.py` | ❌ | ❌ | 0% |

### 2.3 Gaps de Testing Identificados

| Área | Prioridad | Descripción |
|------|-----------|-------------|
| `ConversationMemory` | Alta | Unit tests para add/clear/truncate |
| `StepProgress` | Media | Tests de UI con mocks |
| Error handling OpenAI | Alta | Tests de rate limits, token overflow |
| `validate_environment()` | Media | Tests con env vars mockeadas |

### 2.4 Ejecución de Tests

```bash
# Unit tests (rápidos, sin API)
uv run pytest tests/ -m "not integration" -v

# Integration tests (requiere OPENAI_API_KEY)
uv run pytest tests/ -m integration -v

# Con cobertura (requiere pytest-cov)
uv run pytest tests/ --cov=. --cov-report=html
```

---

## 3. Estrategia de QA

### 3.1 Test Cases Manuales

| ID | Escenario | Pasos | Resultado Esperado |
|----|-----------|-------|-------------------|
| TC-01 | Cold start | 1. Borrar `./qdrant_db` 2. Ejecutar `uv run main.py` | Scripts descargados, indexed en <90s |
| TC-02 | Warm start | Ejecutar con `./qdrant_db` existente | Chat disponible en <3s |
| TC-03 | Pregunta válida | Preguntar "Who is Luke?" | Respuesta basada en scripts |
| TC-04 | Cross-movie | "How does Luke evolve?" | Menciona las 3 películas |
| TC-05 | Memoria | Preguntar sobre Luke, luego "What happens to him?" | Resuelve pronombre |
| TC-06 | Off-topic | "What's the capital of France?" | Respuesta breve + redirect |
| TC-07 | Personaje no-canon | "Who is Rey?" | Indica falta de información |
| TC-08 | Clear command | Escribir `clear` | "Conversation history cleared" |
| TC-09 | Exit command | Escribir `exit` | Termina con mensaje de despedida |
| TC-10 | Sin API key | Ejecutar sin `.env` | Error claro con instrucciones |

### 3.2 Regression Testing

Ejecutar antes de cada release:

1. Todos los unit tests
2. Todos los integration tests
3. TC-01 a TC-10 manuales

---

## 4. Definition of Ready (DoR)

Una tarea está **Ready** cuando cumple:

| # | Criterio |
|---|----------|
| 1 | User story claramente definida con formato estándar |
| 2 | Criterios de aceptación en formato Given/When/Then |
| 3 | Dependencias identificadas y resueltas |
| 4 | Estimación de esfuerzo acordada |
| 5 | No hay bloqueos técnicos conocidos |
| 6 | Casos de error documentados |

---

## 5. Definition of Done (DoD)

Una tarea está **Done** cuando cumple:

| # | Criterio |
|---|----------|
| 1 | Código implementado y funcionando |
| 2 | Unit tests escritos y pasando |
| 3 | Integration tests actualizados si aplica |
| 4 | Código revisado (self-review mínimo) |
| 5 | Documentación actualizada (README, docstrings) |
| 6 | Sin errores de linting |
| 7 | Merge a main sin conflictos |

---

## 6. Runbooks Operativos

### 6.1 Runbook: Rebuild Vector Store

**Cuándo usar:** Cambios en `CHUNK_SIZE`, `CHUNK_OVERLAP`, o `EMBEDDING_MODEL`.

```bash
# 1. Detener aplicación si está corriendo
# 2. Borrar vector store
rm -rf ./qdrant_db

# 3. Ejecutar aplicación (regenerará automáticamente)
uv run main.py
```

**Tiempo estimado:** 30-60 segundos  
**Rollback:** Restaurar backup de `./qdrant_db` (si existe)

---

### 6.2 Runbook: Error de API Key

**Síntoma:** `❌ Invalid API Key` o `❌ Missing required environment variables`

```bash
# 1. Verificar que .env existe
ls -la .env

# 2. Si no existe, crear desde template
cp .env.example .env

# 3. Editar con API key válida
nano .env
# OPENAI_API_KEY=sk-proj-...

# 4. Verificar que la key es válida
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

---

### 6.3 Runbook: OpenAI Quota Exceeded

**Síntoma:** `❌ OpenAI API Quota Exceeded`

```bash
# 1. Verificar saldo de cuenta
# → https://platform.openai.com/account/billing

# 2. Si la cuenta tiene créditos, verificar límites de uso
# → https://platform.openai.com/account/limits

# 3. Si no hay créditos, agregar método de pago o esperar reset mensual
```

---

### 6.4 Runbook: Error de Conexión a IMSDB

**Síntoma:** `RuntimeError: Failed to load script`

```bash
# 1. Verificar conectividad
curl -I https://www.imsdb.com

# 2. Si falla, verificar DNS/firewall
ping imsdb.com

# 3. Si el sitio está caído, esperar y reintentar
# El sistema reintenta 3 veces con backoff exponencial (2s, 4s, 8s)

# 4. Workaround: usar vector store existente si disponible
ls ./qdrant_db  # Si existe, no necesita descargar
```

---

### 6.4 Runbook: Actualizar Dependencias

```bash
# 1. Actualizar lockfile
uv lock --upgrade

# 2. Sincronizar entorno
uv sync

# 3. Ejecutar tests
uv run pytest tests/ -v

# 4. Si pasan, commit
git add uv.lock
git commit -m "chore: update dependencies"
```

---

### 6.5 Runbook: Limpiar Entorno

```bash
# 1. Borrar vector store
rm -rf ./qdrant_db

# 2. Borrar cache de Python
rm -rf __pycache__
rm -rf .pytest_cache

# 3. Recrear entorno virtual (opcional)
rm -rf .venv
uv sync
```

---

## 7. Roadmap

### 7.1 Estado Actual: v1.0 (MVP) ✅

| Feature | Estado |
|---------|--------|
| Chat interactivo | ✅ |
| RAG con trilogía original | ✅ |
| Memoria conversacional | ✅ |
| Persistencia de embeddings | ✅ |
| Streaming + typing effect | ✅ |
| Sugerencias de preguntas | ✅ |
| Tests unitarios | ✅ |
| Tests de integración | ✅ |

---

### 7.2 v1.1 — Mejoras de Robustez

| Feature | Prioridad | Esfuerzo |
|---------|-----------|----------|
| Manejo de rate limits OpenAI (HTTP 429) | Alta | 2h |
| Validación de longitud de contexto | Alta | 2h |
| Logging estructurado (loguru/structlog) | Media | 3h |
| Tests para `ui.py` y `vectorstore.py` | Media | 4h |
| Tests para `ConversationMemory` | Alta | 2h |
| Comando `help` en runtime | Baja | 1h |

---

### 7.3 v1.2 — Mejoras de UX

| Feature | Prioridad | Esfuerzo |
|---------|-----------|----------|
| Persistencia de historial entre sesiones | Media | 4h |
| Configuración por CLI args (--model, --k) | Media | 3h |
| Exportar conversación a markdown | Baja | 2h |
| Modo verbose para debugging | Media | 2h |

---

### 7.4 v2.0 — Extensiones Mayores (Out of Scope Actual)

| Feature | Descripción |
|---------|-------------|
| Web UI | Interface Streamlit o Gradio |
| API REST | FastAPI wrapper |
| Multi-fuente | Agregar más películas/series |
| Custom embeddings | Fine-tuned models |
| Analytics | Tracking de preguntas populares |

> [!NOTE]
> v2.0 requiere rediseño arquitectónico y está fuera del alcance actual.

---

## 8. Riesgos

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|--------------|---------|------------|
| R1 | IMSDB cambia estructura HTML | Media | Alto | Monitorear, tener backup de scripts |
| R2 | OpenAI depreca modelo gpt-4o | Baja | Medio | Actualizar `LLM_MODEL` |
| R3 | Rate limits de OpenAI | Media | Medio | Implementar retry con backoff |
| R4 | Cambios en API de Qdrant | Baja | Medio | Pinear versiones en pyproject.toml |
| R5 | Costo de API aumenta | Media | Medio | Monitorear uso, considerar modelos más económicos |

---

## 9. Métricas de Éxito

### 9.1 Métricas Técnicas (Observables)

| Métrica | Cómo Medir | Target |
|---------|------------|--------|
| Tiempo de respuesta | Timestamp antes/después de stream | < 5s inicio |
| Tasa de éxito de requests | Logs de errores | > 95% |
| Tests pasando | `pytest` exit code | 100% |

### 9.2 Métricas de Uso (Futuras)

| Métrica | Implementación Requerida |
|---------|--------------------------|
| Preguntas por sesión | Logging estructurado |
| Temas más consultados | Analytics de queries |
| Tasa de "no encontrado" | Parsing de respuestas |

> [!IMPORTANT]
> Actualmente no hay instrumentación para métricas de uso.
> Requiere implementar logging estructurado (v1.1).

---

## 10. Checklist de Release

### Pre-Release

- [ ] Todos los unit tests pasando
- [ ] Todos los integration tests pasando
- [ ] TC-01 a TC-10 manuales ejecutados
- [ ] `uv.lock` actualizado
- [ ] README.md actualizado si hay cambios
- [ ] Version bump en pyproject.toml

### Release

- [ ] Tag de versión en git
- [ ] Push a main

### Post-Release

- [ ] Verificar funcionamiento en ambiente limpio
- [ ] Actualizar documentación si aplica
