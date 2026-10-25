#!/usr/bin/env python3
"""Builds the static CinemaTherapy site into public/ — one page per language.

  python3 tools/build.py

Texts live in content/i18n.json (it, en, fr, de, es). Edit them there, run the script, commit public/.
Italian is the root (/), the others are /en/, /fr/, /de/, /es/. Each page links the others (hreflang)
so search engines show the right language.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://cinematherapy.it'  # change here if the domain is different
LANGS = ['it', 'en', 'fr', 'de', 'es']
PATH = {l: '/' if l == 'it' else f'/{l}/' for l in LANGS}
META = {
    'it': ('CinemaTherapy · La medicina delle medicine', 'L’arte fa bene, lo dice la scienza. Il cinema, l’arte delle arti, è la medicina delle medicine. CinemaTherapy Production, i creatori di Cine Twins.'),
    'en': ('CinemaTherapy · The medicine of all medicines', 'Art is good for you, science says so. Cinema, the art of all arts, is the medicine of all medicines. CinemaTherapy Production, the makers of Cine Twins.'),
    'fr': ('CinemaTherapy · Le remède des remèdes', 'L’art fait du bien, la science le dit. Le cinéma, l’art des arts, est le remède des remèdes. CinemaTherapy Production, les créateurs de Cine Twins.'),
    'de': ('CinemaTherapy · Die Arznei aller Arzneien', 'Kunst tut gut, sagt die Wissenschaft. Das Kino, die Kunst der Künste, ist die Arznei aller Arzneien. CinemaTherapy Production, die Macher von Cine Twins.'),
    'es': ('CinemaTherapy · La medicina de las medicinas', 'El arte sienta bien, lo dice la ciencia. El cine, el arte de las artes, es la medicina de las medicinas. CinemaTherapy Production, los creadores de Cine Twins.'),
}
NUM = ['i.', 'ii.', 'iii.', 'iv.']

LOGO = '''<svg width="38" height="50" viewBox="0 0 44 60" aria-hidden="true"><path d="M14 10 C14 4 22 2 25 8 C28 2 36 4 36 10 C36 18 25 24 25 24 C25 24 14 18 14 10 Z" fill="#E2312B"/><path d="M10 4 L10 32 M40 4 L40 32 M6 28 L44 28 M10 36 L40 36 M12 36 L38 56 M38 36 L12 56" fill="none" stroke="#F3E9D7" stroke-width="3" stroke-linecap="round"/></svg>'''

def faces(label):
    xs = [22, 66, 110, 154, 198, 242, 286]
    parts = []
    for i, x in enumerate(xs):
        lit = i == 3
        parts.append(f'<circle cx="{x}" cy="25" r="19"{" fill=\"#0F0B0A\"" if lit else ""}/>'
                     f'<path d="M{x-12} 18 h9 v6 h-9 z M{x+3} 18 h9 v6 h-9 z M{x-7} 32 q7 6 14 0"{" stroke=\"#FFD84D\"" if lit else ""}/>')
    return (f'<svg class="faces" viewBox="0 0 308 50" role="img" aria-label="{html.escape(label)}">'
            f'<g stroke="#0F0B0A" stroke-width="1.8" fill="none" stroke-linecap="round">{"".join(parts)}</g></svg>')

def page(lang, t):
    e = lambda s: html.escape(s, quote=False)
    title, desc = META[lang]
    alternates = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{PATH[l]}">' for l in LANGS)
    switch = ''.join(
        f'<a class="lang{" on" if l == lang else ""}" href="{PATH[l]}" hreflang="{l}" lang="{l}"{" aria-current=\"page\"" if l == lang else ""}>{l.upper()}</a>'
        for l in LANGS)
    ben = ''.join(
        f'<article class="ben"><span class="num">{NUM[i]}</span><h3>{e(h)}</h3><p>{e(p)}</p></article>'
        for i, (h, p) in enumerate(t['ben']))
    arts = ''.join(
        f'<div class="row"><span><b>{e(n)}</b><span>{e(d)}</span></span><i>{e(t["qb"])}</i></div>'
        for n, d in t['arts'])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{PATH[lang]}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{PATH[lang]}">
<meta name="theme-color" content="#0F0B0A">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Oswald:wght@300;400;600&family=Fraunces:ital,opsz,wght@0,9..144,300;1,9..144,300;1,9..144,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header class="wrap head">
  <a class="brand" href="{PATH[lang]}" aria-label="CinemaTherapy">{LOGO}<span><b>CinemaTherapy</b><small>PRODUCTION</small></span></a>
  <div class="head-right">
    <nav aria-label="Menu"><a href="#benefici">{e(t["navBen"])}</a><a href="#bugiardino">{e(t["navBug"])}</a><a href="#cinetwins">Cine Twins</a><a class="pill" href="#contatti">{e(t["navMail"])}</a></nav>
    <div class="langs" role="group" aria-label="Lingua · Language">{switch}</div>
  </div>
</header>

<main>
<section class="hero" id="top">
  <div class="beam" aria-hidden="true"></div>
  <div class="wrap hero-in">
    <div class="hero-text">
      <p class="kicker"><span class="dash"></span>{e(t["kicker"])}</p>
      <h1><span>{e(t["h1a"])}</span>{e(t["h1b"])} <em>{e(t["h1c"])}</em></h1>
      <p class="lead">{e(t["heroSub"])}</p>
      <div class="ctas"><a class="btn yellow" href="#cinetwins">{e(t["cta1"])} <span aria-hidden="true">→</span></a><a class="btn ghost" href="#bugiardino">{e(t["cta2"])}</a></div>
    </div>
    <div class="rx-wrap">
      <div class="rx-shadow" aria-hidden="true"></div>
      <div class="rx">
        <div class="rx-top"><span class="rx-mark">Rx</span><span class="rx-no">{e(t["rx"])}<br>N° 0007</span></div>
        <p class="rx-line">{e(t["rxLine"])}</p>
        <div class="rx-list"><span><b>{e(t["posH"])}</b>{e(t["pos"])}</span><span><b>{e(t["effH"])}</b>{e(t["eff"])}</span><span><b>{e(t["conH"])}</b>{e(t["con"])}</span></div>
        <div class="rx-foot"><span>CINEMATHERAPY</span><em>{e(t["doc"])}</em></div>
      </div>
    </div>
  </div>
</section>

<div class="strip" aria-hidden="true"></div>

<section class="sec" id="benefici">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">{e(t["benK"])}</p><h2><span>{e(t["benA"])}</span><em>{e(t["benB"])}</em></h2></div>
      <p class="side">{e(t["benSub"])}</p>
    </div>
    <div class="bens">{ben}</div>
    <p class="src">{e(t["src"])} · <a href="https://www.ibsafoundation.org/it/blog/art-cure-le-evidenze-scientifiche-sui-benefici-della-arte-per-la-salute" rel="noopener">IBSA Foundation</a> · <a href="https://www.istitutobeck.com/beck-news/art-therapy" rel="noopener">Istituto Beck</a> · <a href="https://www.jcmh.org/it/healing-through-art-self-expression-as-therapy/" rel="noopener">JCMH</a> · <a href="https://casadicurasanrossore.it/articoli/arte-e-benessere-la-bellezza-dellarte-ci-aiuta-a-stare-meglio/" rel="noopener">Casa di Cura San Rossore</a></p>
  </div>
</section>

<section class="quote" aria-label="Motto">
  <p>«{e(t["quote"])}»</p>
  <small>{e(t["quoteBy"])}</small>
</section>

<section class="sec" id="bugiardino">
  <div class="wrap bug">
    <div class="bug-text">
      <p class="eyebrow">{e(t["navBug"])}</p>
      <h2><span>{e(t["bugA"])}</span>{e(t["bugB"])} <em>{e(t["bugC"])}</em> {e(t["bugD"])}</h2>
      <p class="side">{e(t["bugP"])}</p>
      <p class="pull"><span>{e(t["bugQ1"])}</span>{e(t["bugQ2"])}</p>
    </div>
    <div class="label">
      <div class="label-top"><span>{e(t["comp"])}</span><small>{e(t["compSub"])}</small></div>
      {arts}
      <p class="label-foot">{e(t["excip"])} · {e(t["src"])}: <a href="https://www.centrostudibaragli.it/articolo/arte-il-cinema-tra-opinioni-e-distinzioni" rel="noopener">Centro Studi Baragli</a>, <a href="https://articoli.euroinnova.com/perche-il-cinema-e-unarte" rel="noopener">Euroinnova</a></p>
    </div>
  </div>
</section>

<div class="strip" aria-hidden="true"></div>

<section class="sec" id="cinetwins">
  <div class="wrap">
    <div class="ct">
      <div class="ct-text">
        <p class="eyebrow dark">{e(t["ctK"])}</p>
        <h2 class="ct-title">Cine <span>Twins</span></h2>
        <p class="ct-p">{e(t["ctP"])}</p>
        <p class="ct-meta">{e(t["ctMeta"])}</p>
        <a class="btn black" href="mailto:team@cinematherapy.it?subject=Cine%20Twins">{e(t["ctCta"])} <span aria-hidden="true">→</span></a>
      </div>
      <div class="ct-faces">{faces(t["ctFaces"])}<em>{e(t["ctFaces"])}</em></div>
    </div>
  </div>
</section>
</main>

<footer class="wrap foot" id="contatti">
  <div class="foot-top">
    <div><p class="eyebrow">{e(t["contK"])}</p><a class="mail" href="mailto:team@cinematherapy.it">team@cinematherapy.it</a></div>
    <p class="disc"><span>{e(t["disc1"])}</span>{e(t["disc2"])}</p>
  </div>
  <div class="foot-bottom"><span>Made with <span class="heart">♥</span> by CinemaTherapy Production</span><span>{e(t["privacy"])} · {e(t["terms"])}</span></div>
</footer>
</body>
</html>
'''

def main():
    data = json.load(open(os.path.join(ROOT, 'content', 'i18n.json'), encoding='utf-8'))
    out = os.path.join(ROOT, 'public')
    for lang in LANGS:
        d = os.path.join(out, '' if lang == 'it' else lang)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(lang, data[lang]))
    urls = ''.join(f'<url><loc>{SITE}{PATH[l]}</loc></url>' for l in LANGS)
    open(os.path.join(out, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(out, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    print('built', ', '.join(PATH[l] for l in LANGS))

if __name__ == '__main__':
    main()
