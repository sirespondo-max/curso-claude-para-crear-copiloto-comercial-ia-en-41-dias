# Arquitectura

Resume cómo encajan las piezas del Copiloto Comercial. Sigue el principio del informe: gratuito o autoalojado por defecto, un solo orquestador y cada pieza sustituible.

## Visión general

```
 Delegado
    │  texto de la visita (escrito, o transcrito con WhatsApp / grabadora de bolsillo)
    ▼
 Telegram (bot) ─────────────► n8n Community
                                  │
          ┌───────────────────────┼─────────────────────────┐
          ▼                       ▼                         ▼
   Validación de entrada    API de Claude            Reglas y cálculos
   (idempotencia, longitud) (extracción con          (fechas, importes,
                             salida estructurada)     prioridades)
          │                       │                         │
          └───────────────────────┼─────────────────────────┘
                                  ▼
                  Pantalla de confirmación en Telegram
                       (el delegado revisa y corrige)
                                  │ aprobado
                                  ▼
                       CRM en Baserow (12 tablas)
                 Interacciones · Tareas · Oportunidades · Auditoría
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
            Borrador de correo           Briefing e informes
            (nunca se envía solo)        (GitHub Actions programado)
```

## Entrada: múltiples canales, un solo pipeline

| Canal | Cómo llega el texto | Notas |
|---|---|---|
| Telegram, texto escrito | Directamente al bot | Canal automatizado principal |
| WhatsApp (nota de voz) | El delegado usa la transcripción nativa de WhatsApp, copia el texto y se lo envía al bot | La transcripción nativa se genera en el móvil para una persona; un bot no puede leerla. Por eso hace falta copiarla |
| Grabadora de bolsillo (tipo Plaud) | Exportar o copiar la transcripción de su app y enviarla al bot | Opcional |

No se automatiza la lectura directa de WhatsApp: la API oficial exige aprobación y las alternativas no oficiales pueden incumplir sus condiciones de servicio y arriesgar el bloqueo del número.

## Flujo de una visita (Nivel B)

1. **Recibir** el texto en Telegram y calcular una clave de idempotencia (fecha, chat y hash del texto). Si ya existe, avisar y parar.
2. **Extraer** con la API de Claude: system prompt vigente más `prompts/extraccion-visita-v1.md`, esquema `schemas/extraccion-visita.schema.json`, salida estructurada (`output_config.format`).
3. **Validar** el JSON contra el esquema. Si `stop_reason` es `refusal` o `max_tokens`, o el JSON no valida, ir a la rama de error.
4. **Identificar** empresa y contacto en Baserow. Si hay ambigüedad (`identificacion_ambigua` o varias coincidencias), preguntar al delegado.
5. **Confirmar:** mostrar resumen, transcripción esquematizada, compromisos con fecha, etapa sugerida y ambigüedades. El delegado corrige lo que haga falta y aprueba.
6. **Escribir** en Baserow solo tras la aprobación: Interacción (con la nota original), Tareas, y la etapa o próxima acción de la Oportunidad si el delegado lo acepta. Registrar cada escritura en Auditoría.
7. **Preparar** un borrador de correo de seguimiento (Gmail, solo borrador).

## Rama de error y degradación segura

- Reintentos limitados (uno o dos) ante fallos temporales de la API.
- Si no se consigue una extracción válida: guardar la nota original como Interacción con `resultado` "Pendiente de revisión", avisar al delegado y no rellenar ningún otro campo.
- Los errores quedan en una cola visible para revisarlos, no se pierden.

## Qué hace GitHub Actions

| Workflow | Cuándo | Qué hace | Coste |
|---|---|---|---|
| `validar-estructura.yml` | En cada push y pull request | Comprueba estructura, esquemas, enumeraciones y workflows | Ninguno (sin IA) |
| `eval-extraccion.yml` | Solo a mano | Ejecuta el conjunto de evaluación contra la API de Claude | Llamadas a la API |
| `informe-diario.yml` | Programado, laborables por la mañana, y a mano | Lee Baserow, calcula las cinco prioridades y las alertas y las envía por Telegram | Ninguno (sin IA) |

## Lo que este repositorio no incluye

- **La exportación de los flujos de n8n.** n8n se ejecuta en tu propia instancia. Cuando tengas los flujos funcionando, expórtalos desde n8n (menú del flujo, Download) y guárdalos en una carpeta `n8n/` para versionarlos. Revisa antes que no contengan credenciales.
- **Datos reales.** Todo el contenido de ejemplo es sintético.

## Evolución prevista

Cuando el circuito principal sea fiable (nota, datos, confirmación, CRM, briefing) se incorporan, por este orden: pipeline y ofertas, posventa, prospección y rutas. La predicción de cierre, el riesgo de abandono y la venta cruzada requieren histórico de pedidos limpio, idealmente de 12 meses o más.
