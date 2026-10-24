# Informe final: agente de IA para un delegado comercial

**Versión:** 1.0  
**Fecha:** 21 de agosto de 2026  
**Enfoque:** herramientas gratuitas o autoalojadas como primera opción

## 1. Resumen ejecutivo

El proyecto consiste en crear un **copiloto comercial disponible 24/7** que acompañe al delegado durante todo el ciclo de venta: planificación de cartera, prospección, preparación de visitas, registro de reuniones, seguimiento, elaboración de ofertas, coordinación de pedidos, posventa, fidelización y análisis del negocio.

Su misión no es sustituir al delegado, sino:

- Reducir el tiempo administrativo.
- Evitar olvidos y compromisos vencidos.
- Mejorar la preparación de cada contacto.
- Mantener el CRM actualizado con el mínimo esfuerzo.
- Recomendar la siguiente mejor acción comercial.
- Acelerar el seguimiento y el avance de oportunidades.
- Convertir datos dispersos en prioridades comprensibles.

La solución debe construirse con el principio **“gratuito por defecto y sustituible al crecer”**. Se priorizan herramientas sin coste de licencia, cuotas gratuitas y componentes ejecutados localmente. No obstante, no debe prometerse un funcionamiento “100 % gratuito” sin matices: el autoalojamiento exige equipo, electricidad, mantenimiento, copias de seguridad y, si se necesita acceso continuo desde Internet, posiblemente un servidor o dominio.

La primera versión recomendada se centra en el circuito de mayor valor y menor riesgo:

> **Nota de voz posterior a la visita → transcripción → extracción de datos → confirmación humana → actualización del CRM → creación de tareas → borrador de seguimiento.**

## 2. Alcance y principios del agente

### 2.1 Alcance

El agente debe ayudar en cuatro planos:

1. **Operativo:** registrar visitas, crear tareas, preparar borradores y actualizar datos.
2. **Comercial:** preparar argumentarios, detectar oportunidades y priorizar cuentas.
3. **Analítico:** explicar el pipeline, las previsiones, la actividad y los riesgos.
4. **Organizativo:** mantener agenda, documentación, compromisos y conocimiento comercial.

### 2.2 Principios de diseño

- **Humano al mando:** la IA propone; el delegado valida las decisiones de impacto.
- **Una fuente de verdad:** empresas, contactos, oportunidades y tareas deben tener un registro principal claramente definido.
- **Automatización antes que IA:** si una función puede resolverse con una regla fiable, no debe encargarse a un modelo generativo.
- **Datos estructurados:** los resúmenes narrativos complementan, pero no sustituyen, campos como fecha, importe, estado o responsable.
- **Trazabilidad:** cada dato debe indicar su fuente, fecha y nivel de confianza.
- **Privacidad desde el diseño:** solo se procesa la información necesaria y se establece cuándo se elimina.
- **Degradación segura:** si falla la IA, el audio y la nota original quedan pendientes; nunca se pierden ni se actualiza el CRM con datos dudosos.
- **Modularidad:** CRM, modelo de IA, transcripción y canal móvil pueden sustituirse sin rehacer todo el sistema.

## 3. Mapa integral de procesos del delegado comercial

| Proceso | Funciones del delegado | Apoyo del agente de IA | Control necesario |
|---|---|---|---|
| Planificación de territorio | Segmentar cartera, fijar objetivos, repartir tiempo | Detectar cuentas prioritarias, huecos de cobertura y zonas desatendidas | Validación mensual |
| Plan diario | Revisar agenda, compromisos y urgencias | Generar las cinco acciones prioritarias y explicar por qué | El delegado reordena |
| Prospección | Buscar empresas y decisores | Preparar fichas a partir de fuentes públicas autorizadas | Revisar identidad y fuente |
| Calificación | Determinar encaje, necesidad y potencial | Calcular puntuación mediante reglas y resumir señales | Aprobar cambios importantes |
| Preparación de visita | Revisar historial, incidencias y objetivos | Crear briefing de un minuto y argumentario personalizado | Confirmar datos críticos |
| Organización de ruta | Agrupar visitas y estimar desplazamientos | Proponer orden geográfico y huecos aprovechables | Confirmar agenda y tráfico |
| Reunión o visita | Descubrir necesidades, presentar soluciones y negociar | Mostrar preguntas, catálogo, casos y objeciones | La conversación es humana |
| Registro posterior | Documentar lo hablado | Transcribir audio y extraer resumen, necesidades, objeciones y tareas | Confirmación obligatoria |
| Gestión de oportunidad | Mantener etapa, importe, probabilidad y fecha | Sugerir etapa y próxima acción; detectar estancamientos | Confirmar cambios de etapa |
| Seguimiento | Enviar información y cumplir compromisos | Crear borradores y recordatorios contextualizados | Aprobar antes de enviar |
| Oferta y negociación | Configurar propuesta, precio y condiciones | Redactar explicación y comprobar reglas comerciales | Precio y descuento siempre validados |
| Pedido y coordinación interna | Transferir condiciones a administración, logística o producción | Crear resumen estructurado y avisar de datos ausentes | Confirmación administrativa |
| Posventa | Supervisar entrega, satisfacción e incidencias | Priorizar problemas y evitar acciones comerciales inoportunas | Responsable humano asignado |
| Fidelización | Mantener relación y anticipar necesidades | Alertar por inactividad, caída de pedidos o fechas relevantes | Revisar causa real |
| Venta cruzada | Detectar productos complementarios | Comparar historial con clientes semejantes | Verificar disponibilidad y pertinencia |
| Recuperación | Reactivar cuentas y oportunidades perdidas | Identificar señal de retorno y preparar contacto | Aprobar estrategia |
| Reporting | Informar de actividad, pipeline y previsión | Generar informe semanal con datos y explicación | Revisar excepciones |
| Gestión de conocimiento | Mantener tarifas, catálogo, casos y respuestas | Buscar únicamente en documentos vigentes y citarlos | Propietario de cada documento |
| Administración y cumplimiento | Consentimientos, bajas, conservación y seguridad | Recordar políticas y registrar evidencias | Supervisión de la empresa |

## 4. Funciones del agente

### 4.1 Planificación y priorización

El agente elaborará un informe diario con:

- Agenda y desplazamientos previstos.
- Compromisos que vencen hoy o están atrasados.
- Oportunidades sin próxima acción.
- Clientes importantes con incidencias abiertas.
- Leads nuevos sin atender.
- Ofertas próximas a vencer.
- Clientes cuya frecuencia de compra está disminuyendo.
- Cinco acciones recomendadas, cada una con motivo, impacto y plazo.

La prioridad puede calcularse inicialmente mediante reglas: valor potencial, urgencia, etapa, días sin contacto, probabilidad, incidencia, fecha comprometida y coste de desplazamiento. Solo después de acumular resultados fiables tendría sentido ajustar pesos con métodos predictivos.

### 4.2 Gestión de cartera y territorio

- Clasificación ABC de clientes por facturación, margen, potencial o estrategia.
- Segmentación por sector, tamaño, ubicación, productos y comportamiento.
- Frecuencia de visita recomendada por segmento.
- Detección de cuentas desatendidas.
- Balance entre mantenimiento de cartera y captación.
- Seguimiento de objetivos por zona, producto y periodo.

### 4.3 Prospección y captación

- Importar leads desde formularios, CSV, correo o alta manual.
- Detectar duplicados y normalizar empresa, dominio, teléfono y dirección.
- Completar una ficha con fuentes empresariales públicas autorizadas.
- Registrar fuente y fecha de cada dato externo.
- Crear una hipótesis de necesidad, claramente marcada como inferencia.
- Buscar empresas similares a los mejores clientes por sector y geografía.
- Calcular un *lead score* explicable.
- Proponer el primer canal, mensaje y objetivo de contacto.

No debe plantearse un “rastreo automático de LinkedIn” indiscriminado. La documentación de LinkedIn indica que la mayoría de permisos y programas requieren aprobación explícita, y las integraciones de ventas exigen ser socio de Sales Navigator. Se usarán datos públicos permitidos o acceso oficial autorizado. [Acceso a las API de LinkedIn](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access).

### 4.4 Preparación de reuniones y visitas

El briefing previo debe caber en una pantalla e incluir:

- Empresa, interlocutores y roles.
- Objetivo de la visita.
- Último contacto y compromisos pendientes.
- Compras y ofertas recientes.
- Incidencias o devoluciones abiertas.
- Necesidades y objeciones conocidas.
- Productos relevantes y disponibilidad confirmada.
- Tres preguntas recomendadas.
- Riesgos y aspectos que no deben prometerse.
- Resultado mínimo deseado y siguiente paso propuesto.

### 4.5 Asistencia durante la visita

Sin interferir en la conversación, el agente puede ofrecer:

- Consulta rápida de catálogo, fichas y tarifas vigentes.
- Buscador de casos de éxito por sector.
- Respuestas aprobadas a preguntas frecuentes.
- Comparativas comerciales autorizadas.
- Lista de preguntas de descubrimiento.
- Captura manual de una nota o fotografía.

No deberá grabar conversaciones de forma oculta ni generar afirmaciones sobre precios, plazos, garantías o capacidades que no estén respaldadas por una fuente vigente.

### 4.6 Nota de voz y actualización del CRM

Al terminar la visita, el delegado envía una nota de voz al bot. El flujo será:

1. Guardar temporalmente el audio con identificador y fecha.
2. Transcribirlo localmente.
3. Identificar empresa y contacto; si hay ambigüedad, preguntar.
4. Extraer en formato estructurado:
   - resumen;
   - necesidades;
   - productos mencionados;
   - objeciones;
   - competidores;
   - presupuesto y plazo;
   - decisores;
   - compromisos del cliente;
   - compromisos del comercial;
   - fecha de cada tarea;
   - etapa sugerida;
   - próxima acción.
5. Mostrar una pantalla de confirmación.
6. Actualizar el CRM solo tras la aprobación.
7. Crear tareas y recordatorios.
8. Preparar un borrador de correo.
9. Eliminar el audio cuando venza el plazo de conservación definido.

### 4.7 Seguimiento

- Borrador de agradecimiento posterior a la visita.
- Envío de documentación acordada.
- Recordatorio de compromisos propios y del cliente.
- Secuencias distintas para lead, oferta, negociación, cliente activo o reactivación.
- Alertas por falta de respuesta sin crear acoso comercial.
- Detección de lenguaje que pueda constituir una promesa no autorizada.
- Registro automático del envío una vez aprobado.

Durante el piloto, el agente creará **borradores**, no envíos autónomos.

### 4.8 Oportunidades y pipeline

- Etapas con criterios de entrada y salida definidos.
- Importe, margen estimado, probabilidad y fecha prevista.
- Próxima acción obligatoria en cada oportunidad abierta.
- Días en la etapa y alerta por estancamiento.
- Motivo de pérdida estructurado.
- Productos y competidores asociados.
- Riesgos, dependencias y persona decisora.
- Previsión ponderada y escenario conservador, probable y optimista.

La IA explicará anomalías y redactará el informe, pero los totales se calcularán con consultas deterministas.

### 4.9 Ofertas y negociación

El agente puede:

- Componer una propuesta desde una plantilla.
- Personalizar beneficios y casos de uso.
- Comprobar que no falten partidas ni condiciones.
- Comparar versiones.
- Preparar respuestas a objeciones.
- Recordar aprobaciones pendientes.

Los importes deben proceder de datos estructurados: tarifa vigente, unidades, IVA, transporte, descuento permitido, margen mínimo, moneda y periodo de validez. La IA no decidirá por sí sola precios, descuentos, crédito, exclusividades, condiciones legales o fechas de entrega.

### 4.10 Pedidos, entrega y coordinación interna

- Convertir una oportunidad ganada en una ficha de traspaso.
- Verificar datos fiscales, dirección, productos, cantidades y condiciones.
- Informar a administración, almacén, logística o servicio técnico.
- Detectar discrepancias entre oferta y pedido.
- Avisar de retrasos o falta de información.
- Mantener al comercial informado sin duplicar mensajes.

### 4.11 Posventa e incidencias

- Seguimiento de entrega y puesta en marcha.
- Encuesta de satisfacción o llamada programada.
- Registro y clasificación de incidencias.
- Alerta antes de visitar o vender a un cliente con un problema grave.
- Resumen de estado para el comercial.
- Confirmación de resolución y aprendizaje de la causa.

### 4.12 Fidelización, venta cruzada y churn

- Avisos por 30, 60 o 90 días sin interacción, ajustados por segmento.
- Comparación entre frecuencia habitual y frecuencia reciente de pedidos.
- Detección de descenso de facturación, margen o categorías compradas.
- Sugerencia de reposición o producto complementario.
- Fechas contractuales, renovaciones y campañas estacionales.
- Identificación de clientes dependientes de un único contacto.
- Acciones de recuperación con motivo concreto.

Estas funciones necesitan datos históricos de pedidos y líneas de producto. Sin integración con ERP, facturación o CSV periódico, deben marcarse como experimentales.

### 4.13 Informes e inteligencia comercial

- Resumen diario de actividad y tareas.
- Informe semanal de pipeline, ofertas estancadas y compromisos.
- Informe mensual de ventas, margen, conversión y cobertura de cartera.
- Previsión frente a objetivo.
- Motivos de pérdida y objeciones frecuentes.
- Rendimiento por producto, sector, zona y fuente del lead.
- Calidad del CRM y registros incompletos.
- Uso, coste, errores y correcciones del propio agente.

## 5. Modelo mínimo de datos

No se debe almacenar todo en una única tabla. El modelo mínimo contiene:

| Entidad | Campos principales |
|---|---|
| Empresas | ID, razón social, CIF, dominio, sector, segmento, zona, dirección, propietario, estado |
| Contactos | ID, empresa, nombre, cargo, email, teléfono, canal preferido, consentimiento, última validación |
| Oportunidades | Empresa, etapa, importe, margen, probabilidad, fecha prevista, origen, competidor, próxima acción |
| Interacciones | Fecha, tipo, participantes, resumen, fuente, resultado, oportunidad relacionada |
| Tareas | Descripción, responsable, vencimiento, prioridad, estado, origen, evidencia |
| Productos | Código, familia, descripción aprobada, tarifa, vigencia, disponibilidad, restricciones |
| Ofertas | Versión, oportunidad, partidas, descuento, impuestos, validez, estado, aprobador |
| Pedidos | Cliente, oferta, fecha, importe, estado, entrega e incidencias |
| Incidencias | Cliente, tipo, gravedad, responsable, estado, fechas y resolución |
| Documentos | Tipo, versión, propietario, fecha de vigencia, ubicación y permisos |
| Fuentes | URL o sistema, fecha de consulta, fiabilidad y dato obtenido |
| Auditoría | Usuario o flujo, acción, registro afectado, antes, después, fecha y resultado |

Reglas de calidad obligatorias:

- Identificadores internos estables.
- Catálogos cerrados para etapas, motivos y estados.
- Zona horaria y formatos de fecha uniformes.
- No sobrescribir un dato confirmado con una inferencia.
- Marcar “desconocido” en lugar de inventar.
- Registrar la nota original junto a la extracción aprobada.
- Deduplicación antes de crear empresas o contactos.

## 6. Arquitectura gratuita priorizada

### 6.1 Arquitectura lógica

```text
Telegram / formulario / correo / calendario
                    │
                    ▼
          n8n Community autoalojado
      ┌─────────────┼──────────────┐
      ▼             ▼              ▼
 Whisper local   Motor de IA     Reglas y validaciones
      │        local o Gemini       │
      └─────────────┼──────────────┘
                    ▼
        Notion o Baserow/PostgreSQL
          │         │          │
          ▼         ▼          ▼
       Tareas   Borradores   Informes/Metabase
                    │
                    ▼
             Aprobación humana
```

### 6.2 Herramientas recomendadas por prioridad

| Componente | Primera opción gratuita | Alternativa | Criterio |
|---|---|---|---|
| Canal móvil | Telegram Bot | Formulario web/PWA | Telegram ofrece una plataforma de bots gratuita y una API sencilla. [Telegram Bots](https://core.telegram.org/bots) |
| Orquestación | n8n Community autoalojado | Make Free / Zapier Free | n8n Community puede usarse gratuitamente de forma indefinida, aunque carece de algunas funciones empresariales. [Ediciones de n8n](https://github.com/n8n-io/n8n-docs/blob/main/docs/deploy/host-n8n/community-edition-features.md) |
| CRM individual | Notion Free | Baserow Cloud Free | Notion es rápido para un piloto de un solo propietario |
| CRM de equipo | Baserow autoalojado | PostgreSQL con interfaz propia | Baserow ofrece núcleo bajo licencia MIT y autoalojamiento. [Conceptos de Baserow](https://baserow.io/user-docs/learn-baserow-basic-concepts) |
| Base transaccional | PostgreSQL | SQLite solo para prototipo local | Mejor integridad y relaciones que una tabla documental |
| IA privada | Modelo local mediante Ollama | Gemini API Free | Local evita enviar datos a terceros, pero necesita hardware suficiente. [Ollama local](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image) |
| IA con cuota externa | Gemini API Free | API de OpenAI de pago | La cuota de Gemini sirve para piloto, con límites y condiciones de datos. [Precios de Gemini](https://ai.google.dev/gemini-api/docs/pricing) |
| Voz a texto | Whisper local | Servicio externo de transcripción | Whisper publica código y pesos bajo licencia MIT. [Repositorio de Whisper](https://github.com/openai/whisper) |
| OCR de tarjetas | Tesseract OCR local | Modelo multimodal con cuota gratuita | Confirmación obligatoria de nombre, email y teléfono |
| Correo | Gmail: crear borrador | Outlook/Microsoft Graph | No enviar automáticamente en la primera fase |
| Calendario | Google Calendar | Outlook Calendar | Agenda, briefing y recordatorios |
| Mapas | Enlaces de navegación + coordenadas guardadas | OSRM/Nominatim autoalojados | Evitar depender de uso masivo de servicios públicos gratuitos |
| Archivos | Carpeta cifrada/Nextcloud existente | Almacenamiento del CRM | Políticas de acceso y conservación |
| Analítica | Vistas del CRM | Metabase autoalojado | Metabase dispone de edición abierta autoalojada. [Documentación de Metabase](https://www.metabase.com/docs/latest/) |
| Copias | Exportación programada + restic a disco cifrado | Copia en NAS existente | Probar restauración, no solo generación |

### 6.3 Elección práctica

**Piloto individual:** Telegram + n8n Community + Notion Free + Whisper local + Gemini Free u Ollama + Gmail/Calendar.

**Piloto de varios comerciales:** Telegram o PWA + n8n Community + Baserow/PostgreSQL + Whisper local + Ollama/Gemini + Metabase.

Notion Free es adecuado para un propietario individual, pero su uso colaborativo gratuito tiene límites: un espacio con un propietario dispone de bloques ilimitados, mientras que con dos o más propietarios se limita a 1.000 bloques. También limita los archivos a 5 MB en el plan gratuito. [Uso de bloques](https://www.notion.com/help/understanding-block-usage) y [precios de Notion](https://www.notion.com/pricing).

La API de OpenAI debe considerarse una alternativa de pago, no la base de la promesa gratuita. La documentación oficial muestra precios por consumo y un sistema de costes de API. [Precios de la API](https://platform.openai.com/pricing) y [uso y costes](https://platform.openai.com/docs/api-reference/usage/audio_transcriptions_object). Según la documentación oficial de OpenAI, el contenido enviado mediante la API no se usa para entrenar sus modelos salvo adhesión voluntaria, aunque existen políticas de almacenamiento y retención que deben revisarse. [Controles de datos de la API](https://platform.openai.com/docs/models/default-usage-policies-by-endpoint).

## 7. Política de autonomía y aprobación

### Nivel A: automático

- Cálculos de días, importes y alertas basadas en reglas.
- Creación de un resumen diario interno.
- Detección de registros incompletos o duplicados.
- Recordatorios internos.
- Copias de seguridad y comprobaciones técnicas.

### Nivel B: propuesta con confirmación

- Transcripción y resumen de visitas.
- Alta o modificación de contactos.
- Cambio de etapa del pipeline.
- Creación de compromisos a partir de una conversación.
- Borradores de correo y mensajes.
- Priorización de clientes.
- Recomendaciones de venta cruzada.

### Nivel C: siempre humano

- Enviar comunicaciones externas durante el piloto.
- Aprobar precios, descuentos, margen o crédito.
- Firmar ofertas, contratos o pedidos.
- Prometer disponibilidad, entrega, garantía o resultado.
- Cerrar una incidencia.
- Eliminar datos personales o históricos materiales.
- Lanzar campañas masivas.
- Tomar decisiones sobre personas basadas únicamente en IA.

## 8. Privacidad, seguridad y cumplimiento

El sistema tratará nombres, cargos, teléfonos, correos, notas y posiblemente voces. Debe cumplir el RGPD y las normas aplicables de comunicaciones comerciales. Los principios europeos exigen licitud, transparencia, finalidad determinada, minimización, exactitud, limitación de conservación, seguridad y responsabilidad demostrable. [Principios del RGPD](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en).

Medidas mínimas:

- Definir base jurídica y aviso de privacidad.
- Informar y obtener autorización cuando proceda antes de grabar.
- Evitar grabaciones continuas; priorizar la nota del propio comercial tras la visita.
- No enviar información confidencial a una cuota gratuita sin evaluación de privacidad.
- El nivel gratuito de Gemini indica que el contenido puede utilizarse para mejorar productos; no debe recibir datos sensibles sin decisión expresa de la empresa. [Gemini API](https://ai.google.dev/gemini-api/docs/pricing).
- Separar datos comerciales de credenciales y secretos.
- Usar HTTPS para cualquier acceso remoto.
- Aplicar autenticación multifactor donde esté disponible.
- Conceder acceso mínimo por usuario y territorio.
- Cifrar copias y dispositivos.
- Establecer plazos de conservación para audios, transcripciones y documentos.
- Registrar accesos, cambios, errores y aprobaciones.
- Disponer de proceso de rectificación, exportación y eliminación.
- Formalizar encargos de tratamiento con proveedores cuando corresponda.

Para correo comercial se deben respetar consentimiento, oposición y bajas, además de los requisitos técnicos del proveedor. Gmail limita las cuentas personales a aproximadamente 500 envíos o destinatarios diarios y puede suspender temporalmente el envío al superar el límite. [Límites de Gmail](https://support.google.com/mail/answer/22839).

## 9. Fiabilidad y calidad de la IA

Cada flujo con IA debe incorporar:

- Salida JSON con esquema fijo y validación de tipos.
- Campo de confianza y lista de ambigüedades.
- Referencia al audio, documento o registro de origen.
- Umbral que derive a revisión en vez de actuar.
- Pruebas con ejemplos reales anonimizados.
- Conjunto de evaluación estable para comparar cambios de modelo o prompt.
- Registro de versión de modelo, prompt y flujo.
- Reintentos limitados y cola de errores.
- Idempotencia para no duplicar contactos, tareas o interacciones.
- Monitorización de latencia, fallos y consumo.
- Revisión periódica de falsos positivos y datos inventados.

La base de conocimiento solo debe utilizar documentos con propietario, versión y fecha de vigencia. Si el agente no encuentra evidencia suficiente, responderá “no consta” y solicitará revisión.

## 10. Indicadores de éxito

### Adopción y eficiencia

- Porcentaje de visitas registradas el mismo día.
- Minutos administrativos por visita.
- Uso semanal del agente.
- Tiempo desde la visita hasta el seguimiento.
- Porcentaje de compromisos con responsable y fecha.

### Calidad

- Precisión de transcripción en nombres, cifras y fechas.
- Porcentaje de extracciones aceptadas sin cambios.
- Correcciones por tipo de campo.
- Duplicados creados.
- Alucinaciones o datos sin fuente.
- Fallos de automatización y tiempo de recuperación.

### Resultados comerciales

- Conversión de lead a oportunidad y de oportunidad a pedido.
- Días medios por etapa.
- Oportunidades sin próxima acción.
- Tasa de seguimiento dentro del plazo.
- Valor y margen del pipeline.
- Precisión de la previsión.
- Clientes reactivados.
- Venta cruzada obtenida.
- Reducción de churn o inactividad.

### Economía del sistema

- Coste de API por usuario y mes.
- Horas de mantenimiento.
- Consumo de almacenamiento.
- Valor del tiempo ahorrado.
- Retorno estimado por mejoras atribuibles al agente.

## 11. Plan de implantación

### Fase 0 — definición y gobierno (1 semana)

- Elegir un único proceso comercial y propietario.
- Definir etapas, campos obligatorios y criterios de avance.
- Crear política de aprobación, privacidad y conservación.
- Seleccionar 20 casos históricos anonimizados para pruebas.
- Establecer métricas de partida.

**Criterio de salida:** modelo de datos y reglas aprobados.

### Fase 1 — MVP posterior a la visita (2–3 semanas)

- Bot de Telegram.
- Recepción y almacenamiento temporal de voz.
- Whisper local.
- Extracción estructurada.
- Confirmación humana.
- Alta de interacción y tareas en Notion/Baserow.
- Borrador de correo.
- Registro de errores y auditoría.

**Criterio de salida:** al menos el 90 % de las notas se procesa sin pérdida; nombres, fechas e importes siempre se confirman.

### Fase 2 — preparación y control diario (2 semanas)

- Briefing antes de la visita.
- Agenda diaria y prioridades.
- Alertas de compromisos e inactividad.
- Pipeline básico.
- Informe semanal.
- Control de calidad de datos.

**Criterio de salida:** toda oportunidad abierta tiene responsable, próxima acción y fecha.

### Fase 3 — conocimiento, ofertas y posventa (3–4 semanas)

- Catálogo documental versionado.
- Argumentarios y gestión de objeciones.
- Plantillas de ofertas.
- Comprobaciones de precios y descuentos mediante reglas.
- Traspaso a pedido e incidencias.

**Criterio de salida:** ninguna propuesta usa tarifa vencida ni omite aprobación requerida.

### Fase 4 — prospección y territorio (3 semanas)

- Importación y deduplicación de leads.
- Investigación en fuentes permitidas.
- *Lead scoring* explicable.
- Agrupación geográfica y rutas.
- Cuadro de cobertura de cartera.

Para mapas, no se debe convertir la API pública de Nominatim en un geocodificador masivo: su política limita el uso intensivo, exige atribución y desaconseja consultas periódicas por lotes. Se almacenarán coordenadas en caché o se autoalojará el servicio si el volumen crece. [Política de Nominatim](https://operations.osmfoundation.org/policies/nominatim/).

### Fase 5 — inteligencia avanzada (cuando existan datos suficientes)

- Integración con ERP o importación periódica de pedidos.
- Venta cruzada basada en líneas de producto.
- Detección de churn.
- Predicción de cierre.
- Segmentación de clientes por comportamiento.
- Paneles en Metabase.

**Criterio de entrada:** datos históricos limpios y comparables, idealmente de 12 meses o más.

## 12. Riesgos principales y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Datos inventados | Fuentes, confianza, esquemas y aprobación humana |
| CRM incompleto | Campos obligatorios y alertas de calidad |
| Duplicados por reintentos | Claves idempotentes y deduplicación |
| Exposición de datos | Procesamiento local, mínimos privilegios y cifrado |
| Dependencia de una cuota gratuita | Proveedor intercambiable y límites de consumo |
| Equipo local apagado | Cola pendiente y procedimiento de reinicio |
| Automatización de correo no deseado | Borradores, consentimiento y límites de frecuencia |
| Scraping no autorizado | Fuentes permitidas y API oficial cuando exista acceso |
| Recomendaciones sesgadas | Reglas visibles, revisión de resultados y posibilidad de impugnación |
| Tarifas o documentos obsoletos | Propietario, versión y caducidad |
| Complejidad excesiva | Implantación por fases y un solo orquestador |
| Falta de uso por el comercial | Interacción de menos de un minuto y diseño con usuarios reales |

## 13. Recomendación final

Se recomienda comenzar con un **MVP individual basado en Telegram, n8n Community, Notion, Whisper local y un motor de IA intercambiable**. Ollama será la primera opción cuando el equipo disponible pueda ejecutar un modelo local con calidad suficiente; Gemini Free puede utilizarse para pruebas no sensibles y dentro de su cuota. La API de OpenAI quedará como alternativa de pago y privacidad evaluada, no como componente gratuito.

El MVP solo hará cinco cosas, pero deberá hacerlas bien:

1. Recibir la nota de voz del delegado.
2. Convertirla en información comercial estructurada.
3. Pedir confirmación antes de modificar el CRM.
4. Crear compromisos y un borrador de seguimiento.
5. Preparar el briefing de la próxima interacción.

Cuando este circuito sea fiable y ahorre tiempo de forma demostrable, se incorporarán priorización diaria, pipeline, ofertas, posventa, prospección y rutas. La inteligencia predictiva —churn, venta cruzada y previsión— se añadirá únicamente después de integrar datos históricos de pedidos y resultados.

El éxito del proyecto no dependerá de que el agente tenga muchas funciones, sino de que mantenga datos fiables, reduzca trabajo real y ayude al delegado a decidir la siguiente mejor acción sin quitarle el control de la relación comercial.

