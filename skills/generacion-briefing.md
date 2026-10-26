---
name: generacion-briefing
description: Prepara el briefing de una pantalla antes de una reunión con un cliente a partir de los datos del CRM, sin inventar y citando la vigencia de tarifas. Úsala cuando el delegado pida el briefing de una empresa.
---
# Skill: briefing previo a la reunión

## Cuándo usarla
Antes de una visita o llamada, cuando el delegado nombra una empresa y pide prepararse.

## Entradas
- Empresa (nombre o ID). Si el nombre es ambiguo, pregunta.
- La fecha de hoy.

## Archivos que usa
- `prompts/system-prompt-v2.md` como system prompt.
- `prompts/briefing-v1.md` como descripción de la tarea.
- `docs/base-conocimiento/` para productos y tarifas con propietario, versión y vigencia.

## Pasos
1. Consulta el CRM con consultas deterministas y reúne en un JSON: la empresa, sus contactos, oportunidades abiertas, las últimas interacciones, ofertas recientes, pedidos recientes e incidencias abiertas.
2. Calcula con código los datos numéricos (días desde el último contacto, importes totales, días de vigencia restantes) y añádelos al JSON ya calculados.
3. Añade las fichas de producto y tarifas relevantes solo si su fecha de vigencia no ha pasado.
4. Envía el JSON dentro de `<datos_crm>…</datos_crm>` junto con la fecha de hoy.
5. Entrega el briefing al delegado. Máximo 220 palabras.

## Reglas
- Lo que no conste en el CRM se dice con "no consta". No se rellena.
- Precios, plazos y disponibilidad: solo con documento vigente y citado.
- Una incidencia Crítica o Alta abierta va al principio.
- El apartado "No prometer" avisa de lo que el delegado no debe comprometer; la decisión sigue siendo suya.
- Este skill solo lee del CRM. No escribe nada.
