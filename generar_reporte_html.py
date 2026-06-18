#!/usr/bin/env python3
"""
Generador de Reportes HTML Profesionales - Global Infinity Marketing
Genera documentos HTML autónomos con CSS embebido, diseño corporativo,
navegación entre pasos, índice de contenidos y soporte de impresión A4.

Uso:
  python generar_reporte_html.py --data-file datos.json --paso 1.1 --cliente "Nombre" --analista "Ana"
  python generar_reporte_html.py --status --cliente "Nombre"
  python generar_reporte_html.py --listar
  python generar_reporte_html.py --generate-index --cliente "Nombre"
"""

import argparse
import datetime
import json
import logging
import os
import pathlib
import re
import sys
from functools import partial

from utils import sanitizar_nombre, listar_clientes

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "Clientes")

COLOR = {
    "azul_oscuro": "#1a2a4a", "azul_medio": "#2d5f8a", "azul_claro": "#4a8bc2",
    "dorado": "#d4a030", "dorado_claro": "#f0d080", "blanco": "#ffffff",
    "gris_claro": "#f5f7fa", "gris_medio": "#e8ecf1", "gris_texto": "#6b7280",
    "texto_oscuro": "#1f2937", "verde": "#10b981", "rojo": "#ef4444", "naranja": "#f59e0b",
}

CSS = r"""@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{
    font-family:'Inter',-apple-system,sans-serif;
    background:linear-gradient(135deg,#f5f7fa 0%,#e8ecf1 50%,#f5f7fa 100%);
    color:#1f2937;line-height:1.6;min-height:100vh;padding:40px 20px}
.container{max-width:1000px;margin:0 auto}
.nav-bar{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;gap:10px;flex-wrap:wrap}
.nav-bar a{text-decoration:none;font-size:13px;font-weight:600;padding:8px 18px;border-radius:25px;transition:all .2s;display:inline-flex;align-items:center;gap:6px}
.nav-index{background:linear-gradient(135deg,#1a2a4a,#2d5f8a);color:#fff;box-shadow:0 2px 10px rgba(26,42,74,.2)}
.nav-index:hover{transform:translateY(-1px);box-shadow:0 4px 15px rgba(26,42,74,.3)}
.nav-prev,.nav-next{background:#fff;color:#1a2a4a;border:1px solid #d1d5db}
.nav-prev:hover,.nav-next:hover{background:#f3f4f6;border-color:#9ca3af}
.nav-disabled{opacity:.3;pointer-events:none}
.nav-center{display:flex;gap:10px}
.header{
    background:linear-gradient(135deg,#1a2a4a 0%,#2d5f8a 50%,#1a2a4a 100%);
    border-radius:20px;padding:0;margin-bottom:30px;box-shadow:0 15px 50px rgba(26,42,74,.3);position:relative;overflow:hidden}
.header::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(212,160,48,.1) 0%,transparent 70%);animation:shimmer 8s ease-in-out infinite}
@keyframes shimmer{0%,100%{transform:translate(0,0)}50%{transform:translate(5%,5%)}}
.header-content{padding:40px 50px;position:relative;z-index:1}
.header-badge{display:inline-block;background:rgba(212,160,48,.2);border:1px solid rgba(212,160,48,.4);color:#f0d080;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:2px;padding:4px 14px;border-radius:20px;margin-bottom:15px}
.header h1{font-family:'Playfair Display',serif;font-size:38px;color:#fff;margin-bottom:5px;letter-spacing:-.5px}
.header .subtitle{font-size:16px;color:rgba(255,255,255,.75);font-weight:300}
.header-meta{display:flex;gap:20px;margin-top:20px;flex-wrap:wrap}
.header-meta-item{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:8px 16px;font-size:13px;color:rgba(255,255,255,.85);display:flex;align-items:center;gap:8px}
.header-meta-item strong{color:#fff}
.card{
    background:#fff;border-radius:16px;padding:30px 35px;margin-bottom:24px;
    box-shadow:0 4px 20px rgba(0,0,0,.06);border:1px solid rgba(0,0,0,.04);transition:transform .2s,box-shadow .2s}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,0,0,.1)}
.card-icon{font-size:28px;margin-bottom:10px}
.card h2{font-size:20px;font-weight:700;color:#1a2a4a;margin-bottom:15px;display:flex;align-items:center;gap:10px}
.card h2 .emoji{font-size:24px}
.card h3{font-size:16px;font-weight:600;color:#2d5f8a;margin:15px 0 8px}
.card p,.card li{font-size:15px;color:#4b5563;line-height:1.7}
.kv-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-top:10px}
.kv-item{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px}
.kv-item .label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;color:#6b7280;margin-bottom:4px}
.kv-item .value{font-size:15px;font-weight:500;color:#1f2937}
.badge{display:inline-block;padding:3px 12px;border-radius:12px;font-size:12px;font-weight:600}
.badge-blue{background:#dbeafe;color:#1d4ed8}
.badge-green{background:#d1fae5;color:#059669}
.badge-gold{background:#fef3c7;color:#b45309}
.badge-red{background:#fee2e2;color:#dc2626}
.badge-purple{background:#ede9fe;color:#7c3aed}
.table-container{overflow-x:auto;margin-top:10px}
table{width:100%;border-collapse:separate;border-spacing:0;font-size:14px;border-radius:12px;overflow:hidden}
thead th{background:linear-gradient(135deg,#1a2a4a,#2d5f8a);color:#fff;font-weight:600;font-size:13px;text-align:left;padding:12px 16px;letter-spacing:.3px}
thead th:not(:last-child){border-right:1px solid rgba(255,255,255,.1)}
tbody tr:nth-child(even){background:#f8fafc}
tbody tr:hover{background:#eef2ff}
tbody td{padding:10px 16px;border-bottom:1px solid #e5e7eb;color:#374151}
tbody tr:last-child td{border-bottom:none}
.section-divider{border:none;height:2px;background:linear-gradient(90deg,transparent,#d4a030,transparent);margin:30px 0;opacity:.5}
.foda-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:10px}
.foda-card{border-radius:12px;padding:20px;border:1px solid}
.foda-card h3{font-size:16px;font-weight:700;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.foda-card ul{list-style:none}
.foda-card li{padding:6px 0;border-bottom:1px solid rgba(0,0,0,.05);font-size:14px;display:flex;align-items:flex-start;gap:8px}
.foda-card li:last-child{border-bottom:none}
.foda-fortaleza{background:#ecfdf5;border-color:#a7f3d0}
.foda-fortaleza h3{color:#059669}
.foda-debilidad{background:#fef2f2;border-color:#fecaca}
.foda-debilidad h3{color:#dc2626}
.foda-oportunidad{background:#eff6ff;border-color:#bfdbfe}
.foda-oportunidad h3{color:#2563eb}
.foda-amenaza{background:#fff7ed;border-color:#fed7aa}
.foda-amenaza h3{color:#d97706}
.timeline{position:relative;padding-left:30px;margin-top:10px}
.timeline::before{content:'';position:absolute;left:10px;top:0;bottom:0;width:3px;background:linear-gradient(180deg,#1a2a4a,#d4a030);border-radius:3px}
.timeline-item{position:relative;margin-bottom:20px;padding-left:20px}
.timeline-item::before{content:'\25CF';position:absolute;left:-25px;top:0;font-size:16px;color:#d4a030}
.timeline-item .tl-title{font-weight:600;font-size:15px;color:#1a2a4a}
.timeline-item .tl-desc{font-size:13px;color:#6b7280;margin-top:2px}
.kpi-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px;margin-top:12px}
.kpi-card{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:18px;text-align:center;transition:transform .2s}
.kpi-card:hover{transform:translateY(-3px)}
.kpi-card .kpi-icon{font-size:32px;margin-bottom:6px}
.kpi-card .kpi-value{font-size:24px;font-weight:800;color:#1a2a4a}
.kpi-card .kpi-label{font-size:12px;color:#6b7280;font-weight:500;text-transform:uppercase;letter-spacing:.5px}
.footer{text-align:center;padding:25px;color:#9ca3af;font-size:13px;border-top:1px solid #e5e7eb;margin-top:40px}
.footer strong{color:#2d5f8a}
@media print{
    @page{size:A4;margin:15mm 15mm 20mm 15mm}
    body{background:#fff!important;padding:0!important;font-size:11pt;color:#000;-webkit-print-color-adjust:exact;print-color-adjust:exact}
    .container{max-width:100%}
    .nav-bar{display:none!important}
    .card{box-shadow:none!important;border:1px solid #ddd;break-inside:avoid}
    .card:hover{transform:none!important}
    .header{box-shadow:none!important;border-radius:0;break-inside:avoid}
    .footer{border-top:1px solid #ccc}
    table{font-size:9pt;break-inside:avoid}
    thead th{background:#1a2a4a!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
    .kpi-card,.foda-card,.kv-item{break-inside:avoid}
    .kv-grid{grid-template-columns:repeat(2,1fr)}
    .foda-grid{grid-template-columns:1fr 1fr}
    .kpi-row{grid-template-columns:repeat(4,1fr)}
    h1{font-size:24pt!important}
    h2{font-size:16pt!important}
    a{text-decoration:none;color:#000}
    .status-step{break-inside:avoid}
    .progress-bar,.status-header{break-inside:avoid}
}"""

PASOS = {
    "1.1": "Brief de Negocio", "1.2": "Matriz de Productos", "1.3": "Perfil de Cliente Ideal",
    "1.4": "Identidad de Marca", "1.5": "Objetivos SMART", "1.6": "Matriz FODA",
    "2.1": "Análisis de Competidores", "2.2": "Calendario Comercial", "2.3": "Benchmark de Precios",
    "2.4": "Palabras Clave", "3.1": "Auditoría de Sitio Web", "3.2": "Auditoría de Redes Sociales",
    "3.3": "Tracking y Píxeles", "3.4": "Análisis SEO", "3.5": "Diagnóstico Email Marketing",
    "4.1": "Mejora del Sitio Web", "4.2": "Optimización de Perfiles", "4.3": "Setup Analítico",
    "5.1": "Propuesta Comercial", "5.2": "Canales y Presupuesto", "5.3": "KPIs y Proyecciones",
    "6.1": "Setup Meta Ads", "6.2": "Setup Google Ads", "6.3": "Creación de Creatividades",
    "6.4": "Configuración de Tracking", "6.5": "Email Flow Setup",
    "7.1": "Campaña Piloto", "7.2": "Pruebas A/B", "7.3": "Análisis y Optimización",
    "8.1": "Lanzamiento Oficial", "8.2": "Escalado", "8.3": "Reporte Semanal", "8.4": "Resumen Ejecutivo",
    "9.1": "Resumen Situacional",
}

FASES = {
    "1": "Diagnóstico Estratégico", "2": "Investigación de Mercado",
    "3": "Auditoría de Activos Digitales", "4": "Presencia Digital",
    "5": "Estrategia y Plan de Medios", "6": "Setup Técnico y Creatividades",
    "7": "Pilotaje y Testeo", "8": "Lanzamiento y Escalado",
    "9": "Resumen Situacional",
}

EMOJIS = {
    "1.1": "\U0001f4cb", "1.2": "\U0001f4e6", "1.3": "\U0001f3af", "1.4": "\U0001f3a8",
    "1.5": "\U0001f3af", "1.6": "\U0001f4ca",
    "2.1": "\U0001f50d", "2.2": "\U0001f4c5", "2.3": "\U0001f4b0", "2.4": "\U0001f511",
    "3.1": "\U0001f310", "3.2": "\U0001f4f1", "3.3": "\U0001f527", "3.4": "\U0001f4c8", "3.5": "\U0001f4e7",
    "4.1": "\U0001f6e0\ufe0f", "4.2": "\u2728", "4.3": "\U0001f4d0",
    "5.1": "\U0001f48e", "5.2": "\U0001f4e1", "5.3": "\U0001f4ca",
    "6.1": "\u2699\ufe0f", "6.2": "\u2699\ufe0f", "6.3": "\U0001f3a8", "6.4": "\U0001f527", "6.5": "\U0001f4e7",
    "7.1": "\U0001f9ea", "7.2": "\U0001f500", "7.3": "\u26a1",
    "8.1": "\U0001f680", "8.2": "\U0001f4c8", "8.3": "\U0001f4ca", "8.4": "\U0001f4d1",
    "9.1": "\U0001f4ca",
}

ORDERED = [
    "1.1","1.2","1.3","1.4","1.5","1.6",
    "2.1","2.2","2.3","2.4",
    "3.1","3.2","3.3","3.4","3.5",
    "4.1","4.2","4.3",
    "5.1","5.2","5.3",
    "6.1","6.2","6.3","6.4","6.5",
    "7.1","7.2","7.3",
    "8.1","8.2","8.3","8.4",
    "9.1",
]


def _get_flexible(d, primary, alternatives=None):
    if primary in d:
        val = d.get(primary)
        if val is not None and val != "":
            return str(val)
    if alternatives:
        for alt in alternatives:
            if alt in d:
                val = d.get(alt)
                if val is not None and val != "":
                    return str(val)
    return "\u2014"


def _extract_list(data):
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        lst = data.get("data", data.get("arquetipos", data.get("eventos", data.get("mejoras", data.get("acciones", data.get("problemas", data.get("quick_wins", [])))))))
        if isinstance(lst, list):
            return lst
        if isinstance(lst, dict):
            return [lst]
        return [data]
    return []


def _escape(s):
    if s is None:
        return ""
    s = str(s)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")


def _obtener_nav_html(paso_actual, cliente, archivos_conocidos=None):
    if paso_actual not in ORDERED:
        return ""
    idx = ORDERED.index(paso_actual)
    prev_paso = ORDERED[idx - 1] if idx > 0 else None
    next_paso = ORDERED[idx + 1] if idx < len(ORDERED) - 1 else None
    carpeta = sanitizar_nombre(cliente)
    dir_cliente = os.path.join(DOCS_DIR, carpeta)
    if archivos_conocidos is None:
        archivos_conocidos = _obtener_info_navegacion(dir_cliente)

    def _link_paso(pid):
        return archivos_conocidos.get(pid)

    html = '<!--NAV_BAR_START-->\n<div class="nav-bar">\n'
    html += '    <a href="_index.html" class="nav-index">\U0001f3e0 Volver al \u00edndice</a>\n'
    html += '    <div class="nav-center">\n'
    if prev_paso:
        prev_file = _link_paso(prev_paso)
        if prev_file:
            html += f'        <a href="{prev_file}" class="nav-prev">\u25c0 {PASOS.get(prev_paso, prev_paso)}</a>\n'
        else:
            html += f'        <span class="nav-prev nav-disabled">\u25c0 {PASOS.get(prev_paso, prev_paso)}</span>\n'
    else:
        html += '        <span class="nav-prev nav-disabled">\u25c0 Anterior</span>\n'
    if next_paso:
        next_file = _link_paso(next_paso)
        if next_file:
            html += f'        <a href="{next_file}" class="nav-next">{PASOS.get(next_paso, next_paso)} \u25b6</a>\n'
        else:
            html += f'        <span class="nav-next nav-disabled">{PASOS.get(next_paso, next_paso)} \u25b6</span>\n'
    else:
        html += '        <span class="nav-next nav-disabled">Siguiente \u25b6</span>\n'
    html += '    </div>\n</div>\n<!--NAV_BAR_END-->\n'
    return html


def _build_header_html(paso, titulo, cliente, analista="", emoji=""):
    fase_num = paso.split(".")[0]
    fase_nombre = FASES.get(fase_num, "")
    hoy = datetime.date.today().strftime("%d/%m/%Y")
    return f"""
    <div class="header">
        <div class="header-content">
            <div class="header-badge">{emoji} Fase {fase_num}: {fase_nombre}</div>
            <h1>{_escape(titulo)}</h1>
            <div class="subtitle">Documento generado para {_escape(cliente)}</div>
            <div class="header-meta">
                <div class="header-meta-item">\U0001f4c5 <strong>Fecha:</strong> {hoy}</div>
                <div class="header-meta-item">\U0001f4cb <strong>Paso:</strong> {paso}</div>
                <div class="header-meta-item">\U0001f464 <strong>Analista:</strong> {_escape(analista) or "\u2014"}</div>
                <div class="header-meta-item">\U0001f3e2 <strong>Cliente:</strong> {_escape(cliente)}</div>
            </div>
        </div>
    </div>"""


def _build_footer_html():
    return f"""
    <div class="footer">
        <strong>Global Infinity Marketing</strong> &mdash; by Design System - Claudio Silveira<br>
        Documento generado el {datetime.date.today().strftime("%d/%m/%Y")}
    </div>"""


def _wrap_html(content, titulo="Reporte", paso=None, cliente=None, archivos_conocidos=None):
    nav_html = _obtener_nav_html(paso, cliente, archivos_conocidos) if paso and cliente else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_escape(titulo)} — Global Infinity Marketing</title>
    <style>{CSS}</style>
</head>
<body>
    <div class="container">
        {nav_html}
        {content}
    </div>
</body>
</html>"""


def _obtener_info_navegacion(dir_cliente):
    info = {}
    if not os.path.isdir(dir_cliente):
        return info
    for fname in os.listdir(dir_cliente):
        if fname.endswith(".html") and not fname.startswith("_"):
            m = re.match(r"(\d)-(\d{2})-", fname)
            if m:
                paso_id = f"{m.group(1)}.{m.group(2)}"
                info[paso_id] = fname
            else:
                for pid in ORDERED:
                    if pid.replace(".", "-") in fname:
                        info[pid] = fname
                        break
    return info


def _build_kv_section(items_html, card_title="", card_emoji=""):
    return f"""<div class="card">
        <h2><span class="emoji">{card_emoji}</span> {card_title}</h2>
        <div class="kv-grid">{items_html}</div>
    </div>"""


def _kv_item(label, value):
    return f"""<div class="kv-item"><div class="label">{label}</div><div class="value">{_escape(value)}</div></div>"""


def _build_table_section(data, columns, card_title="", card_emoji=""):
    items = _extract_list(data)
    if not items:
        items = [{c.get("key", ""): "\u2014" for c in columns}]
    rows = ""
    for item in items:
        cells = ""
        for col in columns:
            key = col.get("key", "")
            val = item.get(key, "\u2014") if isinstance(item, dict) else "\u2014"
            val = _escape(val)
            if col.get("strong"):
                val = f"<strong>{val}</strong>"
            if col.get("badge"):
                val = f"""<span class="badge badge-{col['badge']}">{val}</span>"""
            if col.get("badge_map"):
                bm = col["badge_map"]
                bc = bm.get(val.lower(), col.get("default_badge", "badge-blue"))
                val = f"""<span class="badge {bc}">{val}</span>"""
            cells += f"<td>{val}</td>"
        rows += f"<tr>{cells}</tr>\n"
    headers = "".join(f"<th>{c['header']}</th>" for c in columns)
    return f"""<div class="card">
        <h2><span class="emoji">{card_emoji}</span> {card_title}</h2>
        <div class="table-container">
            <table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>
        </div>
    </div>"""


def _build_foda_section(d):
    f = d if isinstance(d, dict) else {}
    fortalezas = f.get("fortalezas", f.get("data", {}).get("fortalezas", []))
    debilidades = f.get("debilidades", f.get("data", {}).get("debilidades", []))
    oportunidades = f.get("oportunidades", f.get("data", {}).get("oportunidades", []))
    amenazas = f.get("amenazas", f.get("data", {}).get("amenazas", []))
    if not isinstance(fortalezas, list): fortalezas = [str(fortalezas)] if fortalezas else []
    if not isinstance(debilidades, list): debilidades = [str(debilidades)] if debilidades else []
    if not isinstance(oportunidades, list): oportunidades = [str(oportunidades)] if oportunidades else []
    if not isinstance(amenazas, list): amenazas = [str(amenazas)] if amenazas else []

    def _li(items):
        if not items: return "<li>\u2014</li>"
        return "".join(f"<li>\u2705 {_escape(i if isinstance(i, str) else i.get('descripcion', str(i)))}</li>" for i in items)

    content = f"""<div class="card">
        <h2><span class="emoji">\U0001f4ca</span> Matriz FODA</h2>
        <div class="foda-grid">
            <div class="foda-card foda-fortaleza"><h3>\U0001f4aa Fortalezas</h3><ul>{_li(fortalezas)}</ul></div>
            <div class="foda-card foda-debilidad"><h3>\u26a0\ufe0f Debilidades</h3><ul>{_li(debilidades)}</ul></div>
            <div class="foda-card foda-oportunidad"><h3>\U0001f680 Oportunidades</h3><ul>{_li(oportunidades)}</ul></div>
            <div class="foda-card foda-amenaza"><h3>\U0001f525 Amenazas</h3><ul>{_li(amenazas)}</ul></div>
        </div>
    </div>"""
    capacidad = _get_flexible(f, "capacidad_operativa")
    if capacidad and capacidad != "\u2014":
        content += f"""<div class="card"><h2><span class="emoji">\u26a1</span> Capacidad Operativa</h2><p>{_escape(capacidad)}</p></div>"""
    return content


def _build_kpi_row(items, card_title="", card_emoji=""):
    cards = ""
    for icono, valor, label in items:
        cards += f"""<div class="kpi-card"><div class="kpi-icon">{icono}</div><div class="kpi-value">{_escape(valor)}</div><div class="kpi-label">{label}</div></div>"""
    return f"""<div class="card"><h2><span class="emoji">{card_emoji}</span> {card_title}</h2><div class="kpi-row">{cards}</div></div>"""


def _build_timeline(items, card_title="", card_emoji=""):
    entries = ""
    for title, desc in items:
        entries += f"""<div class="timeline-item"><div class="tl-title">{_escape(title)}</div><div class="tl-desc">{_escape(desc)}</div></div>"""
    return f"""<div class="card"><h2><span class="emoji">{card_emoji}</span> {card_title}</h2><div class="timeline">{entries}</div></div>"""


def generar_index_html(cliente):
    carpeta = sanitizar_nombre(cliente)
    dir_cliente = os.path.join(DOCS_DIR, carpeta)
    if not os.path.isdir(dir_cliente):
        return None
    navegacion = _obtener_info_navegacion(dir_cliente)
    completados = set(navegacion.keys())
    total = len(ORDERED)
    comp_count = len(completados)
    pct = round(comp_count / total * 100) if total else 0
    hoy = datetime.date.today().strftime("%d/%m/%Y")

    fases_html = ""
    for num in ["1","2","3","4","5","6","7","8","9"]:
        nombre_fase = FASES.get(num, f"Fase {num}")
        pasos_fase = [p for p in ORDERED if p.startswith(f"{num}.")]
        if not pasos_fase:
            continue
        rows = ""
        for pid in pasos_fase:
            n = PASOS.get(pid, pid)
            e = EMOJIS.get(pid, "\U0001f4c4")
            if pid in completados:
                fname = navegacion[pid]
                rows += f"""<tr>
                    <td><span class="step-icon completed-icon">\u2705</span></td>
                    <td><strong>{e} <a href="{fname}" class="step-link">{n}</a></strong></td>
                    <td><span class="badge badge-green">Completado</span></td>
                </tr>\n"""
            else:
                rows += f"""<tr>
                    <td><span class="step-icon pending-icon">\u2b55</span></td>
                    <td><strong>{e} {n}</strong></td>
                    <td><span class="badge badge-blue">Pendiente</span></td>
                </tr>\n"""
        icon = chr(0x31 + int(num) - 1) + "\ufe0f\u20e3"
        fases_html += f"""
        <div class="card fase-card">
            <h2>{icon} {nombre_fase}</h2>
            <div class="table-container">
                <table>
                    <thead><tr><th style="width:40px">\u2714\ufe0f</th><th>Paso</th><th style="width:130px">Estado</th></tr></thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
        </div>"""

    pbar = f"""<div class="progress-bar"><div class="progress-fill" style="width:{pct}%"></div></div>
    <div class="progress-label">
        <span><strong>{comp_count}</strong> de <strong>{total}</strong> pasos completados</span>
        <span><strong>{pct}%</strong></span>
    </div>"""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>\u00cdndice de Reportes — {_escape(cliente)}</title>
    <style>{CSS}
        .index-title{{font-family:'Playfair Display',serif;font-size:36px;color:#1a2a4a;margin-bottom:5px}}
        .index-sub{{font-size:16px;color:#6b7280;margin-bottom:20px}}
        .progress-label{{display:flex;justify-content:space-between;font-size:14px;color:#6b7280;margin-bottom:6px}}
        .progress-label strong{{color:#1a2a4a}}
        .progress-bar{{height:10px;background:#e5e7eb;border-radius:10px;overflow:hidden;margin-bottom:4px}}
        .progress-fill{{height:100%;background:linear-gradient(90deg,#2d5f8a,#d4a030);border-radius:10px;transition:width .5s}}
        .step-icon{{font-size:18px}}
        .completed-icon{{color:#10b981}}
        .pending-icon{{color:#d1d5db}}
        .step-link{{color:#2d5f8a;text-decoration:none;font-weight:600}}
        .step-link:hover{{color:#1a2a4a;text-decoration:underline}}
        .fase-card{{border-left:4px solid #d4a030}}
        .fase-card h2{{font-size:18px;color:#1a2a4a}}
        .summary-strip{{display:flex;gap:15px;flex-wrap:wrap;margin-bottom:25px}}
        .summary-item{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:15px 20px;flex:1;min-width:120px;text-align:center}}
        .summary-item .num{{font-size:28px;font-weight:800;color:#1a2a4a}}
        .summary-item .lbl{{font-size:12px;color:#6b7280;text-transform:uppercase;letter-spacing:.5px}}
        @media print{{.summary-strip,.fase-card,.progress-bar,.status-header{{break-inside:avoid}}}}
    </style>
</head>
<body>
    <div class="container">
        <div class="status-header">
            <h1>\U0001f3e0 {_escape(cliente)}</h1>
            <p>\u00cdndice de Reportes — Onboarding de Marketing Digital</p>
            {pbar}
        </div>
        <div class="summary-strip">
            <div class="summary-item"><div class="num">{comp_count}</div><div class="lbl">Completados</div></div>
            <div class="summary-item"><div class="num">{total - comp_count}</div><div class="lbl">Pendientes</div></div>
            <div class="summary-item"><div class="num">{pct}%</div><div class="lbl">Progreso</div></div>
            <div class="summary-item"><div class="num">9</div><div class="lbl">Fases</div></div>
        </div>
        {fases_html}
        <div class="footer">
            <strong>Global Infinity Marketing</strong> &mdash; by Design System - Claudio Silveira<br>
            \u00cdndice generado el {hoy}
        </div>
    </div>
</body>
</html>"""
    ruta = os.path.join(dir_cliente, "_index.html")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    return ruta


def _actualizar_nav_de_vecinos(cliente, paso_actual):
    carpeta = sanitizar_nombre(cliente)
    dir_cliente = os.path.join(DOCS_DIR, carpeta)
    if not os.path.isdir(dir_cliente):
        return
    archivos = _obtener_info_navegacion(dir_cliente)
    if paso_actual in ORDERED:
        idx = ORDERED.index(paso_actual)
        vecinos = []
        if idx > 0:
            vecinos.append(ORDERED[idx - 1])
        if idx < len(ORDERED) - 1:
            vecinos.append(ORDERED[idx + 1])
        for vid in vecinos:
            if vid not in archivos:
                continue
            fname = archivos[vid]
            ruta_vecino = os.path.join(dir_cliente, fname)
            try:
                with open(ruta_vecino, "r", encoding="utf-8") as f:
                    contenido = f.read()
                nueva_nav = _obtener_nav_html(vid, cliente, archivos_conocidos=archivos)
                start_marker = "<!--NAV_BAR_START-->"
                end_marker = "<!--NAV_BAR_END-->"
                si = contenido.find(start_marker)
                ei = contenido.find(end_marker)
                if si != -1 and ei != -1:
                    ei += len(end_marker)
                    contenido = contenido[:si] + nueva_nav + contenido[ei:]
                    with open(ruta_vecino, "w", encoding="utf-8") as f:
                        f.write(contenido)
            except Exception as e:
                logger.warning("No se pudo actualizar navegación en %s: %s", ruta_vecino, e)


def _guardar_html(html, cliente, prefijo, paso=None):
    carpeta = sanitizar_nombre(cliente)
    dir_cliente = os.path.join(DOCS_DIR, carpeta)
    os.makedirs(dir_cliente, exist_ok=True)
    fecha = datetime.date.today().strftime("%Y%m%d")
    sanitizado = f"{prefijo}-{carpeta}-{fecha}"
    sanitizado = re.sub(r'[<>:"/\\|?*]', '_', sanitizado)
    nombre = f"{sanitizado}.html"
    ruta = os.path.join(dir_cliente, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    if paso:
        _actualizar_nav_de_vecinos(cliente, paso)
    generar_index_html(cliente)
    return ruta


CUSTOM_HANDLERS = {}

def _register_custom(paso_id):
    def decorator(func):
        CUSTOM_HANDLERS[paso_id] = func
        return func
    return decorator


# ═══════════════════════════════════════════════════════════════
#  CUSTOM HANDLERS — 33 funciones _custom_X_Y()
# ═══════════════════════════════════════════════════════════════

# ── FASE 1: DIAGNÓSTICO ESTRATÉGICO ──

@_register_custom("1.1")
def _custom_1_1(d):
    return f"""
    <div class="card">
        <div class="card-icon">\U0001f3e2</div>
        <h2><span class="emoji">\U0001f4d6</span> Historia de la Empresa</h2>
        <p>{_escape(_get_flexible(d, "historia"))}</p>
    </div>
    <div class="card">
        <h2><span class="emoji">\U0001f4e6</span> Productos y Servicios</h2>
        <div class="kv-grid">
            {_kv_item("Productos/Servicios", _get_flexible(d, "productos_servicios"))}
            {_kv_item("M\u00e1s Rentable", _get_flexible(d, "mas_rentable"))}
            {_kv_item("Modelo de Negocio", _get_flexible(d, "modelo_negocio"))}
        </div>
    </div>
    <div class="card">
        <h2><span class="emoji">\U0001f465</span> Clientes</h2>
        <div class="kv-grid">
            {_kv_item("Clientes Actuales", _get_flexible(d, "clientes_actuales"))}
            {_kv_item("Clientes Deseados", _get_flexible(d, "clientes_deseados", ["expansion_deseada"]))}
        </div>
    </div>
    <div class="card">
        <h2><span class="emoji">\U0001f4a1</span> Diferenciaci\u00f3n y Canales</h2>
        <div class="kv-grid">
            {_kv_item("Diferenciaci\u00f3n", _get_flexible(d, "diferenciacion", ["diferencial"]))}
            {_kv_item("Canales de Venta", _get_flexible(d, "canales_venta"))}
            {_kv_item("Atenci\u00f3n al Cliente", _get_flexible(d, "atencion_cliente", ["posventa"]))}
        </div>
    </div>
    {_build_timeline([
        ("3 meses", _get_flexible(d, "objetivo_3m", ["objetivos_3_meses"])),
        ("6 meses", _get_flexible(d, "objetivo_6m", ["objetivos_6_meses"])),
        ("12 meses", _get_flexible(d, "objetivo_12m", ["objetivos_12_meses"])),
    ], "Objetivos", "\U0001f3af")}
    <div class="card">
        <h2><span class="emoji">\U0001f4e2</span> Publicidad y Presupuesto</h2>
        <div class="kv-grid">
            {_kv_item("Experiencia en Publicidad Digital", _get_flexible(d, "pub_digital", ["publicidad_digital_previa"]))}
            {_kv_item("Presupuesto Mensual Estimado", _get_flexible(d, "presupuesto", ["presupuesto_mensual"]))}
        </div>
    </div>"""


@_register_custom("1.2")
def _custom_1_2(d):
    return _build_table_section(d, [
        {"header": "Producto", "key": "nombre", "strong": True},
        {"header": "Precio", "key": "precio"},
        {"header": "Costo", "key": "costo"},
        {"header": "Categor\u00eda", "key": "categoria", "badge": "blue"},
        {"header": "Diferencial", "key": "diferencial"},
        {"header": "Demanda", "key": "demanda", "badge": "green"},
    ], "Matriz de Productos", "\U0001f4e6")


@_register_custom("1.3")
def _custom_1_3(d):
    content = f"""
    <div class="card">
        <h2><span class="emoji">\U0001f464</span> Datos Demogr\u00e1ficos</h2>
        <div class="kv-grid">
            {_kv_item("Edad", _get_flexible(d, "edad"))}
            {_kv_item("Zona Geogr\u00e1fica", _get_flexible(d, "zona", ["zona_geografica"]))}
            {_kv_item("Nivel de Ingresos", _get_flexible(d, "ingresos", ["nivel_ingresos"]))}
            {_kv_item("Intereses", _get_flexible(d, "intereses"))}
            {_kv_item("Redes Sociales", _get_flexible(d, "redes", ["redes_sociales"]))}
            {_kv_item("Preferencia de Compra", _get_flexible(d, "preferencia_compra"))}
            {_kv_item("Objeciones Comunes", _get_flexible(d, "objeciones", ["objeciones_compra"]))}
        </div>
    </div>"""
    arquetipos = d.get("arquetipos", [])
    if isinstance(arquetipos, list):
        for a in arquetipos:
            content += f"""
    <div class="card">
        <h2><span class="emoji">\U0001f3ad</span> Arquetipo: {_escape(a.get('nombre', '\u2014'))}</h2>
        <div class="kv-grid">
            {_kv_item("Edad", a.get('edad', '\u2014'))}
            {_kv_item("Ocupaci\u00f3n", a.get('ocupacion', '\u2014'))}
            {_kv_item("Motivaci\u00f3n", a.get('motivacion', '\u2014'))}
            {_kv_item("Dolores", a.get('dolores', '\u2014'))}
        </div>
    </div>"""
    return content


@_register_custom("1.4")
def _custom_1_4(d):
    return f"""
    <div class="card">
        <h2><span class="emoji">\U0001f3af</span> Misi\u00f3n, Visi\u00f3n y Valores</h2>
        <div class="kv-grid">
            {_kv_item("Misi\u00f3n", _get_flexible(d, "mision"))}
            {_kv_item("Visi\u00f3n", _get_flexible(d, "vision"))}
            {_kv_item("Valores", _get_flexible(d, "valores"))}
        </div>
    </div>
    <div class="card">
        <h2><span class="emoji">\U0001f4ac</span> Personalidad de Marca</h2>
        <div class="kv-grid">
            {_kv_item("Tono de Comunicaci\u00f3n", _get_flexible(d, "tono_comunicacion"))}
            {_kv_item("Percepci\u00f3n Deseada", _get_flexible(d, "percepcion_deseada"))}
            {_kv_item("Manual de Marca", _get_flexible(d, "manual_marca"))}
        </div>
    </div>"""


@_register_custom("1.5")
def _custom_1_5(d):
    objetivos = _extract_list(d)
    if not objetivos:
        objetivos = [{"objetivo": "\u2014"}]
    content = ""
    for i, o in enumerate(objetivos, 1):
        content += f"""
    <div class="card">
        <h2><span class="emoji">\U0001f3af</span> Objetivo {i}: {_escape(o.get('objetivo', '\u2014'))}</h2>
        <div class="kv-grid">
            {_kv_item("S - Espec\u00edfico", o.get('specific', o.get('especifico', '\u2014')))}
            {_kv_item("M - Medible", o.get('measurable', o.get('medible', '\u2014')))}
            {_kv_item("A - Alcanzable", o.get('achievable', o.get('alcanzable', '\u2014')))}
            {_kv_item("R - Relevante", o.get('relevant', o.get('relevante', '\u2014')))}
            {_kv_item("T - Con Plazo", o.get('timebound', o.get('plazo', '\u2014')))}
            {_kv_item("KPI Principal", o.get('kpi', '\u2014'))}
            {_kv_item("ROAS Esperado", o.get('roas_esperado', '\u2014'))}
            {_kv_item("CPA M\u00e1ximo", o.get('cpa_maximo', '\u2014'))}
        </div>
    </div>"""
    return content


@_register_custom("1.6")
def _custom_1_6(d):
    return _build_foda_section(d)


# ── FASE 2: INVESTIGACIÓN DE MERCADO ──

@_register_custom("2.1")
def _custom_2_1(d):
    return _build_table_section(d, [
        {"header": "Competidor", "key": "nombre", "strong": True},
        {"header": "Fortalezas", "key": "fortalezas"},
        {"header": "Debilidades", "key": "debilidades"},
        {"header": "Precios", "key": "precios", "badge": "blue"},
        {"header": "Estrategia", "key": "estrategia"},
    ], "Matriz Competitiva", "\U0001f50d")


@_register_custom("2.2")
def _custom_2_2(d):
    eventos = d.get("eventos", d.get("data", []))
    if isinstance(eventos, list) and eventos:
        rows = ""
        for e in eventos:
            rows += f"""<tr>
                <td>{_escape(e.get('fecha', '\u2014'))}</td>
                <td><strong>{_escape(e.get('evento', '\u2014'))}</strong></td>
                <td>{_escape(e.get('oportunidad', '\u2014'))}</td>
                <td><span class="badge badge-gold">{_escape(e.get('prioridad', 'Media'))}</span></td>
            </tr>"""
        return f"""
        <div class="card">
            <h2><span class="emoji">\U0001f4c5</span> Calendario de Oportunidades</h2>
            <div class="table-container">
                <table>
                    <thead><tr><th>Fecha</th><th>Evento</th><th>Oportunidad</th><th>Prioridad</th></tr></thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
        </div>"""
    return _build_timeline([
        ("Enero", "Temporada tur\u00edstica"),
        ("Febrero-Marzo", "Vuelta a clases, Semana de Turismo"),
        ("Mayo", "D\u00eda de la Madre"),
        ("Junio", "D\u00eda del Padre"),
        ("Julio-Agosto", "Hot Sale, D\u00eda del Ni\u00f1o"),
        ("Noviembre", "Cyber Monday"),
        ("Diciembre", "Navidad y Reyes"),
    ], "Eventos Clave Uruguay", "\U0001f4c5")


@_register_custom("2.3")
def _custom_2_3(d):
    return _build_table_section(d, [
        {"header": "Producto", "key": "producto", "strong": True},
        {"header": "Precio Cliente", "key": "precio_cliente"},
        {"header": "Precio Competencia", "key": "precio_competencia"},
        {"header": "Diferencia", "key": "diferencia"},
        {"header": "Promociones", "key": "promociones", "badge": "purple"},
    ], "Benchmark de Precios", "\U0001f4b0")


@_register_custom("2.4")
def _custom_2_4(d):
    return _build_table_section(d, [
        {"header": "Keyword", "key": "keyword", "strong": True},
        {"header": "Volumen", "key": "volumen"},
        {"header": "Intenci\u00f3n", "key": "intencion",
         "badge_map": {"comercial": "badge-gold", "transaccional": "badge-green", "informativa": "badge-blue"},
         "default_badge": "badge-blue"},
        {"header": "Competencia", "key": "competencia"},
    ], "Palabras Clave", "\U0001f511")


# ── FASE 3: AUDITORÍA DE ACTIVOS DIGITALES ──

@_register_custom("3.1")
def _custom_3_1(d):
    content = _build_kpi_row([
        ("\U0001f310", _get_flexible(d, "url"), "URL del Sitio"),
        ("\U0001f4c8", _get_flexible(d, "velocidad"), "Velocidad de Carga"),
        ("\U0001f4f1", _get_flexible(d, "mobile"), "Experiencia Mobile"),
        ("\U0001f512", _get_flexible(d, "ssl"), "SSL / HTTPS"),
    ], "KPIs del Sitio", "\U0001f4ca")
    problemas = d.get("problemas", [])
    if isinstance(problemas, list) and problemas:
        items = "".join(f"<li>\U0001f534 {_escape(p if isinstance(p, str) else p.get('descripcion', str(p)))}</li>" for p in problemas)
        content += f"""<div class="card"><h2><span class="emoji">\u26a0\ufe0f</span> Problemas Detectados</h2><ul>{items}</ul></div>"""
    return content


@_register_custom("3.2")
def _custom_3_2(d):
    redes = _extract_list(d)
    content = ""
    for r in redes:
        content += f"""
    <div class="card">
        <h2><span class="emoji">\U0001f4f1</span> {_escape(r.get('red', r.get('nombre', 'Red Social')))}</h2>
        <div class="kv-grid">
            {_kv_item("Perfil", r.get('perfil', r.get('url', '\u2014')))}
            {_kv_item("Seguidores", r.get('seguidores', '\u2014'))}
            {_kv_item("Engagement", r.get('engagement', '\u2014'))}
            {_kv_item("Frecuencia", r.get('frecuencia', '\u2014'))}
            {_kv_item("Tono", r.get('tono', '\u2014'))}
            {_kv_item("Recomendaci\u00f3n", r.get('recomendacion', '\u2014'))}
        </div>
    </div>"""
    return content or f"""<div class="card"><h2><span class="emoji">\U0001f4f1</span> Redes Sociales</h2><p>No se encontraron datos de redes sociales.</p></div>"""


@_register_custom("3.3")
def _custom_3_3(d):
    return _build_kv_section("".join([
        _kv_item("\U0001f4d8 Meta Pixel", _get_flexible(d, "meta_pixel")),
        _kv_item("\U0001f4ca Google Analytics 4", _get_flexible(d, "ga4")),
        _kv_item("\U0001f3af Google Ads Tag", _get_flexible(d, "google_ads")),
        _kv_item("\U0001f50d Google Search Console", _get_flexible(d, "gsc")),
        _kv_item("\U0001f4e7 Klaviyo", _get_flexible(d, "klaviyo")),
        _kv_item("\u26a1 Eventos Configurados", _get_flexible(d, "events", ["eventos"])),
    ]), "Estado del Tracking", "\U0001f527")


@_register_custom("3.4")
def _custom_3_4(d):
    content = _build_kpi_row([
        ("\U0001f441\ufe0f", _get_flexible(d, "impresiones"), "Impresiones"),
        ("\U0001f5b1\ufe0f", _get_flexible(d, "clicks", ["clics"]), "Clicks"),
        ("\U0001f4ca", _get_flexible(d, "ctr"), "CTR"),
        ("\U0001f4cd", _get_flexible(d, "posicion", ["posicion_media"]), "Posici\u00f3n Media"),
    ], "Rendimiento Org\u00e1nico", "\U0001f4c8")
    qw = d.get("quick_wins", [])
    if isinstance(qw, list) and qw:
        items = "".join(f"<li>\u26a1 {_escape(q if isinstance(q, str) else q.get('descripcion', str(q)))}</li>" for q in qw)
        content += f"""<div class="card"><h2><span class="emoji">\u26a1</span> Quick Wins</h2><ul>{items}</ul></div>"""
    return content


@_register_custom("3.5")
def _custom_3_5(d):
    return _build_kv_section("".join([
        _kv_item("Herramienta", _get_flexible(d, "herramienta")),
        _kv_item("Contactos", _get_flexible(d, "contactos")),
        _kv_item("Tasa de Apertura", _get_flexible(d, "tasa_apertura")),
        _kv_item("CTR", _get_flexible(d, "ctr")),
        _kv_item("Flujos Activos", _get_flexible(d, "flujos")),
        _kv_item("Segmentaci\u00f3n", _get_flexible(d, "segmentacion")),
    ]), "Estado del Email Marketing", "\U0001f4e7")


# ── FASE 4: PRESENCIA DIGITAL ──

@_register_custom("4.1")
def _custom_4_1(d):
    content = ""
    mejoras = d.get("mejoras", [])
    if isinstance(mejoras, list) and mejoras:
        items = "".join(f"<li>\u2705 {_escape(m if isinstance(m, str) else m.get('descripcion', str(m)))}</li>" for m in mejoras)
        content += f"""<div class="card"><h2><span class="emoji">\U0001f6e0\ufe0f</span> Mejoras Implementadas</h2><ul>{items}</ul></div>"""
    content += f"""<div class="card"><h2><span class="emoji">\U0001f4dd</span> Observaciones</h2><p>{_escape(_get_flexible(d, "observaciones"))}</p></div>"""
    return content


@_register_custom("4.2")
def _custom_4_2(d):
    return _build_kv_section("".join([
        _kv_item("Bio Actualizada", _get_flexible(d, "bio")),
        _kv_item("Im\u00e1genes", _get_flexible(d, "imagenes")),
        _kv_item("Descripciones", _get_flexible(d, "descripciones")),
        _kv_item("Links", _get_flexible(d, "links")),
    ]), "Acciones Realizadas", "\u2728")


@_register_custom("4.3")
def _custom_4_3(d):
    return _build_kv_section("".join([
        _kv_item("\U0001f4ca Google Analytics 4", _get_flexible(d, "ga4")),
        _kv_item("\U0001f50d Google Search Console", _get_flexible(d, "gsc")),
        _kv_item("\U0001f4d8 Meta Pixel", _get_flexible(d, "meta_pixel")),
        _kv_item("\U0001f3af Google Ads", _get_flexible(d, "google_ads")),
        _kv_item("\U0001f4e7 Klaviyo", _get_flexible(d, "klaviyo")),
    ]), "Stack Anal\u00edtico", "\U0001f4d0")


# ── FASE 5: ESTRATEGIA Y PLAN DE MEDIOS ──

@_register_custom("5.1")
def _custom_5_1(d):
    return _build_kv_section("".join([
        _kv_item("Mensaje Principal", _get_flexible(d, "mensaje_principal", ["mensaje"])),
        _kv_item("Diferenciador Clave", _get_flexible(d, "diferenciador")),
        _kv_item("P\u00fablico Objetivo", _get_flexible(d, "publico", ["publico_objetivo"])),
        _kv_item("Promesa de Marca", _get_flexible(d, "promesa")),
    ]), "Propuesta de Valor \u00danica (UVP)", "\U0001f48e")


@_register_custom("5.2")
def _custom_5_2(d):
    return _build_kv_section("".join([
        _kv_item("Presupuesto Total", _get_flexible(d, "presupuesto_total", ["presupuesto"])),
        _kv_item("Meta Ads", _get_flexible(d, "meta_ads")),
        _kv_item("Google Ads", _get_flexible(d, "google_ads")),
        _kv_item("Otros Canales", _get_flexible(d, "otros")),
    ]), "Plan de Medios", "\U0001f4e1")


@_register_custom("5.3")
def _custom_5_3(d):
    return _build_table_section(d, [
        {"header": "KPI", "key": "kpi", "strong": True},
        {"header": "Valor Actual", "key": "actual"},
        {"header": "Meta", "key": "meta"},
        {"header": "Per\u00edodo", "key": "periodo", "badge": "blue"},
    ], "KPIs y Proyecciones", "\U0001f4ca")


# ── FASE 6: SETUP TÉCNICO Y CREATIVIDADES ──

@_register_custom("6.1")
def _custom_6_1(d):
    return _build_kv_section("".join([
        _kv_item("Cuenta Publicitaria", _get_flexible(d, "cuenta")),
        _kv_item("Pixel", _get_flexible(d, "pixel")),
        _kv_item("Cat\u00e1logo", _get_flexible(d, "catalogo")),
        _kv_item("Eventos", _get_flexible(d, "eventos")),
    ]), "Configuraci\u00f3n Meta Ads", "\u2699\ufe0f")


@_register_custom("6.2")
def _custom_6_2(d):
    return _build_kv_section("".join([
        _kv_item("Cuenta", _get_flexible(d, "cuenta")),
        _kv_item("Conversion Tracking", _get_flexible(d, "conversion_tracking")),
        _kv_item("Remarketing", _get_flexible(d, "remarketing")),
    ]), "Configuraci\u00f3n Google Ads", "\u2699\ufe0f")


@_register_custom("6.3")
def _custom_6_3(d):
    return _build_table_section(d, [
        {"header": "Tipo", "key": "tipo"},
        {"header": "Nombre", "key": "nombre", "strong": True},
        {"header": "Descripci\u00f3n", "key": "descripcion"},
        {"header": "Formato", "key": "formato", "badge": "purple"},
    ], "Creatividades Generadas", "\U0001f3a8")


@_register_custom("6.4")
def _custom_6_4(d):
    return _build_kv_section("".join([
        _kv_item("Meta CAPI", _get_flexible(d, "meta_capi")),
        _kv_item("GA4 Events", _get_flexible(d, "ga4_events", ["eventos_ga4"])),
        _kv_item("Google Ads Tag", _get_flexible(d, "google_ads_tag")),
        _kv_item("Klaviyo Webhook", _get_flexible(d, "klaviyo_webhook")),
    ]), "Tracking Configurado", "\U0001f527")


@_register_custom("6.5")
def _custom_6_5(d):
    return _build_kv_section("".join([
        _kv_item("Welcome Flow", _get_flexible(d, "welcome_flow")),
        _kv_item("Abandoned Cart", _get_flexible(d, "abandoned_cart")),
        _kv_item("Post Purchase", _get_flexible(d, "post_purchase")),
        _kv_item("Segmentos", _get_flexible(d, "segmentos")),
    ]), "Flujos de Email Configurados", "\U0001f4e7")


# ── FASE 7: PILOTAJE Y TESTEO ──

@_register_custom("7.1")
def _custom_7_1(d):
    return _build_kv_section("".join([
        _kv_item("Campa\u00f1a", _get_flexible(d, "campania", ["nombre"])) if _get_flexible(d, "campania", ["nombre"]) != "\u2014" else "",
        _kv_item("Inversi\u00f3n", _get_flexible(d, "inversion")),
        _kv_item("Impresiones", _get_flexible(d, "impresiones")),
        _kv_item("Clics", _get_flexible(d, "clics", ["clicks"])),
        _kv_item("CTR", _get_flexible(d, "ctr")),
        _kv_item("Conversiones", _get_flexible(d, "conversiones")),
        _kv_item("CPA", _get_flexible(d, "cpa")),
        _kv_item("ROAS", _get_flexible(d, "roas")),
    ]), "Resultados de Campa\u00f1a Piloto", "\U0001f9ea")


@_register_custom("7.2")
def _custom_7_2(d):
    return _build_table_section(d, [
        {"header": "Variable", "key": "variable", "strong": True},
        {"header": "Versi\u00f3n A", "key": "version_a"},
        {"header": "Versi\u00f3n B", "key": "version_b"},
        {"header": "Resultado", "key": "resultado", "badge": "green"},
        {"header": "Ganador", "key": "ganador"},
    ], "Pruebas A/B Realizadas", "\U0001f500")


@_register_custom("7.3")
def _custom_7_3(d):
    content = ""
    acciones = d.get("acciones", [])
    if isinstance(acciones, list) and acciones:
        items = "".join(f"<li>\u26a1 {_escape(a if isinstance(a, str) else a.get('descripcion', str(a)))}</li>" for a in acciones)
        content += f"""<div class="card"><h2><span class="emoji">\u26a1</span> Acciones de Optimizaci\u00f3n</h2><ul>{items}</ul></div>"""
    content += f"""<div class="card"><h2><span class="emoji">\U0001f4ca</span> Resultados Post-Optimizaci\u00f3n</h2><p>{_escape(_get_flexible(d, "resultados"))}</p></div>"""
    return content


# ── FASE 8: LANZAMIENTO Y ESCALADO ──

@_register_custom("8.1")
def _custom_8_1(d):
    return _build_kv_section("".join([
        _kv_item("Fecha de Lanzamiento", _get_flexible(d, "fecha")),
        _kv_item("Canales Activados", _get_flexible(d, "canales")),
        _kv_item("Presupuesto Inicial", _get_flexible(d, "presupuesto")),
        _kv_item("Responsable", _get_flexible(d, "responsable")),
    ]), "Checklist de Lanzamiento", "\U0001f680")


@_register_custom("8.2")
def _custom_8_2(d):
    return _build_kv_section("".join([
        _kv_item("Estrategia", _get_flexible(d, "estrategia")),
        _kv_item("Incremento Semanal", _get_flexible(d, "incremento")),
        _kv_item("Meta de Gasto", _get_flexible(d, "meta_gasto")),
        _kv_item("Meta de ROAS", _get_flexible(d, "meta_roas")),
    ]), "Plan de Escalado", "\U0001f4c8")


@_register_custom("8.3")
def _custom_8_3(d):
    return _build_kpi_row([
        ("\U0001f4b0", _get_flexible(d, "inversion"), "Inversi\u00f3n Total"),
        ("\U0001f4c8", _get_flexible(d, "impresiones"), "Impresiones"),
        ("\U0001f5b1\ufe0f", _get_flexible(d, "clics", ["clicks"]), "Clics"),
        ("\U0001f4ca", _get_flexible(d, "ctr"), "CTR"),
        ("\U0001f514", _get_flexible(d, "conversiones"), "Conversiones"),
        ("\U0001f4b5", _get_flexible(d, "cpa"), "CPA"),
        ("\U0001f4c9", _get_flexible(d, "roas"), "ROAS"),
        ("\U0001f4b6", _get_flexible(d, "ingresos"), "Ingresos"),
    ], "KPIs Semanales", "\U0001f4ca")


@_register_custom("8.4")
def _custom_8_4(d):
    content = f"""
    <div class="card">
        <h2><span class="emoji">\U0001f4d1</span> Resumen del Proyecto</h2>
        <div class="kv-grid">
            {_kv_item("Resumen", _get_flexible(d, "resumen"))}
            {_kv_item("Logros", _get_flexible(d, "logros"))}
            {_kv_item("Pr\u00f3ximos Pasos", _get_flexible(d, "proximos_pasos"))}
            {_kv_item("Recomendaciones", _get_flexible(d, "recomendaciones"))}
        </div>
    </div>"""
    content += _build_kpi_row([
        ("\U0001f4b0", _get_flexible(d, "inversion_total"), "Inversi\u00f3n Total"),
        ("\U0001f4c9", _get_flexible(d, "roas_general"), "ROAS General"),
        ("\U0001f4b5", _get_flexible(d, "cpa_promedio"), "CPA Promedio"),
        ("\U0001f514", _get_flexible(d, "conversiones_totales"), "Conversiones"),
    ], "KPIs Generales", "\U0001f4ca")
    return content


def _sg(label, sub, keys):
    if not isinstance(sub, dict): return ""
    items = "".join(_kv_item(k.replace("_"," ").title(), sub.get(k, "\u2014")) for k in keys if k in sub)
    return f'<div class="card"><h2>{label}</h2><div class="kv-grid">{items}</div></div>' if items else ""


def _sd(html_id, label, emoji="📊"):
    """Section divider for macro-blocks"""
    return f"""<hr class="section-divider" id="{html_id}" data-label="{label}">
<div style="text-align:center;margin:-10px 0 25px 0">
    <span style="background:#d4a030;color:#fff;padding:6px 20px;border-radius:20px;font-size:13px;font-weight:600;letter-spacing:.5px">
        {emoji} {label}
    </span>
</div>"""


@_register_custom("9.1")
def _custom_9_1(d):
    content = ""

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  BLOQUE 1: ¿QUIÉN ES? — Identidad y origen                 ║
    # ╚══════════════════════════════════════════════════════════════╝

    # ── 1: KPI DASHBOARD ──
    kpi = d.get("kpi_dashboard", {})
    if isinstance(kpi, dict):
        content += _build_kpi_row([
            ("📅", kpi.get("anos_mercado","—"), "Años en el mercado"),
            ("📱", kpi.get("seguidores_ig","—"), "Seguidores Instagram"),
            ("💰", kpi.get("presupuesto_mensual","—"), "Presupuesto/mes"),
            ("📈", kpi.get("margen_promedio","—"), "Margen promedio"),
            ("📦", kpi.get("productos_estrella","—"), "Producto estrella"),
            ("📊", kpi.get("meta_ventas","—"), "Meta ventas 3 meses"),
            ("🏪", kpi.get("canales_activos","—"), "Canales activos"),
            ("👩", kpi.get("clientas_cartera","—"), "Clientas en cartera"),
        ], "Dashboard de Indicadores Clave", "📊")

    content += _sd("quien-es", "BLOQUE 1: ¿QUIÉN ES? — Identidad y origen", "🏢")

    # ── 2: FICHA DE LA EMPRESA ──
    dg = d.get("datos_generales", {})
    if isinstance(dg, dict):
        content += _sg("🏢 Ficha de la Empresa", dg,
            ["nombre","rubro","anos_mercado","ubicacion","fundadora","modelo_negocio","canales_venta","diferencial_principal","atencion_cliente","empleados","presencia_geografica"])

    # ── 3: HISTORIA Y TRAYECTORIA ──
    hist = d.get("historia", {})
    if isinstance(hist, dict):
        content += _sg("📈 Historia y Trayectoria", hist,
            ["inicio","hitos_clave","crecimiento","situacion_actual","curva_crecimiento"])

    # ── 4: IDENTIDAD DE MARCA ──
    idm = d.get("identidad_marca", {})
    if isinstance(idm, dict):
        content += _sg("🎨 Identidad de Marca", idm,
            ["mision","vision","valores","tono_comunicacion","personalidad_marca","eslogan_no_formal"])

    # ── 5: PROPUESTA DE VALOR ──
    pv = d.get("propuesta_valor", {})
    if isinstance(pv, dict):
        content += _sg("💎 Propuesta de Valor y Posicionamiento", pv,
            ["uvp","mensaje_principal","promesa_marca","diferenciadores_clave","tono_comunicacion","personalidad_marca"])

    # ── 6: ANÁLISIS DE PRODUCTOS (con BCG) ──
    prods = d.get("analisis_productos", [])
    if isinstance(prods, list) and prods:
        content += _build_table_section(
            {"data": prods},
            [
                {"header": "Producto", "key": "producto", "strong": True},
                {"header": "Precio venta", "key": "precio_venta"},
                {"header": "Precio costo", "key": "precio_costo"},
                {"header": "Margen", "key": "margen", "badge": "green"},
                {"header": "Volumen", "key": "volumen_venta", "badge": "blue"},
                {"header": "Tipo BCG", "key": "tipo_bcg", "badge": "gold"},
            ],
            "📦 Análisis de Productos — Cartera y Márgenes",
            "📦"
        )

    # ── 7: MATRIZ BCG ──
    bcg = d.get("matriz_bcg", {})
    if isinstance(bcg, dict):
        content += _sg("📊 Matriz BCG — Ciclo de Vida del Producto", bcg,
            ["estrellas","vacas_lecheras","interrogantes","perros"])

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  BLOQUE 2: ¿DE DÓNDE VIENE? — Trayectoria y audiencia       ║
    # ╚══════════════════════════════════════════════════════════════╝
    content += _sd("de-donde-viene", "BLOQUE 2: ¿DE DÓNDE VIENE? — Audiencia y Contenido", "👥")

    # ── 8: CLIENTE IDEAL (ICP) ──
    ci = d.get("cliente_ideal", {})
    if isinstance(ci, dict):
        content += _sg("🎯 Cliente Ideal (ICP)", ci,
            ["descripcion_general","edad","ubicacion_geografica","nivel_ingresos","intereses","motivacion_compra","canales_preferidos","objeciones_comunes"])

    # ── 9: ARQUETIPOS DETALLADOS ──
    arquetipos = d.get("arquetipos", [])
    if isinstance(arquetipos, list) and arquetipos:
        archtml = ""
        for a in arquetipos:
            archtml += f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:20px">
                <h3 style="color:#1a2a4a;font-size:16px;margin-bottom:10px">👤 {a.get('nombre','')}</h3>
                <div class="kv-grid" style="grid-template-columns:1fr 1fr">
                    {_kv_item("Edad", a.get('edad','—'))}
                    {_kv_item("Ubicación", a.get('ubicacion','—'))}
                    {_kv_item("Ingresos", a.get('ingresos','—'))}
                    {_kv_item("Intereses", a.get('intereses','—'))}
                    {_kv_item("Dolor/Necesidad", a.get('dolor','—'))}
                    {_kv_item("Trigger de compra", a.get('trigger_compra','—'))}
                    {_kv_item("Objeción", a.get('objecion','—'))}
                    {_kv_item("Cómo llegar", a.get('como_llegar','—'))}
                </div>
            </div>"""
        content += f"""<div class="card"><h2>👤 Arquetipos de Cliente — Perfiles Detallados</h2>
        <p style="font-size:13px;color:#6b7280;margin-bottom:15px">Segmentación cualitativa de la audiencia con dolores, triggers y estrategia de aproximación.</p>
        <div style="display:grid;gap:16px">{archtml}</div></div>"""

    # ── 10: CUSTOMER JOURNEY MAP ──
    cj = d.get("customer_journey", {})
    if isinstance(cj, dict):
        # Journey as timeline with stages
        stages = [
            ("Descubrimiento", cj.get('descubrimiento','—'), "🔍"),
            ("Interés", cj.get('interes','—'), "💡"),
            ("Consideración", cj.get('consideracion','—'), "🤔"),
            ("Decisión", cj.get('decision','—'), "✅"),
            ("Compra", cj.get('compra','—'), "🛒"),
            ("Post-venta", cj.get('postventa','—'), "📞"),
            ("Fidelización", cj.get('fidelizacion','—'), "❤️"),
        ]
        journey_html = ""
        for i, (stage, desc, emoji) in enumerate(stages):
            arrow = "→" if i < len(stages)-1 else ""
            journey_html += f"""
            <div style="text-align:center;min-width:120px;flex:1;padding:10px">
                <div style="font-size:28px;margin-bottom:5px">{emoji}</div>
                <div style="font-weight:700;font-size:13px;color:#1a2a4a;margin-bottom:4px">{stage}</div>
                <div style="font-size:11px;color:#6b7280;line-height:1.4">{desc[:80]}{'...' if len(desc)>80 else ''}</div>
                <div style="font-size:20px;color:#d4a030;margin-top:5px">{arrow}</div>
            </div>"""
        content += f"""<div class="card"><h2>🔍 Customer Journey Map — Viaje de la Cliente</h2>
        <p style="font-size:13px;color:#6b7280;margin-bottom:12px">Las 7 etapas por las que pasa una clienta desde que descubre MG Joyas hasta que se fideliza.</p>
        <div style="display:flex;flex-wrap:wrap;gap:4px;justify-content:center">{journey_html}</div>"""
        brecha = cj.get("brecha_detectada","")
        if brecha:
            content += f'<div style="margin-top:12px;padding:10px 14px;background:#fef2f2;border:1px solid #fecaca;border-radius:8px;font-size:13px;color:#dc2626"><strong>🔴 Brecha detectada:</strong> {brecha}</div>'
        content += "</div>"

    # ── 11: EMBUDO DE VENTAS ──
    embudo = d.get("embudo_ventas", {})
    if isinstance(embudo, dict):
        funnel_stages = [
            ("TOFU — Alcance", embudo.get('tofu_alcance','—'), embudo.get('tofu_accion','—'), "#dbeafe", "#1d4ed8"),
            ("MOFU — Interés", embudo.get('mofu_interes','—'), embudo.get('mofu_nutricion','—'), "#c7d2fe", "#4338ca"),
            ("BOFU — Decisión", embudo.get('bofu_decision','—'), embudo.get('bofu_conversion','—'), "#a5f3fc", "#0891b2"),
        ]
        funnel_html = ""
        for stage, alcance, accion, bg, color in funnel_stages:
            funnel_html += f"""
            <div style="background:{bg};border-radius:12px;padding:16px;margin-bottom:10px;border-left:4px solid {color}">
                <h3 style="font-size:15px;font-weight:700;color:{color};margin-bottom:6px">{stage}</h3>
                <div style="font-size:13px;color:#374151;line-height:1.5"><strong>Qué es:</strong> {alcance}</div>
                <div style="font-size:13px;color:#374151;line-height:1.5;margin-top:4px"><strong>Acción esperada:</strong> {accion}</div>
            </div>"""
        content += f"""<div class="card"><h2>🔄 Embudo de Ventas — TOFU → MOFU → BOFU</h2>
        <p style="font-size:13px;color:#6b7280;margin-bottom:12px">Estrategia por etapa del funnel: cómo atraer, nutrir y convertir clientas.</p>
        {funnel_html}"""
        rmkt = embudo.get('remarketing','')
        if rmkt:
            content += f'<div style="margin-top:10px;padding:10px 14px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-size:13px;color:#92400e"><strong>🔄 Remarketing:</strong> {rmkt}</div>'
        content += "</div>"

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  BLOQUE 3: ¿DÓNDE ESTÁ? — Posicionamiento y mercado         ║
    # ╚══════════════════════════════════════════════════════════════╝
    content += _sd("donde-esta", "BLOQUE 3: ¿DÓNDE ESTÁ? — Posicionamiento y Mercado", "🌍")

    # ── 12: MATRIZ FODA ──
    foda = d.get("foda", {})
    if isinstance(foda, dict) and any(isinstance(v,list) and v for v in foda.values()):
        content += """
        <div class="card">
            <h2>📊 Matriz FODA — Análisis de Situación Actual</h2>
            <p style="font-size:13px;color:#6b7280;margin-bottom:12px">Diagnóstico estratégico que resume fortalezas, debilidades, oportunidades y amenazas identificadas durante el onboarding.</p>
            <div class="foda-grid">"""
        for label, style, key in [
            ("✅ Fortalezas — Activos con los que cuenta", "foda-fortaleza", "fortalezas"),
            ("❌ Debilidades — Áreas a mejorar", "foda-debilidad", "debilidades"),
            ("💡 Oportunidades — Factores externos favorables", "foda-oportunidad", "oportunidades"),
            ("⚠️ Amenazas — Riesgos externos", "foda-amenaza", "amenazas"),
        ]:
            items = foda.get(key, [])
            if isinstance(items, list) and items:
                lis = "".join(f"<li>• {i}</li>" for i in items)
                content += f'<div class="foda-card {style}"><h3>{label}</h3><ul>{lis}</ul></div>'
        content += "</div></div>"

    # ── 13: ANÁLISIS DE COMPETENCIA ──
    comp = d.get("competencia_analisis", {})
    if isinstance(comp, dict):
        content += _sg("🔍 Análisis de Competencia", comp,
            ["competidores_directos","quienes_son","rango_precios_competencia","posicion_mg_joyas","ventajas_frente_a_competencia","desventajas_frente_a_competencia","oportunidades_competitivas"])

    # ── 14: MATRIZ COMPETITIVA ──
    mc = d.get("matriz_competitiva", [])
    if isinstance(mc, list) and mc:
        content += _build_table_section(
            {"data": mc},
            [
                {"header": "Competidor", "key": "competidor", "strong": True},
                {"header": "Seguidores IG", "key": "seguidores_ig"},
                {"header": "Web", "key": "tiene_web"},
                {"header": "Tienda física", "key": "tiene_tienda"},
                {"header": "Precio", "key": "precio_relativo", "badge_map": {"bajo": "badge-green", "medio": "badge-gold", "alto": "badge-red"}, "default_badge": "badge-blue"},
                {"header": "Publicidad", "key": "publicidad"},
                {"header": "Fortaleza principal", "key": "fortaleza_principal"},
            ],
            "🏆 Matriz Competitiva — MG Joyas vs. Competidores",
            "🏆"
        )

    # ── 15: BENCHMARK DE PRECIOS ──
    bm = d.get("benchmark_precios", [])
    if isinstance(bm, list) and bm:
        content += _build_table_section(
            {"data": bm},
            [
                {"header": "Producto MG", "key": "producto", "strong": True},
                {"header": "Precio MG", "key": "precio_mg"},
                {"header": "Precio Competencia", "key": "precio_comp"},
                {"header": "Diferencia", "key": "diferencia", "badge": "green"},
                {"header": "Competidor", "key": "competidor"},
            ],
            "💰 Benchmark de Precios vs. Competencia",
            "💰"
        )

    # ── 16: PALABRAS CLAVE ──
    kw = d.get("palabras_clave", [])
    if isinstance(kw, list) and kw:
        content += _build_table_section(
            {"data": kw},
            [
                {"header": "Keyword", "key": "keyword", "strong": True},
                {"header": "Volumen", "key": "volumen", "badge": "blue"},
                {"header": "Intención", "key": "intencion", "badge": "purple"},
                {"header": "Prioridad", "key": "prioridad", "badge": "gold"},
            ],
            "🔑 Palabras Clave del Mercado Uruguayo",
            "🔑"
        )

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  BLOQUE 4: ¿ADÓNDE VA? — Estrategia y objetivos             ║
    # ╚══════════════════════════════════════════════════════════════╝
    content += _sd("adonde-va", "BLOQUE 4: ¿ADÓNDE VA? — Estrategia y Objetivos", "🎯")

    # ── 17: OBJETIVOS SMART ──
    smart = d.get("objetivos_smart", {})
    if isinstance(smart, dict):
        content += _sg("🎯 Objetivos SMART", smart,
            ["especifico","medible","alcanzable","relevante","temporal"])
        # Add extended vision targets if present
        extra = ""
        for k, v in [("objetivo_6_meses","6 meses"), ("objetivo_12_meses","12 meses")]:
            val = smart.get(k, "")
            if val:
                extra += _kv_item(f"Visión {v}", val)
        if extra:
            content += f'<div class="card"><h2>🔭 Visión Extendida</h2><div class="kv-grid">{extra}</div></div>'

    # ── 18: PLAN DE MEDIOS ──
    plan_m = d.get("plan_medios", {})
    if isinstance(plan_m, dict):
        content += _sg("📡 Plan de Medios y Presupuesto", plan_m,
            ["presupuesto_mensual","canal_principal","distribucion","objetivo_principal","kpis_principales","metas_3_meses","publicidad_previa","estructura_campana_sugerida"])

    # ── 19: CALENDARIO COMERCIAL ──
    cal = d.get("calendario_comercial", [])
    if isinstance(cal, list) and cal:
        content += _build_table_section(
            {"data": cal},
            [
                {"header": "Oportunidad", "key": "oportunidad", "strong": True},
                {"header": "Fecha", "key": "fecha"},
                {"header": "Prioridad", "key": "prioridad", "badge": "gold"},
                {"header": "Producto sugerido", "key": "producto"},
                {"header": "Acción sugerida", "key": "accion_sugerida"},
            ],
            "📅 Calendario Comercial — Oportunidades y Acciones 2026-2027",
            "📅"
        )

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  BLOQUE 5: ¿CÓMO LLEGA? — Setup técnico y activos           ║
    # ╚══════════════════════════════════════════════════════════════╝
    content += _sd("como-llega", "BLOQUE 5: ¿CÓMO LLEGA? — Setup Técnico y Activos Digitales", "🔧")

    # ── 20: ACTIVOS DIGITALES ──
    dig = d.get("activos_digitales", {})
    if isinstance(dig, dict):
        content += _sg("📱 Activos Digitales — Estado Actual", dig,
            ["sitio_web","redes_sociales","plataformas","seguidores_totales","frecuencia_contenido","formato_contenido","engagement_estimado","whatsapp_business","email_marketing"])

    # ── 21: REDES SOCIALES (DETALLADO) ──
    rrss = d.get("redes_sociales", {})
    if isinstance(rrss, dict):
        content += _sg("📹 Rendimiento en Redes Sociales", rrss,
            ["plataforma_principal","seguidores","seguidos","publicaciones_semana","tipo_contenido","destacados","link_bio","ultima_publicacion","formato_dominante","horarios_publicacion","hashtags_uso","tasa_engagement_estimada"])

    # ── 22: ANÁLISIS DE CONTENIDO ACTUAL ──
    ac = d.get("analisis_contenido_actual", {})
    if isinstance(ac, dict):
        content += _sg("🎬 Análisis de Contenido Actual", ac,
            ["tipo_contenido_dominante","variedad_formatos","frecuencia","storytelling","uso_ugc","recomendacion_principal","oportunidad_mejora"])

    # ── 23: ESTRATEGIA DE CONTENIDO PROPUESTA ──
    ec = d.get("estrategia_contenido_propuesta", {})
    if isinstance(ec, dict):
        content += _sg("📋 Estrategia de Contenido Propuesta", ec,
            ["distribucion_semanal","tipos_reels","storytelling_marca","ugc_estrategia","hashtag_estrategia"])
        # Calendar grid
        cal_ed = ec.get("calendario_editorial_semanal", {})
        if isinstance(cal_ed, dict):
            dias_html = "".join(
                f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center">
                    <div style="font-weight:700;font-size:12px;color:#1a2a4a;text-transform:uppercase">{dia}</div>
                    <div style="font-size:12px;color:#6b7280;margin-top:4px">{cont}</div>
                </div>"""
                for dia, cont in cal_ed.items()
            )
            content += f"""<div class="card"><h2>📆 Calendario Editorial Semanal Sugerido</h2>
            <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:10px">{dias_html}</div></div>"""

    # ── 24: TRACKING ──
    track = d.get("tracking_medicion", {})
    if isinstance(track, dict):
        content += _sg("🔧 Tracking y Medición", track,
            ["meta_pixel","google_tag","ga4","gsc","utm_params","capi_conversions_api","estado_general","plan_inmediato"])

    # ── 25: SETUP TÉCNICO ──
    setup = d.get("setup_tecnico", {})
    if isinstance(setup, dict):
        content += _sg("⚙️ Setup Técnico — Estado por Herramienta", setup,
            ["meta_business","facebook_page","meta_pixel","google_ads","google_tag","creatividades","email_tool","estado_general"])

    # ── 26: QUICK WINS ──
    qw = d.get("quick_wins", [])
    if isinstance(qw, list) and qw:
        content += _build_table_section(
            {"data": qw},
            [
                {"header": "Acción rápida", "key": "accion", "strong": True},
                {"header": "Impacto", "key": "impacto", "badge": "green"},
                {"header": "Esfuerzo", "key": "esfuerzo", "badge_map": {"muy bajo": "badge-green", "bajo": "badge-blue", "medio": "badge-gold", "alto": "badge-red"}, "default_badge": "badge-blue"},
                {"header": "Plazo", "key": "plazo", "badge": "gold"},
            ],
            "⚡ Quick Wins — Lo que se puede hacer YA sin inversión",
            "⚡"
        )

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  BLOQUE 6: ANÁLISIS FINANCIERO                              ║
    # ╚══════════════════════════════════════════════════════════════╝
    content += _sd("analisis-financiero", "BLOQUE 6: ANÁLISIS FINANCIERO Y PROYECCIONES", "💰")

    # ── 27: ESTRUCTURA FINANCIERA ──
    af = d.get("analisis_financiero", {})
    if isinstance(af, dict):
        content += _sg("💰 Análisis Financiero", af,
            ["ticket_promedio_estimado","margen_promedio_general","estructura_costos","punto_equilibrio_ads"])

    # ── 28: PROYECCIÓN MENSUAL ──
    proy = af.get("proyeccion_3_meses", {}) if isinstance(af, dict) else {}
    if isinstance(proy, dict) and proy:
        proy_html = ""
        for mes_key, mes_label in [("mes_1_julio", "Mes 1 — Julio"), ("mes_2_agosto", "Mes 2 — Agosto"), ("mes_3_septiembre", "Mes 3 — Septiembre")]:
            desc = proy.get(mes_key, "")
            if desc:
                proy_html += _kv_item(mes_label, desc)
        if proy_html:
            content += f'<div class="card"><h2>📈 Proyección Primeros 3 Meses</h2><div class="kv-grid">{proy_html}</div></div>'

    # ── 29: ESCENARIOS DE ROI ──
    esc = af.get("escenarios_roi", {}) if isinstance(af, dict) else {}
    if isinstance(esc, dict) and esc:
        esc_html = ""
        for tipo, color in [("conservador", "#f59e0b"), ("realista", "#3b82f6"), ("optimista", "#10b981")]:
            desc = esc.get(tipo, "")
            if desc:
                esc_html += f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:16px;border-left:4px solid {color}">
                    <div style="font-weight:700;font-size:14px;color:{color};text-transform:capitalize;margin-bottom:4px">{tipo}</div>
                    <div style="font-size:13px;color:#4b5563">{desc}</div>
                </div>"""
        if esc_html:
            content += f"""<div class="card"><h2>📊 Escenarios de ROI Proyectado</h2>
            <p style="font-size:13px;color:#6b7280;margin-bottom:12px">Proyecciones basadas en benchmarks del mercado uruguayo para joyería en Meta Ads.</p>
            <div style="display:grid;gap:12px">{esc_html}</div></div>"""

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  BLOQUE 7: RIESGOS Y PLAN DE ACCIÓN                        ║
    # ╚══════════════════════════════════════════════════════════════╝
    content += _sd("riesgos-plan", "BLOQUE 7: RIESGOS, BRECHAS Y PLAN DE ACCIÓN", "⚠️")

    # ── 30: ANÁLISIS DE RIESGOS ──
    riesgos = d.get("analisis_riesgos", [])
    if isinstance(riesgos, list) and riesgos:
        content += _build_table_section(
            {"data": riesgos},
            [
                {"header": "Riesgo", "key": "riesgo", "strong": True},
                {"header": "Probabilidad", "key": "probabilidad", "badge_map": {"alta": "badge-red", "media": "badge-gold", "baja": "badge-green"}, "default_badge": "badge-blue"},
                {"header": "Impacto", "key": "impacto", "badge_map": {"alto": "badge-red", "medio": "badge-gold", "bajo": "badge-green"}, "default_badge": "badge-blue"},
                {"header": "Plan de contingencia", "key": "plan_contingencia"},
            ],
            "⚠️ Análisis de Riesgos — Matriz Probabilidad x Impacto",
            "⚠️"
        )

    # ── 31: BRECHAS DETECTADAS ──
    brechas = d.get("brechas", [])
    if isinstance(brechas, list) and brechas:
        content += _build_table_section(
            {"data": brechas},
            [
                {"header": "Brecha Detectada", "key": "brecha", "strong": True},
                {"header": "Urgencia", "key": "urgencia", "badge": "red"},
                {"header": "Área", "key": "area", "badge": "blue"},
            ],
            "⛔ Brechas Detectadas — Lo que falta para avanzar",
            "⛔"
        )

    # ── 32: PLAN DE ACCIÓN ──
    plan = d.get("plan_accion", [])
    if isinstance(plan, list) and plan:
        content += _build_table_section(
            {"data": plan},
            [
                {"header": "Paso", "key": "paso", "strong": True},
                {"header": "Responsable", "key": "responsable"},
                {"header": "Plazo", "key": "plazo", "badge": "gold"},
                {"header": "Prioridad", "key": "prioridad", "badge": "red"},
            ],
            "🗺️ Plan de Acción — Próximos pasos",
            "🗺️"
        )

    # ── 33: INDICADORES DE ÉXITO ──
    ie = d.get("indicadores_exito", {})
    if isinstance(ie, dict):
        content += _sg("📊 Indicadores Clave de Éxito", ie,
            ["semanales","mensuales","trimestrales","dashboard_propuesto"])

    # ╔══════════════════════════════════════════════════════════════╗
    # ║  BLOQUE 8: FUTURO Y CIERRE                                  ║
    # ╚══════════════════════════════════════════════════════════════╝
    content += _sd("futuro-cierre", "BLOQUE 8: VISIÓN A FUTURO Y SÍNTESIS", "🔭")

    # ── 34: ROADMAP DE IMPLEMENTACIÓN ──
    road = d.get("roadmap", [])
    if isinstance(road, list) and road:
        tl = "".join(
            f'<div class="timeline-item"><div class="tl-title">{r.get("semana","")}</div><div class="tl-desc">{r.get("accion","")}</div></div>'
            for r in road
        )
        content += f"""
        <div class="card">
            <h2>🗓️ Roadmap de Implementación</h2>
            <div class="timeline">{tl}</div>
        </div>"""

    # ── 35: VISIÓN A FUTURO ──
    vf = d.get("vision_futuro", {})
    if isinstance(vf, dict):
        v_html = ""
        for periodo, color in [("vision_6_meses", "#3b82f6"), ("vision_12_meses", "#8b5cf6"), ("vision_24_meses", "#d4a030")]:
            desc = vf.get(periodo, "")
            if desc:
                v_html += f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:16px;border-left:4px solid {color}">
                    <div style="font-weight:700;font-size:14px;color:{color};margin-bottom:4px">{
                        periodo.replace("_"," ").title().replace("Vision","Visión")}</div>
                    <div style="font-size:13px;color:#4b5563">{desc}</div>
                </div>"""
        hitos = vf.get("hitos_crecimiento", "")
        if v_html:
            content += f"""<div class="card"><h2>🔭 Visión a Futuro — ¿Hacia dónde vamos?</h2>
            <p style="font-size:13px;color:#6b7280;margin-bottom:12px">La hoja de ruta estratética que guía el crecimiento de MG Joyas en los próximos 2 años.</p>
            <div style="display:grid;gap:12px">{v_html}</div>"""
            if hitos:
                content += f'<div style="margin-top:12px;padding:10px 14px;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;font-size:13px;color:#92400e"><strong>🏁 Hitos de crecimiento:</strong> {hitos}</div>'
            content += "</div>"

    # ── 36: SÍNTESIS FINAL ──
    sintesis = d.get("sintesis", "")
    if sintesis and sintesis != "—":
        content += f"""
        <div class="card" style="border-left:4px solid #d4a030;background:#fffbeb">
            <h2>📊 Síntesis de Situación Actual</h2>
            <p style="font-size:15px;color:#4b5563;line-height:1.7">{sintesis}</p>
        </div>"""

    if not content:
        content = '<div class="card"><p>No hay datos suficientes para generar el resumen situacional.</p></div>'

    return content


# ═══════════════════════════════════════════════════════════════
#  GENERADOR PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def gen_paso(paso_id, data, cliente, analista=""):
    config = PASOS[paso_id]
    d = data if isinstance(data, dict) else {}
    titulo = config
    emoji = EMOJIS.get(paso_id, "\U0001f4c4")
    content = _build_header_html(paso_id, titulo, cliente, analista, emoji)
    if paso_id in CUSTOM_HANDLERS:
        content += CUSTOM_HANDLERS[paso_id](d)
    else:
        content += gen_paso_generico(data, cliente, paso_id, titulo, analista)
    content += _build_footer_html()
    return _wrap_html(content, f"{titulo} - {cliente}", paso=paso_id, cliente=cliente)


def gen_paso_generico(data, cliente, paso, titulo, analista=""):
    d = data if isinstance(data, dict) else {}
    items = data if isinstance(data, list) else (d.get("data", data) if isinstance(data, dict) else [])
    content = _build_header_html(paso, titulo, cliente, analista)
    if isinstance(d, dict):
        kv_rows = ""
        for key, val in d.items():
            if key.startswith("_") or key == "data": continue
            label = key.replace("_", " ").title()
            kv_rows += _kv_item(label, val)
        if kv_rows:
            content += _build_kv_section(kv_rows, titulo, "\U0001f4cb")
    if isinstance(items, list) and items and isinstance(items[0], dict):
        headers = list(items[0].keys())
        cols = [{"header": h.replace("_", " ").title(), "key": h} for h in headers]
        content += _build_table_section(data, cols, "Datos", "\U0001f4ca")
    content += _build_footer_html()
    return _wrap_html(content, f"{titulo} - {cliente}", paso=paso, cliente=cliente)


def _generar_paso(paso_id, data, cliente, analista=""):
    titulo = PASOS.get(paso_id, f"Paso {paso_id}")
    prefijo = paso_id.replace(".", "-")
    if paso_id in CUSTOM_HANDLERS:
        html = gen_paso(paso_id, data, cliente, analista)
    else:
        html = gen_paso_generico(data, cliente, paso_id, titulo, analista)
    ruta = _guardar_html(html, cliente, f"{prefijo}-{titulo.replace(' ', '-')}", paso=paso_id)
    return ruta


def _listar_clientes():
    return listar_clientes(DOCS_DIR)


def _status(cliente):
    carpeta = sanitizar_nombre(cliente)
    dir_cliente = os.path.join(DOCS_DIR, carpeta)
    if not os.path.isdir(dir_cliente):
        logger.error("No se encontr\u00f3 la carpeta para '%s'.", cliente)
        logger.error("  Ruta esperada: %s", dir_cliente)
        return
    nav = _obtener_info_navegacion(dir_cliente)
    completados = sorted(nav.keys(), key=lambda p: ORDERED.index(p) if p in ORDERED else 999)
    logger.info("Documentos encontrados para %s:", cliente)
    logger.info("  Carpeta: %s", dir_cliente)
    for pid in completados:
        emoji = EMOJIS.get(pid, "\U0001f4c4")
        nombre = PASOS.get(pid, pid)
        logger.info("    %s [%s] %s", emoji, pid, nombre)
    if not completados:
        logger.info("    (sin reportes generados)")
    ruta_status = generar_index_html(cliente)
    if ruta_status:
        logger.info("Navegaci\u00f3n generada: %s", ruta_status)


def main():
    parser = argparse.ArgumentParser(description="Generador de Reportes HTML - Global Infinity Marketing")
    parser.add_argument("--data-file", "-f", help="Archivo JSON con los datos del paso")
    parser.add_argument("--paso", "-p", help="N\u00famero de paso (ej: 1.1, 2.3)")
    parser.add_argument("--cliente", "-c", help="Nombre del cliente")
    parser.add_argument("--analista", "-a", help="Nombre del analista (opcional)")
    parser.add_argument("--status", "-s", action="store_true", help="Ver estado de un cliente")
    parser.add_argument("--listar", "-l", action="store_true", help="Listar clientes existentes")
    parser.add_argument("--generate-index", action="store_true", help="Regenerar \u00edndice de un cliente")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if args.listar:
        clientes = _listar_clientes()
        if clientes:
            logger.info("Clientes existentes:")
            for c in clientes:
                logger.info("    %s", c)
        else:
            logger.info("No hay clientes registrados.")
        return

    if args.status:
        if not args.cliente:
            print("\n  Us\u00e1: python generar_reporte_html.py --status --cliente \"Nombre\"", file=sys.stderr)
            return
        _status(args.cliente)
        return

    if args.generate_index:
        if not args.cliente:
            print("\n  Us\u00e1: python generar_reporte_html.py --generate-index --cliente \"Nombre\"", file=sys.stderr)
            return
        ruta = generar_index_html(args.cliente)
        if ruta:
            logger.info("Navegaci\u00f3n generada: %s", ruta)
        else:
            logger.error("No se encontr\u00f3 la carpeta para '%s'.", args.cliente)
        return

    if not args.data_file:
        print("\n  Us\u00e1: python generar_reporte_html.py --data-file datos.json", file=sys.stderr)
        print("  Opciones: --paso X.Y --cliente \"Nombre\" --analista \"Nombre\"", file=sys.stderr)
        return

    if not os.path.isfile(args.data_file):
        logger.error("No se encontr\u00f3 el archivo '%s'", args.data_file)
        return

    with open(args.data_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error("El archivo JSON no es v\u00e1lido: %s", e)
            return

    cliente = args.cliente or data.pop("_cliente", None) or data.get("cliente", "")
    paso = args.paso or data.pop("_paso", None) or ""
    analista = args.analista or data.pop("_analista", None) or data.pop("analista", "")

    if not cliente:
        logger.error("No se especific\u00f3 el cliente. Us\u00e1 --cliente o inclu\u00ed '_cliente' en el JSON.")
        return
    if not paso:
        logger.error("No se especific\u00f3 el paso. Us\u00e1 --paso o inclu\u00ed '_paso' en el JSON.")
        return

    if isinstance(data, dict):
        for k in ["_cliente", "_paso", "_analista", "cliente", "analista"]:
            data.pop(k, None)

    logger.info("Datos cargados desde %s", args.data_file)
    titulo = PASOS.get(paso, f"Paso {paso}")
    logger.info("Generando reporte: %s \u2014 %s", titulo, cliente)
    ruta = _generar_paso(paso, data, cliente, analista)
    logger.info("Reporte generado exitosamente: %s", ruta)
    ruta_url = pathlib.Path(ruta).as_uri()
    logger.info("Para abrir con Chrome DevTools: chrome-devtools_new_page con: %s", ruta_url)


if __name__ == "__main__":
    main()
