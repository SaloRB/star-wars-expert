# AI Support Context — Star Wars Expert

## Identidad del Producto

**Star Wars Expert** es un chatbot de línea de comandos que responde preguntas sobre la **trilogía original de Star Wars** (Episodios IV, V, VI) usando los scripts reales de las películas.

### Quick Facts

| Atributo | Valor |
|----------|-------|
| Tipo | CLI chatbot (terminal) |
| Stack | Python + LangChain + OpenAI |
| Fuente de datos | Scripts de IMSDB.com |
| Cobertura | Solo trilogía original (A New Hope, Empire Strikes Back, Return of the Jedi) |
| Idioma | Inglés |
| Usuarios | Single-user, local |

---

## Capacidades del Sistema

### ✅ El sistema PUEDE

1. Responder preguntas sobre personajes, diálogos y escenas de Episodios IV-VI
2. Citar diálogos específicos de los scripts
3. Mantener contexto de las últimas 5 interacciones
4. Sugerir 3 preguntas relacionadas después de cada respuesta
5. Funcionar offline después de la primera indexación (excepto generación de respuestas)

### ❌ El sistema NO PUEDE

1. Responder sobre precuelas, secuelas o spin-offs
2. Generar fanfiction o contenido creativo
3. Recordar conversaciones entre sesiones
4. Funcionar sin conexión a OpenAI API
5. Soportar múltiples usuarios simultáneos
6. Ofrecer interfaz web o móvil

---

## Comandos Disponibles

| Comando | Acción |
|---------|--------|
| *cualquier texto* | Enviar pregunta |
| `clear` | Limpiar historial de conversación |
| `exit` / `quit` | Terminar sesión |

---

## Arquitectura Simplificada

```
Usuario → Terminal → RAG Chain → OpenAI → Respuesta con sugerencias
                         ↓
              Qdrant (scripts indexados)
```

---

## Referencias a Documentación

| Tema | Archivo |
|------|---------|
| Instalación y uso | [README.md](file:///Users/salo/dev/langchain/star-wars-expert/README.md) |
| Funcionalidad completa | [DOCUMENTACION_FUNCIONAL.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/DOCUMENTACION_FUNCIONAL.md) |
| Arquitectura técnica | [ARQUITECTURA_TECNICA.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/ARQUITECTURA_TECNICA.md) |
| Operación y troubleshooting | [CALIDAD_Y_OPERACION.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/CALIDAD_Y_OPERACION.md) |
