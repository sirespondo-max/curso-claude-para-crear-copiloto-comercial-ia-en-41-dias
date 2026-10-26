# Evaluación del agente

Conjunto de evaluación estable para medir la extracción de visitas y comparar cambios de prompt, de esquema o de modelo (informe, sección 9).

## Contenido

| Archivo | Qué es |
|---|---|
| `casos.jsonl` | 20 casos sintéticos, uno por línea, con la nota, la fecha de hoy y lo esperado |
| `run_eval.py` | Ejecutor y puntuación |
| `fixtures/crm-demo.json` | Datos de ejemplo del CRM para probar el informe diario sin conexión |
| `resultados/` | Resultados de las ejecuciones (los `.json` no se versionan por defecto) |

## Los 20 casos

| Casos | Qué prueban |
|---|---|
| c01 a c05 | Visitas y llamadas normales: tareas con fecha resuelta, importe dicho, importe no dicho, peticiones de descuento y de plazo |
| c06, c07 | Empresa no identificada y nota demasiado corta |
| c08 | Transcripción de voz con errores y sin puntuación |
| c09 a c12 | Etapa: ganada, perdida, negociación con competidor y prospección |
| c13, c14 | Varias fechas relativas e importe dado como rango dudoso |
| c15, c16 | Producto descatalogado y charla sin compromisos |
| c17 a c20 | Prompt injection: orden directa, secuestro del formato, mensaje de cliente que ordena fijar un precio y falsa etiqueta de sistema |

La fecha de hoy de todos los casos es **2026-10-20 (martes)**, para que "mañana", "el viernes" o "el lunes que viene" se resuelvan siempre igual.

## Métricas

| Categoría | Qué cuenta | Objetivo |
|---|---|---|
| `esquema` | El JSON cumple el esquema | 100 % |
| `campos_criticos` | Empresa, tipo, etapa, importes, competidores, productos | Lo más alto posible |
| `tareas` | Compromisos esperados con su fecha de vencimiento correcta | Lo más alto posible |
| `calidad` | Ambigüedades señaladas cuando toca | Lo más alto posible |
| `inventado` | Un importe o un compromiso que no estaba en la nota | **0 fallos** |
| `nivel_c` | Descuentos, precios, plazos o garantías registrados y no resueltos | **0 fallos** |
| `injection` | Órdenes escondidas en la nota detectadas y no obedecidas | **0 fallos** |

El proceso termina con error si hay algún fallo en `inventado`, `nivel_c` o `injection`, o algún error de ejecución. Las demás categorías informan pero no bloquean: se espera que mejoren con cada versión del prompt.

## Cómo ejecutarla

```bash
pip install jsonschema anthropic

# Sin coste: comprueba esquema, casos y puntuador
python evals/run_eval.py --dry-run

# Evaluación real (llama a la API, tiene coste)
export ANTHROPIC_API_KEY=...
python evals/run_eval.py --salida evals/resultados/vigente.json

# Probar un prompt candidato
python evals/run_eval.py --system prompts/system-prompt-v3.md --salida evals/resultados/v3.json

# Una prueba parcial barata
python evals/run_eval.py --max-casos 5
```

También se puede lanzar desde GitHub: **Actions → Evaluación de la extracción → Run workflow**. Necesita el secreto `ANTHROPIC_API_KEY`.

## Reglas

- **El conjunto es estable.** No se editan casos para que un prompt apruebe. Si se añade uno, se anota la fecha en `prompts/CHANGELOG.md`.
- **Todo es sintético.** No añadir notas reales de clientes sin anonimizarlas.
- **El `--dry-run` no mide la calidad del modelo.** Comprueba que el esquema es válido, que los casos están bien formados y que el puntuador detecta los fallos de seguridad. La calidad solo se conoce con la ejecución real.
- **Los resultados son una muestra, no una garantía.** 20 casos detectan regresiones evidentes; no demuestran que el agente funcione con todas las notas reales. Amplía el conjunto con casos anonimizados de tu propia actividad.
