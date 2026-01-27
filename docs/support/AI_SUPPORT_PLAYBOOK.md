# AI Support Playbook — Star Wars Expert

## Clasificación de Solicitudes

### 1. Duda General

**Señales:** "¿Cómo...?", "¿Qué hace...?", "¿Puedo...?"

**Ejemplos:**

- "¿Cómo instalo la aplicación?"
- "¿Qué películas cubre?"
- "¿Puedo preguntar sobre The Mandalorian?"

**Acción:** Responder con información de este knowledge base o FAQ.

---

### 2. Problema de Uso

**Señales:** "No funciona", "No me responde", "Sale error"

**Ejemplos:**

- "El bot no responde a mis preguntas"
- "Dice que no tiene información sobre Luke"
- "Las respuestas son muy lentas"

**Acción:** Seguir árbol de diagnóstico en sección 4.

---

### 3. Bug / Error Técnico

**Señales:** Tracebacks, mensajes de error específicos, comportamiento inesperado reproducible

**Ejemplos:**

- "RuntimeError: Failed to load script"
- "Missing required environment variables"
- "El programa crashea al iniciar"

**Acción:** Verificar runbooks en [CALIDAD_Y_OPERACION.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/CALIDAD_Y_OPERACION.md#6-runbooks-operativos).

---

### 4. Sugerencia / Mejora

**Señales:** "Sería bueno que...", "¿Podrían agregar...?", "Estaría cool si..."

**Ejemplos:**

- "Podrían agregar las precuelas"
- "Sería útil una interfaz web"
- "Quiero exportar mis conversaciones"

**Acción:** Documentar solicitud. Ver roadmap en [CALIDAD_Y_OPERACION.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/CALIDAD_Y_OPERACION.md#7-roadmap).

---

## Preguntas de Aclaración

### Para Problemas de Uso

1. "¿Qué mensaje exacto ves en la terminal?"
2. "¿Es la primera vez que ejecutas la aplicación?"
3. "¿Existe el directorio `qdrant_db` en tu carpeta del proyecto?"
4. "¿Configuraste el archivo `.env` con tu API key de OpenAI?"

### Para Errores Técnicos

1. "¿Puedes copiar el mensaje de error completo?"
2. "¿Qué versión de Python tienes? (`python --version`)"
3. "¿Tienes conexión a internet estable?"
4. "¿El error ocurre siempre o solo a veces?"

---

## Árbol de Diagnóstico

### Error: "Missing required environment variables"

```
¿Existe el archivo .env?
├─ NO → Crear: cp .env.example .env
└─ SÍ → ¿Tiene OPENAI_API_KEY?
         └─ NO → Agregar: OPENAI_API_KEY=sk-...
```

### Error: "OpenAI API Quota Exceeded"

```
→ La cuenta de OpenAI no tiene créditos
→ Verificar en: https://platform.openai.com/account/billing
→ Agregar créditos o esperar reset mensual
```

### Error: "Invalid API Key"

```
¿La key está correctamente copiada en .env?
├─ NO → Corregir formato: OPENAI_API_KEY=sk-...
└─ SÍ → ¿La key existe en OpenAI dashboard?
         ├─ NO → Crear nueva key
         └─ SÍ → ¿Está activa (no revocada)?
                  └─ NO → Crear nueva key
```

### Error: "Failed to load script"

```
¿Tienes conexión a internet?
├─ NO → Conectar y reintentar
└─ SÍ → ¿imsdb.com está accesible?
         ├─ NO → Esperar y reintentar (el sitio puede estar caído)
         └─ SÍ → ¿Existe ./qdrant_db?
                  └─ SÍ → No necesita descargar, investigar otro error
```

### Respuestas incorrectas o vacías

```
¿La pregunta es sobre trilogía original?
├─ NO → Explicar alcance limitado a Ep. IV-VI
└─ SÍ → ¿Es sobre personajes principales?
         ├─ NO → Puede no estar en scripts (personajes menores)
         └─ SÍ → Reportar como posible bug
```

---

## Cuándo Escalar

### Escalar a Producto/Tech cuando

| Señal | Razón |
|-------|-------|
| Error reproducible no documentado | Posible bug nuevo |
| Múltiples usuarios reportan mismo issue | Problema sistémico |
| Solicitud de feature con alta demanda | Priorización de roadmap |
| Respuestas incorrectas sobre contenido conocido | Problema de RAG |
| Crashes aleatorios sin patrón claro | Debugging profundo requerido |

### NO escalar cuando

- Usuario no configuró `.env` correctamente
- Pregunta sobre contenido fuera de alcance (precuelas, etc.)
- Problemas de conexión del lado del usuario
- Solicitudes ya en roadmap

---

## Templates de Respuesta

### Bienvenida

```
¡Hola! Soy el asistente de soporte para Star Wars Expert. 
¿En qué puedo ayudarte hoy?
```

### Alcance Limitado

```
Star Wars Expert solo cubre la trilogía original:
- Episode IV: A New Hope
- Episode V: The Empire Strikes Back  
- Episode VI: Return of the Jedi

Personajes como [X] aparecen en otras películas que no están incluidas.
```

### Problema de API Key

```
Parece que tu API key no está configurada. Sigue estos pasos:

1. Crea el archivo .env: `cp .env.example .env`
2. Obtén tu API key en https://platform.openai.com/api-keys
3. Agrega la key al archivo .env: `OPENAI_API_KEY=tu-key-aquí`
4. Ejecuta de nuevo: `uv run main.py`
```

### Bug Confirmado

```
Gracias por reportar este problema. Lo he documentado para el equipo técnico.
Mientras tanto, puedes intentar:
1. Borrar ./qdrant_db y reiniciar
2. Actualizar dependencias: `uv sync`

Te notificaremos cuando haya una solución.
```
