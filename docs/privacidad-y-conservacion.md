# Privacidad, seguridad y conservación

Borrador de trabajo para el piloto, basado en la sección 8 del informe. **No es asesoramiento legal.** Antes de usarlo con datos reales de clientes, debe revisarlo la persona responsable de protección de datos de la empresa o un asesor.

## Qué datos trata el sistema

| Dato | Dónde vive | Notas |
|---|---|---|
| Nombres, cargos, correos y teléfonos de contactos | CRM en Baserow | Datos personales de profesionales |
| Notas de visita (texto) | CRM (campo `resumen` de Interacciones) y nota original | La entrada es siempre texto; no se guardan audios |
| Texto enviado a Claude para extraer los datos | API de Claude (proveedor externo) | Revisar las condiciones de uso y retención de datos del proveedor antes de enviar datos reales |
| Registro de aprobaciones y cambios | Tabla Auditoría | Contiene el estado anterior y el nuevo de cada registro |
| Secretos (claves de API, tokens) | Secretos de GitHub Actions y de n8n | Nunca en el repositorio ni en el CRM |

## Repositorios públicos y registros de GitHub Actions

- Los registros (logs) de Actions de un repositorio público los puede leer cualquiera. El informe diario con datos reales **no debe imprimirse** en ellos: el workflow usa `--enviar`, que lo manda por Telegram sin mostrarlo.
- Los mensajes de error del script son seguros: no incluyen tokens ni contenido del CRM.
- Los secretos se pasan siempre por `env` desde los secretos de GitHub; nunca se escriben en el repositorio. Si un secreto se publica por error, se revoca de inmediato.
- Los resultados de evaluación (`evals/resultados/*.json`) no se versionan; se descargan como artefacto del workflow y caducan a los 30 días.
- Si el repositorio es público, usa solo datos sintéticos en él. Para trabajar con datos reales, usa un repositorio privado.

## Principios aplicados

Licitud y transparencia, finalidad determinada, minimización, exactitud, limitación de conservación, seguridad y responsabilidad demostrable (principios del RGPD citados en el informe).

## Medidas mínimas del piloto

1. **Minimizar lo que se envía al modelo.** Solo el texto de la nota. No se envían listados de clientes ni datos que no hagan falta para la extracción.
2. **Sin grabaciones continuas.** Se prioriza la nota que escribe o transcribe el propio delegado tras la visita. Si en algún momento se graba una conversación con el cliente, hay que informarle y obtener la autorización que corresponda antes de grabar.
3. **Sin audios almacenados.** Este proyecto parte de texto. La transcripción con WhatsApp o con una grabadora de bolsillo se hace fuera del sistema.
4. **Datos de ejemplo sintéticos en el repositorio.** `docs/` y `evals/` no contienen datos reales. No se suben notas de clientes sin anonimizarlas.
5. **Acceso mínimo.** Cada persona accede solo a su cartera o territorio. Autenticación multifactor donde esté disponible.
6. **Cifrado y copias.** Copias de seguridad cifradas y restauración probada, no solo generada.
7. **Trazabilidad.** Todos los accesos, cambios, errores y aprobaciones quedan registrados en Auditoría.
8. **Derechos de las personas.** Debe existir un procedimiento para rectificar, exportar y eliminar los datos de un contacto cuando lo solicite.
9. **Comunicaciones comerciales.** El campo `consentimiento` de Contactos debe respetarse; los borradores no se envían sin comprobarlo. Hay que atender oposiciones y bajas.

## Plazos de conservación

Propuesta inicial, **a validar por la empresa**. No hay un plazo universal: depende de la finalidad y de la normativa aplicable.

| Dato | Propuesta inicial | A decidir |
|---|---|---|
| Notas de visita y resumen | Mientras dure la relación comercial más el plazo que fije la empresa | Plazo exacto |
| Audios (si algún día se usan) | Eliminar tras confirmar la extracción | Plazo exacto |
| Contactos sin actividad | Revisión periódica y supresión si ya no hay base para tratarlos | Frecuencia y criterio |
| Registro de auditoría | Conservar el tiempo necesario para demostrar el cumplimiento | Plazo exacto |

## Proveedores externos

- Con cada proveedor que reciba datos personales (modelo de IA, alojamiento, correo) conviene revisar condiciones de uso, retención y, cuando corresponda, formalizar el encargo de tratamiento.
- Una cuenta gratuita de cualquier servicio puede tener condiciones de uso de datos distintas de las de un plan de empresa. No enviar información confidencial o sensible sin esa evaluación.

## Qué hacer ante un incidente

1. Revocar de inmediato el secreto o el acceso afectado (clave de API, token de Baserow o de Telegram).
2. Revisar la tabla Auditoría para delimitar qué se vio o se cambió.
3. Avisar a la persona responsable de protección de datos para valorar si hay que notificar.
4. Anotar la causa y la corrección.
