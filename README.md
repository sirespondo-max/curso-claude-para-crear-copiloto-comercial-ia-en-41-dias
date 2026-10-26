# Curso de Claude para crear un Copiloto Comercial de IA en 41 días

**Aprende Claude haciendo, no leyendo: construye paso a paso un asistente de IA para un delegado de ventas, usando una cuenta gratuita de Claude.**

Este curso está pensado para quien nunca ha usado Claude de forma seria ni ha programado, pero ya se maneja con el ordenador y ha probado algún chatbot de IA. Al terminar tendrás dos cosas: un agente comercial funcionando y las competencias para diseñar cualquier otro agente de IA.

---

## Pensado para una cuenta gratuita de Claude

Todo el diseño del curso parte de una limitación real: la cuenta gratuita de [claude.ai](https://claude.ai) tiene un límite diario de mensajes. Por eso el curso no se hace en sesiones largas, sino en **lecciones diarias cortas**:

- **Una lección al día, con pocos mensajes al chat.** Los días con más pruebas contra Claude (extracción de datos, herramientas, evaluación) están repartidos en varios días pequeños en vez de concentrarse en uno.
- **La teoría va en un descargable, no en el chat.** Cada lección tiene su archivo con el resumen de la lección, los deberes y el checklist. Se lee sin gastar mensajes.
- **Los deberes se hacen offline, paso a paso.** Cada proceso técnico está desglosado en pasos numerados, con las URLs exactas y el resultado que debes ver.
- **No se avanza sin completar el día anterior.** Al empezar cada lección, el tutor te pregunta si has marcado todo el checklist. Si falta algo, ese día se dedica a resolverlo.
- **Una conversación por tarea.** El Día 5 enseña a gestionar la ventana de contexto para no malgastar cuota.

> **Una precisión honesta sobre costes:** las lecciones y los ejercicios con el chat funcionan con el plan gratuito de claude.ai. Las automatizaciones que llaman a Claude por **API** (desde n8n o GitHub Actions) se facturan aparte del plan gratuito. El curso las fragmenta para minimizar las llamadas y el resto del stack (Telegram, n8n Community, Baserow) tiene opciones gratuitas o autoalojables, pero conviene que sepas que esa parte no es gratis por defecto.

---

## Qué vas a construir

Un **Copiloto Comercial de IA** para un delegado de ventas de campo. Tras una visita o llamada, le pasas el texto de lo ocurrido y el agente:

- Lo convierte en un resumen estructurado: **nombres, fechas, peticiones, cantidades, productos, objeciones y compromisos**.
- Te lo muestra para que lo **revises y corrijas** antes de guardar nada.
- Registra la información en tu **CRM en Baserow** (12 tablas: Empresas, Contactos, Oportunidades, Interacciones, Tareas, Productos, Ofertas, Pedidos, Incidencias, Documentos, Fuentes y Auditoría).
- Prepara el **briefing de una pantalla** antes de tu próxima reunión con ese cliente.
- Te propone cada mañana tus **5 acciones prioritarias** y te avisa de oportunidades paradas, clientes inactivos u ofertas a punto de caducar.
- Responde sobre catálogo y tarifas **citando la fuente**, y dice "no consta" en vez de inventarse un dato.
- **Nunca decide** descuentos, precios ni plazos, y no envía nada a un cliente: eso lo hace siempre la persona.

La entrada de datos es siempre texto: escrito a mano, o transcrito por la función nativa de WhatsApp (o por una grabadora de bolsillo tipo Plaud) y copiado. No necesitas instalar ningún programa de transcripción.

---

## Qué aprenderás (y podrás aplicar a cualquier otro proyecto)

| Competencia | Para qué sirve más allá de este curso |
|---|---|
| Prompt engineering con roles, límites y ejemplos | Delegar cualquier tarea a una IA con resultados fiables |
| Salida estructurada (JSON Schema) | Convertir texto libre en datos que un sistema pueda usar |
| Automatización con control humano (niveles A/B/C) | Decidir qué puede hacer una IA sola y qué debe aprobar una persona |
| RAG sin alucinaciones | Responder sobre normativa, documentación o políticas con fuente |
| Seguridad frente a prompt injection | Proteger a un agente que procesa contenido externo |
| Tool Use y MCP | Conectar una IA a CRMs, bases de datos y otras herramientas |
| Evaluación de agentes | Medir con datos si un sistema con IA funciona de verdad |
| Estructura de proyecto y GitHub Actions | Organizar y automatizar cualquier proyecto con Claude |

---

## Programa: 41 lecciones diarias

| Módulo | Contenido | Días |
|---|---|---|
| Presentación | Qué vas a construir y qué te llevas | Día 0 |
| 1. Fundamentos | Prompting, system prompt, modelo de datos en Baserow, ventana de contexto | Días 1–5 |
| 2. Extracción de datos | De la nota de una visita a JSON estructurado | Días 6–11 |
| 3. Automatización y control humano | Niveles A/B/C, n8n, confirmación humana, canales de entrada | Días 12–17 |
| 4. RAG y briefings | Catálogo sin alucinaciones, briefing previo, prompt injection | Días 18–23 |
| 5. Funciones avanzadas | Tool use, MCP, prioridades diarias, alertas | Días 24–29 |
| 6. Despliegue y evaluación | RGPD, logs, fallback, eval set | Días 30–34 |
| 7. Estructura de proyecto y GitHub Actions | `CLAUDE.md`, skills, workflows automáticos | Días 35–40 |
| Proyecto integrador | Ensamblaje y evaluación final del agente | Día 41 |

---

## Cómo seguir el curso

1. Crea una cuenta gratuita en [claude.ai](https://claude.ai) y otra en [Baserow](https://baserow.io).
2. Abre una conversación nueva con Claude.
3. Pega el contenido de [`prompt_maestro_curso_claude.md`](prompt_maestro_curso_claude.md) y adjunta [`informe_final_agente_ia_delegado_comercial.md`](informe_final_agente_ia_delegado_comercial.md), que es la especificación técnica del proyecto.
4. Claude actuará como tu tutor: te presentará el curso y te entregará el descargable de cada día.
5. Haz los deberes, marca el checklist y vuelve a la conversación diciendo "listo día N".

---

## Las lecciones diarias

Con cada lección recibirás un **descargable propio**, generado por el tutor en la conversación, con tres partes:

1. **Resumen de la lección:** el material didáctico para leer offline.
2. **Deberes offline:** pasos numerados, con URLs y el resultado esperado en cada paso.
3. **Checklist final:** para confirmar que todo está hecho antes de pasar al día siguiente.

Los descargables diarios **no se incluyen en este repositorio**: los genera Claude durante el curso, adaptados a tu avance.

---

## Contenido del repositorio

Es el resultado final del curso: el Copiloto Comercial completo, con datos sintéticos. Los descargables diarios no se incluyen.

| Ruta | Qué es |
|---|---|
| [`prompt_maestro_curso_claude.md`](prompt_maestro_curso_claude.md) | El prompt que convierte a Claude en tutor del curso |
| [`informe_final_agente_ia_delegado_comercial.md`](informe_final_agente_ia_delegado_comercial.md) | Especificación técnica del agente en la que se basa todo el curso |
| [`CLAUDE.md`](CLAUDE.md) | Instrucciones persistentes y reglas inviolables del agente |
| [`about-me.md`](about-me.md) | Contexto del usuario y del escenario de ejemplo |
| [`prompts/`](prompts) | System prompts y prompts de tarea, versionados |
| [`schemas/`](schemas) | Esquema de extracción de visitas y esquema del CRM en Baserow |
| [`skills/`](skills) | Tareas reutilizables documentadas |
| [`docs/`](docs) | Política de autonomía, privacidad, arquitectura, base de conocimiento y [guía de puesta en marcha](docs/puesta-en-marcha.md) |
| [`evals/`](evals) | 20 casos de evaluación y su ejecutor |
| [`scripts/`](scripts) | Validación de estructura e informe diario de prioridades |
| [`.github/workflows/`](.github/workflows) | Validación en cada cambio, evaluación manual e informe diario |

---|---|
| [`prompt_maestro_curso_claude.md`](prompt_maestro_curso_claude.md) | El prompt que convierte a Claude en tutor del curso |
| [`informe_final_agente_ia_delegado_comercial.md`](informe_final_agente_ia_delegado_comercial.md) | Especificación técnica del agente en la que se basa todo el curso |

---

## Stack

- **Claude** (chat, y API en los módulos de automatización) como motor de inteligencia
- **Baserow** como CRM
- **Telegram** como canal de entrada del agente
- **n8n Community** para orquestar los flujos
- **GitHub y GitHub Actions** para versionar y automatizar

Principio de diseño: gratuito o autoalojado por defecto, y sustituible cuando el uso crezca.

---

## Licencia

Este repositorio se distribuye bajo la licencia [MIT](LICENSE). Puedes usar, copiar, modificar y compartir su contenido, siempre que mantengas el aviso de copyright y el texto de la licencia.

---

## Autoría

Curso creado por **Anibal Pedreño** como proyecto de aprendizaje y portfolio profesional en ventas con IA.
