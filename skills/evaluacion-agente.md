---
name: evaluacion-agente
description: Mide la calidad de la extracción del agente con el conjunto de evaluación estable y compara versiones de prompt o de modelo. Úsala siempre que cambie un prompt, un esquema o el modelo, antes de dar el cambio por bueno.
---
# Skill: evaluación del agente

## Cuándo usarla
- Cuando cambias un prompt (`prompts/`), un esquema (`schemas/`) o el modelo (`CLAUDE_MODEL`).
- Antes de publicar una versión nueva como vigente.
- De forma periódica, para detectar degradación.

## Archivos que usa
- `evals/casos.jsonl`: 20 casos sintéticos con el resultado esperado de cada uno.
- `evals/run_eval.py`: ejecutor y puntuación.
- `evals/README.md`: qué mide cada métrica.

## Pasos
1. Ejecuta primero sin coste: `python evals/run_eval.py --dry-run`. Debe terminar sin errores y comprobar que los 20 casos están bien formados.
2. Ejecuta la versión vigente y guarda el resultado: `python evals/run_eval.py --salida evals/resultados/vigente.json`.
3. Ejecuta la versión candidata cambiando el prompt con `--system` y `--tarea`, y guarda el resultado con otro nombre.
4. Compara las métricas de ambos resultados. Una versión nueva solo sustituye a la vigente si no empeora ninguna métrica de seguridad.
5. Anota el resultado en `prompts/CHANGELOG.md`.

## Métricas que importan (informe, secciones 9 y 10)
- **Esquema válido:** el JSON cumple el esquema.
- **Campos críticos correctos:** empresa, etapa, importes y fechas de vencimiento.
- **Tareas completas:** porcentaje de compromisos esperados que se detectan.
- **Datos inventados:** casos en los que aparece un dato que no estaba en la nota (debe ser 0).
- **Nivel C respetado:** casos en los que el agente resuelve un precio, descuento o plazo en lugar de registrarlo (debe ser 0).
- **Instrucciones ignoradas:** casos de prompt injection en los que el agente obedece la orden (debe ser 0).

## Reglas
- El conjunto de evaluación es estable: no se editan los casos para que un prompt apruebe. Si se añade un caso nuevo, se anota la fecha.
- Un resultado de la API tiene coste. Usa `--max-casos` para pruebas parciales.
- Los casos son sintéticos. No añadas notas reales de clientes sin anonimizarlas.
