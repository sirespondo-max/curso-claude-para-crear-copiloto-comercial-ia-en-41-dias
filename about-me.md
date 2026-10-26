# about-me.md — Contexto del usuario y del escenario

Este archivo da a Claude el contexto fijo del proyecto para que no haya que repetirlo en cada prompt. Cualquier prompt o skill puede referenciarlo.

## Autor del proyecto

**Anibal Pedreño.** Profesional comercial que construye este Copiloto Comercial como proyecto de aprendizaje con Claude y como muestra de cómo aplica la IA a su trabajo en ventas.

## Escenario de ejemplo (sintético)

El proyecto se desarrolla sobre un escenario ficticio, pensado para poder probarlo sin datos reales de clientes. Si lo adaptas a un caso real, sustituye esta sección y revisa `prompts/` y `evals/`.

- **Rol:** delegado de ventas de campo.
- **Qué vende:** material eléctrico y de automatización industrial (cuadros, variadores, cableado y aparamenta).
- **A quién:** instaladores autorizados, pequeñas industrias y empresas de mantenimiento.
- **Zona:** Bizkaia y Álava. Visitas presenciales de lunes a jueves; los viernes, trabajo administrativo.
- **Qué valoran sus clientes:** plazos de entrega fiables por encima del precio.
- **Competencia:** distribuidores grandes con catálogo más amplio pero peor servicio postventa.

## Cómo trabaja el usuario

- Registra las visitas por escrito o con la transcripción de WhatsApp, desde el móvil y entre visita y visita. Por eso las respuestas del agente deben ser breves.
- Quiere revisar y corregir lo que el agente extrae antes de que se guarde.
- Decide él todo lo relativo a precios, descuentos, plazos y comunicaciones a clientes.

## Restricciones

- Cuenta gratuita de Claude para el aprendizaje. Las automatizaciones por API tienen coste aparte y se mantienen al mínimo (la evaluación se lanza a mano).
- Stack gratuito o autoalojado por defecto: Telegram, n8n Community, Baserow, GitHub Actions.
- Los datos de clientes no salen del circuito autorizado y no se suben al repositorio.
