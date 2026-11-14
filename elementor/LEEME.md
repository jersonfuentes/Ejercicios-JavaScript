# Landing ICPI para Elementor Pro

Paquete para publicar la landing del Instituto de Consejería Pastoral Integral (ICPI)
en WordPress con Elementor Pro, con todo editable desde el editor visual.

## Qué trae

| Archivo | Para qué sirve |
|---|---|
| `icpi-landing-elementor.json` | La página completa, lista para importar en Elementor |
| `imagenes/` | Las 6 imágenes (logo, logo en blanco, favicon, portada, amanecer y foto del fundador) |
| `build_elementor.py` | Generador de la plantilla (opcional, solo si necesitas cambiar rutas de imágenes) |

## Requisitos

- WordPress con **Elementor** y **Elementor Pro**.
- Elementor Pro se usa para tres cosas: el **Menú de navegación**, la **barra fija (Sticky)** y el **CSS personalizado** de la página.
- Todo lo demás son widgets nativos: Encabezado, Editor de texto, Botón, Imagen, Lista de iconos y Caja de icono.
- Está armada con **secciones y columnas**, que funcionan en todas las versiones 3.x de Elementor. Si tu sitio usa Contenedores, Elementor puede convertirlas (clic derecho sobre la sección → *Convertir a contenedor*).

## Instalación paso a paso

### 1. Crear el menú de la barra (2 minutos)

El menú de arriba es un widget de Elementor Pro que lee un menú de WordPress.

1. **Apariencia → Menús → Crear un nuevo menú**. Nómbralo exactamente **`Landing ICPI`** (su identificador queda `landing-icpi`).
2. En **Enlaces personalizados** agrega estos seis, uno por uno, con **Añadir al menú**:

   | Texto del enlace | URL |
   |---|---|
   | Próximos eventos | `#eventos` |
   | Qué aprenderás | `#aprenderas` |
   | Para quién | `#para-quien` |
   | Fundador | `#fundador` |
   | Expositor | `#expositor` |
   | Cursos dictados | `#cursos` |

3. **Guardar menú**. No hace falta asignarle una ubicación.

### 2. Importar la plantilla

1. **Elementor → Plantillas → Plantillas guardadas → Importar plantillas**.
2. Elige `icpi-landing-elementor.json` y pulsa **Importar ahora**.

La plantilla enlaza las imágenes a copias públicas. Al importar, Elementor las descarga y las guarda en tu **Biblioteca de medios**. Si alguna queda como imagen de relleno, mira la sección *Imágenes* más abajo.

### 3. Crear la página

1. **Páginas → Añadir nueva**, ponle título (por ejemplo "Curso La salud mental del líder").
2. **Editar con Elementor**.
3. Pulsa el icono de carpeta (**Añadir plantilla**) → pestaña **Mis plantillas** → **ICPI – Landing curso La salud mental del líder** → **Insertar**.
4. Si pregunta si aplicar los ajustes de página, responde **Sí**.
5. Abre **Ajustes de la página** (engranaje, abajo a la izquierda) y comprueba: **Diseño: Elementor Canvas** (sin cabecera ni pie del tema) y **Ocultar título: Sí**.
6. En el widget del menú (arriba, junto al logo), si no aparecen los enlaces, selecciona el menú **Landing ICPI** en su panel.
7. **Publicar**.

## Imágenes

La carpeta `imagenes/` trae los archivos con el prefijo `icpi-` para no chocar con otros de tu biblioteca.

| Archivo | Dónde se usa |
|---|---|
| `icpi-logo.png` | Logo de la cabecera |
| `icpi-logo-blanco.png` | Logo del pie de página (versión blanca) |
| `icpi-favicon.png` | Icono del sitio (se configura aparte, ver abajo) |
| `icpi-hero.jpg` | Fondo de la portada |
| `icpi-amanecer.jpg` | Fondo de la franja de la frase |
| `icpi-herbert-grenett.jpg` | Foto del fundador y avatar del expositor |

**Si prefieres subirlas tú:** *Medios → Añadir nuevo* y arrastra los 6 archivos. Después, en el editor, haz clic en cada imagen y elige la tuya desde la biblioteca.

**Cambio masivo de rutas sin tocar una por una:** si subiste las imágenes a `https://TU-SITIO.com/wp-content/uploads/AAAA/MM/`, usa **Elementor → Herramientas → Reemplazar URL**:

- *Antigua:* `https://raw.githubusercontent.com/jersonfuentes/Ejercicios-JavaScript/c3341ce1f71fc6a1e5c4d15e55ad47b6e7371b64/elementor/imagenes`
- *Nueva:* `https://TU-SITIO.com/wp-content/uploads/AAAA/MM`

**Favicon:** Elementor no lo importa desde la plantilla. Súbelo en *Apariencia → Personalizar → Identidad del sitio → Icono del sitio*.

## Qué editar y dónde

- **Nueva fecha de un curso:** en la portada, tarjeta **Datos del curso** (cuatro filas), y en la sección **Próximos eventos** (las dos tarjetas). También el texto de la **barra de aviso** de arriba.
- **Correo de inscripción:** los botones **Recibir aviso** llevan a `mailto:saludmentalenlaiglesia@gmail.com`. Se cambia en el campo *Enlace* de cada botón.
- **Si más adelante tienes un formulario o enlace de inscripción:** reemplaza ese enlace en los botones **Recibir aviso**, **Quiero recibir el aviso** y **Recibir aviso por correo**.
- **Cursos dictados:** son tarjetas independientes. Para añadir una, duplica una columna con clic derecho → *Duplicar*.
- **Textos de la barra de menú:** *Apariencia → Menús → Landing ICPI*.

## Colores de la marca

Azul marino `#25377e` y celeste `#9cb0db`, tomados del logo. Se pueden registrar en **Ajustes del sitio → Colores globales** para reutilizarlos en otras páginas.

Tonos derivados que usa la página: `#131d47` (marino oscuro), `#f4f6fb` (fondo), `#dde3f1` (bordes), `#51607f` (texto secundario).

## Tipografías

**Fraunces** (títulos) e **Inter** (textos), de Google Fonts. Elementor las carga solo. Si tu sitio tiene activada la opción de desactivar Google Fonts, reactívala en *Elementor → Ajustes → Avanzado*.

## Regenerar la plantilla (opcional)

Si necesitas apuntar a otras imágenes o a otro menú:

```bash
python3 build_elementor.py --base-url https://TU-SITIO.com/wp-content/uploads/AAAA/MM --menu-slug landing-icpi
```

Genera un nuevo `icpi-landing-elementor.json`.

## Si algo se ve distinto al diseño original

La página se construyó con los ajustes estándar de Elementor, pero cada sitio tiene un tema y un kit global distintos. Lo más habitual:

- **Espacios entre bloques:** se ajustan con el relleno de la sección o la columna.
- **Tamaño de letra:** viene fijado en cada widget. Si el tema impone otro, se corrige en el panel *Estilo → Tipografía* del widget.
- **Móvil y tablet:** revisa ambos desde el icono de dispositivos del editor (abajo, a la izquierda).
