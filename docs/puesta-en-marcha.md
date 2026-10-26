# Puesta en marcha

Guía para quien quiera usar este repositorio como base de su propio Copiloto Comercial. **No es necesario configurar nada para leer el repositorio ni para que pase la validación**: sin configuración, la validación funciona y el informe diario se omite solo.

> Haz una copia propia (*Use this template* o *Fork*) y trabaja en un repositorio **privado** si vas a usar datos reales. Este repositorio solo contiene datos sintéticos.

## Qué necesitas

| Pieza | Para qué | Coste |
|---|---|---|
| Cuenta de GitHub | Ejecutar los workflows | Gratis |
| Baserow (cloud gratuito o autoalojado) | El CRM de 12 tablas | Gratis |
| Bot de Telegram | Recibir el informe diario | Gratis |
| Clave de la API de Claude | Solo para la evaluación de la extracción | De pago, aparte del plan gratuito de Claude |

## 1. Crea el CRM en Baserow

1. Crea una base de datos nueva.
2. Crea las 12 tablas, campos y opciones de selección exactamente como indica [`schemas/crm-baserow.json`](../schemas/crm-baserow.json) (fuente de verdad).
3. Anota el número de cada tabla: aparece en la URL al abrirla (`/database/X/table/NÚMERO`).
4. En Ajustes → *Database tokens*, crea un token con permiso solo de **lectura**.

## 2. Crea el bot de Telegram

1. En Telegram, habla con **@BotFather**, escribe `/newbot` y sigue los pasos. Guarda el token.
2. Escribe cualquier mensaje a tu bot.
3. Abre `https://api.telegram.org/bot<TOKEN>/getUpdates` en el navegador y busca `"chat":{"id":NÚMERO`. Ese número es tu `TELEGRAM_CHAT_ID`.

## 3. Configura GitHub

En tu repositorio: **Settings → Secrets and variables → Actions**.

**Secrets** (pestaña Secrets, *New repository secret*). Pega los valores tú; nunca los escribas en archivos ni en chats.

| Nombre | Valor | Obligatorio para |
|---|---|---|
| `BASEROW_TOKEN` | Token de lectura de Baserow | Informe diario |
| `TELEGRAM_BOT_TOKEN` | Token de BotFather | Envío del informe |
| `TELEGRAM_CHAT_ID` | Número de tu chat | Envío del informe |
| `ANTHROPIC_API_KEY` | Clave de console.anthropic.com | Evaluación real |

**Variables** (pestaña Variables, *New repository variable*):

| Nombre | Valor |
|---|---|
| `BASEROW_URL` | Dirección de tu Baserow, sin barra final |
| `BASEROW_TABLE_EMPRESAS`, `BASEROW_TABLE_OPORTUNIDADES`, `BASEROW_TABLE_INTERACCIONES`, `BASEROW_TABLE_TAREAS`, `BASEROW_TABLE_OFERTAS`, `BASEROW_TABLE_INCIDENCIAS` | Número de cada tabla |
| `CLAUDE_MODEL` | Opcional. Por defecto `claude-sonnet-5-5` |

## 4. Prueba

1. **Actions → Validar estructura**: debe salir en verde.
2. **Actions → Informe diario → Run workflow**: recibirás el informe en Telegram. Si falla, el mensaje indica qué falta y nunca muestra tokens.
3. **Actions → Evaluación de la extracción → Run workflow** (tiene coste): puedes empezar con 5 casos.

Para probar sin red ni cuentas, en local:

```bash
pip install jsonschema pyyaml
python scripts/check_structure.py
python evals/run_eval.py --dry-run
python scripts/prioridades_diarias.py --fixture evals/fixtures/crm-demo.json
```

## 5. Arranca el circuito principal (n8n)

El repositorio no incluye los flujos de n8n (ver [`arquitectura.md`](arquitectura.md)). Monta tu instancia de n8n Community, implementa el flujo nota → extracción → confirmación → CRM y exporta los flujos a una carpeta `n8n/` sin credenciales.

## Seguridad

- Un repositorio **público** muestra sus logs a cualquiera. El informe diario se envía con `--enviar`, que no lo imprime. No añadas `--mostrar`.
- Usa datos reales solo en repositorios privados y revisa [`privacidad-y-conservacion.md`](privacidad-y-conservacion.md).
- Si un secreto se publica por error, revócalo de inmediato y crea uno nuevo.
- Las reglas del agente ([`politica-autonomia.md`](politica-autonomia.md)) no se relajan: propone, el humano decide.
