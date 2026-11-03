# Sin Límites · Medios de Instagram

Repositorio de trabajo del Instagram de [@sinlimitesterapias](https://www.instagram.com/sinlimitesterapias/) (Sin Límites · Espacio Interdisciplinario, Berazategui).

- `medios/banco/` tomas de video y fondos reutilizables (acuarela pastel, sin personas).
- `medios/voces/` locuciones.
- `reels/AAAA-MM-nombre/` cada reel: script de montaje y MP4 final.
- `medios/pedidos.json` lista de archivos a bajar: el proceso **Bajar medios** (GitHub Actions) los descarga a `medios/` al hacer push.

Los MP4 finales se publican desde su URL pública de `raw.githubusercontent.com`.

## Marca
`medios/marca/`: logo de Sin Límites vectorizado desde el flyer (SVG y PNG transparente de 2400 px).
- `sin-limites-logo-acuarela` (con la pincelada pastel), `-tinta` (letras azul noche), `-blanco` (para fondos de color).
- `trazar-logo.py` regenera el trazado.
