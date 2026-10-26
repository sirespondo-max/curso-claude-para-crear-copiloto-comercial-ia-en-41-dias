---
name: extraccion-visita
description: Convierte el texto de una visita o llamada comercial en datos estructurados para el CRM, con transcripción esquematizada, ambigüedades y confianza. Úsala cuando el delegado envíe la nota de una interacción con un cliente.
---
# Skill: extracción de una visita

## Cuándo usarla
Cuando llega texto de lo ocurrido en una visita o llamada: escrito a mano, o transcrito por WhatsApp o por una grabadora de bolsillo. La entrada es siempre texto; este proyecto no procesa audio.

## Entradas
- El texto de la nota.
- La fecha de hoy (AAAA-MM-DD), para resolver "mañana" o "el viernes".

## Archivos que usa
- `prompts/system-prompt-v2.md` (vigente) como system prompt.
- `prompts/extraccion-visita-v1.md` como descripción de la tarea.
- `schemas/extraccion-visita.schema.json` como formato de salida.

## Pasos
1. Compón el system prompt: contenido de `system-prompt-v2.md` más una línea en blanco más `extraccion-visita-v1.md` (sin la cabecera `---`).
2. Envía como mensaje de usuario: la fecha de hoy y la nota dentro de `<nota>…</nota>`.
3. Pide la respuesta con salida estructurada (`output_config.format` de tipo `json_schema`) usando el esquema.
4. Comprueba `stop_reason`: si es `refusal` o `max_tokens`, no uses la salida; reintenta una vez con más `max_tokens` o pasa a revisión manual.
5. Valida el JSON contra el esquema y compara las opciones de selección sin distinguir mayúsculas.
6. Muestra al delegado la pantalla de confirmación (resumen, transcripción esquematizada, compromisos con fecha, etapa sugerida, ambigüedades) y deja que corrija cualquier campo.
7. Solo tras la aprobación explícita, escribe en el CRM (Nivel B). Un dato `desconocido` o `null` no sobrescribe un valor ya confirmado.

## Qué se escribe en el CRM tras la aprobación
- Interacciones: fecha, tipo, participantes, resumen (la transcripción esquematizada revisada), fuente y resultado.
- Tareas: una por compromiso, con responsable, vencimiento y prioridad.
- Oportunidades: etapa y próxima acción, solo si el delegado acepta el cambio.
- Auditoría: una fila por cada escritura, con el estado anterior y el nuevo.

## Reglas
- Nunca resuelvas las `solicitudes_nivel_c`: se registran y las decide el delegado.
- Si `requiere_revision` es true o `identificacion_ambigua` es true, pregunta antes de continuar.
- Idempotencia: usa una clave (fecha, empresa y hash del texto) para no crear interacciones o tareas duplicadas si se reenvía la nota.
- Guarda la nota original junto a la extracción aprobada.
