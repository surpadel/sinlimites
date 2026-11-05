#!/bin/sh
# Regenera web/index.html (la publicada) a partir de web/d/index.html.
cd "$(dirname "$0")"
sed 's|\.\./img/|img/|g; s|content="img/compartir-lema.jpg"|content="https://sinlimitesterapias.com.ar/img/compartir-lema.jpg"|' d/index.html > index.html
sed -i 's|<meta property="og:type" content="website">|<meta property="og:type" content="website">\n<meta property="og:url" content="https://sinlimitesterapias.com.ar/">\n<link rel="canonical" href="https://sinlimitesterapias.com.ar/">|' index.html
