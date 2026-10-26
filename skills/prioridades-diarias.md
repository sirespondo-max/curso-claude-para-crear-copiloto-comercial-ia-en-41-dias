---
name: prioridades-diarias
description: Genera el informe de la mañana con las cinco acciones prioritarias del día y las alertas comerciales, calculadas con reglas deterministas a partir del CRM. Úsala cuando el delegado pida su plan del día o cuando se ejecute el informe programado.
---
# Skill: prioridades diarias y alertas

## Cuándo usarla
- Cada mañana laborable, de forma programada (`.github/workflows/informe-diario.yml`).
- A petición, cuando el delegado pregunte qué debería hacer hoy.

## Archivos que usa
- `scripts/prioridades_diarias.py`: lee el CRM, puntúa y genera el informe.
- `docs/politica-autonomia.md`: este informe es Nivel A (automático, interno).

## Principio
El orden de las prioridades y todos los números salen de código con reglas visibles, no del modelo. Si se usa Claude, es solo para redactar o explicar un resultado ya calculado.

## Reglas de puntuación (por oportunidad abierta)
Cada oportunidad suma puntos y se ordena de mayor a menor. Los pesos están en el script, en un único bloque, para poder revisarlos.
- **Valor potencial:** importe multiplicado por la probabilidad.
- **Etapa:** más peso cuanto más cerca del cierre (Negociación y Propuesta suman más).
- **Días sin contacto:** suma al pasar de 14 días y más al pasar de 30.
- **Sin próxima acción:** suma, porque el informe exige que toda oportunidad abierta tenga una.
- **Fecha prevista próxima o vencida:** suma.
- **Incidencia abierta del cliente:** suma según gravedad (Crítica y Alta pesan más).

## Alertas que genera
- Compromisos (tareas) que vencen hoy o están atrasados.
- Oportunidades abiertas sin próxima acción.
- Oportunidades estancadas (más de 30 días sin interacción).
- Ofertas que caducan en los próximos 7 días.
- Clientes con incidencia Crítica o Alta abierta.
- Clientes activos sin interacción en 30, 60 o 90 días.

## Salida
Texto breve para Telegram: las cinco acciones, cada una con motivo, impacto y plazo, y las alertas agrupadas. Sin recalcular nada.

## Límites
- No envía nada a clientes. Es un informe interno para el delegado.
- Las funciones de frecuencia de compra decreciente y de previsión necesitan histórico de pedidos y están marcadas como experimentales hasta que exista.
