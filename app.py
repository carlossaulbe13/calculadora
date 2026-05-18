import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Calculadora Matemática",
    page_icon="🔢",
    layout="centered"
)

# ── CSS ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Ocultar decoración de Streamlit */
footer, #MainMenu, [data-testid="stToolbar"],
[data-testid="stDecoration"], header { display: none !important; }

/* ── Fondo de página: escritorio ─────────────────── */
.stApp, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 20% 30%, rgba(80,100,160,0.25) 0%, transparent 55%),
        radial-gradient(ellipse at 80% 70%, rgba(60,80,140,0.20) 0%, transparent 55%),
        #2c3142 !important;
}

/* ── Cuerpo de la calculadora ────────────────────── */
[data-testid="stMainBlockContainer"] {
    max-width: 560px !important;
    margin: 28px auto 48px !important;
    padding: 0 !important;

    /* Plástico dark anthracite */
    background:
        repeating-linear-gradient(
            180deg,
            rgba(255,255,255,0.013) 0px, rgba(255,255,255,0.013) 1px,
            transparent 1px, transparent 3px
        ),
        linear-gradient(175deg,
            #2a2a2f 0%,
            #1e1e23 30%,
            #1a1a1f 65%,
            #202025 100%
        ) !important;

    border-radius: 28px 28px 36px 36px !important;
    position: relative !important;

    /* Bordes que simulan plástico moldeado */
    border-top:    1px solid rgba(255,255,255,0.10) !important;
    border-left:   1px solid rgba(255,255,255,0.06) !important;
    border-right:  1px solid rgba(0,0,0,0.55) !important;
    border-bottom: 4px solid rgba(0,0,0,0.7)  !important;

    /* Sombra 3-D profunda */
    box-shadow:
        0 0 0 2px #0c0c10,
        0 0 0 4px #16161a,
        0 60px 140px rgba(0,0,0,0.90),
        0 24px  60px rgba(0,0,0,0.65),
        inset 0 2px  0 rgba(255,255,255,0.09),
        inset 0 -3px 0 rgba(0,0,0,0.50) !important;
}

/* ── Tornillos en las 4 esquinas ─────────────────── */
.calc-screws {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 50;
}
.screw {
    position: absolute;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: radial-gradient(circle at 38% 35%, #38383e, #111115);
    border: 1px solid #0a0a0d;
    box-shadow:
        inset 0 1px 2px rgba(0,0,0,0.9),
        inset 0 -1px 1px rgba(255,255,255,0.04),
        0 1px 0 rgba(255,255,255,0.05);
}
/* Ranura del tornillo */
.screw::after {
    content: '';
    position: absolute;
    top: 50%; left: 20%; right: 20%;
    height: 1.5px;
    background: rgba(0,0,0,0.7);
    transform: translateY(-50%) rotate(45deg);
    border-radius: 1px;
}
.screw.tl { top:  16px; left:  16px; }
.screw.tr { top:  16px; right: 16px; }
.screw.bl { bottom: 20px; left:  16px; }
.screw.br { bottom: 20px; right: 16px; }

/* ── Franja de marca (top) ───────────────────────── */
.brand-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 22px 36px 0;
    margin-bottom: 16px;
}
.brand-left {}
.brand-name {
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 5px;
    color: #5a5a65;
    text-transform: uppercase;
    display: block;
}
.brand-model {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 2px;
    color: #38383f;
    display: block;
    margin-top: 1px;
}
/* Panel solar falso */
.solar-panel {
    display: flex;
    gap: 3px;
    align-items: center;
}
.solar-cell {
    width: 18px; height: 10px;
    background: linear-gradient(160deg, #0d1f0d 0%, #071007 100%);
    border: 1px solid #040c04;
    border-radius: 2px;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.7), 0 0 2px rgba(34,197,94,0.04);
}

/* ── Zona interior (padding real) ────────────────── */
.calc-inner {
    padding: 0 28px 32px;
}

/* ── Pantalla LCD ────────────────────────────────── */
.lcd-bezel {
    background: #111115;
    border-radius: 12px;
    padding: 10px;
    margin: 0 0 14px;
    box-shadow:
        inset 0 4px 12px rgba(0,0,0,0.8),
        inset 0 0 0 1px rgba(0,0,0,0.6),
        0 2px 0 rgba(255,255,255,0.04);
    border: 1px solid #0a0a0e;
}
.lcd {
    background: #071209;
    border-radius: 7px;
    padding: 14px 18px 16px;
    box-shadow:
        inset 0 6px 22px rgba(0,0,0,0.85),
        0 0 24px rgba(34,197,94,0.05);
    min-height: 82px;
    position: relative;
    overflow: hidden;
}
/* Efecto scanlines en el LCD */
.lcd::after {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        rgba(0,0,0,0.10) 0px,
        rgba(0,0,0,0.10) 1px,
        transparent 1px,
        transparent 3px
    );
    pointer-events: none;
    border-radius: 7px;
}
.lcd-lbl {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.56rem;
    color: #145226;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.lcd-eq {
    font-family: 'Share Tech Mono', 'Courier New', monospace;
    font-size: 1.3rem;
    color: #4ade80;
    text-shadow: 0 0 14px rgba(74,222,128,0.55), 0 0 4px rgba(74,222,128,0.3);
    letter-spacing: 1px;
    line-height: 1.35;
}
.lcd-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #16a34a;
    opacity: 0.8;
    margin-top: 5px;
    text-shadow: 0 0 8px rgba(22,163,74,0.35);
}

/* ── Línea divisora entre pantalla y teclas ──────── */
.panel-divider {
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        #111115 10%,
        #111115 90%,
        transparent 100%
    );
    margin: 0 0 14px;
    border-radius: 1px;
}

/* ── Teclas de modo (radio → botones físicos) ─────── */
div[data-testid="stRadio"] > label { display: none !important; }
/* Ocultar etiqueta del grupo aunque esté anidada */
div[data-testid="stRadio"] label:not(:has(input[type="radio"])) { display: none !important; }
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    gap: 5px !important;
    flex-wrap: nowrap !important;
    overflow: visible !important;
}
div[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex: 1 0 auto !important;   /* crece pero NO encoge */
    overflow: visible !important;
    /* Tecla de plástico */
    background: linear-gradient(175deg, #2c2c32 0%, #202025 60%, #1c1c21 100%) !important;
    color: #4a4a55 !important;
    border-top:    1px solid rgba(255,255,255,0.08) !important;
    border-left:   1px solid rgba(255,255,255,0.05) !important;
    border-right:  1px solid rgba(0,0,0,0.4) !important;
    border-bottom: 3px solid rgba(0,0,0,0.55) !important;
    border-radius: 8px !important;
    padding: 10px 8px !important;
    font-size: 0.60rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    cursor: pointer !important;
    text-align: center !important;
    transition: all 0.10s ease !important;
    text-transform: uppercase !important;
    white-space: nowrap !important;
    box-shadow: 0 3px 6px rgba(0,0,0,0.5) !important;
}
div[data-testid="stRadio"] label > div {
    overflow: visible !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
div[data-testid="stRadio"] label:hover {
    background: linear-gradient(175deg, #323238 0%, #262630 60%, #22222a 100%) !important;
    color: #6a6a78 !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stRadio"] label:has(input[type="radio"]:checked) {
    background: linear-gradient(175deg, #7c3aed 0%, #6366f1 60%, #5254cc 100%) !important;
    color: #fff !important;
    border-top:    1px solid rgba(255,255,255,0.25) !important;
    border-left:   1px solid rgba(255,255,255,0.15) !important;
    border-right:  1px solid rgba(0,0,0,0.3) !important;
    border-bottom: 1px solid rgba(0,0,0,0.4) !important;  /* hundida */
    box-shadow: 0 1px 3px rgba(0,0,0,0.5), inset 0 1px 3px rgba(0,0,0,0.3) !important;
    transform: translateY(2px) !important;  /* efecto presionada */
}
div[data-testid="stRadio"] input[type="radio"] { display: none !important; }
div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
    margin: 0 !important;
    font-size: 0.60rem !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
}

/* ── Separador entre teclas de modo e inputs ─────── */
.key-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a30 30%, #2a2a30 70%, transparent);
    margin: 14px 0;
}

/* ── Etiquetas de sección ───────────────────────── */
.section-lbl {
    font-size: 0.60rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #3a3a45;
    margin: 12px 0 6px;
}

/* ── Number inputs ─────────────────────────────── */
[data-testid="stNumberInput"] input {
    background: #101014 !important;
    color: #b0b0c0 !important;
    border: 1px solid #2a2a32 !important;
    border-radius: 8px !important;
    font-family: 'Share Tech Mono', 'Courier New', monospace !important;
    font-size: 0.95rem !important;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.6) !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.6), 0 0 0 2px rgba(99,102,241,0.25) !important;
    outline: none !important;
}
[data-testid="stNumberInput"] label {
    color: #505060 !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}
[data-testid="stNumberInput"] button {
    background: #181820 !important;
    color: #404050 !important;
    border-color: #2a2a32 !important;
}

/* ── Botón CALCULAR  = ──────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(175deg, #f97316 0%, #ea580c 50%, #c2410c 100%) !important;
    color: #fff !important;
    border-top:    1px solid rgba(255,255,255,0.22) !important;
    border-left:   1px solid rgba(255,255,255,0.12) !important;
    border-right:  1px solid rgba(0,0,0,0.35) !important;
    border-bottom: 4px solid rgba(0,0,0,0.5) !important;
    border-radius: 11px !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    padding: 14px !important;
    box-shadow: 0 6px 20px rgba(234,88,12,0.35) !important;
    transition: all 0.08s ease !important;
    margin-top: 6px !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(234,88,12,0.45) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(3px) !important;
    border-bottom: 1px solid rgba(0,0,0,0.5) !important;
    box-shadow: 0 2px 8px rgba(234,88,12,0.3) !important;
}

/* ── Botón Limpiar ──────────────────────────────── */
.stButton > button[kind="secondary"] {
    background: linear-gradient(175deg, #2c2c32 0%, #202025 100%) !important;
    color: #4a4a55 !important;
    border-top:    1px solid rgba(255,255,255,0.07) !important;
    border-left:   1px solid rgba(255,255,255,0.04) !important;
    border-right:  1px solid rgba(0,0,0,0.4) !important;
    border-bottom: 3px solid rgba(0,0,0,0.55) !important;
    border-radius: 8px !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.4) !important;
    transition: all 0.09s ease !important;
}
.stButton > button[kind="secondary"]:hover {
    color: #6a6a78 !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"]:active {
    transform: translateY(2px) !important;
    border-bottom: 1px solid rgba(0,0,0,0.55) !important;
}

/* ── Tarjeta resultado ───────────────────────────── */
.result-card {
    background: #0d0d11;
    border: 1px solid #1e1e28;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0;
    animation: bounceIn 0.4s cubic-bezier(0.22,1,0.36,1);
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.5);
}
.result-card .rlabel {
    font-size: 0.58rem;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: #5254cc;
    font-weight: 700;
    margin-bottom: 8px;
}
.result-card .rvalue {
    font-size: 1.55rem;
    font-weight: 700;
    color: #4ade80;
    font-family: 'Share Tech Mono', 'Courier New', monospace;
    text-shadow: 0 0 12px rgba(74,222,128,0.35);
    line-height: 1.4;
}
.result-card .rnote {
    font-size: 0.72rem;
    color: #3a3a4a;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #18181e;
    font-family: 'Share Tech Mono', monospace;
}

/* ── Tarjeta error ───────────────────────────────── */
.error-card {
    background: #180a0a;
    border: 1px solid #3a1010;
    border-radius: 10px;
    padding: 11px 16px;
    color: #f87171;
    font-weight: 500;
    font-size: 0.86rem;
    animation: fadeUp 0.3s ease;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.5);
}

/* ── Info (discriminante) ────────────────────────── */
[data-testid="stInfo"] {
    background: #0d0d14 !important;
    border-color: #1e2040 !important;
    color: #7c86cc !important;
    border-radius: 9px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.82rem !important;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.4) !important;
}

/* ── Animaciones ─────────────────────────────────── */
@keyframes bounceIn {
    0%   { transform: scale(0.92); opacity: 0; }
    55%  { transform: scale(1.02); opacity: 1; }
    100% { transform: scale(1); }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Divider nativo */
hr { border-color: #1e1e24 !important; }

/* Contenedor de columnas — quitar margen extra y alinear verticalmente */
[data-testid="stHorizontalBlock"] { gap: 8px !important; align-items: center !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ──────────────────────────────────────────────────────────────────────
def result_card(label, value, note=""):
    note_html = f'<div class="rnote">{note}</div>' if note else ""
    return f"""<div class="result-card">
        <div class="rlabel">{label}</div>
        <div class="rvalue">{value}</div>
        {note_html}
    </div>"""

def error_card(msg):
    return f'<div class="error-card">⚠ {msg}</div>'

def styled_fig(title):
    fig, ax = plt.subplots(figsize=(7.5, 4))
    fig.patch.set_facecolor("#0d0d11")
    ax.set_facecolor("#0d0d11")
    ax.set_title(title, fontsize=11, fontweight="bold", color="#8080a0", pad=10)
    ax.grid(True, linestyle="--", alpha=0.25, color="#1e1e28")
    ax.axhline(0, color="#2a2a35", linewidth=1)
    ax.axvline(0, color="#2a2a35", linewidth=1)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#1e1e28")
    ax.tick_params(colors="#3a3a50")
    return fig, ax

# ── Datos de pantalla LCD por modo ───────────────────────────────────────────────
MODOS  = ["1° GRD", "2° GRD", "SISTEMA", "LINEAL", "CUADRÁT"]
SCREEN = [
    ("ax + b = 0",                          "x = −b / a"),
    ("ax² + bx + c = 0",                    "x = (−b ± √Δ) / 2a"),
    ("a₁x + b₁y = c₁  |  a₂x + b₂y = c₂", "Método de Cramer"),
    ("y = mx + b",                           "Función lineal"),
    ("y = ax² + bx + c",                    "Vértice: (−b/2a ,  f(−b/2a))"),
]

if "modo" not in st.session_state:
    st.session_state.modo = 0

# ── Tornillos + marca (top del cuerpo) ───────────────────────────────────────────
st.markdown("""
<div class="calc-screws">
    <div class="screw tl"></div>
    <div class="screw tr"></div>
    <div class="screw bl"></div>
    <div class="screw br"></div>
</div>
<div class="brand-strip">
    <div class="brand-left">
        <span class="brand-name">Calcumat</span>
        <span class="brand-model">FX-500 SCIENTIFIC</span>
    </div>
    <div class="solar-panel">
        <div class="solar-cell"></div>
        <div class="solar-cell"></div>
        <div class="solar-cell"></div>
        <div class="solar-cell"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Pantalla LCD ──────────────────────────────────────────────────────────────────
eq, sub = SCREEN[st.session_state.modo]
st.markdown(f"""
<div style="padding: 0 28px;">
<div class="lcd-bezel">
  <div class="lcd">
    <div class="lcd-lbl">▸ FÓRMULA ACTIVA</div>
    <div class="lcd-eq">{eq}</div>
    <div class="lcd-sub">{sub}</div>
  </div>
</div>
</div>
""", unsafe_allow_html=True)

# ── Separador ─────────────────────────────────────────────────────────────────────
st.markdown('<div style="padding:0 28px"><div class="panel-divider"></div></div>',
            unsafe_allow_html=True)

# ── Teclas de modo ────────────────────────────────────────────────────────────────
with st.container():
    # padding lateral via columnas vacías
    _, inner, _ = st.columns([0.08, 11.84, 0.08])
    with inner:
        key_col, clr_col = st.columns([5.2, 0.8])
        with key_col:
            sel = st.radio("Modo", MODOS,
                           index=st.session_state.modo,
                           horizontal=True,
                           key="modo_radio",
                           label_visibility="collapsed")
        with clr_col:
            if st.button("🗑", use_container_width=True, help="Limpiar campos"):
                modo_bak = st.session_state.modo
                for k in list(st.session_state.keys()):
                    if k not in ("modo", "modo_radio"):
                        del st.session_state[k]
                st.session_state.modo = modo_bak
                st.rerun()

new_idx = MODOS.index(sel)
if new_idx != st.session_state.modo:
    for k in list(st.session_state.keys()):
        if k not in ("modo", "modo_radio"):
            del st.session_state[k]
    st.session_state.modo = new_idx
    st.rerun()

idx = st.session_state.modo

# ── Zona de inputs y resultados (con padding lateral) ────────────────────────────
_, body, _ = st.columns([0.08, 11.84, 0.08])

with body:
    st.markdown('<div class="key-divider"></div>', unsafe_allow_html=True)

    # ── 1. Ecuación de 1er grado ─────────────────────────────────────────────
    if idx == 0:
        st.markdown('<p class="section-lbl">Coeficientes</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        a = c1.number_input("a  (de x)", key="e1_a", format="%.6g",
                            help="Multiplicador de x — no puede ser 0")
        b = c2.number_input("b  (término independiente)", key="e1_b", format="%.6g")

        if st.button("CALCULAR", type="primary", use_container_width=True, key="calc1"):
            if a == 0:
                st.markdown(error_card("El coeficiente <b>a</b> no puede ser 0."),
                            unsafe_allow_html=True)
            else:
                x = -b / a
                verif = a * x + b
                st.markdown(result_card(
                    "Solución",
                    f"x = {x:.6g}",
                    note=f"Verif: {a}·({x:.4g}) + {b} = {verif:.2e} ≈ 0 ✓"
                ), unsafe_allow_html=True)

    # ── 2. Ecuación de 2do grado ──────────────────────────────────────────────
    elif idx == 1:
        st.markdown('<p class="section-lbl">Coeficientes</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        a = c1.number_input("a  (x²)", key="e2_a", format="%.6g", help="No puede ser 0")
        b = c2.number_input("b  (x)", key="e2_b", format="%.6g")
        c = c3.number_input("c  (independiente)", key="e2_c", format="%.6g")

        if st.button("CALCULAR", type="primary", use_container_width=True, key="calc2"):
            if a == 0:
                st.markdown(error_card("El coeficiente <b>a</b> no puede ser 0."),
                            unsafe_allow_html=True)
            else:
                disc = b**2 - 4*a*c
                st.info(f"Δ = b² − 4ac = {b}² − 4·{a}·{c} = {disc:.6g}")
                if disc > 0:
                    r1 = (-b + math.sqrt(disc)) / (2*a)
                    r2 = (-b - math.sqrt(disc)) / (2*a)
                    st.markdown(result_card(
                        "Dos raíces reales  (Δ > 0)",
                        f"x₁ = {r1:.6g}<br>x₂ = {r2:.6g}",
                        note=f"Suma = {r1+r2:.4g} = −b/a  |  Producto = {r1*r2:.4g} = c/a"
                    ), unsafe_allow_html=True)
                elif disc == 0:
                    r = -b / (2*a)
                    st.markdown(result_card(
                        "Raíz doble  (Δ = 0)",
                        f"x = {r:.6g}",
                        note="La parábola es tangente al eje x."
                    ), unsafe_allow_html=True)
                else:
                    re = -b / (2*a)
                    im = math.sqrt(-disc) / (2*a)
                    st.markdown(result_card(
                        "Sin raíces reales  (Δ < 0)",
                        f"x₁ = {re:.4g} + {im:.4g}i<br>x₂ = {re:.4g} − {im:.4g}i",
                        note="La parábola no intersecta el eje x."
                    ), unsafe_allow_html=True)

    # ── 3. Sistema de ecuaciones 2×2 ─────────────────────────────────────────
    elif idx == 2:
        st.markdown('<p class="section-lbl">Primera ecuación  —  a₁x + b₁y = c₁</p>',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        a1  = c1.number_input("a₁", key="s_a1", format="%.6g")
        b1  = c2.number_input("b₁", key="s_b1", format="%.6g")
        c1v = c3.number_input("c₁", key="s_c1", format="%.6g")

        st.markdown('<p class="section-lbl">Segunda ecuación  —  a₂x + b₂y = c₂</p>',
                    unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        a2  = c1.number_input("a₂", key="s_a2", format="%.6g")
        b2  = c2.number_input("b₂", key="s_b2", format="%.6g")
        c2v = c3.number_input("c₂", key="s_c2", format="%.6g")

        if st.button("CALCULAR", type="primary", use_container_width=True, key="calc3"):
            D = a1*b2 - a2*b1
            if D == 0:
                st.markdown(error_card(
                    "Determinante = 0. Sin solución única (paralelas o coincidentes)."
                ), unsafe_allow_html=True)
            else:
                xs = (c1v*b2 - c2v*b1) / D
                ys = (a1*c2v - a2*c1v) / D
                v1 = a1*xs + b1*ys
                v2 = a2*xs + b2*ys
                st.markdown(result_card(
                    "Solución del sistema",
                    f"x = {xs:.6g}  ,  y = {ys:.6g}",
                    note=(f"Verif 1ª: {v1:.4g} (esp. {c1v})  |  "
                          f"2ª: {v2:.4g} (esp. {c2v})")
                ), unsafe_allow_html=True)

                fig, ax = styled_fig("Sistema 2×2")
                rng = np.linspace(xs - 10, xs + 10, 400)
                if b1 != 0:
                    ax.plot(rng, (c1v - a1*rng)/b1, lw=2.2, color="#818cf8",
                            label=f"{a1}x + {b1}y = {c1v}")
                else:
                    ax.axvline(c1v/a1, lw=2.2, color="#818cf8",
                               label=f"x = {c1v/a1:.4g}")
                if b2 != 0:
                    ax.plot(rng, (c2v - a2*rng)/b2, lw=2.2, color="#fbbf24",
                            label=f"{a2}x + {b2}y = {c2v}")
                else:
                    ax.axvline(c2v/a2, lw=2.2, color="#fbbf24",
                               label=f"x = {c2v/a2:.4g}")
                ax.scatter([xs], [ys], s=120, color="#f87171", zorder=6,
                           label=f"({xs:.3g}, {ys:.3g})")
                ax.legend(fontsize=8, facecolor="#111115", edgecolor="#1e1e28",
                          labelcolor="#8080a0")
                st.pyplot(fig)
                plt.close(fig)

    # ── 4. Función lineal ─────────────────────────────────────────────────────
    elif idx == 3:
        modo = st.radio("Método", ["Intercepto", "2 Puntos"],
                        horizontal=True, key="lin_modo",
                        label_visibility="collapsed")
        st.markdown('<p class="section-lbl">Datos</p>', unsafe_allow_html=True)

        if modo == "Intercepto":
            c1, c2 = st.columns(2)
            m  = c1.number_input("Pendiente m",  key="lin_m",  format="%.6g")
            bv = c2.number_input("Intercepto b", key="lin_b",  format="%.6g")
            xv = st.number_input("x a evaluar",  key="lin_xv", format="%.6g")

            if st.button("CALCULAR", type="primary", use_container_width=True, key="calc4a"):
                yv = m*xv + bv
                st.markdown(result_card(
                    "Resultado",
                    f"y = {yv:.6g}",
                    note=f"y = {m}·({xv}) + {bv} = {yv:.4g}"
                ), unsafe_allow_html=True)
                fig, ax = styled_fig("Función lineal")
                rng = np.linspace(xv - 10, xv + 10, 400)
                ax.plot(rng, m*rng + bv, lw=2.2, color="#818cf8",
                        label=f"y = {m}x + {bv}")
                ax.scatter([xv], [yv], s=120, color="#f87171", zorder=6,
                           label=f"({xv}, {yv:.4g})")
                ax.legend(fontsize=8, facecolor="#111115", edgecolor="#1e1e28",
                          labelcolor="#8080a0")
                st.pyplot(fig)
                plt.close(fig)
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("<span style='color:#404050;font-size:.72rem;font-weight:700;"
                            "letter-spacing:1px;text-transform:uppercase'>Punto 1</span>",
                            unsafe_allow_html=True)
                px1 = st.number_input("x₁", key="lin_px1", format="%.6g")
                py1 = st.number_input("y₁", key="lin_py1", format="%.6g")
            with c2:
                st.markdown("<span style='color:#404050;font-size:.72rem;font-weight:700;"
                            "letter-spacing:1px;text-transform:uppercase'>Punto 2</span>",
                            unsafe_allow_html=True)
                px2 = st.number_input("x₂", key="lin_px2", format="%.6g")
                py2 = st.number_input("y₂", key="lin_py2", format="%.6g")
            xv = st.number_input("x a evaluar", key="lin_xv2", format="%.6g")

            if st.button("CALCULAR", type="primary", use_container_width=True, key="calc4b"):
                if px2 == px1:
                    st.markdown(error_card("Los puntos tienen el mismo x (recta vertical)."),
                                unsafe_allow_html=True)
                else:
                    m  = (py2 - py1) / (px2 - px1)
                    bv = py1 - m*px1
                    yv = m*xv + bv
                    st.markdown(result_card(
                        "Ecuación y resultado",
                        f"y = {m:.4g}x + {bv:.4g}<br>y({xv}) = {yv:.6g}",
                        note=f"m = ({py2}−{py1}) / ({px2}−{px1}) = {m:.4g}"
                    ), unsafe_allow_html=True)
                    fig, ax = styled_fig("Función lineal (desde dos puntos)")
                    lo = min(px1, px2, xv) - 5
                    hi = max(px1, px2, xv) + 5
                    rng = np.linspace(lo, hi, 400)
                    ax.plot(rng, m*rng + bv, lw=2.2, color="#818cf8",
                            label=f"y = {m:.4g}x + {bv:.4g}")
                    ax.scatter([px1, px2], [py1, py2], s=100, color="#fbbf24",
                               zorder=5, label="Puntos dados")
                    ax.scatter([xv], [yv], s=120, color="#f87171", zorder=6,
                               label=f"({xv}, {yv:.4g})")
                    ax.legend(fontsize=8, facecolor="#111115", edgecolor="#1e1e28",
                              labelcolor="#8080a0")
                    st.pyplot(fig)
                    plt.close(fig)

    # ── 5. Función cuadrática ─────────────────────────────────────────────────
    elif idx == 4:
        st.markdown('<p class="section-lbl">Coeficientes</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        a = c1.number_input("a  (x²)", key="q_a", format="%.6g", help="No puede ser 0")
        b = c2.number_input("b  (x)",  key="q_b", format="%.6g")
        c = c3.number_input("c  (independiente)", key="q_c", format="%.6g")

        if st.button("CALCULAR", type="primary", use_container_width=True, key="calc5"):
            if a == 0:
                st.markdown(error_card("El coeficiente <b>a</b> no puede ser 0."),
                            unsafe_allow_html=True)
            else:
                xv   = -b / (2*a)
                yv   = a*xv**2 + b*xv + c
                disc = b**2 - 4*a*c
                tipo = "Mínimo" if a > 0 else "Máximo"

                st.markdown(result_card(
                    f"Vértice  ({tipo})",
                    f"V = ({xv:.6g} ,  {yv:.6g})",
                    note=f"Eje de simetría: x = {xv:.4g}  |  Abre {'arriba ↑' if a > 0 else 'abajo ↓'}"
                ), unsafe_allow_html=True)

                if disc > 0:
                    r1 = (-b + math.sqrt(disc)) / (2*a)
                    r2 = (-b - math.sqrt(disc)) / (2*a)
                    st.markdown(result_card(
                        "Raíces reales  (Δ > 0)",
                        f"x₁ = {r1:.6g}<br>x₂ = {r2:.6g}",
                        note=f"Δ = {disc:.4g}  |  Separación: {abs(r1-r2):.4g}"
                    ), unsafe_allow_html=True)
                elif disc == 0:
                    r = -b / (2*a)
                    st.markdown(result_card("Raíz doble  (Δ = 0)", f"x = {r:.6g}",
                                            note="Tangente al eje x."), unsafe_allow_html=True)
                else:
                    st.markdown(result_card("Sin raíces reales  (Δ < 0)", "∅",
                                            note=f"Δ = {disc:.4g} < 0"),
                                unsafe_allow_html=True)

                fig, ax = styled_fig("Función cuadrática")
                rng = np.linspace(xv - 10, xv + 10, 500)
                y   = a*rng**2 + b*rng + c
                ax.plot(rng, y, lw=2.2, color="#818cf8",
                        label=f"y = {a}x² + {b}x + {c}")
                ax.scatter([xv], [yv], s=130, color="#34d399", zorder=6,
                           label=f"Vértice ({xv:.3g}, {yv:.3g})")
                if disc > 0:
                    r1 = (-b + math.sqrt(disc)) / (2*a)
                    r2 = (-b - math.sqrt(disc)) / (2*a)
                    ax.scatter([r1, r2], [0, 0], s=100, color="#f87171", zorder=6,
                               label=f"Raíces: {r1:.3g}, {r2:.3g}")
                elif disc == 0:
                    r = -b / (2*a)
                    ax.scatter([r], [0], s=100, color="#f87171", zorder=6,
                               label=f"Raíz doble: {r:.3g}")
                ax.legend(fontsize=8, facecolor="#111115", edgecolor="#1e1e28",
                          labelcolor="#8080a0")
                st.pyplot(fig)
                plt.close(fig)

# ── Espacio inferior dentro del cuerpo ────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
