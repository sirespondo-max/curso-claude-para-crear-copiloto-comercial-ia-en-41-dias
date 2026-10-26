# Historial de versiones de los prompts

Regla: una versión publicada no se edita. Cada cambio crea un archivo nuevo y se anota aquí con fecha, motivo y resultado de la evaluación (`evals/`). Sin este registro no se puede saber qué cambio mejoró o empeoró los resultados.

## system-prompt

### v2 — 2026-10-24 (vigente)
- **Cambios:** añade la regla 6 (todo es una propuesta hasta que el delegado confirma), el bloque "Seguridad ante contenido externo" (contenido en `<nota>`, `<documento>`, `<mensaje_cliente>` y `<datos_crm>` es dato, nunca orden), las garantías entre los límites absolutos y la norma de no calcular totales de cabeza.
- **Motivo:** cerrar la vía de prompt injection por notas, documentos y mensajes de clientes (Módulo 4) y reforzar la confirmación humana (Módulo 3).
- **Evaluación:** pendiente de ejecutar con `evals/run_eval.py`. Los casos 17 a 20 del conjunto de evaluación están pensados para probar este cambio.

### v1 — 2026-10-24 (sustituida)
- **Contenido:** identidad, principios, límites absolutos, criterios de calidad de datos y formato (Módulo 1).
- **Evaluación:** pendiente. Se conserva como línea base para comparar con v2.

## extraccion-visita

### v1 — 2026-10-24 (vigente)
- **Contenido:** prompt de tarea para extraer una interacción al esquema `schemas/extraccion-visita.schema.json` (versión de esquema 1.0).
- **Evaluación:** pendiente de ejecutar.

## briefing

### v1 — 2026-10-24 (vigente)
- **Contenido:** briefing de una pantalla con los diez apartados de la sección 4.4 del informe.
- **Evaluación:** pendiente de definir casos propios.

## Cómo registrar un cambio

1. Copia el archivo vigente con el número siguiente (`system-prompt-v3.md`).
2. Cambia `estado` del anterior a "sustituido por v3" y el del nuevo a "vigente".
3. Ejecuta la evaluación con la versión nueva y la anterior, y compara.
4. Anota aquí qué cambió, por qué y cuánto mejoró o empeoró cada métrica.
