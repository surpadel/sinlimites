# Sin Límites · Medios de Instagram

Repositorio de trabajo del Instagram de [@sinlimitesterapias](https://www.instagram.com/sinlimitesterapias/) (Sin Límites · Espacio Interdisciplinario, Berazategui).

- `medios/banco/` tomas de video y fondos reutilizables (acuarela pastel, sin personas).
- `medios/voces/` locuciones.
- `reels/AAAA-MM-nombre/` cada reel: script de montaje y MP4 final.
- `medios/pedidos.json` lista de archivos a bajar: el proceso **Bajar medios** (GitHub Actions) los descarga a `medios/` al hacer push.

Los MP4 finales se publican desde su URL pública de `raw.githubusercontent.com`.

## Marca
`medios/marca/`: logo de Sin Límites (SVG y PNG transparente de ~2500 px).
- `sin-limites-logo-acuarela` (principal): letras negras vectorizadas desde el logo de Instagram (`fuentes/logo-referencia-instagram.png`, script `trazar-logo-negro.py`), pincelada pastel generada con OpenAI desde el conector propio de Nico (`fuentes/pincelada-openai-3.png`) y piezas de rompecabezas sutiles. Se arma con `componer-logo-acuarela.py`.
- `-tinta` (letras negras) y `-blanco` (para fondos de color).
- Descartados: `-acuarela-trazos.svg` (saturado) y las pinceladas `-1` (pálida) y `-2` (demasiado prolija).
