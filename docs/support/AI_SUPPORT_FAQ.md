# AI Support FAQ — Star Wars Expert

## Instalación y Configuración

### ¿Cómo instalo Star Wars Expert?

```bash
git clone https://github.com/SaloRB/star-wars-expert.git
cd star-wars-expert
uv sync
cp .env.example .env
# Editar .env con tu OPENAI_API_KEY
uv run main.py
```

**Requisitos:** Python 3.10+, conexión a internet, API key de OpenAI.

---

### ¿Dónde obtengo mi API key de OpenAI?

1. Ve a <https://platform.openai.com/api-keys>
2. Crea una cuenta o inicia sesión
3. Haz clic en "Create new secret key"
4. Copia la key y pégala en tu archivo `.env`

> ⚠️ La key solo se muestra una vez. Si la pierdes, crea una nueva.

---

### ¿Cuánto cuesta usar la aplicación?

La aplicación es gratuita, pero **OpenAI cobra por uso de API**:

- Embeddings (~$0.02 por indexación inicial)
- Chat completions (~$0.01-0.03 por pregunta con GPT-4o)

Consulta precios actualizados en <https://openai.com/pricing>

---

## Uso General

### ¿Qué películas cubre Star Wars Expert?

Solo la **trilogía original**:

- Episode IV: A New Hope (1977)
- Episode V: The Empire Strikes Back (1980)
- Episode VI: Return of the Jedi (1983)

**NO incluye:** Precuelas, secuelas, The Mandalorian, Clone Wars, ni ningún otro contenido.

---

### ¿Por qué no responde sobre [personaje/evento]?

Posibles razones:

1. **No está en la trilogía original** (ej: Rey, Kylo Ren, Jar Jar)
2. **Es un personaje menor** no mencionado en los scripts
3. **El nombre está mal escrito** en tu pregunta

---

### ¿Cómo hago preguntas de seguimiento?

Simplemente pregunta usando pronombres. El sistema recuerda las últimas 5 interacciones.

**Ejemplo:**

```
You: Who is Darth Vader?
[respuesta sobre Vader]

You: What happens to him at the end?
[respuesta sobre el destino de Vader en ROTJ]
```

---

### ¿Cómo borro el historial de conversación?

Escribe `clear` en el chat. Esto borra la memoria de la sesión actual.

---

### ¿Cómo salgo de la aplicación?

Escribe `exit` o `quit`.

---

## Problemas Comunes

### Error: "Missing required environment variables"

**Causa:** No configuraste el archivo `.env` con tu API key.

**Solución:**

```bash
cp .env.example .env
# Editar .env y agregar OPENAI_API_KEY=tu-key
```

---

### Error: "OpenAI API Quota Exceeded"

**Causa:** Tu cuenta de OpenAI no tiene créditos disponibles.

**Solución:**

1. Ve a <https://platform.openai.com/account/billing>
2. Verifica tu saldo y agrega créditos si es necesario
3. Reinicia la aplicación

---

### Error: "Invalid API Key"

**Causa:** La API key en tu archivo `.env` es inválida o expiró.

**Solución:**

1. Ve a <https://platform.openai.com/api-keys>
2. Crea una nueva key si es necesario
3. Actualiza tu archivo `.env` con la nueva key
4. Reinicia la aplicación

---

### Error: "Rate Limit Reached"

**Causa:** Demasiadas solicitudes a OpenAI en poco tiempo.

**Solución:** Espera unos segundos y reintenta tu pregunta.

---

### Error: "Failed to load script"

**Causa:** Problemas de conexión o IMSDB.com no disponible.

**Solución:**

1. Verifica tu conexión a internet
2. Espera unos minutos y reintenta
3. Si tienes `./qdrant_db`, los scripts ya están indexados y no debería ocurrir

---

### La primera ejecución es muy lenta

**Es normal.** La primera vez:

1. Descarga 3 scripts de IMSDB (~5s)
2. Genera embeddings con OpenAI (~30-60s)
3. Guarda en disco

Las siguientes ejecuciones cargan directamente (~1s).

---

### Las respuestas son lentas

Posibles causas:

- **Latencia de OpenAI API** — depende de su servicio
- **Conexión lenta** — verifica tu internet
- **Contexto largo** — preguntas complejas usan más contexto

---

### El bot no recuerda lo que le dije antes

El sistema recuerda solo las **últimas 5 interacciones**. Si hiciste más preguntas, el contexto antiguo se descarta.

Además, el historial **no persiste entre sesiones**. Si cierras y abres la app, empieza desde cero.

---

## Funcionalidades

### ¿Puedo cambiar el modelo de OpenAI?

Sí, editando `config.py`:

```python
LLM_MODEL = "gpt-4o"  # Cambiar a otro modelo
```

Después de cambiar, ejecuta normalmente.

---

### ¿Puedo agregar más películas?

Técnicamente sí, pero requiere:

1. Encontrar URLs de scripts en formato similar
2. Agregar a `STAR_WARS_SCRIPTS` en `config.py`
3. Borrar `./qdrant_db` y re-ejecutar

> ⚠️ Esta funcionalidad no está oficialmente soportada.

---

### ¿Hay versión web o móvil?

No. Actualmente es solo aplicación de terminal (CLI).

Está en el roadmap para v2.0, pero sin fecha estimada.

---

## Troubleshooting Avanzado

### ¿Cómo reconstruyo el índice desde cero?

```bash
rm -rf ./qdrant_db
uv run main.py
```

Útil si cambias configuración de chunks o modelo de embeddings.

---

### ¿Cómo actualizo las dependencias?

```bash
uv lock --upgrade
uv sync
```

---

### ¿Cómo ejecuto los tests?

```bash
# Tests rápidos (sin API)
uv run pytest tests/ -m "not integration"

# Tests completos (requiere API key)
uv run pytest tests/ -v
```
