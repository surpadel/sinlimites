# Sin Límites · Medios de Instagram

Repositorio de trabajo del Instagram de [@sinlimitesterapias](https://www.instagram.com/sinlimitesterapias/) (Sin Límites · Espacio Interdisciplinario, Berazategui).

- `medios/banco/` tomas de video y fondos reutilizables (acuarela pastel, sin personas).
- `medios/voces/` locuciones.
- `reels/AAAA-MM-nombre/` cada reel: script de montaje y MP4 final.
- `medios/pedidos.json` lista de archivos a bajar: el proceso **Bajar medios** (GitHub Actions) los descarga a `medios/` al hacer push.

Los MP4 finales se publican desde su URL pública de `raw.githubusercontent.com`.

## Marca (logo oficial aprobado por Nico el 03/11/2026)
`medios/marca/`:
- `sin-limites-logo-acuarela.png` / `.svg` — **logo principal**: título negro "Sin Límites" vectorizado del logo de Instagram, subtítulo "Espacio Interdisciplinario" vectorizado del flyer, pincelada pastel texturada (OpenAI), 3 piezas de rompecabezas y estrellitas sutiles.
- `sin-limites-logo-tinta` (solo letras negras) y `sin-limites-logo-blanco` (para fondos de color), SVG y PNG.
- Para rearmarlo: `trazar-logo-negro.py` → `armar-letras.py` → `componer-logo-acuarela.py`. Fuentes en `fuentes/`.
