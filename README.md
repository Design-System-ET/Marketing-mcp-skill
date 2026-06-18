# Global Infinity Marketing

Workspace de **opencode** para la agencia digital **Global Infinity Marketing** (Uruguay).
Sistema automatizado de **onboarding de clientes** con 9 fases, 2 skills de IA, generación
de reportes HTML/Word profesionales e integración con MCPs de marketing digital.

## Requisitos

- [Node.js](https://nodejs.org/) 18+
- [opencode](https://opencode.ai) — CLI de IA para el workspace
- [Python 3.14+](https://python.org) — para los scripts de generación de reportes

### Instalación del entorno virtual

```powershell
# Crear el entorno virtual
python -m venv venv

# Activar (PowerShell)
.\venv\Scripts\Activate.ps1

# Activar (CMD)
venv\Scripts\activate.bat

# Instalar dependencias desde requirements.txt
pip install -r requirements.txt
```

## Skills de IA

El onboarding se divide en **9 fases** ejecutadas por 2 skills especializadas:

```
marketing-analyst (F1→F2→F3→F5) → campaign-manager (F4→F6→F7→F8) → marketing-analyst (F9)
```

### `marketing-analyst` — Estudio/Diagnóstico
- **Ubicación:** `.opencode/skills/marketing-analyst/SKILL.md`
- **Fases:** F1 Diagnóstico, F2 Investigación, F3 Auditoría, F5 Estrategia, F9 Resumen
- **Qué hace:** Entrevista al cliente, analiza mercado, audita activos digitales, define estrategia, genera macro-informe final
- **MCPs:** notion, google-search, brave-search, mercadolibre, sequential-thinking, google-sheets, ga4, google-search-console, meta-ads, klaviyo, x-twitter

### `campaign-manager` — Operativa
- **Ubicación:** `.opencode/skills/campaign-manager/SKILL.md`
- **Fases:** F4 Presencia Digital, F6 Setup Técnico, F7 Pilotaje, F8 Lanzamiento
- **Qué hace:** Mejora activos digitales, configura Meta/Google Ads, lanza pilotos, escala campañas
- **MCPs:** meta-ads, google-ads, ga4, klaviyo, google-sheets, google-search-console, sequential-thinking

## Generadores de Reportes

| Script | Formato | Propósito |
|--------|---------|-----------|
| `generar_reporte_html.py` | HTML | Genera 34+ reportes HTML profesionales con navegación, índice y CSS optimizado para A4 |
| `generar_reporte_word.py` | DOCX | Compila todos los HTMLs en un documento Word con portada, TOC, capítulos y pie de página |
| `generar_metodologia.py` | DOCX | Documento de metodología integrada |
| `utils.py` | — | Utilidades compartidas (`sanitizar_nombre`, `listar_clientes`) |

### Flujo de trabajo

1. La skill `marketing-analyst` recolecta datos del cliente (F1-F3, F5).
2. La skill `campaign-manager` ejecuta la parte operativa (F4, F6-F8).
3. `marketing-analyst` genera el resumen final (F9).
4. Cada paso genera su reporte HTML con `generar_reporte_html.py --paso X.Y --cliente "Nombre" --analista "Nombre" --data-file temp.json`.
5. `generar_reporte_word.py --cliente "NOMBRE"` compila todos los HTMLs en un Word profesional.
6. Los reportes se guardan en `Clientes/[nombre_cliente]/`.

### Comandos útiles

```powershell
# Ver estado de un cliente
python generar_reporte_html.py --status --cliente "Nombre"

# Generar índice manualmente
python generar_reporte_html.py --generate-index --cliente "Nombre"

# Generar documento Word completo
python generar_reporte_word.py --cliente "NOMBRE"
```

## MCPs disponibles

### Listos para usar (sin configuración)

| MCP | Uso |
|-----|-----|
| **Meta Ads** | Campañas de Facebook e Instagram Ads (OAuth por navegador al primer uso) |
| **Klaviyo** | Email marketing, flows, segmentos y campañas (OAuth por navegador) |
| **Google Search** | Búsqueda en Google desde el agente (100% gratis, sin API key) |
| **Sequential Thinking** | Razonamiento paso a paso para análisis estratégicos (100% gratis) |
| **X/Twitter** | Publicar tweets, buscar, analizar perfiles y tendencias (100% gratis, sin API key) |
| **Chrome DevTools** | Navegador automatizado — captura de pantallas, auditorías, debugging |

> **Automatización por navegador:** Los MCPs de Meta Ads, Klaviyo, X/Twitter, Google Search y Chrome DevTools operan **interactuando automáticamente con el navegador** — inician sesión, navegan, recopilan datos y ejecutan acciones sin necesidad de APIs ni tokens manuales. El agente de IA orquesta todo: abre páginas, completa formularios, extrae información y genera reportes, replicando el trabajo de un analista humano pero de forma totalmente automatizada.

### Requieren credenciales

| MCP | Qué necesitas configurar |
|-----|--------------------------|
| **Mercado Libre** | `CLIENT_ID` y `CLIENT_SECRET` — crear app en [developers.mercadolibre.com](https://developers.mercadolibre.com) |
| **Google Ads** | `CLIENT_ID`, `CLIENT_SECRET`, `DEVELOPER_TOKEN`, `REFRESH_TOKEN` — proyecto en Google Cloud + Google Ads API |
| **GA4** | `CLIENT_ID`, `CLIENT_SECRET`, `REFRESH_TOKEN` — proyecto en Google Cloud + habilitar Analytics APIs |
| **HubSpot** | `PRIVATE_APP_ACCESS_TOKEN` — crear Private App en HubSpot |
| **Google Sheets** | `CLIENT_ID`, `CLIENT_SECRET`, `REFRESH_TOKEN` — proyecto en Google Cloud + OAuth |
| **Google Search Console** | `GOOGLE_APPLICATION_CREDENTIALS` — proyecto en Google Cloud + habilitar Search Console API (gratis) |
| **Notion** | `NOTION_TOKEN` — crear integración en [notion.so/profile/integrations](https://www.notion.so/profile/integrations) (gratis) |
| **n8n** | Servidor n8n local o remoto para automatización de flujos (self-hosted, gratis) |
| **Brave Search** | API key gratuita en [api.search.brave.com](https://api.search.brave.com) (2,000 consultas/mes) |

> [!TIP]
> Consulta `PENDIENTES.md` para el estado detallado de cada integración.

## Estructura del proyecto

```
/
├── .opencode/
│   └── skills/
│       ├── marketing-analyst/
│       │   ├── SKILL.md              # Skill de diagnóstico (F1, F2, F3, F5, F9)
│       │   └── references/           # Checklist, template brief
│       └── campaign-manager/
│           └── SKILL.md              # Skill operativa (F4, F6, F7, F8)
├── Clientes/
│   └── MG Joyas/                     # Primer cliente onboardeado
│       ├── _index.html               # Índice interactivo con barra de progreso
│       ├── 1-1-*.html a 9-1-*.html   # 34 reportes HTML
│       └── Onboarding-MG Joyas-*.docx # Documento Word completo
├── opencode.json                     # Configuración MCPs + skills
├── CONTEXT.md                        # Contexto completo del proyecto
├── PENDIENTES.md                     # MCPs pendientes de configurar
├── utils.py                          # Funciones compartidas
├── generar_reporte_html.py           # Generador principal — 34+ reportes HTML
├── generar_reporte_word.py           # Generador Word con portada y TOC
├── generar_metodologia.py            # Documento de metodología integrada
└── README.md                         # Este archivo
```

## Convenciones

- Los reportes HTML se guardan en `Clientes/[NOMBRE]/XX-YY-Titulo-NOMBRE-YYYYMMDD.html`
- El índice se llama `_index.html` y se regenera automáticamente al generar cada reporte
- Los JSON temporales usan snake_case con metadatos `_cliente`, `_paso`, `_analista`
- Los números de paso (1.1 a 9.1) son fijos y compartidos entre skills

## Lo que ya está hecho

- [x] Skill `marketing-analyst` creada con 5 fases de diagnóstico
- [x] Skill `campaign-manager` creada con 4 fases operativas
- [x] Sistema de reportes HTML funcional (34+ handlers)
- [x] Sistema de reportes Word funcional
- [x] MG Joyas: 34 reportes + índice + Word generados
- [x] MCPs listos: Meta Ads, Klaviyo, X/Twitter, Google Search, Sequential Thinking, Chrome DevTools

## Cómo empezar

1. Clona o copia este workspace en tu máquina local.
2. Abre la carpeta con opencode: `opencode .`
3. Configura las credenciales de los MCPs que necesites en `opencode.json`.
4. Usa la skill `marketing-analyst` para comenzar el onboarding de un cliente.

## Personalización

- **Agregar un nuevo MCP**: Añádelo en la sección `"mcp"` del `opencode.json`.
- **Modificar skills**: Edita los archivos `SKILL.md` en `.opencode/skills/`.
- **Generar reportes manualmente**: `python generar_reporte_html.py --paso 1.1 --cliente "Nombre" --analista "Nombre" --data-file temp.json`

## Licencia

MIT &copy; 2026 Design System - Claudio Silveira. Ver [LICENSE](LICENSE).
