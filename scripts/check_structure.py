#!/usr/bin/env python3
"""Validación de la estructura del repositorio del Copiloto Comercial.

Comprueba, sin llamar a ninguna API:
  1. Que existen los archivos y carpetas que exige CLAUDE.md.
  2. Que los esquemas JSON son válidos y el de extracción cumple las
     restricciones de la salida estructurada de la API de Claude.
  3. Que las opciones de etapa, tipo y prioridad del esquema de extracción
     coinciden con el esquema del CRM (la fuente de verdad), y que el propio
     esquema del CRM es coherente.
  4. Que los prompts versionados y las skills tienen su cabecera, que solo hay
     una versión vigente por prompt y que el CHANGELOG las recoge.
  5. Que los workflows de GitHub Actions son válidos y siguen las reglas de
     seguridad del proyecto (permisos mínimos, secretos permitidos, sin
     inyección desde entradas, evaluación solo manual).
  6. Que no hay secretos escritos en ningún archivo y que los enlaces
     relativos de los documentos Markdown apuntan a archivos que existen.

Uso:   python scripts/check_structure.py
Salida: código 0 si todo es correcto; 1 si hay errores. Los avisos no fallan.
Requiere: pip install jsonschema pyyaml
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
    import yaml
except ImportError as exc:  # pragma: no cover
    sys.exit(f"Falta una dependencia ({exc.name}). Instala con: pip install jsonschema pyyaml")

RAIZ = Path(__file__).resolve().parent.parent

REQUERIDOS = [
    "CLAUDE.md", "README.md", "LICENSE", "about-me.md", ".gitignore",
    "prompt_maestro_curso_claude.md", "informe_final_agente_ia_delegado_comercial.md",
    "prompts/CHANGELOG.md",
    "schemas/crm-baserow.json", "schemas/extraccion-visita.schema.json",
    "skills/extraccion-visita.md", "skills/generacion-briefing.md",
    "skills/evaluacion-agente.md", "skills/prioridades-diarias.md",
    "docs/arquitectura.md", "docs/puesta-en-marcha.md", "docs/politica-autonomia.md", "docs/privacidad-y-conservacion.md",
    "docs/base-conocimiento/catalogo-ejemplo.md", "docs/base-conocimiento/tarifa-2026.md",
    "evals/README.md", "evals/casos.jsonl", "evals/run_eval.py", "evals/fixtures/crm-demo.json",
    "scripts/check_structure.py", "scripts/prioridades_diarias.py",
    ".github/workflows/validar-estructura.yml", ".github/workflows/eval-extraccion.yml",
    ".github/workflows/informe-diario.yml",
]

TABLAS_CRM = ["Empresas", "Contactos", "Oportunidades", "Interacciones", "Tareas", "Productos",
              "Ofertas", "Pedidos", "Incidencias", "Documentos", "Fuentes", "Auditoría"]

# Palabras clave de JSON Schema que la salida estructurada de la API no admite (ver CLAUDE.md).
CLAVES_PROHIBIDAS = ("minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "minLength", "maxLength")

SECRETOS_PERMITIDOS = {"ANTHROPIC_API_KEY", "BASEROW_TOKEN", "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "GITHUB_TOKEN"}
VARIABLES_PERMITIDAS = re.compile(r"^(BASEROW_URL|BASEROW_TABLE_[A-Z]+|CLAUDE_MODEL)$")

# Disparadores esperados por workflow: (obligatorios, prohibidos).
DISPARADORES = {
    "validar-estructura.yml": ({"push", "pull_request"}, set()),
    "eval-extraccion.yml": ({"workflow_dispatch"}, {"push", "pull_request", "schedule"}),  # tiene coste: solo a mano
    "informe-diario.yml": ({"schedule", "workflow_dispatch"}, {"pull_request"}),
}

PATRONES_SECRETOS = {
    "clave de API de Anthropic": r"sk-ant-[A-Za-z0-9_\-]{20,}",
    "token de GitHub": r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})",
    "token de bot de Telegram": r"\b\d{8,10}:[A-Za-z0-9_\-]{35}\b",
    "clave de AWS": r"\bAKIA[0-9A-Z]{16}\b",
    "clave privada": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
}
EXCLUIR_ESCANEO = {".git", "__pycache__", "node_modules"}

errores: list[str] = []
avisos: list[str] = []


def error(msg: str) -> None:
    errores.append(msg)
    print(f"  ✗ {msg}")


def aviso(msg: str) -> None:
    avisos.append(msg)
    print(f"  ! {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def seccion(titulo: str) -> None:
    print(f"\n{titulo}")


def leer_json(ruta: str):
    try:
        return json.loads((RAIZ / ruta).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error(f"{ruta}: no se puede leer como JSON ({exc})")
        return None


def cabecera(ruta: Path) -> dict | None:
    """Devuelve la cabecera YAML (--- ... ---) de un archivo, o None si no la tiene."""
    texto = ruta.read_text(encoding="utf-8")
    if not texto.startswith("---"):
        return None
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return None
    try:
        datos = yaml.safe_load(partes[1])
    except yaml.YAMLError:
        return None
    return datos if isinstance(datos, dict) else None


# --------------------------------------------------------------------------
# 1. Archivos requeridos
# --------------------------------------------------------------------------
def comprobar_archivos() -> None:
    seccion("1. Archivos y carpetas requeridos")
    faltan = [r for r in REQUERIDOS if not (RAIZ / r).exists()]
    for r in faltan:
        error(f"Falta {r}")
    if not faltan:
        ok(f"{len(REQUERIDOS)} archivos presentes")
    gi = RAIZ / ".gitignore"
    if gi.exists():
        lineas = {linea.strip() for linea in gi.read_text(encoding="utf-8").splitlines()}
        for patron in (".env", "evals/resultados/*.json"):
            if patron not in lineas:
                error(f".gitignore debe incluir «{patron}»")
        if {".env", "evals/resultados/*.json"} <= lineas:
            ok(".gitignore protege .env y los resultados de evaluación")


# --------------------------------------------------------------------------
# 2. Esquemas
# --------------------------------------------------------------------------
def subesquemas(nodo: dict, ruta: str):
    """Recorre un esquema visitando solo nodos que son esquemas (no nombres de propiedades)."""
    yield nodo, ruta
    for clave in ("properties", "$defs", "definitions", "patternProperties"):
        for nombre, sub in (nodo.get(clave) or {}).items():
            if isinstance(sub, dict):
                yield from subesquemas(sub, f"{ruta}/{clave}/{nombre}")
    for clave in ("items", "not", "if", "then", "else", "additionalProperties", "contains"):
        sub = nodo.get(clave)
        if isinstance(sub, dict):
            yield from subesquemas(sub, f"{ruta}/{clave}")
    for clave in ("anyOf", "oneOf", "allOf", "prefixItems"):
        for i, sub in enumerate(nodo.get(clave) or []):
            if isinstance(sub, dict):
                yield from subesquemas(sub, f"{ruta}/{clave}[{i}]")


def comprobar_esquema_extraccion(esq: dict) -> None:
    try:
        jsonschema.Draft202012Validator.check_schema(esq)
        ok("extraccion-visita.schema.json es JSON Schema válido (draft 2020-12)")
    except jsonschema.SchemaError as exc:
        error(f"extraccion-visita.schema.json no es un esquema válido: {exc.message}")
        return
    problemas = 0
    for nodo, ruta in subesquemas(esq, "#"):
        tipos = nodo.get("type")
        tipos = tipos if isinstance(tipos, list) else [tipos]
        if ("object" in tipos or "properties" in nodo) and nodo.get("additionalProperties") is not False:
            error(f"{ruta}: los objetos deben llevar additionalProperties: false"); problemas += 1
        for k in CLAVES_PROHIBIDAS:
            if k in nodo:
                error(f"{ruta}: «{k}» no se admite en la salida estructurada de la API"); problemas += 1
        if "minItems" in nodo and nodo["minItems"] not in (0, 1):
            error(f"{ruta}: minItems solo puede ser 0 o 1 (es {nodo['minItems']})"); problemas += 1
        if "properties" in nodo and "required" in nodo:
            sin = [r for r in nodo["required"] if r not in nodo["properties"]]
            if sin:
                error(f"{ruta}: required nombra propiedades inexistentes: {sin}"); problemas += 1
        if "properties" in nodo and set(nodo.get("required", [])) != set(nodo["properties"]):
            aviso(f"{ruta}: hay propiedades no obligatorias; el esquema de extracción las exige todas para no omitir datos")
    if not problemas:
        ok("Cumple las restricciones de la API (additionalProperties, sin límites, minItems 0 o 1)")


def comprobar_crm(crm: dict) -> dict[str, dict[str, list[str]]]:
    """Valida el esquema del CRM y devuelve {tabla: {campo_select: opciones}}."""
    selects: dict[str, dict[str, list[str]]] = {}
    tablas = {t.get("nombre"): t for t in crm.get("tablas", [])}
    if sorted(tablas) != sorted(TABLAS_CRM):
        error(f"crm-baserow.json debe tener exactamente las 12 tablas {TABLAS_CRM}; tiene {sorted(tablas)}")
    n_sel = 0
    problemas = 0
    for nombre, t in tablas.items():
        vistos = set()
        selects[nombre] = {}
        for c in t.get("campos", []):
            if c["nombre"] in vistos:
                error(f"{nombre}: campo repetido «{c['nombre']}»"); problemas += 1
            vistos.add(c["nombre"])
            if c.get("tipo") == "single_select":
                n_sel += 1
                ops = c.get("opciones", [])
                selects[nombre][c["nombre"]] = ops
                if not ops or len(ops) != len(set(ops)):
                    error(f"{nombre}.{c['nombre']}: las opciones están vacías o repetidas"); problemas += 1
            if c.get("tipo") == "link_row" and c.get("enlaza_con") not in tablas:
                error(f"{nombre}.{c['nombre']}: enlaza con una tabla inexistente ({c.get('enlaza_con')})"); problemas += 1
    if not problemas:
        ok(f"crm-baserow.json: {len(tablas)} tablas, {n_sel} selects, enlaces e identificadores coherentes")
    return selects


def comprobar_enumeraciones(esq: dict, selects: dict) -> None:
    props = esq.get("properties", {})
    pares = [
        ("tipo_interaccion", props.get("tipo_interaccion", {}).get("enum"), ("Interacciones", "tipo")),
        ("etapa_sugerida", props.get("etapa_sugerida", {}).get("enum"), ("Oportunidades", "etapa")),
        ("compromiso.prioridad_sugerida",
         esq.get("$defs", {}).get("compromiso", {}).get("properties", {}).get("prioridad_sugerida", {}).get("enum"),
         ("Tareas", "prioridad")),
    ]
    todos_ok = True
    for nombre, enum, (tabla, campo) in pares:
        crm = selects.get(tabla, {}).get(campo)
        if enum is None or crm is None:
            error(f"No se puede comparar {nombre} con {tabla}.{campo}"); todos_ok = False
            continue
        extra = [e for e in enum if e != "desconocido"]
        if extra != crm:
            error(f"{nombre} {extra} no coincide con {tabla}.{campo} {crm}"); todos_ok = False
    if todos_ok:
        ok("Las enumeraciones de extracción coinciden con las del CRM (salvo «desconocido»)")


# --------------------------------------------------------------------------
# 3. Prompts y skills
# --------------------------------------------------------------------------
def comprobar_prompts_y_skills() -> None:
    seccion("4. Prompts versionados y skills")
    changelog = (RAIZ / "prompts/CHANGELOG.md").read_text(encoding="utf-8") if (RAIZ / "prompts/CHANGELOG.md").exists() else ""
    vigentes: dict[str, list[str]] = {}
    n = 0
    for f in sorted((RAIZ / "prompts").glob("*.md")):
        if f.name == "CHANGELOG.md":
            continue
        n += 1
        h = cabecera(f)
        if not h:
            error(f"{f.relative_to(RAIZ)}: falta la cabecera YAML"); continue
        falta = [k for k in ("nombre", "version", "fecha", "estado") if k not in h]
        if falta:
            error(f"{f.relative_to(RAIZ)}: faltan campos en la cabecera: {falta}"); continue
        if f.name != f"{h['nombre']}-{h['version']}.md":
            error(f"{f.name}: el nombre del archivo debe ser {h['nombre']}-{h['version']}.md")
        if f"### {h['version']} " not in changelog:
            error(f"{f.name}: la versión {h['version']} no está anotada en prompts/CHANGELOG.md")
        if str(h["estado"]).startswith("vigente"):
            vigentes.setdefault(h["nombre"], []).append(f.name)
    for nombre, lista in vigentes.items():
        if len(lista) > 1:
            error(f"Hay varias versiones vigentes de {nombre}: {lista}")
    if n and not any(e.startswith("Hay varias") or "prompts/" in e for e in errores):
        ok(f"{n} prompts con cabecera, nombre coherente, anotados en el CHANGELOG y una sola versión vigente por prompt")

    # Los valores por defecto del evaluador deben apuntar a versiones vigentes.
    run = (RAIZ / "evals/run_eval.py").read_text(encoding="utf-8") if (RAIZ / "evals/run_eval.py").exists() else ""
    for const in ("SYSTEM_DEFECTO", "TAREA_DEFECTO"):
        m = re.search(rf'{const}\s*=\s*RAIZ\s*/\s*"prompts"\s*/\s*"([^"]+)"', run)
        if not m:
            aviso(f"No se pudo leer {const} de evals/run_eval.py"); continue
        h = cabecera(RAIZ / "prompts" / m.group(1)) if (RAIZ / "prompts" / m.group(1)).exists() else None
        if not h or not str(h.get("estado", "")).startswith("vigente"):
            error(f"run_eval.py usa {m.group(1)} por defecto, pero no existe o no está vigente")
    ok("El evaluador usa por defecto prompts vigentes") if not any("run_eval.py usa" in e for e in errores) else None

    skills = sorted((RAIZ / "skills").glob("*.md"))
    malas = 0
    for f in skills:
        h = cabecera(f)
        if not h or h.get("name") != f.stem or not str(h.get("description", "")).strip():
            error(f"skills/{f.name}: la cabecera debe tener name={f.stem} y description"); malas += 1
    if skills and not malas:
        ok(f"{len(skills)} skills con cabecera name/description correcta")


# --------------------------------------------------------------------------
# 4. Workflows
# --------------------------------------------------------------------------
def disparadores(wf: dict) -> set[str]:
    on = wf.get("on", wf.get(True))  # PyYAML interpreta la clave «on» como True
    if isinstance(on, str):
        return {on}
    if isinstance(on, list):
        return set(on)
    return set(on or {})


def comprobar_workflows() -> None:
    seccion("5. Workflows de GitHub Actions")
    carpeta = RAIZ / ".github/workflows"
    archivos = sorted(carpeta.glob("*.y*ml")) if carpeta.exists() else []
    if not archivos:
        error("No hay workflows en .github/workflows"); return
    previos = len(errores)
    for f in archivos:
        raw = f.read_text(encoding="utf-8")
        try:
            wf = yaml.safe_load(raw)
        except yaml.YAMLError as exc:
            error(f"{f.name}: YAML no válido ({exc})"); continue
        if not isinstance(wf, dict) or not wf.get("name"):
            error(f"{f.name}: debe tener «name»"); continue
        trig = disparadores(wf)
        if not trig:
            error(f"{f.name}: no define disparadores (on)")
        oblig, prohib = DISPARADORES.get(f.name, (set(), set()))
        if oblig - trig:
            error(f"{f.name}: faltan disparadores {sorted(oblig - trig)}")
        if prohib & trig:
            error(f"{f.name}: no debe dispararse con {sorted(prohib & trig)}")
        if "permissions" not in wf:
            error(f"{f.name}: declara «permissions» al nivel del workflow (permisos mínimos)")
        jobs = wf.get("jobs") or {}
        if not jobs:
            error(f"{f.name}: no tiene jobs")
        for jn, job in jobs.items():
            if "runs-on" not in job:
                error(f"{f.name}/{jn}: falta runs-on")
            if not job.get("steps"):
                error(f"{f.name}/{jn}: no tiene steps")
            if "timeout-minutes" not in job:
                aviso(f"{f.name}/{jn}: conviene fijar timeout-minutes")
            for st in job.get("steps", []):
                uses = st.get("uses")
                if uses and ("@" not in uses or uses.split("@")[1] in ("main", "master")):
                    error(f"{f.name}: la acción «{uses}» debe fijarse a una versión, no a main/master")
                run = st.get("run", "")
                if re.search(r"\$\{\{\s*(?:github\.event\.|inputs\.|github\.head_ref)", run):
                    error(f"{f.name}: no interpoles entradas en «run» (riesgo de inyección); pásalas por env")
        usados = set(re.findall(r"secrets\.([A-Za-z0-9_]+)", raw))
        if usados - SECRETOS_PERMITIDOS:
            error(f"{f.name}: usa secretos no documentados en CLAUDE.md: {sorted(usados - SECRETOS_PERMITIDOS)}")
        for v in set(re.findall(r"vars\.([A-Za-z0-9_]+)", raw)):
            if not VARIABLES_PERMITIDAS.match(v):
                error(f"{f.name}: usa la variable «{v}» no documentada en CLAUDE.md")
        if (usados - {"GITHUB_TOKEN"}) and "pull_request" in trig:
            error(f"{f.name}: usa secretos y se dispara con pull_request (los secretos no deben exponerse a ramas ajenas)")
    if len(errores) == previos:
        ok(f"{len(archivos)} workflows válidos: permisos mínimos, acciones fijadas, secretos y variables documentados, sin inyección, evaluación solo manual")


# --------------------------------------------------------------------------
# 5. Secretos y enlaces
# --------------------------------------------------------------------------
def archivos_de_texto():
    for p in RAIZ.rglob("*"):
        if p.is_file() and not (EXCLUIR_ESCANEO & set(p.relative_to(RAIZ).parts)):
            try:
                yield p, p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue


def comprobar_secretos_y_enlaces() -> None:
    seccion("6. Secretos escritos y enlaces entre documentos")
    previos = len(errores)
    n = 0
    for p, texto in archivos_de_texto():
        n += 1
        rel = p.relative_to(RAIZ)
        for nombre, patron in PATRONES_SECRETOS.items():
            if re.search(patron, texto):
                error(f"{rel}: parece contener {nombre}. Retírala y revócala")
    if len(errores) == previos:
        ok(f"Ningún secreto reconocible en {n} archivos de texto")
    previos = len(errores)
    enlaces = 0
    for p, texto in archivos_de_texto():
        if p.suffix != ".md":
            continue
        sin_codigo = re.sub(r"```.*?```", "", texto, flags=re.S)
        sin_codigo = re.sub(r"`[^`\n]*`", "", sin_codigo)
        for destino in re.findall(r"\]\(([^)\s]+)\)", sin_codigo):
            if re.match(r"^(https?:|mailto:|#)", destino):
                continue
            enlaces += 1
            ruta = destino.split("#")[0]
            if ruta and not (p.parent / ruta).exists():
                error(f"{p.relative_to(RAIZ)}: enlace roto → {destino}")
    if len(errores) == previos:
        ok(f"{enlaces} enlaces relativos resueltos")


def comprobar_casos_y_fixture() -> None:
    seccion("3b. Casos de evaluación y datos de ejemplo")
    ruta = RAIZ / "evals/casos.jsonl"
    if ruta.exists():
        ids, malos = [], 0
        for n, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            if not linea.strip():
                continue
            try:
                c = json.loads(linea)
            except json.JSONDecodeError:
                error(f"casos.jsonl línea {n}: JSON no válido"); malos += 1; continue
            ids.append(c.get("id"))
            if any(k not in c for k in ("id", "nombre", "nota", "fecha_hoy", "esperado")):
                error(f"casos.jsonl línea {n}: faltan campos obligatorios"); malos += 1
        if len(ids) != len(set(ids)):
            error("casos.jsonl: hay ids repetidos"); malos += 1
        if not malos:
            ok(f"{len(ids)} casos de evaluación bien formados")
    fx = leer_json("evals/fixtures/crm-demo.json")
    if fx is not None:
        tablas = fx.get("tablas", {})
        falta = [t for t in ("Oportunidades", "Interacciones", "Tareas", "Ofertas", "Incidencias") if t not in tablas]
        if falta or "hoy" not in fx:
            error(f"crm-demo.json: faltan {falta or ['hoy']}")
        else:
            ok("crm-demo.json tiene las tablas y la fecha que necesita el informe diario")


def main() -> int:
    print("Comprobando la estructura del repositorio…")
    comprobar_archivos()
    seccion("2. Esquemas JSON")
    crm = leer_json("schemas/crm-baserow.json")
    esq = leer_json("schemas/extraccion-visita.schema.json")
    if crm is not None and esq is not None:
        comprobar_esquema_extraccion(esq)
        selects = comprobar_crm(crm)
        seccion("3. Coherencia entre el CRM y la extracción")
        comprobar_enumeraciones(esq, selects)
    comprobar_casos_y_fixture()
    comprobar_prompts_y_skills()
    comprobar_workflows()
    comprobar_secretos_y_enlaces()
    print("\n" + "-" * 60)
    print(f"{len(errores)} error(es), {len(avisos)} aviso(s)")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
