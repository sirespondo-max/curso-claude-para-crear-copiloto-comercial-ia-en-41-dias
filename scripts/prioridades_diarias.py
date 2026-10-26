#!/usr/bin/env python3
"""Informe diario de prioridades y alertas del Copiloto Comercial.

Lee el CRM en Baserow (o un archivo de ejemplo), puntúa las oportunidades
abiertas con reglas deterministas y genera el plan del día: cinco acciones con
motivo, impacto y plazo, más las alertas comerciales. Es Nivel A (automático e
interno): no usa IA, no modifica el CRM y no envía nada a clientes.

Uso:
  python scripts/prioridades_diarias.py --fixture evals/fixtures/crm-demo.json
  python scripts/prioridades_diarias.py                  lee Baserow y muestra el informe
  python scripts/prioridades_diarias.py --enviar         lo envía por Telegram (no lo muestra)

Variables de entorno (ver CLAUDE.md):
  BASEROW_URL, BASEROW_TOKEN, BASEROW_TABLE_OPORTUNIDADES, _INTERACCIONES,
  _TAREAS, _OFERTAS, _INCIDENCIAS y, recomendada, BASEROW_TABLE_EMPRESAS.
  TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID solo con --enviar.

Solo usa la biblioteca estándar de Python.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path

# ==========================================================================
# REGLAS DE PUNTUACIÓN: único bloque que hay que revisar para cambiar pesos.
# ==========================================================================
PESOS = {
    "valor_puntos_max": 30,        # el valor ponderado suma 1 punto por cada 'valor_euros_por_punto'
    "valor_euros_por_punto": 1000,
    "etapa": {"Prospección": 5, "Cualificación": 10, "Propuesta": 20, "Negociación": 25},
    "sin_contacto_mas_14": 10,
    "sin_contacto_mas_30": 20,     # también si nunca hay contacto registrado
    "sin_proxima_accion": 15,
    "fecha_vencida": 20,
    "fecha_en_7_dias": 15,
    "fecha_en_14_dias": 8,
    "incidencia": {"Crítica": 25, "Alta": 15, "Media": 5, "Baja": 0},
}
UMBRAL_ESTA_SEMANA = 40            # a partir de estos puntos el plazo pasa de "14 días" a "esta semana"
DIAS_ESTANCADA = 30
DIAS_OFERTA_PROXIMA = 7
TRAMOS_INACTIVIDAD = (90, 60, 30)  # días sin interacción de un cliente activo
NUM_ACCIONES = 5
MAX_POR_ALERTA = 8
LIMITE_TELEGRAM = 4000             # el máximo de Telegram es 4096 caracteres

ETAPAS_ABIERTAS = tuple(PESOS["etapa"])
TAREA_ABIERTA = ("Pendiente", "En curso")
OFERTA_VIVA = ("Borrador", "Pendiente de aprobación", "Enviada")
INCIDENCIA_ABIERTA = ("Nueva", "En curso", "Escalada")
GRAVEDAD_ORDEN = ("Crítica", "Alta", "Media", "Baja")
GRAVEDAD_ALERTA = ("Crítica", "Alta")
PRIORIDAD_ORDEN = ("Urgente", "Alta", "Media", "Baja")

TABLAS_OBLIGATORIAS = ("Oportunidades", "Interacciones", "Tareas", "Ofertas", "Incidencias")
TABLAS_OPCIONALES = ("Empresas",)
DIAS_SEMANA = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")


class ErrorInforme(Exception):
    """Error de configuración o de red con un mensaje seguro (sin secretos)."""


# ==========================================================================
# Normalización de datos (formato de la API de Baserow con user_field_names)
# ==========================================================================
def valor(x):
    """Un single_select llega como {'id', 'value', 'color'}; se devuelve solo el valor."""
    if isinstance(x, dict) and "value" in x:
        return x["value"]
    return x


def texto(x) -> str:
    v = valor(x)
    return "" if v is None else str(v).strip()


def numero(x) -> float | None:
    v = valor(x)
    if v in (None, ""):
        return None
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def fecha(x) -> date | None:
    v = valor(x)
    if not v:
        return None
    try:
        return date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


def enlaces(x) -> list[dict]:
    """Un link_row llega como lista de {'id', 'value'}."""
    if not isinstance(x, list):
        return []
    return [e for e in x if isinstance(e, dict) and "id" in e]


def probabilidad(x) -> float:
    """Devuelve una fracción 0-1. Un valor mayor que 1 se interpreta como porcentaje."""
    p = numero(x)
    if p is None or p < 0:
        return 0.0
    return p / 100 if p > 1 else p


def eur(n: float) -> str:
    return f"{n:,.0f} €".replace(",", ".")


def fmt_fecha(d: date) -> str:
    return d.strftime("%d/%m/%Y")


def plural(n: int, uno: str, varios: str) -> str:
    return f"{n} {uno if n == 1 else varios}"


# ==========================================================================
# Carga de datos
# ==========================================================================
def cargar_fixture(ruta: Path) -> tuple[dict[str, list[dict]], date | None]:
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ErrorInforme(f"No se pudo leer el archivo de ejemplo {ruta}: {exc}") from None
    tablas = datos.get("tablas")
    if not isinstance(tablas, dict):
        raise ErrorInforme(f"{ruta}: falta el objeto 'tablas'")
    faltan = [t for t in TABLAS_OBLIGATORIAS if t not in tablas]
    if faltan:
        raise ErrorInforme(f"{ruta}: faltan las tablas {', '.join(faltan)}")
    return tablas, fecha(datos.get("hoy"))


def _url_base(url: str) -> str:
    p = urllib.parse.urlparse(url)
    local = p.hostname in ("localhost", "127.0.0.1", "::1")
    if p.scheme != "https" and not (p.scheme == "http" and local):
        raise ErrorInforme("BASEROW_URL debe empezar por https:// (http solo se admite en localhost)")
    if not p.hostname:
        raise ErrorInforme("BASEROW_URL no es una URL válida")
    return url.rstrip("/")


def filas_baserow(base: str, token: str, tabla_id: str, nombre: str) -> list[dict]:
    """Lee todas las filas de una tabla. Pagina con un contador, sin seguir
    URLs devueltas por el servidor, para no enviar el token a otro destino."""
    filas: list[dict] = []
    for pagina in range(1, 101):
        url = f"{base}/api/database/rows/table/{urllib.parse.quote(str(tabla_id))}/?user_field_names=true&size=200&page={pagina}"
        req = urllib.request.Request(url, headers={"Authorization": f"Token {token}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                cuerpo = json.load(resp)
        except urllib.error.HTTPError as exc:
            raise ErrorInforme(f"Baserow respondió {exc.code} al leer la tabla {nombre}. Revisa el token y el id de tabla.") from None
        except (urllib.error.URLError, TimeoutError):
            raise ErrorInforme(f"No se pudo conectar con Baserow al leer la tabla {nombre}.") from None
        except json.JSONDecodeError:
            raise ErrorInforme(f"Baserow devolvió una respuesta no válida al leer la tabla {nombre}.") from None
        resultados = cuerpo.get("results", [])
        filas += resultados
        if not resultados or len(filas) >= cuerpo.get("count", 0):
            break
    return filas


def cargar_baserow() -> tuple[dict[str, list[dict]], list[str]]:
    token = os.environ.get("BASEROW_TOKEN", "")
    url = os.environ.get("BASEROW_URL", "")
    if not token or not url:
        raise ErrorInforme("Faltan BASEROW_URL y/o BASEROW_TOKEN. Usa --fixture para probar sin conexión.")
    base = _url_base(url)
    ids = {t: os.environ.get(f"BASEROW_TABLE_{t.upper()}", "").strip() for t in TABLAS_OBLIGATORIAS + TABLAS_OPCIONALES}
    faltan = [f"BASEROW_TABLE_{t.upper()}" for t in TABLAS_OBLIGATORIAS if not ids[t]]
    if faltan:
        raise ErrorInforme("Faltan variables: " + ", ".join(faltan))
    tablas, avisos = {}, []
    for t, tid in ids.items():
        if tid:
            tablas[t] = filas_baserow(base, token, tid, t)
    if "Empresas" not in tablas:
        avisos.append("No hay BASEROW_TABLE_EMPRESAS: los nombres de empresa pueden salir como códigos y no se calcula la alerta de clientes inactivos.")
    return tablas, avisos


# ==========================================================================
# Cálculo
# ==========================================================================
def calcular(tablas: dict[str, list[dict]], hoy: date) -> dict:
    empresas = {f["id"]: f for f in tablas.get("Empresas", [])}
    tiene_empresas = "Empresas" in tablas

    def nombre_empresa(lnk: dict) -> str:
        fila = empresas.get(lnk["id"])
        if fila is not None and texto(fila.get("razón social")):
            return texto(fila["razón social"])
        return texto(lnk.get("value")) or f"empresa {lnk['id']}"

    def empresa_de_oportunidad(op: dict) -> list[dict]:
        return enlaces(op.get("empresa"))

    oportunidades = {f["id"]: f for f in tablas["Oportunidades"]}

    # Último contacto por oportunidad y por empresa (a través de sus oportunidades).
    ultimo_opp: dict[int, date] = {}
    for it in tablas["Interacciones"]:
        d = fecha(it.get("fecha"))
        if d is None or d > hoy:
            continue
        for lnk in enlaces(it.get("oportunidad")):
            if d > ultimo_opp.get(lnk["id"], date.min):
                ultimo_opp[lnk["id"]] = d
    ultimo_emp: dict[int, date] = {}
    for oid, d in ultimo_opp.items():
        op = oportunidades.get(oid)
        for lnk in (empresa_de_oportunidad(op) if op else []):
            if d > ultimo_emp.get(lnk["id"], date.min):
                ultimo_emp[lnk["id"]] = d

    # Incidencia abierta más grave por cliente.
    grave_emp: dict[int, str] = {}
    incidencias_graves: dict[int, list[str]] = {}
    for inc in tablas["Incidencias"]:
        if texto(inc.get("estado")) not in INCIDENCIA_ABIERTA:
            continue
        g = texto(inc.get("gravedad"))
        for lnk in enlaces(inc.get("cliente")):
            actual = grave_emp.get(lnk["id"])
            if g in GRAVEDAD_ORDEN and (actual is None or GRAVEDAD_ORDEN.index(g) < GRAVEDAD_ORDEN.index(actual)):
                grave_emp[lnk["id"]] = g
            if g in GRAVEDAD_ALERTA:
                incidencias_graves.setdefault(lnk["id"], []).append(f"{texto(inc.get('tipo')) or 'incidencia'} ({g.lower()}, {texto(inc.get('estado')).lower()})")

    # ---- Puntuación de oportunidades abiertas ----
    acciones, abiertas = [], 0
    imp_total = pond_total = 0.0
    sin_proxima, estancadas = [], []
    for op in tablas["Oportunidades"]:
        etapa = texto(op.get("etapa"))
        if etapa not in ETAPAS_ABIERTAS:
            continue
        abiertas += 1
        lnk_emp = empresa_de_oportunidad(op)
        empresa = nombre_empresa(lnk_emp[0]) if lnk_emp else "Empresa sin identificar"
        importe = numero(op.get("importe")) or 0.0
        ponderado = importe * probabilidad(op.get("probabilidad"))
        imp_total += importe
        pond_total += ponderado

        puntos, motivos = 0.0, []
        pv = min(ponderado / PESOS["valor_euros_por_punto"], PESOS["valor_puntos_max"])
        puntos += pv
        if ponderado > 0:
            motivos.append(f"valor ponderado de {eur(ponderado)}")
        puntos += PESOS["etapa"][etapa]
        motivos.append(f"etapa {etapa}")

        ultimo = ultimo_opp.get(op["id"])
        dias_contacto = (hoy - ultimo).days if ultimo else None
        if dias_contacto is None:
            puntos += PESOS["sin_contacto_mas_30"]
            motivos.append("sin contacto registrado")
        elif dias_contacto > 30:
            puntos += PESOS["sin_contacto_mas_30"]
            motivos.append(f"{dias_contacto} días sin contacto")
        elif dias_contacto > 14:
            puntos += PESOS["sin_contacto_mas_14"]
            motivos.append(f"{dias_contacto} días sin contacto")
        if dias_contacto is None or dias_contacto > DIAS_ESTANCADA:
            estancadas.append((empresa, etapa, dias_contacto))

        prox = texto(op.get("próxima acción"))
        sin_prox = prox.lower() in ("", "desconocido")
        if sin_prox:
            puntos += PESOS["sin_proxima_accion"]
            motivos.append("sin próxima acción definida")
            sin_proxima.append((empresa, etapa))

        urgente = False
        fp = fecha(op.get("fecha prevista"))
        if fp is not None:
            dias = (fp - hoy).days
            if dias < 0:
                puntos += PESOS["fecha_vencida"]
                motivos.append(f"fecha prevista vencida hace {plural(-dias, 'día', 'días')}")
                urgente = True
            elif dias <= 7:
                puntos += PESOS["fecha_en_7_dias"]
                motivos.append("cierre previsto hoy" if dias == 0 else f"cierre previsto en {plural(dias, 'día', 'días')}")
                urgente = urgente or dias <= 2
            elif dias <= 14:
                puntos += PESOS["fecha_en_14_dias"]
                motivos.append(f"cierre previsto en {dias} días")

        grav = None
        for lnk in lnk_emp:
            g = grave_emp.get(lnk["id"])
            if g and (grav is None or GRAVEDAD_ORDEN.index(g) < GRAVEDAD_ORDEN.index(grav)):
                grav = g
        if grav:
            puntos += PESOS["incidencia"][grav]
            if PESOS["incidencia"][grav]:
                motivos.append(f"incidencia {grav.lower()} abierta del cliente")
            urgente = urgente or grav == "Crítica"

        accion = "Definir y registrar la próxima acción" if sin_prox else prox
        if grav in GRAVEDAD_ALERTA:
            accion = f"Revisar la incidencia abierta antes de contactar; después: {accion[0].lower() + accion[1:]}"
        plazo = "hoy" if urgente else ("esta semana" if puntos >= UMBRAL_ESTA_SEMANA else "en los próximos 14 días")

        impacto = f"valor ponderado {eur(ponderado)} (importe {eur(importe)})" if importe else "importe no informado en el CRM"
        acciones.append({"empresa": empresa, "etapa": etapa, "puntos": round(puntos, 1), "accion": accion,
                         "motivos": motivos, "impacto": impacto, "plazo": plazo})
    acciones.sort(key=lambda a: (-a["puntos"], a["empresa"]))

    # ---- Alertas ----
    tareas = []
    for t in tablas["Tareas"]:
        if texto(t.get("estado")) not in TAREA_ABIERTA:
            continue
        v = fecha(t.get("vencimiento"))
        if v is None or v > hoy:
            continue
        atraso = (hoy - v).days
        prio = texto(t.get("prioridad"))
        tareas.append((atraso, PRIORIDAD_ORDEN.index(prio) if prio in PRIORIDAD_ORDEN else 9, texto(t.get("descripción")),
                       "vence hoy" if atraso == 0 else f"atrasada {plural(atraso, 'día', 'días')}", prio or "sin prioridad"))
    tareas.sort(key=lambda x: (x[1], -x[0], x[2]))  # primero la prioridad, después la antigüedad

    ofertas = []
    for o in tablas["Ofertas"]:
        if texto(o.get("estado")) not in OFERTA_VIVA:
            continue
        v = fecha(o.get("validez"))
        if v is None:
            continue
        dias = (v - hoy).days
        if dias > DIAS_OFERTA_PROXIMA:
            continue
        empresa = "empresa sin identificar"
        for lnk in enlaces(o.get("oportunidad")):
            op = oportunidades.get(lnk["id"])
            if op and empresa_de_oportunidad(op):
                empresa = nombre_empresa(empresa_de_oportunidad(op)[0])
        estado = texto(o.get("estado")).lower()
        cod = texto(o.get("ID")) or "oferta"
        if dias < 0:
            msg = f"{cod} · {empresa}: validez vencida hace {plural(-dias, 'día', 'días')} y sigue en estado «{estado}»; actualiza el estado"
        elif dias == 0:
            msg = f"{cod} · {empresa}: caduca hoy ({estado})"
        else:
            msg = f"{cod} · {empresa}: caduca en {plural(dias, 'día', 'días')} ({estado})"
        ofertas.append((dias, msg))
    ofertas.sort()

    graves = []
    for eid, lista in incidencias_graves.items():
        nombre = nombre_empresa({"id": eid, "value": texto(empresas.get(eid, {}).get("ID"))})
        graves.append((GRAVEDAD_ORDEN.index(grave_emp[eid]), nombre, "; ".join(sorted(lista))))
    graves.sort()

    inactivos = []
    if tiene_empresas:
        for eid, e in empresas.items():
            if texto(e.get("estado")) != "Cliente Activo":
                continue
            ult = ultimo_emp.get(eid)
            nombre = texto(e.get("razón social")) or texto(e.get("ID")) or f"empresa {eid}"
            if ult is None:
                inactivos.append((9999, nombre, "sin interacciones registradas"))
                continue
            dias = (hoy - ult).days
            tramo = next((t for t in TRAMOS_INACTIVIDAD if dias >= t), None)
            if tramo:
                inactivos.append((dias, nombre, f"{dias} días sin interacción (tramo de {tramo})"))
        inactivos.sort(key=lambda x: (-x[0], x[1]))

    return {
        "hoy": hoy.isoformat(),
        "resumen": {"oportunidades_abiertas": abiertas, "importe_abierto": round(imp_total, 2),
                    "valor_ponderado": round(pond_total, 2)},
        "acciones": acciones[:NUM_ACCIONES],
        "alertas": {
            "tareas": tareas,
            "sin_proxima_accion": sorted(sin_proxima),
            "estancadas": sorted(estancadas, key=lambda x: (-(x[2] if x[2] is not None else 9999), x[0])),
            "ofertas": [m for _, m in ofertas],
            "incidencias_graves": [(n, d) for _, n, d in graves],
            "clientes_inactivos": [(n, d) for _, n, d in inactivos],
            "inactividad_disponible": tiene_empresas,
        },
    }


# ==========================================================================
# Texto del informe
# ==========================================================================
def _bloque(titulo: str, lineas: list[str]) -> list[str]:
    if not lineas:
        return []
    visibles = lineas[:MAX_POR_ALERTA]
    extra = len(lineas) - len(visibles)
    out = [f"{titulo} ({len(lineas)})"] + [f"• {x}" for x in visibles]
    if extra > 0:
        out.append(f"• … y {extra} más")
    return out + [""]


def redactar(res: dict, avisos: list[str]) -> str:
    hoy = date.fromisoformat(res["hoy"])
    r, al = res["resumen"], res["alertas"]
    L = [f"Plan del día · {DIAS_SEMANA[hoy.weekday()]} {fmt_fecha(hoy)}", ""]
    L.append(f"Pipeline abierto: {plural(r['oportunidades_abiertas'], 'oportunidad', 'oportunidades')} · "
             f"importe {eur(r['importe_abierto'])} · valor ponderado {eur(r['valor_ponderado'])}")
    L.append("")
    L.append(f"TUS {NUM_ACCIONES} ACCIONES PRIORITARIAS" if len(res["acciones"]) >= NUM_ACCIONES else "ACCIONES PRIORITARIAS")
    if not res["acciones"]:
        L += ["No hay oportunidades abiertas en el CRM.", ""]
    for i, a in enumerate(res["acciones"], 1):
        puntos_es = f"{a['puntos']:g}".replace(".", ",")
        L += [f"{i}. {a['empresa']} ({a['etapa']}) · {puntos_es} puntos",
              f"   Acción: {a['accion']}",
              f"   Motivo: {'; '.join(a['motivos'])}",
              f"   Impacto: {a['impacto']}",
              f"   Plazo: {a['plazo']}", ""]

    L.append("ALERTAS")
    antes = len(L)
    L += _bloque("Compromisos que vencen hoy o están atrasados",
                 [f"{d} ({v}; prioridad {p.lower()})" for _, _, d, v, p in al["tareas"]])
    L += _bloque("Oportunidades abiertas sin próxima acción", [f"{e} ({et})" for e, et in al["sin_proxima_accion"]])
    L += _bloque("Oportunidades estancadas (más de 30 días sin contacto)",
                 [f"{e} ({et}): " + ("sin contacto registrado" if d is None else f"{d} días") for e, et, d in al["estancadas"]])
    L += _bloque("Ofertas que caducan en 7 días o ya vencidas", al["ofertas"])
    L += _bloque("Clientes con incidencia crítica o alta abierta", [f"{n}: {d}" for n, d in al["incidencias_graves"]])
    if al["inactividad_disponible"]:
        L += _bloque("Clientes activos sin interacción", [f"{n}: {d}" for n, d in al["clientes_inactivos"]])
    else:
        L += ["Clientes inactivos: no calculado (falta la tabla Empresas).", ""]
    if len(L) == antes:
        L += ["Sin alertas hoy.", ""]
    for a in avisos:
        L.append(f"Aviso: {a}")
    L.append("Informe interno automático (Nivel A). Cálculo con reglas fijas; no se ha enviado nada a ningún cliente.")
    texto_final = "\n".join(L).rstrip() + "\n"
    if len(texto_final) > LIMITE_TELEGRAM:
        texto_final = texto_final[: LIMITE_TELEGRAM - 40].rstrip() + "\n… (informe recortado por longitud)\n"
    return texto_final


# ==========================================================================
# Envío por Telegram
# ==========================================================================
def enviar_telegram(mensaje: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat:
        raise ErrorInforme("Para --enviar hacen falta TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID.")
    datos = urllib.parse.urlencode({"chat_id": chat, "text": mensaje}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=datos)
    try:
        urllib.request.urlopen(req, timeout=30).read()
    except urllib.error.HTTPError as exc:
        raise ErrorInforme(f"Telegram respondió {exc.code}. Revisa el token del bot y el id del chat.") from None
    except (urllib.error.URLError, TimeoutError):
        raise ErrorInforme("No se pudo conectar con Telegram.") from None


def hoy_madrid() -> date:
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Madrid")).date()
    except Exception:  # noqa: BLE001  (sin base de zonas horarias: se usa la fecha local)
        return date.today()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fixture", help="Archivo JSON con datos de ejemplo; no usa Baserow")
    p.add_argument("--hoy", help="Fecha AAAA-MM-DD para el cálculo (por defecto, hoy en Madrid o la del fixture)")
    p.add_argument("--enviar", action="store_true", help="Envía el informe por Telegram y no lo imprime")
    p.add_argument("--mostrar", action="store_true", help="Con --enviar, imprime también el informe")
    p.add_argument("--json", action="store_true", help="Imprime el resultado estructurado en lugar del texto")
    args = p.parse_args()

    try:
        avisos: list[str] = []
        if args.fixture:
            tablas, hoy_fx = cargar_fixture(Path(args.fixture))
        else:
            tablas, avisos = cargar_baserow()
            hoy_fx = None
        hoy = date.fromisoformat(args.hoy) if args.hoy else (hoy_fx or hoy_madrid())
        resultado = calcular(tablas, hoy)
        informe = redactar(resultado, avisos)
        if args.enviar:
            enviar_telegram(informe)
            print(f"Informe enviado por Telegram ({len(informe)} caracteres, "
                  f"{len(resultado['acciones'])} acciones, "
                  f"{sum(len(v) for k, v in resultado['alertas'].items() if isinstance(v, list))} alertas).")
        if args.json:
            print(json.dumps(resultado, ensure_ascii=False, indent=2, default=str))
        elif not args.enviar or args.mostrar:
            print(informe, end="")
        return 0
    except ErrorInforme as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Error: fecha no válida ({exc})", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
