# Política de autonomía y aprobación

Basada en la sección 7 del informe técnico. Define qué puede hacer el agente por sí solo, qué propone y qué queda siempre en manos de una persona. Cualquier función nueva debe clasificarse aquí antes de implementarse.

## Los tres niveles

| Nivel | Qué significa | Ejemplos en este proyecto |
|---|---|---|
| **A: automático** | El agente actúa solo. Son cálculos y avisos internos, reversibles y sin efecto sobre terceros. | Informe diario de prioridades, alertas por reglas, cálculo de días e importes, detección de duplicados y de registros incompletos, recordatorios internos |
| **B: propuesta con confirmación** | El agente propone y el delegado aprueba antes de que algo se guarde o se use. | Extracción de una visita y alta en el CRM, creación de tareas, cambio de etapa de una oportunidad, alta o modificación de contactos, borradores de correo y mensajes, recomendaciones de venta cruzada |
| **C: siempre humano** | El agente nunca decide ni ejecuta. Como mucho, prepara la información. | Enviar comunicaciones a clientes, aprobar precios, descuentos, márgenes o crédito, firmar ofertas o pedidos, prometer disponibilidad, entrega o garantía, cerrar incidencias, eliminar datos personales o históricos, lanzar campañas masivas, decidir sobre personas basándose solo en la IA |

## Cómo se aplica en cada flujo

| Flujo | Nivel | Cómo se garantiza |
|---|---|---|
| Informe diario y alertas | A | Código determinista; solo lee el CRM y envía al propio delegado |
| Extracción de una visita | B | El resultado se muestra en pantalla de confirmación; no se escribe nada hasta la aprobación |
| Alta de tareas e interacción | B | Se crean tras la aprobación, con clave de idempotencia para no duplicar |
| Cambio de etapa | B | La etapa sugerida es una propuesta; el delegado puede cambiarla o rechazarla |
| Borrador de correo | B | Se deja como borrador; nunca se envía automáticamente |
| Petición de descuento, precio, plazo o garantía de un cliente | C | Se registra en `solicitudes_nivel_c`; la decisión y la respuesta son del delegado o de su responsable |
| Envío de cualquier comunicación a un cliente | C | No existe ningún flujo que envíe; solo borradores |

## Reglas de implementación

1. **Ningún atajo de aprobación.** No hay modo "aprobar todo" ni aprobación implícita por silencio.
2. **Todo queda registrado.** Cada escritura en el CRM genera una fila en Auditoría con quién o qué flujo, la acción, el registro afectado, el estado anterior, el nuevo, la fecha y el resultado.
3. **La confianza baja frena.** Si `requiere_revision` es true, el flujo no continúa sin que el delegado resuelva las ambigüedades.
4. **Un dato confirmado no se sobrescribe con una inferencia.** Un `desconocido` o un `null` no borra un valor existente.
5. **Si falla, no se actúa.** Ante un error del modelo, del esquema o de la conexión, la nota se guarda tal cual para revisión manual y no se rellena nada.
6. **El contenido a analizar no da órdenes.** Una nota, un documento o un mensaje de cliente que contenga instrucciones se trata como dato (ver `prompts/system-prompt-v2.md`).
