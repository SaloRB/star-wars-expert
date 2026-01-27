# AI Support Knowledge Base — Star Wars Expert

## Glosario de Términos

| Término | Definición |
|---------|------------|
| **RAG** | Retrieval-Augmented Generation. Busca información relevante antes de generar respuesta |
| **Chunk** | Fragmento de texto del script (~2500 caracteres) |
| **Embedding** | Representación numérica del texto para búsqueda semántica |
| **Vector Store** | Base de datos que almacena embeddings (Qdrant) |
| **IMSDB** | Internet Movie Script Database. Fuente de los guiones |
| **Cold Start** | Primera ejecución que descarga e indexa scripts |
| **Warm Start** | Ejecución posterior con índice ya creado |
| **API Key** | Credencial para acceder a servicios de OpenAI |

---

## User Stories Resumidas

| Como... | Quiero... | Para... |
|---------|-----------|---------|
| Usuario | Hacer preguntas sobre Star Wars | Obtener respuestas basadas en scripts reales |
| Usuario | Hacer preguntas de seguimiento | Mantener contexto conversacional |
| Usuario | Ver sugerencias de preguntas | Explorar más temas |
| Usuario | Limpiar historial con `clear` | Empezar conversación nueva |
| Usuario | Salir con `exit` | Terminar sesión |

---

## Flujos Paso a Paso

### Flujo: Primera Instalación

```
1. Clonar repositorio
   $ git clone https://github.com/SaloRB/star-wars-expert.git

2. Entrar al directorio
   $ cd star-wars-expert

3. Instalar dependencias
   $ uv sync

4. Configurar API key
   $ cp .env.example .env
   $ nano .env  # agregar OPENAI_API_KEY=...

5. Ejecutar
   $ uv run main.py
```

### Flujo: Sesión de Chat Típica

```
1. Ejecutar aplicación
2. Esperar banner de bienvenida
3. Escribir pregunta → Enter
4. Esperar respuesta streaming
5. Ver sugerencias al final
6. Repetir 3-5 o escribir "exit"
```

### Flujo: Limpiar y Reiniciar

```
1. Escribir "clear" → Limpia memoria
2. Nueva pregunta parte desde cero
3. Pronombres no se resolverán sin contexto
```

---

## Mapeo de Pantallas/Estados

| Estado | Descripción | Acciones Posibles |
|--------|-------------|-------------------|
| Inicializando | Descargando scripts o cargando índice | Esperar |
| Listo | Banner mostrado, esperando input | Escribir pregunta, clear, exit |
| Procesando | Generando respuesta | Esperar (o Ctrl+C para cancelar) |
| Streaming | Mostrando respuesta caracter por caracter | Leer |
| Error | Mensaje de error mostrado | Seguir instrucciones de error |

---

## Contenido por Película

### Episode IV: A New Hope

**Personajes principales:**

- Luke Skywalker (héroe protagonista)
- Princess Leia Organa
- Han Solo
- Obi-Wan Kenobi (Ben)
- Darth Vader
- C-3PO y R2-D2
- Chewbacca
- Grand Moff Tarkin

**Eventos clave:**

- Robo de planos de la Death Star
- Rescate de Leia
- Destrucción de la Death Star
- Muerte de Obi-Wan

---

### Episode V: The Empire Strikes Back

**Personajes nuevos:**

- Yoda
- Lando Calrissian
- Boba Fett
- Emperor (mención)

**Eventos clave:**

- Batalla de Hoth
- Entrenamiento en Dagobah
- "I am your father"
- Han congelado en carbonita

---

### Episode VI: Return of the Jedi

**Eventos clave:**

- Rescate de Han en Jabba's Palace
- Muerte de Yoda
- Batalla de Endor
- Redención de Vader
- Muerte del Emperor

---

## Límites del Conocimiento

### El sistema CONOCE

- ✅ Diálogos exactos de personajes
- ✅ Descripciones de escenas (INT./EXT.)
- ✅ Nombres de locaciones
- ✅ Secuencia de eventos por película

### El sistema NO CONOCE

- ❌ Behind-the-scenes o producción
- ❌ Lore de libros/cómics/EU
- ❌ Películas fuera de trilogía original
- ❌ Teorías de fans
- ❌ Información de Wikipedia

---

## Señales de Respuesta Incorrecta

| Señal | Posible Causa |
|-------|---------------|
| "I don't have information about that" | Tema fuera de alcance o personaje menor |
| Mezcla información de otras películas | Posible alucinación (reportar) |
| Respuesta genérica sin citas | Chunks recuperados no relevantes |
| Respuesta cortada | Límite de tokens alcanzado |

---

## Referencias Cruzadas

| Tema | Documento | Sección |
|------|-----------|---------|
| Instalación | [README.md](file:///Users/salo/dev/langchain/star-wars-expert/README.md) | Installation |
| Configuración | [README.md](file:///Users/salo/dev/langchain/star-wars-expert/README.md) | Configuration |
| User Stories completas | [DOCUMENTACION_FUNCIONAL.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/DOCUMENTACION_FUNCIONAL.md) | §6 |
| Criterios de aceptación | [DOCUMENTACION_FUNCIONAL.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/DOCUMENTACION_FUNCIONAL.md) | §7 |
| Arquitectura | [ARQUITECTURA_TECNICA.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/ARQUITECTURA_TECNICA.md) | §1-2 |
| Manejo de errores | [ARQUITECTURA_TECNICA.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/ARQUITECTURA_TECNICA.md) | §7 |
| Runbooks | [CALIDAD_Y_OPERACION.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/CALIDAD_Y_OPERACION.md) | §6 |
| Testing | [CALIDAD_Y_OPERACION.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/CALIDAD_Y_OPERACION.md) | §2-3 |
| Roadmap | [CALIDAD_Y_OPERACION.md](file:///Users/salo/dev/langchain/star-wars-expert/docs/CALIDAD_Y_OPERACION.md) | §7 |
