# CinemaTherapy · sito

> Il documento di progetto completo (Cine Twins, Cloudflare, dominio, cose aperte) è in [`cine-twins/PROGETTO.md`](https://github.com/giovannipecora/cine-twins/blob/main/PROGETTO.md).

Sito statico di CinemaTherapy Production in 5 lingue: italiano (`/`), inglese (`/en/`), francese (`/fr/`), tedesco (`/de/`), spagnolo (`/es/`).

## Modificare i testi

1. Cambia i testi in `content/i18n.json` (una sezione per lingua).
2. Rigenera le pagine: `python3 tools/build.py`
3. Fai commit di tutto, anche della cartella `public/`.

Lo stile è in `public/style.css`. Il dominio usato per canonical, hreflang e sitemap è in `tools/build.py` (`SITE`).

## Pubblicare su Cloudflare (Workers)

Il repository ha `wrangler.jsonc`: nella schermata «Set up your application» lascia Build command vuoto e Deploy command `npx wrangler deploy`. Poi Settings → Domains & Routes → aggiungi il dominio.

## In alternativa: Cloudflare Pages

Workers & Pages → Create → Pages → Connect to Git → `cinematherapy-site`:

- Production branch: `main`
- Framework preset: `None`
- Build command: *(vuoto)*
- Build output directory: `public`

Poi in **Custom domains** aggiungi `cinematherapy.it` (e `www.cinematherapy.it`).
A differenza del prototipo di Cine Twins, questo sito è indicizzabile: c'è `robots.txt` con la sitemap.
