# Sin Límites · Medios de Instagram

Repositorio de trabajo del Instagram de [@sinlimitesterapias](https://www.instagram.com/sinlimitesterapias/) (Sin Límites · Espacio Interdisciplinario, Berazategui).

- `medios/banco/` tomas de video y fondos reutilizables (acuarela pastel, sin personas).
- `medios/voces/` locuciones.
- `reels/AAAA-MM-nombre/` cada reel: script de montaje y MP4 final.
- `medios/pedidos.json` lista de archivos a bajar: el proceso **Bajar medios** (GitHub Actions) los descarga a `medios/` al hacer push.

Los MP4 finales se publican desde su URL pública de `raw.githubusercontent.com`.

## Marca
`medios/marca/`: logo de Sin Límites vectorizado desde el flyer (SVG y PNG transparente de 2400 px).
- `sin-limites-logo-acuarela.png` (principal): letras vectoriales sobre pincelada pastel generada con OpenAI (`fuentes/pincelada-openai-1.png`) y estrellitas; se arma con `componer-logo-acuarela.py`.
- `-tinta` (letras azul noche) y `-blanco` (para fondos de color), en SVG y PNG.
- `-acuarela-trazos.svg`: versión anterior con trazos dibujados por código (descartada por saturada).
- `trazar-logo.py` regenera el trazado.
