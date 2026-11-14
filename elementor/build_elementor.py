#!/usr/bin/env python3
"""
Genera la plantilla de Elementor (JSON importable) de la landing de ICPI.

Usa solo widgets nativos de Elementor (Encabezado, Editor de texto, Botón,
Imagen, Lista de iconos, Caja de icono) sobre secciones y columnas, que
funcionan en todas las versiones 3.x. Las funciones de Elementor Pro que usa
son: Menú de navegación, Sticky (barra fija) y CSS personalizado de la página.

Uso:
    python3 build_elementor.py
    python3 build_elementor.py --base-url https://TU-SITIO.com/wp-content/uploads/2026/11
    python3 build_elementor.py --menu-slug mi-menu

--base-url es la carpeta donde están las imágenes (los nombres de archivo
deben ser los de la carpeta "imagenes").
"""
import argparse
import hashlib
import json
from pathlib import Path

# Las imágenes se sirven desde este commit fijo del repositorio (público).
# Al importar la plantilla, Elementor las descarga a la Biblioteca de medios.
DEFAULT_BASE = (
    "https://raw.githubusercontent.com/jersonfuentes/Ejercicios-JavaScript/"
    "c3341ce1f71fc6a1e5c4d15e55ad47b6e7371b64/elementor/imagenes"
)

# ---------------------------------------------------------------- colores ---
NAVY = "#25377e"   # azul marino del logo
SKY = "#9cb0db"    # celeste del logo
INK = "#131d47"    # marino muy oscuro
SAND = "#f4f6fb"   # fondo de página
PAPER = "#ffffff"
LINE = "#dde3f1"
MUTED = "#51607f"
FOOT = "#0c1330"
CHIP = "#e7ecf8"
SERIF = "Fraunces"
SANS = "Inter"

MAIL = ("mailto:saludmentalenlaiglesia@gmail.com?subject=Quiero%20recibir%20"
        "informaci%C3%B3n%20de%20la%20pr%C3%B3xima%20edici%C3%B3n")
IG = "https://www.instagram.com/icpi.consejeria/"

_counter = [0]


def nid():
    """ID de 7 caracteres hexadecimales, único y determinista."""
    _counter[0] += 1
    return hashlib.md5(f"icpi-{_counter[0]}".encode()).hexdigest()[:7]


# --------------------------------------------------------------- utilidades --
def sz(v, unit="px"):
    return {"unit": unit, "size": v, "sizes": []}


def box(t=0, r=0, b=0, l=0, unit="px"):
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b),
            "left": str(l), "isLinked": t == r == b == l}


def link(url="", external=False):
    return {"url": url, "is_external": "on" if external else "",
            "nofollow": "", "custom_attributes": ""}


def typo(prefix="typography", family=None, size=None, size_t=None, size_m=None,
         weight=None, lh=None, ls=None, transform=None, italic=False):
    d = {f"{prefix}_typography": "custom"}
    if family:
        d[f"{prefix}_font_family"] = family
    if size is not None:
        d[f"{prefix}_font_size"] = sz(size)
    if size_t is not None:
        d[f"{prefix}_font_size_tablet"] = sz(size_t)
    if size_m is not None:
        d[f"{prefix}_font_size_mobile"] = sz(size_m)
    if weight:
        d[f"{prefix}_font_weight"] = str(weight)
    if lh:
        d[f"{prefix}_line_height"] = sz(lh, "em")
    if ls is not None:
        d[f"{prefix}_letter_spacing"] = sz(ls)
    if transform:
        d[f"{prefix}_text_transform"] = transform
    if italic:
        d[f"{prefix}_font_style"] = "italic"
    return d


def spacing(mt=0, mb=0, mr=0, ml=0):
    return {"_margin": box(mt, mr, mb, ml)}


def widget(wtype, settings):
    return {"id": nid(), "elType": "widget", "settings": settings,
            "elements": [], "widgetType": wtype}


# ------------------------------------------------------------------ widgets --
def heading(text, tag="h2", color=INK, align="left", family=SERIF, size=40,
            size_t=None, size_m=None, weight=600, lh=1.15, ls=None,
            transform=None, italic=False, mt=0, mb=16, align_m=None):
    s = {"title": text, "header_size": tag, "align": align,
         "title_color": color,
         **typo("typography", family, size, size_t, size_m, weight, lh, ls,
                transform, italic), **spacing(mt, mb)}
    if align_m:
        s["align_mobile"] = align_m
    return widget("heading", s)


def kicker(text, color=NAVY, align="left", mb=12):
    return heading(text, "div", color, align, SANS, 13, weight=600, lh=1.3,
                   ls=2.2, transform="uppercase", mb=mb)


def pill(text, bg, color, size=12, transform="uppercase", ls=1.2, weight=600,
         border=None, mr=8, mb=8, pad=(6, 14)):
    """Etiqueta redondeada en línea (chip / insignia)."""
    s = {"title": text, "header_size": "div", "title_color": color,
         **typo("typography", SANS, size, weight=weight, lh=1.3, ls=ls,
                transform=transform),
         "_element_width": "auto", **spacing(0, mb, mr, 0),
         "_background_background": "classic", "_background_color": bg,
         "_padding": box(pad[0], pad[1], pad[0], pad[1]),
         "_border_radius": box(999, 999, 999, 999)}
    if border:
        s.update({"_border_border": "solid", "_border_width": box(1, 1, 1, 1),
                  "_border_color": border})
    return widget("heading", s)


def text(html, color=MUTED, size=17, size_m=None, lh=1.65, family=SANS,
         weight=None, align="left", mb=16, mt=0, align_m=None):
    s = {"editor": html, "text_color": color, "align": align,
         **typo("typography", family, size, None, size_m, weight, lh),
         **spacing(mt, mb)}
    if align_m:
        s["align_mobile"] = align_m
    return widget("text-editor", s)


def button(label, url, bg=None, color=INK, border=None, hover_bg=None,
           hover_color=None, size="md", align="left", fs=16,
           pad=(14, 28), auto=False, mr=0, mb=0, mt=0, external=False):
    s = {"text": label, "link": link(url, external), "align": align,
         "size": size, "button_text_color": color,
         "border_radius": box(999, 999, 999, 999),
         "text_padding": box(pad[0], pad[1], pad[0], pad[1]),
         **typo("typography", SANS, fs, weight=600, lh=1.2),
         **spacing(mt, mb, mr, 0)}
    if bg:
        s.update({"background_background": "classic", "background_color": bg})
    if border:
        s.update({"border_border": "solid", "border_width": box(2, 2, 2, 2),
                  "border_color": border, "button_hover_border_color": "#ffffff"})
    if hover_bg:
        s["button_background_hover_color"] = hover_bg
    if hover_color:
        s["hover_color"] = hover_color
    if auto:
        s["_element_width"] = "auto"
    return widget("button", s)


def image(url, alt="", width=None, width_t=None, width_m=None, height=None,
          align="left", radius=None, shadow=False, href=None, mb=0, circle=False):
    s = {"image": {"url": url, "id": "", "alt": alt}, "image_size": "full",
         "align": align, "link_to": "custom" if href else "none",
         "open_lightbox": "no", **spacing(0, mb)}
    if href:
        s["link"] = link(href)
    if width is not None:
        s["width"] = sz(width)
    if width_t is not None:
        s["width_tablet"] = sz(width_t)
    if width_m is not None:
        s["width_mobile"] = sz(width_m)
    if height is not None:
        s["height"] = sz(height)
        s["object-fit"] = "cover"
    if circle:
        s["image_border_radius"] = box(50, 50, 50, 50, "%")
    elif radius:
        s["image_border_radius"] = box(radius, radius, radius, radius)
    if shadow:
        s["image_box_shadow_box_shadow_type"] = "yes"
        s["image_box_shadow_box_shadow"] = {
            "horizontal": 0, "vertical": 18, "blur": 40, "spread": 0,
            "color": "rgba(19,29,71,0.22)"}
    return widget("image", s)


def icon_list(items, color=INK, bullet=SKY, size=16, gap=8, mb=18, mt=0):
    return widget("icon-list", {
        "icon_list": [{
            "text": t, "_id": nid(),
            "selected_icon": {"value": "fas fa-circle", "library": "fa-solid"},
            "link": link()} for t in items],
        "view": "traditional", "icon_color": bullet, "icon_size": sz(8),
        "text_color": color, "text_indent": sz(12),
        "space_between": sz(gap),
        **typo("icon_typography", SANS, size, weight=400, lh=1.5),
        **spacing(mt, mb)})


def iconbox(title, desc, title_color=INK, desc_color=MUTED, title_family=SERIF,
            title_size=17, title_weight=600, title_transform=None, title_ls=None,
            desc_family=SANS, desc_size=15, desc_weight=400, desc_lh=1.5,
            align="left", box_bg=None, box_border=None, radius=14,
            pad=(16, 18), mb=12, tb=4, divider_bottom=False, divider_color=LINE):
    s = {"selected_icon": {"value": "", "library": ""},
         "title_text": title, "description_text": desc,
         "title_size": "div", "position": "top", "text_align": align,
         "title_color": title_color, "description_color": desc_color,
         "title_bottom_space": sz(tb),
         **typo("title_typography", title_family, title_size, weight=title_weight,
                lh=1.3, ls=title_ls, transform=title_transform),
         **typo("description_typography", desc_family, desc_size,
                weight=desc_weight, lh=desc_lh),
         **spacing(0, mb)}
    if box_bg or box_border:
        s["_padding"] = box(pad[0], pad[1], pad[0], pad[1])
        s["_border_radius"] = box(radius, radius, radius, radius)
    if box_bg:
        s.update({"_background_background": "classic", "_background_color": box_bg})
    if box_border:
        s.update({"_border_border": "solid", "_border_width": box(1, 1, 1, 1),
                  "_border_color": box_border})
    if divider_bottom:
        s.update({"_border_border": "solid", "_border_width": box(0, 0, 1, 0),
                  "_border_color": divider_color,
                  "_padding": box(0, 0, 14, 0), "_margin": box(0, 0, 14, 0)})
    return widget("icon-box", s)


# ------------------------------------------------- columnas y secciones -----
def col(widgets, size=100, size_t=None, size_m=None, bg=None, border=None,
        radius=None, pad=None, pad_t=None, pad_m=None, shadow=None, valign=None,
        space_between=None, extra=None):
    s = {"_column_size": int(round(size)), "_inline_size": size}
    if size_t is not None:
        s["_inline_size_tablet"] = size_t
    s["_inline_size_mobile"] = size_m if size_m is not None else 100
    if bg:
        s.update({"background_background": "classic", "background_color": bg})
    if border:
        s.update({"border_border": "solid", "border_width": box(1, 1, 1, 1),
                  "border_color": border})
    if radius:
        s["border_radius"] = box(radius, radius, radius, radius)
    if pad:
        s["padding"] = box(*pad)
    if pad_t:
        s["padding_tablet"] = box(*pad_t)
    if pad_m:
        s["padding_mobile"] = box(*pad_m)
    if shadow:
        s["box_shadow_box_shadow_type"] = "yes"
        s["box_shadow_box_shadow"] = shadow
    if valign:
        s["content_position"] = valign
    if space_between is not None:
        s["space_between_widgets"] = space_between
    if extra:
        s.update(extra)
    return {"id": nid(), "elType": "column", "settings": s,
            "elements": widgets, "isInner": False}


def section(columns, anchor=None, bg=None, pad=(72, 20, 72, 20),
            pad_t=None, pad_m=None, width=1120, gap="no", middle=False,
            border_tb=None, extra=None, inner=False):
    s = {"layout": "boxed", "content_width": sz(width), "gap": gap,
         "padding": box(*pad)}
    if pad_t:
        s["padding_tablet"] = box(*pad_t)
    if pad_m:
        s["padding_mobile"] = box(*pad_m)
    if anchor:
        s["_element_id"] = anchor
    if bg:
        s.update({"background_background": "classic", "background_color": bg})
    if middle:
        s["column_position"] = "middle"
    if border_tb:
        s.update({"border_border": "solid", "border_width": box(1, 0, 1, 0),
                  "border_color": border_tb})
    if extra:
        s.update(extra)
    for c in columns:
        c["isInner"] = inner
    return {"id": nid(), "elType": "section", "settings": s,
            "elements": columns, "isInner": inner}


def head(k, title, para=None, k_color=NAVY, t_color=INK, p_color=MUTED,
         align="left", mb=0):
    ws = [kicker(k, k_color, align),
          heading(title, "h2", t_color, align, size=40, size_t=34, size_m=28,
                  mb=14 if para else mb)]
    if para:
        ws.append(text(f"<p>{para}</p>", p_color, 17, mb=mb, align=align))
    return ws


# ---------------------------------------------------------------- contenido --
def build(base, menu_slug):
    img = lambda f: f"{base.rstrip('/')}/{f}"
    LOGO, LOGO_W = img("icpi-logo.png"), img("icpi-logo-blanco.png")
    HERO, AMANECER, HERBERT = (img("icpi-hero.jpg"), img("icpi-amanecer.jpg"),
                               img("icpi-herbert-grenett.jpg"))
    ALT_LOGO = "ICPI – Instituto de Consejería Pastoral Integral"
    S = []

    # ---- 0. Barra de aviso -------------------------------------------------
    S.append(section([col([text(
        '<p>Nuevas fechas de cursos online en preparación. '
        f'<a href="#eventos" style="color:{SKY};font-weight:600">'
        'Ver próximos eventos →</a></p>',
        "#ffffff", 14, lh=1.4, align="center", mb=0)])],
        bg=NAVY, pad=(9, 20, 9, 20), pad_t=(9, 20, 9, 20), pad_m=(9, 16, 9, 16)))

    # ---- 1. Cabecera fija (Pro: Sticky + Menú de navegación) ---------------
    nav = widget("nav-menu", {
        "layout": "horizontal", "menu": menu_slug, "align_items": "end",
        "pointer": "underline", "animation_line": "fade",
        "dropdown": "tablet", "toggle": "burger", "toggle_align": "center",
        "full_width": "stretch", "toggle_color": NAVY,
        "color_menu_item": INK, "color_menu_item_hover": NAVY,
        "color_menu_item_active": NAVY,
        "pointer_color_menu_item_hover": SKY,
        "pointer_color_menu_item_active": NAVY,
        "padding_horizontal_menu_item": sz(11),
        "padding_vertical_menu_item": sz(8),
        **typo("menu_typography", SANS, 15, weight=500),
        "color_dropdown_item": INK, "background_color_dropdown_item": PAPER,
        "color_dropdown_item_hover": NAVY,
        "background_color_dropdown_item_hover": SAND,
    })
    S.append(section([
        col([image(LOGO, ALT_LOGO, 205, 185, 150, href="#inicio")],
            24, 30, 50, valign="center"),
        col([nav], 54, 30, 16, valign="center"),
        col([button("Recibir aviso", "#inscripcion", NAVY, "#ffffff", size="sm",
                    align="right", fs=14.5, pad=(10, 20),
                    hover_bg="#3a4f9c")],
            22, 40, 34, valign="center"),
    ], bg=PAPER, pad=(10, 20, 10, 20), pad_m=(8, 12, 8, 12), middle=True,
        extra={"border_border": "solid", "border_width": box(0, 0, 1, 0),
               "border_color": LINE, "sticky": "top",
               "sticky_on": ["desktop", "tablet", "mobile"],
               "sticky_offset": 0, "sticky_effects_offset": 0,
               "sticky_anchor_link_offset": 70, "z_index": 1000}))

    # ---- 2. Portada ---------------------------------------------------------
    facts = [("Próxima edición", "Por anunciar"),
             ("Última edición", "Sábado 30 de mayo de 2026"),
             ("Modalidad", "Sincrónica, vía Zoom · 3 horas (horario de Chile)"),
             ("Valor última edición", "$20.000 CLP · Extranjeros: USD 25")]
    fact_widgets = [heading("Datos del curso", "div", MUTED, "left", SANS, 17,
                            weight=600, lh=1.3, mb=10)]
    for i, (k, v) in enumerate(facts):
        fact_widgets.append(iconbox(
            k, v, title_color=NAVY, desc_color=INK, title_family=SANS,
            title_size=11.5, title_weight=600, title_transform="uppercase",
            title_ls=1.6, desc_family=SANS, desc_size=18, desc_weight=500,
            desc_lh=1.35, tb=4, divider_bottom=(i < len(facts) - 1), mb=0))
    hero_left = col([
        heading("Curso taller · Online en vivo", "div", SKY, "left", SANS, 13,
                weight=600, lh=1.3, ls=2.2, transform="uppercase", mb=18),
        heading('La salud mental del líder: <em><span style="color:' + SKY +
                '">piedra angular</span></em> para el ministerio efectivo',
                "h1", "#ffffff", "left", SERIF, 58, 44, 34, 600, 1.12, mb=22),
        text("<p>Aprende a reconocer, valorar y cultivar tu salud mental y "
             "espiritual como fundamento de un ministerio efectivo, sustentable "
             "y fiel al llamado de Dios.</p>", "#e4e9f6", 18, 16.5, 1.65, mb=30),
        button("Quiero recibir el aviso", "#inscripcion", SKY, INK, size="lg",
               fs=17, pad=(16, 32), auto=True, mr=12, mb=12, hover_bg="#c3d0ec"),
        button("Ver qué aprenderás", "#aprenderas", None, "#ffffff",
               border="rgba(255,255,255,0.4)", size="lg", fs=17, pad=(14, 30),
               auto=True, mb=12),
        text('<p>Imparte: <strong style="color:#ffffff">Mg. Herbert Grenett '
             'Ortiz</strong> · pastor y psicólogo clínico · director de ICPI</p>',
             "#c6cfe6", 15, lh=1.5, mt=14, mb=0),
    ], 62, 100, pad=(0, 32, 0, 0), pad_m=(0, 0, 0, 0))
    hero_right = col(fact_widgets, 38, 100, bg=PAPER, radius=18,
                     pad=(26, 24, 26, 24), valign="center",
                     shadow={"horizontal": 0, "vertical": 24, "blur": 60,
                             "spread": 0, "color": "rgba(0,0,0,0.28)"})
    S.append(section([hero_left, hero_right], anchor="inicio", bg=INK,
                     pad=(88, 20, 104, 20), pad_t=(64, 20, 72, 20),
                     pad_m=(48, 20, 56, 20), middle=True, extra={
        "background_background": "classic", "background_color": INK,
        "background_image": {"url": HERO, "id": ""},
        "background_position": "center center", "background_repeat": "no-repeat",
        "background_size": "cover",
        "background_overlay_background": "gradient",
        "background_overlay_color": "rgba(19,29,71,0.95)",
        "background_overlay_color_stop": sz(0, "%"),
        "background_overlay_color_b": "rgba(19,29,71,0.5)",
        "background_overlay_color_b_stop": sz(100, "%"),
        "background_overlay_gradient_type": "linear",
        "background_overlay_gradient_angle": sz(100, "deg"),
        "background_overlay_opacity": sz(1)}))

    # ---- 3. Próximos eventos -----------------------------------------------
    S.append(section([col(head(
        "Próximos eventos", "Nuevas fechas en preparación",
        "Formamos en consejería pastoral integral con cursos online en vivo. "
        "Cuando abramos las próximas inscripciones, te avisaremos primero.",
        mb=0), 72, 100)],
        anchor="eventos", bg=PAPER, pad=(72, 20, 0, 20), pad_m=(48, 20, 0, 20),
        extra={"border_border": "solid", "border_width": box(1, 0, 0, 0),
               "border_color": LINE}))
    soon = col([
        pill("Próximamente", SKY, INK, mb=14),
        heading("Próxima edición por anunciar", "h3", "#ffffff", size=26, mb=10),
        text("<p>Escríbenos y te avisamos apenas haya fecha.</p>", "#dbe3f5", 17, mb=14),
        icon_list(["Sábados por la mañana (horario de Chile)",
                   "Online en vivo, vía Zoom",
                   "Valor de las últimas ediciones: $20.000 CLP · Extranjeros: USD 25"],
                  color="#ffffff", mb=22),
        button("Recibir aviso por correo", MAIL, SKY, INK, hover_bg="#c3d0ec"),
    ], 50, 100, bg=NAVY, radius=18, pad=(30, 26, 30, 26), space_between=0)
    last = col([
        pill("Último curso realizado", CHIP, NAVY, mb=14),
        heading("Crecer con Autismo", "h3", INK, size=26, mb=6),
        text("<p>Desafíos y apoyos en las distintas etapas de la vida</p>", MUTED,
             18, family=SERIF, lh=1.4, mb=12),
        text("<p>Una mirada integral al autismo, recorriendo las distintas "
             "etapas de la vida y los apoyos que favorecen el desarrollo, el "
             "bienestar y la inclusión.</p>", INK, 16.5, mb=14),
        icon_list(["Sábado 17 de octubre de 2026",
                   "09:30 a 12:30 hrs (horario de Chile) · vía Zoom",
                   "$20.000 CLP · Extranjeros: USD 25"], mb=20),
        text(f'<p><a href="{IG}p/DdPam0oB9zR/" target="_blank" rel="noopener" '
             f'style="color:{NAVY};font-weight:600;border-bottom:2px solid {SKY};'
             'text-decoration:none">Ver la publicación en Instagram →</a></p>',
             NAVY, 16, mb=0),
    ], 50, 100, bg=PAPER, border=LINE, radius=18, pad=(30, 26, 30, 26),
        space_between=0)
    S.append(section([soon, last], bg=PAPER, pad=(32, 20, 72, 20),
                     pad_m=(24, 20, 48, 20), width=1140, gap="default"))

    # ---- 4. Qué aprenderás ---------------------------------------------------
    S.append(section([col(head(
        "Qué aprenderás", "Un ministerio sano comienza en un líder sano",
        "Integramos perspectivas bíblicas, psicológicas y espirituales para que "
        "identifiques dinámicas disfuncionales internas, las prevengas y las "
        "reemplaces por prácticas de bienestar integral.", mb=0), 72, 100)],
        anchor="aprenderas", bg=SAND, pad=(72, 20, 32, 20), pad_m=(48, 20, 24, 20)))
    S.append(section([col([
        kicker("Objetivo general", SKY, mb=10),
        heading("Capacitar a líderes de iglesias para que aprendan a reconocer, "
                "valorar y cultivar su salud mental y espiritual como fundamento "
                "indispensable de un ministerio efectivo, sustentable y fiel al "
                "llamado de Dios.", "div", "#ffffff", "left", SERIF, 24, 21, 19,
                500, 1.5, mb=0),
    ], 100, bg=NAVY, radius=18, pad=(32, 28, 32, 28), space_between=0)],
        bg=SAND, pad=(0, 20, 18, 20), pad_m=(0, 20, 14, 20), width=1120))

    def obj(num, title, body, dark=False, size=33.333):
        c_num = SKY if dark else NAVY
        c_title = "#ffffff" if dark else INK
        c_body = "#d3dbef" if dark else MUTED
        return col([
            heading(num, "div", c_num, "left", SERIF, 38, weight=600, lh=1, mb=14),
            heading(title, "h3", c_title, "left", SERIF, 20, weight=600, lh=1.3, mb=10),
            text(f"<p>{body}</p>", c_body, 15.5, lh=1.6, mb=0),
        ], size, 50, bg=INK if dark else PAPER,
            border=INK if dark else LINE, radius=18, pad=(26, 24, 26, 24),
            space_between=0)

    S.append(section([
        obj("01", "Reconoce un liderazgo emocionalmente enfermo",
            "Identifica los síntomas y patrones de un liderazgo emocionalmente "
            "enfermo, contrástalos con un modelo saludable y asume una postura "
            "honesta frente a tu propia realidad interior."),
        obj("02", "Sacrificio genuino vs. agotamiento",
            "Comprende la diferencia entre sacrificio genuino y agotamiento "
            "autodestructivo, los factores personales y culturales que llevan al "
            "burnout ministerial y los principios bíblicos de un servicio "
            "apasionado y sostenible."),
        obj("03", "Las toxinas del alma",
            "Identifica las principales toxinas que deterioran la salud mental "
            "del líder y reflexiona sobre cuáles de ellas están operando en tu "
            "propia experiencia ministerial."),
    ], bg=SAND, pad=(0, 20, 0, 20), width=1140, gap="default"))
    S.append(section([
        obj("04", "Reabastecimiento espiritual",
            "Descubre y asume prácticas concretas para liderar desde un alma "
            "plena, y no desde el vacío, la obligación o el agotamiento."),
        obj("05", "Te llevas tu propio plan de cuidado del alma",
            "Elabora una propuesta personal: identifica al menos tres áreas de "
            "mejora en tu salud mental y espiritual y define pasos concretos, "
            "sostenibles y bíblicamente fundamentados para el período inmediato.",
            dark=True, size=66.667),
    ], bg=SAND, pad=(0, 20, 72, 20), pad_m=(0, 20, 48, 20), width=1140, gap="default"))

    # ---- 5. Banda con foto y frase ------------------------------------------
    S.append(section([col([
        kicker("Reabastecimiento espiritual", SKY, "center", mb=14),
        heading('Liderar desde un <em><span style="color:' + SKY +
                '">alma plena</span></em>, y no desde el vacío, la obligación o '
                'el agotamiento.', "h2", "#ffffff", "center", SERIF, 44, 36, 28,
                500, 1.3, mb=0),
    ], 100)], bg=NAVY, width=900, pad=(104, 20, 104, 20), pad_t=(80, 20, 80, 20),
        pad_m=(64, 20, 64, 20), extra={
        "background_background": "classic", "background_color": NAVY,
        "background_image": {"url": AMANECER, "id": ""},
        "background_position": "center center", "background_repeat": "no-repeat",
        "background_size": "cover",
        "background_overlay_background": "classic",
        "background_overlay_color": "rgba(12,19,51,0.68)",
        "background_overlay_opacity": sz(1)}))

    # ---- 6. Para quién -----------------------------------------------------
    chips_w = [pill(t, PAPER, INK, size=15, transform=None, ls=0, weight=500,
                    border=LINE, mr=10, mb=10, pad=(10, 18)) for t in [
        "Pastores", "Ancianos", "Presbíteros", "Diáconos",
        "Maestros de escuela dominical", "Líderes de ministerios",
        "Docentes de instituto bíblico", "Profesionales cristianos"]]
    for w in chips_w:
        w["settings"]["_background_color"] = SAND
    S.append(section([col(head("Dirigido a", "Para quienes sirven en la iglesia",
                               mb=28) + chips_w + [
        heading("…y toda persona que esté llamada a servir en el Reino de Dios.",
                "div", INK, "left", SERIF, 21, weight=500, lh=1.4, mt=18, mb=0)],
        100)],
        anchor="para-quien", bg=PAPER, pad=(72, 20, 72, 20),
        pad_m=(48, 20, 48, 20), border_tb=LINE))

    # ---- 7. Fundador -------------------------------------------------------
    S.append(section([
        col([image(HERBERT, "Mg. Herbert Grenett Ortiz", 280, 280, 240,
                   radius=18, shadow=True)], 28, 100, 100, pad=(0, 0, 0, 0)),
        col([
            kicker("Fundador de ICPI", NAVY, mb=10),
            heading("Mg. Herbert Grenett Ortiz", "h2", INK, size=40, size_t=34,
                    size_m=28, mb=6),
            heading("Fundador y director del Instituto de Consejería Pastoral "
                    "Integral", "div", NAVY, "left", SANS, 17, weight=600, lh=1.4,
                    mb=18),
            heading("Pastor y psicólogo clínico, une en su trabajo el cuidado "
                    "pastoral con la práctica clínica.", "div", INK, "left", SERIF,
                    22, weight=500, lh=1.4, mb=14),
            text("<p>ICPI ofrece formación en consejería pastoral integral que une "
                 "fe y salud mental, en modalidad online.</p>", MUTED, 16.5, mb=20),
            icon_list([
                "Ministro ordenado de Las Asambleas de Dios de Chile.",
                "Pastorea junto a su esposa Carolina la Iglesia Luz de Esperanza "
                "para la Familia, en Quilpué, Chile.",
                "Docente en institutos bíblicos interdenominacionales.",
                "Finalizando una maestría en teología práctica en la Facultad de "
                "Teología de Las Asambleas de Dios de América Latina y el Caribe."],
                mb=0),
        ], 72, 100, pad=(0, 0, 0, 44), pad_t=(24, 0, 0, 0), pad_m=(24, 0, 0, 0)),
    ], anchor="fundador", bg=SAND, pad=(72, 20, 72, 20), pad_m=(48, 20, 48, 20)))

    # ---- 8. Expositor y formación -------------------------------------------
    def group(title, items):
        return col([heading(title, "h4", NAVY, "left", SANS, 12.5, weight=600,
                            lh=1.3, ls=1.5, transform="uppercase", mb=12)] + [
            iconbox(t, d, box_bg=SAND, box_border=LINE) for t, d in items],
            33.333, 100, space_between=0)

    S.append(section([col([
        kicker("Sobre el expositor", NAVY, mb=14),
        # fila avatar + nombre: sección interna
        section([
            col([image(HERBERT, "", 76, 76, 64, 76, circle=True)], 10, 15, 22,
                valign="center"),
            col([heading("Mg. Herbert Grenett Ortiz", "h2", INK, size=32, size_t=28,
                         size_m=24, mb=4),
                 heading("Expositor de este curso taller", "div", NAVY, "left", SANS,
                         16, weight=600, lh=1.4, mb=0)], 90, 85, 78, valign="center"),
        ], pad=(0, 0, 0, 0), width=1120, inner=True, middle=True),
        icon_list(
            ["Psicólogo clínico acreditado, con máster en terapias psicológicas de "
             "tercera generación.",
             "Entrenamientos clínicos centrados en adicciones, depresión, ansiedad, "
             "trauma y TOC.",
             "Docente de pregrado y posgrado en la formación de psicólogos "
             "clínicos, a nivel nacional e internacional."], mt=22, mb=8),
        heading("Formación y acreditaciones", "h3", INK, size=22, mt=36, mb=0),
    ], 100)], anchor="expositor", bg=PAPER, pad=(72, 20, 8, 20),
        pad_m=(48, 20, 8, 20), border_tb=LINE,
        extra={"border_width": box(1, 0, 0, 0)}))
    S.append(section([
        group("Base clínica y acreditación", [
            ("Licenciado en Psicología", "Universidad del Mar, Valparaíso (2005)"),
            ("Especialista en Psicoterapia acreditado",
             "CONAPC: Sociedad Chilena de Psicología Clínica y Colegio de "
             "Psicólogos de Chile (2015)"),
            ("Máster en Terapias de Tercera Generación",
             "ISEB · Universidad Isabel I de Castilla (2023–2024)")]),
        group("Terapias cognitivo-conductuales", [
            ("Terapia Cognitivo-Conductual",
             "Postítulo de especialización y acreditación clínica, Instituto del "
             "Comportamiento (2012–2014)"),
            ("Terapia Conductual Dialéctica (DBT)",
             "Entrenamiento con DBT Latinoamérica y Linehan Institute Behavioral "
             "Tech (2016–2017)"),
            ("Terapia de Aceptación y Compromiso (ACT)",
             "Diplomado en curso, ITECOC México (2025 a la fecha)")]),
        group("Áreas de especialización", [
            ("TOC y espectro obsesivo-compulsivo",
             "Diplomado, TOC Argentina (2022) · Entrenamiento clínico BTTI, "
             "International OCD Foundation (2024)"),
            ("Adicciones",
             "Diplomados en prevención, tratamiento y rehabilitación, Facultad de "
             "Medicina, Universidad de Santiago (2005 y 2008)"),
            ("Trauma",
             "Entrenamiento en Terapia de Exposición Prolongada (2021) y en "
             "Terapia de Exposición Narrativa (2023)"),
            ("Depresión y ansiedad",
             "Actualización en Activación Conductual y TCC de la depresión (2020) "
             "y en trastornos de ansiedad (2014)")]),
    ], bg=PAPER, pad=(0, 20, 72, 20), pad_m=(0, 20, 48, 20), width=1140,
        gap="default"))

    # ---- 9. Cursos dictados ------------------------------------------------
    def course(tag, title, sub, desc, fecha, lnk=None):
        ws = [heading(tag, "div", NAVY, "left", SANS, 11.5, weight=600, lh=1.3,
                      ls=1.5, transform="uppercase", mb=8),
              heading(title, "h3", INK, "left", SERIF, 20, weight=600, lh=1.3,
                      mb=8)]
        if sub:
            ws.append(text(f"<p>{sub}</p>", MUTED, 16, family=SERIF, lh=1.4, mb=8))
        if desc:
            ws.append(text(f"<p>{desc}</p>", MUTED, 15, lh=1.55, mb=10))
        if lnk:
            ws.append(text(
                f'<p><a href="{lnk[0]}"' + (' target="_blank" rel="noopener"'
                                           if lnk[0].startswith("http") else "") +
                f' style="color:{NAVY};font-weight:600;border-bottom:2px solid '
                f'{SKY};text-decoration:none">{lnk[1]}</a></p>',
                NAVY, 15, mb=12))
        ws.append(text(f"<p>{fecha}</p>", INK, 14.5, weight=500, mb=8, mt=6))
        ws.append(pill("Realizado", CHIP, NAVY, size=11.5, mb=0, pad=(5, 12)))
        return col(ws, 33.333, 50, bg=PAPER, border=LINE, radius=18,
                   pad=(24, 22, 24, 22), space_between=0)

    c = [
        course("Autismo e inclusión", "Crecer con Autismo",
               "Desafíos y apoyos en las distintas etapas de la vida",
               "Una mirada integral al autismo y a los apoyos que favorecen el "
               "desarrollo, el bienestar y la inclusión.",
               "Sábado 17 de octubre de 2026",
               (f"{IG}p/DdPam0oB9zR/", "Ver en Instagram →")),
        course("Familia y matrimonio", "Renovando Nuestro Amor",
               "Herramientas prácticas para fortalecer el matrimonio",
               "Principios cristianos y herramientas para fortalecer la "
               "comunicación, resolver conflictos con sabiduría y cultivar el "
               "perdón.", "Sábado 1 de agosto de 2026",
               (f"{IG}p/DbMN4c4Fb5T/", "Ver en Instagram →")),
        course("Liderazgo cristiano", "La Salud Mental del Líder",
               "Piedra angular para un liderazgo efectivo",
               "Para líderes de iglesias que desean cuidar su salud mental y "
               "espiritual como base de un ministerio efectivo y sustentable.",
               "Sábado 30 de mayo de 2026", ("#aprenderas", "Ver el temario →")),
        course("Familia y crianza", "Cómo acompañar HOY a los padres en la crianza",
               "", "", "Sábado 28 de marzo de 2026"),
        course("Duelo y consuelo", "Consejería Pastoral Integral del Duelo",
               "", "", "Sábado 22 de noviembre de 2025"),
        course("Prevención del suicidio",
               "Intervención Pastoral en la Prevención del Suicidio",
               "", "", "Edición anterior"),
    ]
    S.append(section([col(head(
        "Cursos que ya hemos dictado", "Fe y salud mental, curso a curso",
        "Formación en consejería pastoral integral, en modalidad online. Estos "
        "son los cursos de las últimas ediciones.", mb=0), 72, 100)],
        anchor="cursos", bg=SAND, pad=(72, 20, 32, 20), pad_m=(48, 20, 24, 20)))
    S.append(section(c[:3], bg=SAND, pad=(0, 20, 0, 20), width=1140, gap="default"))
    for cc in c[3:]:
        cc["settings"]["_inline_size_tablet"] = 50
    S.append(section(c[3:], bg=SAND, pad=(20, 20, 0, 20), width=1140, gap="default"))

    temas = ["Consejería pastoral integral", "Duelo y consuelo",
             "Fe y salud mental en la iglesia", "Cómo acompañar al que sufre",
             "Familia, matrimonio y crianza", "Liderazgo cristiano",
             "Prevención del suicidio", "Autismo e inclusión"]
    S.append(section([col(
        [heading("Temas que trabajamos", "h3", INK, size=22, mt=34, mb=16)] +
        [pill(t, PAPER, INK, size=15, transform=None, ls=0, weight=500,
              border=LINE, mr=10, mb=10, pad=(10, 18)) for t in temas] +
        [heading("Equipo docente de ICPI", "h3", INK, size=22, mt=28, mb=4)],
        100)], bg=SAND, pad=(0, 20, 0, 20)))
    team = [("Herbert Grenett O.", "Director · pastor y psicólogo clínico"),
            ("Jorge Sobarzo B.", "Médico psiquiatra infanto-juvenil"),
            ("Vladimir Rodríguez", "Psicólogo")]
    S.append(section([col([iconbox(n, r, box_bg=PAPER, box_border=LINE, title_size=17,
                                   desc_size=14.7, mb=0)],
                          33.333, 100, space_between=0) for n, r in team],
                     bg=SAND, pad=(10, 20, 72, 20), pad_m=(10, 20, 48, 20),
                     width=1140, gap="default"))

    # ---- 10. Próxima edición / aviso ----------------------------------------
    def price(label, amount):
        return col([iconbox(label, amount, title_color=SKY, desc_color="#ffffff",
                            title_family=SANS, title_size=11.5, title_weight=600,
                            title_transform="uppercase", title_ls=1.5,
                            desc_family=SERIF, desc_size=32, desc_weight=600,
                            desc_lh=1.2, align="center", tb=6, mb=0)],
                   50, 100, bg="rgba(255,255,255,0.05)", border="rgba(255,255,255,0.18)",
                   radius=18, pad=(22, 16, 22, 16), space_between=0)

    S.append(section([col([
        kicker("Próxima edición", SKY, "center", mb=12),
        heading("Sé de los primeros en enterarte de la próxima fecha", "h2",
                "#ffffff", "center", SERIF, 44, 36, 28, 600, 1.15, mb=16),
        text("<p>Escríbenos y te avisamos cuando abramos inscripciones. Formato "
             "habitual: sábados por la mañana, online en vivo por Zoom.</p>",
             "#d3dbef", 17, align="center", mb=26),
        section([price("Valor última edición · Chile", "$20.000 CLP"),
                 price("Valor última edición · Extranjeros", "USD 25")],
                pad=(0, 0, 0, 0), width=640, gap="default", inner=True),
        button("Recibir aviso por correo", MAIL, SKY, INK, size="lg", align="center",
               fs=17, pad=(16, 34), hover_bg="#c3d0ec", mt=28, mb=18),
        text(f'<p>Escríbenos a <a href="mailto:saludmentalenlaiglesia@gmail.com" '
             f'style="color:{SKY}">saludmentalenlaiglesia@gmail.com</a> o por '
             f'Instagram a <a href="{IG}" target="_blank" rel="noopener" '
             f'style="color:{SKY}">@icpi.consejeria</a>.</p>',
             "#b9c4e2", 15, align="center", mb=0),
    ], 100)], anchor="inscripcion", bg=INK, width=800, pad=(80, 20, 80, 20),
        pad_m=(56, 20, 56, 20), extra={
        "background_background": "gradient", "background_color": INK,
        "background_color_stop": sz(0, "%"), "background_color_b": "#1d2a67",
        "background_color_b_stop": sz(100, "%"),
        "background_gradient_type": "linear",
        "background_gradient_angle": sz(160, "deg")}))

    # ---- 11. Pie -------------------------------------------------------------
    S.append(section([
        col([image(LOGO_W, ALT_LOGO, 200, 190, 170, mb=14),
             heading("Bendiciones para tu vida, familia y ministerio.", "div",
                     "#ffffff", "left", SERIF, 19, weight=500, lh=1.4, mb=0)],
            60, 100),
        col([text(f'<p style="text-align:right"><a href="mailto:saludmentalenlaiglesia'
                  f'@gmail.com" style="color:{SKY}">saludmentalenlaiglesia@gmail.com'
                  f'</a><br><a href="{IG}" target="_blank" rel="noopener" '
                  f'style="color:{SKY}">Síguenos en Instagram · @icpi.consejeria</a></p>',
                  "#b9c4e2", 15, lh=1.8, mb=0, mt=14)], 40, 100, valign="bottom"),
    ], bg=FOOT, pad=(44, 20, 44, 20), pad_m=(36, 20, 36, 20)))

    return S


PAGE_CSS = """/* Landing ICPI: ajustes mínimos que Elementor no trae como control */
html { scroll-behavior: smooth; }
.elementor-section[id] { scroll-margin-top: 84px; }
body, .elementor-widget-text-editor { -webkit-font-smoothing: antialiased; }
.elementor-widget-text-editor a { text-underline-offset: 3px; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default=DEFAULT_BASE,
                    help="carpeta donde están las imágenes (por defecto, el repositorio)")
    ap.add_argument("--menu-slug", default="landing-icpi",
                    help="slug del menú de WordPress para el widget Menú de navegación")
    ap.add_argument("--out", default=str(Path(__file__).with_name("icpi-landing-elementor.json")))
    a = ap.parse_args()

    template = {
        "version": "0.4",
        "title": "ICPI – Landing curso La salud mental del líder",
        "type": "page",
        "content": build(a.base_url, a.menu_slug),
        "page_settings": {
            "template": "elementor_canvas",
            "hide_title": "yes",
            "background_background": "classic",
            "background_color": SAND,
            "custom_css": PAGE_CSS,
        },
    }
    Path(a.out).write_text(json.dumps(template, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    print("Plantilla escrita en", a.out)


if __name__ == "__main__":
    main()
