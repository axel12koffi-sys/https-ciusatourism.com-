#!/usr/bin/env python3
import re, sys
# Génère les pages du site à partir d'un header/footer communs.
# En PHP ces deux blocs deviennent partials/header.php et partials/footer.php.
import os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
from paths import IMG, localize, clean_links
from paths import CLEAN_URLS as CLEAN
from content import BEACHES, BEACH_FAQ, CULTURE, CULTURE_FAQ, ECO, ECO_FAQ
# correspondance entre le nom affiché dans content.py et la page de lieu
SLUGS = {
    'Grand-Bassam': 'grand-bassam', 'Assinie': 'assinie', 'Sassandra': 'sassandra',
    'San Pedro': 'san-pedro', 'Jacqueville': 'jacqueville', 'Grand-Lahou': 'grand-lahou',
    'Yamoussoukro': 'yamoussoukro', 'Korhogo and Senufo country': 'korhogo',
    'Man and the masks of the West': 'man', 'Abidjan': 'abidjan', 'Bouaké': 'bouake',
    'Tiégba': 'tiegba', 'Taï National Park': 'tai', 'Comoé National Park': 'comoe',
    'The Man region': 'man', 'Banco National Park': 'banco',
    'Ehotilé Islands': 'ehotile', 'Mount Nimba': 'nimba',
}


def slug_of(name):
    s = SLUGS.get(name)
    return f'place-{s}.html' if s else 'contact.html'

import os, shutil
import i18n
i18n.set_lang(os.environ.get('CIUSA_LANG', 'en'))
from i18n import pick



def prefer_photos(html):
    """Partout dans la page, remplace un visuel dessiné (.svg) par la vraie
    photo si elle a été déposée dans assets/img/dest/. Complète cover(),
    qui ne couvrait que les fiches de lieu."""
    def sub(m):
        base = m.group(1)
        for ext in ('.webp', '.jpg', '.jpeg', '.png'):
            if (ROOT / 'assets' / 'img' / 'dest' / (base + ext)).exists():
                return f'assets/img/dest/{base}{ext}'
        return m.group(0)
    return re.sub(r'assets/img/dest/([a-z0-9-]+)\.svg', sub, html)


def cover(img):
    """Si une vraie photo du même nom existe (.jpg / .webp / .png), on la
    préfère au visuel de remplacement. Rien d'autre à modifier : il suffit
    de déposer le fichier dans assets/img/dest/."""
    if not img.endswith('.svg'):
        return img
    for ext in ('.webp', '.jpg', '.jpeg', '.png'):  # webp d'abord : plus léger
        if (ROOT / img[:-4]).with_suffix(ext).exists():
            return img[:-4] + ext
    return img


SPRITE = """<svg style="display:none" aria-hidden="true">
<symbol id="plane" viewBox="0 0 24 24"><path fill="currentColor" d="M12 1.4c1.13 0 1.94 1.45 1.94 3.5v3.32l8.06 4.78v2.32l-8.06-2.4v4.62l2.6 1.9v1.86L12 20.36l-4.54.94V19.44l2.6-1.9v-4.62L2 15.32V13l8.06-4.78V4.9c0-2.05.81-3.5 1.94-3.5z"/></symbol>
<symbol id="arrow" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" d="M4 12h15m-6-6 6 6-6 6"/></symbol>
<symbol id="up" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" d="M12 20V5m-7 7 7-7 7 7"/></symbol>
<symbol id="chat" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z"/></symbol>
<symbol id="sendic" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M21 3 3 10.5l7 2.5 2.5 7L21 3z"/></symbol>
<symbol id="pin" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M12 21s-7-4.8-7-10a7 7 0 1 1 14 0c0 5.2-7 10-7 10z"/><circle cx="12" cy="11" r="2.6" fill="none" stroke="currentColor" stroke-width="1.9"/></symbol>
<symbol id="phone" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M21 16.9v2.6a1.7 1.7 0 0 1-1.9 1.7 17 17 0 0 1-7.4-2.6 16.6 16.6 0 0 1-5.1-5.1A17 17 0 0 1 4 6.1 1.7 1.7 0 0 1 5.7 4.2h2.6a1.7 1.7 0 0 1 1.7 1.5c.1.8.3 1.6.6 2.4a1.7 1.7 0 0 1-.4 1.8l-1.1 1.1a13.6 13.6 0 0 0 5.1 5.1l1.1-1.1a1.7 1.7 0 0 1 1.8-.4c.8.3 1.6.5 2.4.6a1.7 1.7 0 0 1 1.5 1.7z"/></symbol>
<symbol id="mail" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M3 6h18v12H3z"/><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="m3 7 9 6 9-6"/></symbol>
<symbol id="beds" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M3 18v-8h18v8M3 14h18M6 10V7h5v3M13 10V7h5v3M3 18v2M21 18v2"/></symbol>
<symbol id="aya" viewBox="0 0 48 48"><circle cx="24" cy="24" r="24" fill="#F77F00"/><path d="M8.5 48c1.6-8.4 8-12.6 15.5-12.6S38 39.6 39.5 48z" fill="#0A3161"/><path d="M24 12.5c5.6 0 8.6 4.4 8.6 10.2S29.2 34 24 34s-8.6-5.5-8.6-11.3S18.4 12.5 24 12.5z" fill="#8B5A34"/><path d="M13.6 21.5C14.3 13.9 18.6 9.4 24 9.4s9.7 4.5 10.4 12.1c-1.2-4-4.9-6.2-10.4-6.2s-9.2 2.2-10.4 6.2z" fill="#009E60"/><circle cx="15.2" cy="25.6" r="1.9" fill="#F2C6A0"/><circle cx="32.8" cy="25.6" r="1.9" fill="#F2C6A0"/></symbol>
<symbol id="search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="m20 20-3.5-3.5"/></symbol>
</svg>"""

def head(title, desc, cur):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Sublime CI-USA</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body data-page="{cur}">

<div id="preloader">
  <svg class="pl-plane"><use href="#plane"/></svg>
  <div class="pl-bar"><i></i></div>
  <div class="pl-txt">Sublime CI-USA</div>
</div>

{SPRITE}
"""

def header(cur):
    def c(name):
        return ' class="nav__item current"' if name == cur else ' class="nav__item"'
    return f"""
<!-- ===== partials/header.php ===== -->
<div class="topbar">
  <div class="topbar__in">
    <div class="topbar__tag" data-i18n="top.tag">A great destination for <strong>American travelers</strong></div>
    <div class="topbar__right">
      <a href="tel:2407568332">Tel: 240 756 8332</a>
      <div class="topbar__soc"><a href="#">FB</a><a href="#">IG</a><a href="#">IN</a><a href="#">YT</a></div>
      <div class="langs"><a class="langs__a on" href="#" data-lang="en" aria-current="page">EN</a><a class="langs__a" href="__FRPATH__" data-lang="fr">FR</a></div>
    </div>
  </div>
</div>

<header class="hdr" id="hdr">
  <div class="hdr__in">
    <a class="logo" href="index.html">
      <img src="assets/img/logo-mark.webp" alt="Sublime Côte d'Ivoire">
      <span class="logo__txt">Sublime CI-USA<span>Washington · Abidjan</span></span>
    </a>
    <nav class="nav" aria-label="Main">
      <div{c('home')}><a class="nav__link" href="index.html"><span data-i18n="nav.home">Home</span> <i></i></a>
        <div class="drop"><a href="mediatheque.html" data-i18n="nav.media">Media library</a><a href="blog.html" data-i18n="nav.blog">Blog &amp; News</a></div></div>
      <div{c('faq')}><a class="nav__link" href="faq.html" data-i18n="nav.faq">FAQ</a></div>
      <div{c('dest')}><a class="nav__link" href="destinations.html"><span data-i18n="nav.dest">Destinations</span> <i></i></a>
        <div class="drop">
          <a href="destinations.html">Destinations — overview</a>
          <a href="destination-beaches.html" data-i18n="nav.beaches">Beaches &amp; coastline</a>
          <a href="destination-culture.html" data-i18n="nav.culture">Cultural trips</a>
          <a href="destination-eco.html" data-i18n="nav.eco">Adventure &amp; ecotourism</a>
        </div></div>
      <div{c('deal')}><a class="nav__link" href="good-deal.html"><span data-i18n="nav.deal">Good Deal</span> <i></i></a>
        <div class="drop"><a href="good-deal.html">Good Deal — overview</a><a href="hotel.html" data-i18n="nav.hotel">Hotel</a><a href="gastronomies.html" data-i18n="nav.gastro">Gastronomies</a><a href="transport.html" data-i18n="nav.transport">Transport</a></div></div>
      <div{c('contact')}><a class="nav__link" href="contact.html" data-i18n="nav.contact">Contact us</a></div>
    </nav>
    <a class="btn btn--go hdr__cta" href="contact.html"><span data-i18n="cta.plan">Plan your trip</span> <svg><use href="#arrow"/></svg></a>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
  <div id="hdrProgress"></div>
</header>

<div class="drawer" id="drawer">
  <div class="drawer__top">
    <span class="logo__txt" style="color:#fff">Sublime CI-USA</span>
    <button class="drawer__close" id="drawerClose" aria-label="Close menu">&times;</button>
  </div>
  <a href="index.html" data-i18n="nav.home">Home</a>
  <div class="m-group"><button type="button"><span style="font-size:24px;font-weight:600" data-i18n="nav.dest">Destinations</span><span>+</span></button>
    <div class="m-sub">
      <a href="destinations.html">Overview</a>
      <a href="destination-beaches.html" data-i18n="nav.beaches">Beaches &amp; coastline</a>
      <a href="destination-culture.html" data-i18n="nav.culture">Cultural trips</a>
      <a href="destination-eco.html" data-i18n="nav.eco">Adventure &amp; ecotourism</a>
    </div></div>
  <div class="m-group"><button type="button"><span style="font-size:24px;font-weight:600" data-i18n="nav.deal">Good Deal</span><span>+</span></button>
    <div class="m-sub">
      <a href="good-deal.html">Overview</a>
      <a href="hotel.html" data-i18n="nav.hotel">Hotel</a>
      <a href="gastronomies.html" data-i18n="nav.gastro">Gastronomies</a>
      <a href="transport.html" data-i18n="nav.transport">Transport</a>
    </div></div>
  <a href="blog.html" data-i18n="nav.blog">Blog &amp; News</a>
  <a href="mediatheque.html" data-i18n="nav.media">Media library</a>
  <a href="faq.html" data-i18n="nav.faq">FAQ</a>
  <a href="contact.html" data-i18n="nav.contact">Contact us</a>
</div>

<div class="flightrail" aria-hidden="true">
  <div class="flightrail__code"><b>IAD</b>Washington</div>
  <div class="flightrail__track" id="track">
    <div class="flightrail__trail" id="trail"></div>
    <div class="flightrail__plane" id="railPlane"><svg><use href="#plane"/></svg></div>
  </div>
  <div class="flightrail__code"><b>ABJ</b>Abidjan</div>
</div>
<!-- ===== /partials/header.php ===== -->
"""

FOOTER = f"""
<!-- ===== partials/footer.php ===== -->
<section class="block cta">
  <div class="cta__trail"></div>
  <svg class="cta__plane" aria-hidden="true"><use href="#plane"/></svg>
  <div class="wrap rv" style="position:relative">
    <div class="eyebrow eyebrow--light eyebrow--center">Next departure</div>
    <h2 class="h-lg">Plan your dream trip<br>to Côte d'Ivoire</h2>
    <p>Send us your dates and what you want out of the trip. We reply with a route, a price and the names of the people who will meet you.</p>
    <a class="btn btn--white" href="contact.html"><span data-i18n="nav.contact">Contact us</span> <svg><use href="#arrow"/></svg></a>
  </div>
</section>

<footer class="ft">
  <div class="wrap">
    <div class="ft__grid">
      <div>
        <img class="mark" src="assets/img/logo-full.webp" alt="Sublime Côte d'Ivoire">
        <p>Sublime CI-USA is a travel agency specialising in trips to Côte d'Ivoire, helping American travelers explore its cultural, natural and historical heritage.</p>
        <div class="ft__soc"><a href="#">Facebook</a><a href="#">Twitter</a><a href="#">Linkedin</a></div>
      </div>
      <div><h4>Site map</h4>
        <ul><li><a href="index.html">Home</a></li><li><a href="destinations.html">Destinations</a></li><li><a href="hotel.html">Hotels</a></li><li><a href="gastronomies.html">Gastronomies</a></li><li><a href="transport.html">Transport</a></li><li><a href="blog.html">Blog &amp; News</a></li><li><a href="mediatheque.html">Media library</a></li><li><a href="contact.html">Contact us</a></li></ul></div>
      <div><h4>Liens utiles</h4>
        <ul>
          <li><a href="https://snedai.com/e-visa/" target="_blank" rel="noopener noreferrer">Official e-Visa (SNEDAI)</a></li>
          <li><a href="https://www.tourisme.gouv.ci/" target="_blank" rel="noopener noreferrer">Ministry of Tourism</a></li>
          <li><a href="https://www.cotedivoiretourisme.ci/" target="_blank" rel="noopener noreferrer">Côte d'Ivoire Tourisme</a></li>
          <li><a href="https://ambaciusa.org/" target="_blank" rel="noopener noreferrer">Embassy in Washington, D.C.</a></li>
          <li><a href="faq.html">FAQ</a></li>
        </ul></div>
      <div><h4>Contact us</h4>
        <ul>
          <li><a href="mailto:tourism@ambaciusa.org">tourism@ambaciusa.org</a></li>
          <li><a href="tel:2407568332">(240) 756-8332</a></li>
          <li>2424 Massachusetts Avenue N.W.<br>Washington, D.C. 20008</li>
        </ul>
        <h4 style="margin-top:24px">Newsletter</h4>
        <div class="nl" id="nlForm">
          <input type="email" placeholder="Your email address" aria-label="Your email address">
          <button type="button">Send</button>
        </div>
        <div class="nlMsg" id="nlMsg"></div>
      </div>
    </div>
    <div class="ft__bar"><span>© 2026 Sublime CI-USA. All rights reserved.</span><span>IAD → ABJ</span></div>
  </div>
</footer>

<button id="toTop" aria-label="Back to top"><svg><use href="#up"/></svg></button>

<!-- ===== chatbot ===== -->
<button id="chatBtn" aria-label="Chat with Aya">
  <span class="chatBtn__av" data-aya="button"></span><span data-i18n="chat.title">Chat with Aya</span><span class="badge"></span>
</button>
<div id="chatPanel" role="dialog" aria-label="Sublime CI-USA assistant">
  <div class="chat__hd">
    <div class="chat__av" data-aya="panel"></div>
    <div><b>Aya</b><small><i></i><span data-i18n="chat.status">Ivorian-American · online</span></small></div>
    <button class="chat__close" id="chatClose" aria-label="Close chat">&times;</button>
  </div>
  <div class="chat__log" id="chatLog"></div>
  <div class="chat__quick" id="chatQuick"></div>
  <div class="chat__in">
    <input id="chatInput" type="text" placeholder="Write your message…" data-i18n="chat.ph" aria-label="Message">
    <button id="chatSend" aria-label="Send"><svg><use href="#sendic"/></svg></button>
  </div>
</div>
<!-- ===== /partials/footer.php ===== -->

<script src="assets/js/main.js"></script>
<script src="assets/js/aya.js"></script>
<script src="assets/js/chatbot.js"></script>
</body>
</html>"""

def phero(crumb, title, sub, img):
    links = ''.join(f'<a href="{h}">{t}</a><i></i>' for h, t in crumb[:-1]) + f'<span>{crumb[-1][1]}</span>'
    return f"""
<section class="phero">
  <div class="phero__bg" style="background-image:url('{img}')"></div>
  <svg class="phero__plane" aria-hidden="true"><use href="#plane"/></svg>
  <div class="wrap">
    <div class="crumb">{links}</div>
    <h1 class="h-lg">{title}</h1>
    <p class="lede" style="color:rgba(255,255,255,.74)">{sub}</p>
  </div>
</section>"""

# ============================================================ PAGES
PAGES = {}

# ---------- INDEX ----------
PAGES['index.html'] = ('Washington D.C. to Abidjan', 'Tailor-made trips to Côte d\'Ivoire for American travelers.', 'home', f"""
<section class="hero" id="top">
  <div class="hero__slides">
    <div class="hero__slide" style="background-image:url('assets/img/dest/hero-1.svg')"></div>
    <div class="hero__slide" style="background-image:url('assets/img/dest/hero-2.svg')"></div>
    <div class="hero__slide" style="background-image:url('assets/img/dest/hero-3.svg')"></div>
  </div>
  <div class="hero__grid"></div>
  <div class="hero__in">
    <div class="hero__route">IAD <span class="dash"><svg><use href="#plane"/></svg></span> <span>ABJ</span></div>
    <h1 class="h-xl">Abidjan is closer<br>than you <em>think</em>.</h1>
    <p class="hero__lede">Sublime CI-USA plans the whole journey from Washington, D.C. — beaches, culture, forests and food — with people on the ground in Côte d'Ivoire.</p>
    <div class="hero__btns">
      <a class="btn btn--go" href="contact.html"><span data-i18n="cta.plan">Plan your trip</span> <svg><use href="#arrow"/></svg></a>
      <a class="btn btn--onDark" href="destinations.html" data-i18n="cta.see">See destinations</a>
    </div>
    <div class="hero__dots" id="heroDots"></div>
  </div>
  <div class="boarding">
    <div class="boarding__in">
      <div class="boarding__cell"><div class="boarding__k">Departure</div><div class="boarding__v">Washington, D.C.</div></div>
      <div class="boarding__cell"><div class="boarding__k">Arrival</div><div class="boarding__v">Abidjan, Côte d'Ivoire</div></div>
      <div class="boarding__cell"><div class="boarding__k">Best season</div><div class="boarding__v">December — April</div></div>
      <div class="boarding__cell boarding__cell--go"><a href="contact.html"><span><div class="boarding__k">Ready when you are</div><div class="boarding__v">Get a quote</div></span><svg><use href="#arrow"/></svg></a></div>
    </div>
  </div>
</section>

<section class="block" data-way>
  <div class="wrap">
    <div class="head rv">
      <div><div class="eyebrow" data-i18n="nav.dest">Destinations</div>
        <h2 class="h-lg">Three ways to see<br>Côte d'Ivoire<svg class="flyin"><use href="#plane"/></svg></h2></div>
      <a class="btn btn--ghost" href="destinations.html">All destinations <svg><use href="#arrow"/></svg></a>
    </div>
    <div class="cards">
      <a class="card rv" data-d="1" href="destination-beaches.html">
        <div class="card__img" style="background-image:url('assets/img/dest/cat-beach.svg')"></div>
        <span class="card__tag">Coastline</span>
        <div class="card__body"><h3 class="h-md">Best Beaches in Ivory Coast</h3>
          <p>Assinie, Grand-Bassam, Sassandra — a southern coast of lagoons, surf and fishing villages, mapped end to end.</p>
          <span class="more">Explore <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card rv" data-d="2" href="destination-culture.html">
        <div class="card__img" style="background-image:url('assets/img/dest/cat-culture.svg')"></div>
        <span class="card__tag">Culture</span>
        <div class="card__body"><h3 class="h-md">Cultural Trips</h3>
          <p>Festivals, mask traditions, markets and music — travel alongside guides who grew up with these stories.</p>
          <span class="more">Explore <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card card--green rv" data-d="3" href="destination-eco.html">
        <div class="card__img" style="background-image:url('assets/img/dest/cat-eco.svg')"></div>
        <span class="card__tag">Nature</span>
        <div class="card__body"><h3 class="h-md">Adventure &amp; Ecotourism</h3>
          <p>Taï rainforest, Man's waterfalls and highlands — small groups, low impact, local hosts.</p>
          <span class="more">Explore <svg><use href="#arrow"/></svg></span></div></a>
    </div>
  </div>
</section>

<section class="block partners" style="background:#fff;border-block:1px solid var(--line)" data-way>
  <div class="wrap">
    <div class="head rv">
      <div><div class="eyebrow">News</div><h2 class="h-lg">Unforgettable experiences</h2></div>
      <a class="btn btn--ghost" href="blog.html">Read the blog <svg><use href="#arrow"/></svg></a>
    </div>
    <div class="posts">
      <a class="post post--next rv" data-d="1" href="event-two-cities.html"><div class="post__media"><img src="assets/img/dest/event-two-cities.webp" alt="Two Cities, One Friendship"><span class="post__flag">Upcoming</span></div>
        <span class="post__date">11.12.2026 · Event</span><h3 class="h-sm">Two Cities, One Friendship: Rockville meets Korhogo</h3></a>
      <a class="post rv" data-d="2" href="blog.html"><div class="post__media"><img src="assets/img/dest/blog-passport.webp" alt="Passport DC at the Embassy of Côte d'Ivoire"></div>
        <span class="post__date">04.05.2026 · Washington</span><h3 class="h-sm">Passport DC: Côte d'Ivoire opens its doors</h3></a>
      <a class="post rv" data-d="3" href="blog.html"><div class="post__media"><img src="assets/img/dest/blog-culture.svg" alt="Femua"></div>
        <span class="post__date">09.01.2026 · Culture</span><h3 class="h-sm">Femua, the festival that fills Abidjan</h3></a>
    </div>
  </div>
</section>

<section class="block" data-way>
  <div class="wrap split">
    <div class="rv">
      <div class="eyebrow">Welcome to Sublime CI-USA</div>
      <h2 class="h-lg">One agency on<br>both ends of<br>the route.</h2>
      <p class="lede" style="margin-top:22px">We are based in Washington, D.C. and work with partners in Abidjan, so the trip you book here is the trip that happens there. Landscapes, culture, history — organised by people who answer the phone in both time zones.</p>
      <div class="stats">
        <div><b data-count="2">2</b><span>Cities, one team</span></div>
        <div><b data-count="5">5</b><span>Services end to end</span></div>
        <div><b data-count="9">9</b><span>Partners on the ground</span></div>
        <div><b data-count="100" data-suffix="%">100%</b><span>Tailor-made itineraries</span></div>
      </div>
      <a class="btn btn--go" style="margin-top:26px" href="destinations.html">Learn more <svg><use href="#arrow"/></svg></a>
    </div>
    <div class="routemap rv" data-d="2">
      <div class="routemap__grid"></div>
      <svg class="arc" viewBox="0 0 400 210" fill="none" aria-hidden="true">
        <path d="M28 168 C 130 34, 268 34, 372 150" stroke="rgba(255,255,255,.28)" stroke-width="2" stroke-dasharray="7 8"/>
        <path id="arcLive" d="M28 168 C 130 34, 268 34, 372 150" stroke="#F77F00" stroke-width="2.4" stroke-linecap="round"/>
        <circle cx="28" cy="168" r="6" fill="#B31942"/><circle cx="28" cy="168" r="12" fill="#B31942" opacity=".22"/>
        <circle cx="372" cy="150" r="6" fill="#009E60"/><circle cx="372" cy="150" r="12" fill="#009E60" opacity=".22"/>
        <g id="arcPlane" style="opacity:0"><use href="#plane" x="-11" y="-11" width="22" height="22" fill="#fff"/></g>
      </svg>
      <div class="routemap__pins"><div class="a"><b>IAD</b>Washington Dulles</div><div class="b"><b>ABJ</b>Félix-Houphouët-Boigny</div></div>
    </div>
  </div>
</section>

<section class="block services" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Our services</div>
      <h2 class="h-lg">Explore, discover, and<br>experience Côte d'Ivoire</h2></div></div>
    <div class="srv rv">
      <div class="srv__i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 7h18M3 12h18M3 17h11"/></svg>
        <h3 class="h-sm">Tailor-Made Trips</h3><p>Itineraries built around what you actually want — adventure, rest, eco-tourism or culture.</p></div>
      <div class="srv__i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 20V9l9-5 9 5v11M9 20v-6h6v6"/></svg>
        <h3 class="h-sm">Booking</h3><p>Hotels, lodges and guesthouses we have visited, chosen for comfort and character.</p></div>
      <div class="srv__i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 16V7h11v9M15 10h4l2 3v3h-6M6.5 19a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm11 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/></svg>
        <h3 class="h-sm">Transportation &amp; Logistics</h3><p>Airport transfers, city drivers and excursion vehicles — vetted and insured.</p></div>
      <div class="srv__i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 21s-7-4.8-7-10a7 7 0 1 1 14 0c0 5.2-7 10-7 10z"/><circle cx="12" cy="11" r="2.6"/></svg>
        <h3 class="h-sm">Experienced Tour Guides</h3><p>Local guides who translate more than language — context, etiquette and history.</p></div>
      <div class="srv__i"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M6 3h9l5 5v13H6z"/><path d="M15 3v5h5M9.5 13.5h5M9.5 17h5"/></svg>
        <h3 class="h-sm">Travel Assistance</h3><p>Visa paperwork, flight reservations and the small administrative steps in between.</p></div>
      <div class="srv__i srv__i--cta"><h3 class="h-md">Tell us where you want to go.</h3>
        <p>Send a few dates and we come back with a route.</p>
        <a class="btn btn--onDark" href="contact.html">Start planning <svg><use href="#arrow"/></svg></a></div>
    </div>
  </div>
</section>

<section class="block vision" data-way>
  <svg class="vision__plane" aria-hidden="true"><use href="#plane"/></svg>
  <div class="wrap rv">
    <div class="eyebrow eyebrow--light">Our vision</div>
    <h2 class="h-lg">Travel is discovery,<br>exchange, and<br>something you keep.</h2>
    <div class="vision__q"><p>We are committed to responsible, sustainable tourism that shows Côte d'Ivoire's natural and cultural treasures while supporting the communities that keep them alive.</p></div>
  </div>
</section>

<section class="block" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow" data-i18n="nav.deal">Good Deal</div><h2 class="h-lg">Where to sleep,<br>what to eat</h2></div>
      <a class="btn btn--ghost" href="good-deal.html">All good deals <svg><use href="#arrow"/></svg></a></div>
    <div class="duo">
      <a class="tile rv" data-d="1" href="hotel.html">
        <div class="tile__img" style="background-image:url('assets/img/dest/deal-hotel.svg')"></div>
        <div class="tile__body"><span class="card__tag card__tag--static">Hotels &amp; Restaurants</span>
          <h3 class="h-md">Places we send our own families</h3>
          <p>From lagoon-side lodges to the maquis worth queueing for.</p>
          <span class="more">Learn more <svg><use href="#arrow"/></svg></span></div></a>
      <a class="tile rv" data-d="2" href="gastronomies.html">
        <div class="tile__img" style="background-image:url('assets/img/dest/deal-food.svg')"></div>
        <div class="tile__body"><span class="card__tag card__tag--static">Content of interest</span>
          <h3 class="h-md">Read before you fly</h3>
          <p>Practical guides on transport, gastronomy and the seasons.</p>
          <span class="more">Learn more <svg><use href="#arrow"/></svg></span></div></a>
    </div>
  </div>
</section>

<section class="partners">
  <div class="wrap"><div class="eyebrow">Our partners</div></div>
  <div class="marquee" id="marquee">
    <img src="{IMG}/2025/05/1.png" alt="Partner"><img src="{IMG}/2025/05/7.png" alt="Partner">
    <img src="{IMG}/2025/05/6.png" alt="Partner"><img src="{IMG}/2025/05/4.png" alt="Partner">
    <img src="{IMG}/2025/05/3.png" alt="Partner"><img src="{IMG}/2025/05/2.png" alt="Partner">
    <img src="{IMG}/2026/01/logo-300x68.png" alt="Partner"><img src="{IMG}/2025/09/telechargement-1.png" alt="Partner">
  </div>
</section>
""")

# ---------- DESTINATIONS ----------
CARDS = [
    ('beach', 'Grand-Bassam', 'Coastline', 'A UNESCO colonial quarter one hour from Abidjan, right on the sand.', 'assets/img/dest/grand-bassam.svg', 'destination-beaches.html'),
    ('beach', 'Assinie', 'Coastline', 'Lagoon on one side, Atlantic on the other. Surf, kayaks and long lunches.', 'assets/img/dest/assinie.svg', 'destination-beaches.html'),
    ('beach', 'Sassandra', 'Coastline', 'Fishing port and quiet coves, four hours west along the coast road.', 'assets/img/dest/sassandra.svg', 'destination-beaches.html'),
    ('culture', 'FEMUA, Abidjan', 'Culture', 'The city\'s biggest music festival, with concerts across several neighbourhoods.', 'assets/img/dest/abidjan.svg', '#'),
    ('culture', 'Masks of the West', 'Culture', 'Dan and Wè mask traditions around Man, seen with the families who keep them.', f'assets/img/dest/blog-culture.svg', '#'),
    ('culture', 'Korhogo & the north', 'Culture', 'Senufo weaving, painted cloth and market days in the savanna.', 'assets/img/dest/korhogo.svg', '#'),
    ('eco', 'Taï National Park', 'Nature', 'One of West Africa\'s last primary rainforests. Guided walks, small groups.', 'assets/img/dest/tai.svg', '#'),
    ('eco', 'Man highlands', 'Nature', 'Waterfalls, liana bridges and mountain villages in the west.', 'assets/img/dest/man.svg', '#'),
    ('eco', 'Comoé Park', 'Nature', 'Savanna, rivers and birdlife in the northeast — a full ecosystem in one park.', 'assets/img/dest/comoe.svg', '#'),
]
cards_html = '\n'.join(f"""      <a class="card grid-item rv" data-cat="{cat}" href="{href}">
        <div class="card__img" style="background-image:url('{img}')"></div>
        <span class="card__tag">{tag}</span>
        <div class="card__body"><h3 class="h-md">{name}</h3><p>{desc}</p>
          <span class="more">Explore <svg><use href="#arrow"/></svg></span></div></a>""" for cat, name, tag, desc, img, href in CARDS)


def mini_card(p, cat, page):
    name, img = p['name'], cover(p['img'])
    dist, desc = pick(p['dist']), pick(p['desc'])
    short = desc.split('. ')[0] + '.'
    return f"""      <article class="lcard grid-item rv" data-cat="{cat}" data-name="{name.lower()}">
        <div class="lcard__img"><img loading="lazy" src="{img}" alt="{name}"><span class="lcard__zone">{dist}</span></div>
        <div class="lcard__b"><h3 class="h-sm">{name}</h3>
          <p class="lp">{short}</p>
          <div class="lcard__f"><a class="btn btn--ghost btn--sm" href="{slug_of(name)}">Explore <svg><use href="#arrow"/></svg></a></div></div>
      </article>"""


ALL_PLACES = '\n'.join(
    [mini_card(p, 'beach', 'destination-beaches.html') for p in BEACHES] +
    [mini_card(p, 'culture', 'destination-culture.html') for p in CULTURE] +
    [mini_card(p, 'eco', 'destination-eco.html') for p in ECO])


PAGES['destinations.html'] = ('Destinations', "Beaches, cultural trips and ecotourism in Côte d'Ivoire.", 'dest',
    phero([('index.html','Home'),('','Destinations')], 'Destinations',
          "Dix-huit lieux, répartis en trois familles de voyage. Chaque catégorie a sa page, avec ce qu'on y voit, ce qu'on y fait et les questions qu'on nous pose le plus.",
          'assets/img/dest/cat-beach.svg') + f"""
<section class="block" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Trois familles de voyage</div>
      <h2 class="h-lg">Par où commencer<svg class="flyin"><use href="#plane"/></svg></h2>
      <p class="lede">La plupart de nos voyageurs combinent deux catégories sur dix jours : une base côtière et une incursion culturelle ou nature.</p></div></div>
    <div class="cards">
      <a class="card rv" data-d="1" href="destination-beaches.html">
        <div class="card__img" style="background-image:url('assets/img/dest/cat-beach.svg')"></div>
        <span class="card__tag">6 lieux</span>
        <div class="card__body"><h3 class="h-md">Plages &amp; littoral</h3>
          <p>Grand-Bassam, Assinie, Sassandra, San Pedro, Jacqueville, Grand-Lahou. Lagunes, criques et villages de pêcheurs.</p>
          <span class="more">Voir le littoral <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card rv" data-d="2" href="destination-culture.html">
        <div class="card__img" style="background-image:url('assets/img/dest/cat-culture.svg')"></div>
        <span class="card__tag">6 lieux</span>
        <div class="card__body"><h3 class="h-md">Voyages culturels</h3>
          <p>Yamoussoukro, Korhogo, Man, Abidjan, Bouaké, Tiégba. Masques, artisanat, festivals et patrimoine.</p>
          <span class="more">Voir la culture <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card card--green rv" data-d="3" href="destination-eco.html">
        <div class="card__img" style="background-image:url('assets/img/dest/cat-eco.svg')"></div>
        <span class="card__tag">6 lieux</span>
        <div class="card__body"><h3 class="h-md">Aventure &amp; écotourisme</h3>
          <p>Taï, Comoé, Banco, Man, îles Ehotilé, mont Nimba. Forêt primaire, savane et montagnes.</p>
          <span class="more">Voir la nature <svg><use href="#arrow"/></svg></span></div></a>
    </div>
  </div>
</section>

<section class="block services" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Les 18 lieux</div>
      <h2 class="h-lg">Tout le pays,<br>filtrable</h2></div></div>
    <div class="filters rv" id="filters">
      <button class="on" data-filter="all">Tout</button>
      <button data-filter="beach">Plages</button>
      <button data-filter="culture">Culture</button>
      <button data-filter="washington">Washington</button>
      <button data-filter="eco">Nature</button>
    </div>
    <div class="listing">
{ALL_PLACES}
    </div>
    <p class="empty" id="listEmpty">Aucun lieu ne correspond.</p>
  </div>
</section>

<section class="block" data-way>
  <div class="wrap split">
    <div class="rv">
      <div class="eyebrow">Comment ça marche</div>
      <h2 class="h-lg">D'un premier message<br>au hall d'arrivée.</h2>
      <p class="lede" style="margin-top:20px">Chaque itinéraire est écrit à partir de zéro. Voici la séquence, et c'en est vraiment une : chaque étape dépend de la précédente.</p>
    </div>
    <div class="acc rv" data-d="2" style="background:#fff;border-radius:16px;padding:0 24px;border:1px solid var(--line)">
      <div class="acc__i"><button class="acc__q">1 — Vous décrivez le voyage<span>+</span></button>
        <div class="acc__a"><p>Dates, nombre de personnes, ce que vous en attendez, un budget approximatif. Cinq minutes sur le formulaire ou dix au téléphone.</p></div></div>
      <div class="acc__i"><button class="acc__q">2 — Nous proposons un itinéraire<span>+</span></button>
        <div class="acc__a"><p>Sous deux jours ouvrés, un parcours jour par jour avec hôtels, distances et prix. Rien n'est encore réservé.</p></div></div>
      <div class="acc__i"><button class="acc__q">3 — On l'ajuste ensemble<span>+</span></button>
        <div class="acc__a"><p>Échanger une plage contre un parc, ajouter deux jours, supprimer le vol intérieur. Autant d'allers-retours que nécessaire.</p></div></div>
      <div class="acc__i"><button class="acc__q">4 — Réservations et formalités<span>+</span></button>
        <div class="acc__a"><p>Nous confirmons hôtels et transports, et montons le dossier de visa. Vous recevez un document unique avec tous les contacts.</p></div></div>
      <div class="acc__i"><button class="acc__q">5 — Sur place<span>+</span></button>
        <div class="acc__a"><p>Quelqu'un de notre équipe d'Abidjan vous accueille à l'aéroport, et un numéro reste joignable pendant tout le séjour.</p></div></div>
    </div>
  </div>
</section>
""")

# ---------- DESTINATION DETAIL ----------
PAGES['destination-beaches.html'] = ('Best Beaches in Ivory Coast', 'The southern coast of Côte d\'Ivoire, mapped end to end.', 'dest',
    phero([('index.html','Home'),('destinations.html','Destinations'),('','Best Beaches')], 'Best Beaches in Ivory Coast',
          "Côte d'Ivoire is one of the world's best tourist destinations — for its history, traditions, culture, the warmth of its people and its food, but also for the beauty and variety of the beaches along its entire southern coast.",
          'assets/img/dest/cat-beach.svg') + f"""
<section class="block" data-way>
  <div class="wrap split">
    <div class="rv">
      <div class="eyebrow">The coast</div>
      <h2 class="h-lg">Five hundred kilometres<br>of Atlantic.</h2>
      <p class="lede" style="margin-top:20px">The southern shoreline runs from the Ghanaian border to Liberia: lagoons behind the dunes, fishing villages, and a coast road that makes most of it drivable in a day. These are the stretches we send people to.</p>
      <a class="btn btn--go" style="margin-top:24px" href="contact.html">Build a beach itinerary <svg><use href="#arrow"/></svg></a>
    </div>
    <div class="rv" data-d="2"><img style="border-radius:16px" src="assets/img/dest/cat-eco.svg" alt="Ivorian coastline"></div>
  </div>
</section>

<section class="block services" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Where to go</div><h2 class="h-lg">Three stretches worth<br>the drive</h2></div></div>
    <div class="cards">
      <a class="card rv" data-d="1" href="contact.html"><div class="card__img" style="background-image:url('assets/img/dest/grand-bassam.svg')"></div>
        <span class="card__tag">1 hour from Abidjan</span>
        <div class="card__body"><h3 class="h-md">Grand-Bassam</h3><p>The former colonial capital, a UNESCO World Heritage quarter, with the beach at the end of every street.</p><span class="more">Ask about it <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card rv" data-d="2" href="contact.html"><div class="card__img" style="background-image:url('assets/img/dest/assinie.svg')"></div>
        <span class="card__tag">2 hours</span>
        <div class="card__body"><h3 class="h-md">Assinie</h3><p>A sand spit between lagoon and ocean. Surf, kayaks, boat trips and the best weekend lodges in the country.</p><span class="more">Ask about it <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card card--green rv" data-d="3" href="contact.html"><div class="card__img" style="background-image:url('assets/img/dest/sassandra.svg')"></div>
        <span class="card__tag">4 hours west</span>
        <div class="card__body"><h3 class="h-md">Sassandra</h3><p>A working fishing port with quiet coves either side of it. The quietest option, and the one people remember.</p><span class="more">Ask about it <svg><use href="#arrow"/></svg></span></div></a>
    </div>
  </div>
</section>

<section class="block" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Good to know</div><h2 class="h-lg">Before you pack</h2></div></div>
    <div class="acc rv">
      <div class="acc__i"><button class="acc__q">When is the water best?<span>+</span></button>
        <div class="acc__a"><p>December to April is the main dry season in the south — the calmest sea and the most reliable sunshine. June to September brings the heaviest rain on the coast.</p></div></div>
      <div class="acc__i"><button class="acc__q">Is the Atlantic swimmable everywhere?<span>+</span></button>
        <div class="acc__a"><p>Not everywhere. The open ocean has a strong undertow in places, which is why lagoon-side and sheltered cove locations feature heavily in our itineraries. Your guide will tell you where to swim on each beach.</p></div></div>
      <div class="acc__i"><button class="acc__q">How do we get between beaches?<span>+</span></button>
        <div class="acc__a"><p>By private vehicle with a driver. Grand-Bassam and Assinie are easy day trips from Abidjan; Sassandra is better as an overnight.</p></div></div>
    </div>
  </div>
</section>
""")

# ---------- GOOD DEAL ----------
PAGES['good-deal.html'] = ('Good Deal', 'Hotels, gastronomy and transport in Côte d\'Ivoire.', 'deal',
    phero([('index.html','Home'),('','Good Deal')], 'Good Deal',
          "Where to sleep, what to eat, and how to get around. Everything on this page is somewhere we have actually been.",
          'assets/img/dest/deal-hotel.svg') + f"""
<section class="block" data-way id="hotel">
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow" data-i18n="nav.hotel">Hotel</div><h2 class="h-lg">Places to stay</h2>
      <p class="lede">From lagoon-side lodges in Assinie to business hotels in Plateau. We book the room and you get the rate we get.</p></div></div>
    <div class="duo">
      <a class="tile rv" data-d="1" href="contact.html"><div class="tile__img" style="background-image:url('assets/img/dest/deal-hotel.svg')"></div>
        <div class="tile__body"><span class="card__tag card__tag--static">Coast</span><h3 class="h-md">Lodges &amp; beach houses</h3>
          <p>Assinie, Grand-Bassam and Sassandra — small properties, mostly family-run.</p><span class="more">Ask for options <svg><use href="#arrow"/></svg></span></div></a>
      <a class="tile rv" data-d="2" href="contact.html"><div class="tile__img" style="background-image:url('assets/img/dest/deal-food.svg')"></div>
        <div class="tile__body"><span class="card__tag card__tag--static">Abidjan</span><h3 class="h-md">City hotels</h3>
          <p>Plateau, Cocody and Marcory, chosen for location as much as comfort.</p><span class="more">Ask for options <svg><use href="#arrow"/></svg></span></div></a>
    </div>
  </div>
</section>

<section class="block services" data-way id="gastro">
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow" data-i18n="nav.gastro">Gastronomies</div><h2 class="h-lg">What to eat, and where</h2></div></div>
    <div class="srv rv">
      <div class="srv__i"><h3 class="h-sm">Attiéké &amp; grilled fish</h3><p>Cassava couscous with braised tilapia — the dish to order on your first evening.</p></div>
      <div class="srv__i"><h3 class="h-sm">Maquis</h3><p>Open-air neighbourhood grills. Loud, late, and the best value meal in Abidjan.</p></div>
      <div class="srv__i"><h3 class="h-sm">Kedjenou</h3><p>Chicken slow-cooked in a sealed pot with peppers and tomato. Order it ahead.</p></div>
      <div class="srv__i"><h3 class="h-sm">Garba</h3><p>Fried tuna and attiéké, sold from street kiosks. The national snack.</p></div>
      <div class="srv__i"><h3 class="h-sm">Bangui &amp; bissap</h3><p>Palm wine and hibiscus juice — one for the village, one for the road.</p></div>
      <div class="srv__i srv__i--cta"><h3 class="h-md">Want a food-led itinerary?</h3><p>We build trips around markets, maquis and cooking sessions.</p>
        <a class="btn btn--onDark" href="contact.html">Tell us <svg><use href="#arrow"/></svg></a></div>
    </div>
  </div>
</section>

<section class="block" data-way id="transport">
  <div class="wrap split">
    <div class="rv"><div class="eyebrow" data-i18n="nav.transport">Transport</div>
      <h2 class="h-lg">Getting around,<br>without the guesswork.</h2>
      <p class="lede" style="margin-top:20px">We arrange airport transfers, city drivers and excursion vehicles with drivers we work with regularly. All insured, all reachable on one number for the length of your trip.</p>
      <a class="btn btn--go" style="margin-top:24px" href="contact.html">Arrange transport <svg><use href="#arrow"/></svg></a></div>
    <div class="rv" data-d="2"><img style="border-radius:16px" src="assets/img/dest/cat-beach.svg" alt="Road in Côte d'Ivoire"></div>
  </div>
</section>
""")

# ---------- BLOG ----------
# (titre, date, rubrique, image, filtre[, lien]) — le lien est optionnel :
# sans lui l'article n'est pas encore cliquable.
POSTS = [
    ('Two Cities, One Friendship: Rockville meets Korhogo', '11.12.2026', 'Event',
     'assets/img/dest/event-two-cities.webp', 'washington', 'event-two-cities.html'),
    ("Passport DC: Côte d'Ivoire opens its doors", '04.05.2026', 'Washington', f'assets/img/dest/blog-passport.webp', 'washington'),
    ('Femua, the festival that fills Abidjan', '09.01.2026', 'Culture', f'assets/img/dest/blog-culture.svg', 'culture'),
    ("Côte d'Ivoire, guest of honour at the Embassy Chef Challenge", '16.07.2025', 'Gastronomy', f'assets/img/dest/blog-gastronomy.svg', 'food'),
    ('Where to swim: the beaches worth the drive', '14.05.2025', 'Coastline', f'assets/img/dest/blog-coast.svg', 'travel'),
    ('A first-timer\'s week in Abidjan', '02.04.2025', 'City', f'assets/img/dest/blog-city.svg', 'travel'),
    ('Taï forest: what you actually see', '18.02.2025', 'Nature', f'assets/img/dest/blog-nature.svg', 'travel'),
    ('Five dishes to order before you leave', '11.01.2025', 'Gastronomy', f'assets/img/dest/deal-food.svg', 'food'),
]
posts_html = '\n'.join(f"""      <a class="post grid-item rv" data-cat="{p[4]}" href="{p[5] if len(p) > 5 else '#'}"><div class="post__media"><img src="{p[3]}" alt=""></div>
        <span class="post__date">{p[1]} · {p[2]}</span><h3 class="h-sm">{p[0]}</h3></a>""" for p in POSTS)

PAGES['blog.html'] = ('Blog & News', 'News and travel notes from Côte d\'Ivoire.', 'home',
    phero([('index.html','Home'),('','Blog & News')], 'Blog &amp; News', "Festivals, food, and notes from the road — written by the people who run the trips.", 'assets/img/dest/blog-culture.svg') + f"""
<section class="block" data-way>
  <div class="wrap">
    <div class="filters rv" id="filters">
      <button class="on" data-filter="all">All</button>
      <button data-filter="culture">Culture</button>
      <button data-filter="washington">Washington</button>
      <button data-filter="food">Gastronomy</button>
      <button data-filter="travel">Travel notes</button>
    </div>
    <div class="posts">
{posts_html}
    </div>
  </div>
</section>
""")

# ---------- MEDIATHEQUE ----------
GAL = [f'assets/img/dest/grand-bassam.svg', f'assets/img/dest/korhogo.svg', f'assets/img/dest/tai.svg', f'assets/img/dest/abidjan.svg', f'assets/img/dest/assinie.svg', f'assets/img/dest/comoe.svg', f'assets/img/dest/man.svg', f'assets/img/dest/ehotile.svg']
gal_html = '\n'.join(f'      <button type="button"><img src="{g}" alt="Côte d\'Ivoire"></button>' for g in GAL)

PAGES['mediatheque.html'] = ('Media library', 'Photos and videos of Côte d\'Ivoire.', 'home',
    phero([('index.html','Home'),('','Media library')], 'Media library', "Photographs from our trips and from partners across Côte d'Ivoire. Click any image to open it full size.", 'assets/img/dest/gallery.svg') + f"""
<section class="block" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Photos</div><h2 class="h-lg">The country, as we found it</h2></div></div>
    <div class="gal rv" id="gallery">
{gal_html}
    </div>
  </div>
</section>

<div id="lightbox">
  <button class="lb-btn" id="lbClose" aria-label="Close">&times;</button>
  <button class="lb-btn" id="lbPrev" aria-label="Previous">&#8249;</button>
  <img id="lbImg" alt="">
  <button class="lb-btn" id="lbNext" aria-label="Next">&#8250;</button>
</div>
""")

# ---------- FAQ ----------
FAQS = [
    ('Do American travelers need a visa for Côte d\'Ivoire?', 'Most US passport holders do. We prepare the application file as part of our Travel Assistance service, and yellow fever vaccination is required for entry.'),
    ('When is the best time to go?', 'December to April is the main dry season in the south and the most reliable window for beaches. The north has a different rhythm, with rain concentrated between June and September.'),
    ('Is there a nonstop flight from Washington?', 'No. Itineraries connect through Paris, Brussels, Casablanca or Addis Ababa. We can hold and issue the reservation for you.'),
    ('What language is spoken?', 'French is the official language, alongside around sixty local languages. All our guides work in English.'),
    ('How much does a trip cost?', 'It depends on length, comfort level and group size, so every trip is quoted individually. Send your dates and we come back within two business days with a route and a price.'),
    ('Can you organise trips for groups?', 'Yes — families, church groups, diaspora reunions and small corporate delegations. Above eight people we build the itinerary differently, so tell us the group size early.'),
    ('What about health and safety?', 'We brief you before departure on vaccinations, water, and which areas to avoid, and our Abidjan team is reachable throughout the trip.'),
]
faq_html = '\n'.join(f"""      <div class="acc__i" id="q{i+1}"><button class="acc__q">{q}<span>+</span></button>
        <div class="acc__a"><p>{a}</p></div></div>""" for i, (q, a) in enumerate(FAQS))

PAGES['faq.html'] = ('FAQ', 'Answers about visas, seasons, flights and prices.', 'faq',
    phero([('index.html','Home'),('','FAQ')], 'Frequently asked questions', "Visas, seasons, flights, prices. If your question isn't here, the chat button at the bottom right answers most things instantly.", 'assets/img/dest/hero-2.svg') + f"""
<section class="block" data-way>
  <div class="wrap" style="max-width:900px">
    <div class="acc rv">
{faq_html}
    </div>
  </div>
</section>
""")

# ---------- CONTACT ----------
PAGES['contact.html'] = ('Contact us', 'Plan your trip to Côte d\'Ivoire with Sublime CI-USA.', 'contact',
    phero([('index.html','Home'),('','Contact us')], 'Tell us about your trip', "Dates, group size and what you want out of it. We reply within two business days with a route and a price.", 'assets/img/dest/hero-1.svg') + """
<section class="block" data-way>
  <div class="wrap split">
    <div class="rv">
      <div class="eyebrow">Request a quote</div>
      <div class="alert alert--ok" id="formOk">Thanks — your request is in. We reply within two business days.</div>
      <div class="alert alert--ko" id="formKo"></div>
      <form class="form" id="contactForm" novalidate>
        <div class="row2">
          <div class="field"><label for="fn">First name</label><input id="fn" name="first_name" required><div class="msg">Required.</div></div>
          <div class="field"><label for="ln">Last name</label><input id="ln" name="last_name" required><div class="msg">Required.</div></div>
        </div>
        <div class="row2">
          <div class="field"><label for="em">Email</label><input id="em" type="email" name="email" required><div class="msg">Enter a valid email address.</div></div>
          <div class="field"><label for="ph">Phone</label><input id="ph" type="tel" name="phone"><div class="msg">Required.</div></div>
        </div>
        <div class="row2">
          <div class="field"><label for="tp">Type of trip</label>
            <select id="tp" name="trip_type" required>
              <option value="">Choose one</option>
              <option>Beaches</option><option>Cultural trip</option>
              <option>Adventure &amp; ecotourism</option><option>Mixed / not sure yet</option>
            </select><div class="msg">Required.</div></div>
          <div class="field"><label for="dt">Approximate dates</label><input id="dt" name="dates" placeholder="e.g. March 2027, 10 days"><div class="msg">Required.</div></div>
        </div>
        <div style="position:absolute;left:-9999px" aria-hidden="true">
          <label for="website">Leave this empty</label>
          <input id="website" name="website" type="text" tabindex="-1" autocomplete="off">
          <input id="started" name="started" type="text" tabindex="-1" autocomplete="off" value="">
        </div>
        <div class="field"><label for="ms">Your message</label><textarea id="ms" name="message" required placeholder="How many of you, what you'd like to see, anything we should know."></textarea><div class="msg">Required.</div></div>
        <button type="submit" class="btn btn--go" style="justify-self:start">Send request <svg><use href="#arrow"/></svg></button>
        <p class="formNote">By sending this form you agree that we may contact you about your trip. We do not share your details with anyone else.</p>
      </form>
    </div>

    <div class="rv" data-d="2">
      <div class="routemap">
        <div class="routemap__grid"></div>
        <svg class="arc" viewBox="0 0 400 210" fill="none" aria-hidden="true">
          <path d="M28 168 C 130 34, 268 34, 372 150" stroke="rgba(255,255,255,.28)" stroke-width="2" stroke-dasharray="7 8"/>
          <path id="arcLive" d="M28 168 C 130 34, 268 34, 372 150" stroke="#F77F00" stroke-width="2.4" stroke-linecap="round"/>
          <circle cx="28" cy="168" r="6" fill="#B31942"/><circle cx="28" cy="168" r="12" fill="#B31942" opacity=".22"/>
          <circle cx="372" cy="150" r="6" fill="#009E60"/><circle cx="372" cy="150" r="12" fill="#009E60" opacity=".22"/>
          <g id="arcPlane" style="opacity:0"><use href="#plane" x="-11" y="-11" width="22" height="22" fill="#fff"/></g>
        </svg>
        <div class="routemap__pins"><div class="a"><b>IAD</b>Washington Dulles</div><div class="b"><b>ABJ</b>Félix-Houphouët-Boigny</div></div>
      </div>
      <div class="stats">
        <div><b style="font-size:19px">tourism@ambaciusa.org</b><span>Email</span></div>
        <div><b style="font-size:19px">(240) 756-8332</b><span>Phone</span></div>
        <div style="grid-column:1/-1"><b style="font-size:19px;line-height:1.4">2424 Massachusetts Avenue N.W.<br>Washington, D.C. 20008</b><span>Office</span></div>
      </div>
    </div>
  </div>
</section>
""")

# ============================================================ LISTINGS
from data import HOTELS, RESTOS, VTC

def meta(icon, txt, href=None):
    if not txt: return ''
    inner = f'<a href="{href}">{txt}</a>' if href else txt
    return f'<div><svg><use href="#{icon}"/></svg><span>{inner}</span></div>'

def tel_href(t):
    return 'tel:' + t.split('·')[0].replace(' ', '').strip()

WARN = '<div class="lwarn">Contact details to confirm</div>'

def hotel_card(h):
    name, zone, cap, tel, mail, loc, img, warn = h
    m = meta('beds', f'{cap} rooms' if cap != '—' else 'Capacity n/a')
    m += meta('pin', loc)
    m += meta('phone', tel, tel_href(tel)) if tel else ''
    m += meta('mail', mail, 'mailto:' + mail) if mail else ''
    return f"""      <article class="lcard grid-item rv" data-cat="{zone}" data-name="{name.lower()} {loc.lower()}">
        <div class="lcard__img"><img loading="lazy" src="{img}" alt="{name}"><span class="lcard__zone">{loc.split(',')[0]}</span></div>
        <div class="lcard__b">
          <h3 class="h-sm">{name}</h3>
          <div class="lmeta">{m}</div>
          {WARN if warn else ''}
          <div class="lcard__f"><a class="btn btn--ghost btn--sm" href="contact.html">Book through us <svg><use href="#arrow"/></svg></a></div>
        </div>
      </article>"""

def resto_card(r):
    name, zone, tel, loc, img, warn = r
    m = meta('pin', loc) + (meta('phone', tel, tel_href(tel)) if tel else '')
    return f"""      <article class="lcard grid-item rv" data-cat="{zone}" data-name="{name.lower()} {loc.lower()}">
        <div class="lcard__img"><img loading="lazy" src="{img}" alt="{name}"></div>
        <div class="lcard__b">
          <h3 class="h-sm">{name}</h3>
          <div class="lmeta">{m}</div>
          {WARN if warn else ''}
          <div class="lcard__f"><a class="btn btn--ghost btn--sm" href="contact.html">Reserve a table <svg><use href="#arrow"/></svg></a></div>
        </div>
      </article>"""

def tools(filters, placeholder, total):
    btns = ''.join(f'<button{" class=\"on\"" if i == 0 else ""} data-filter="{k}">{v}</button>' for i, (k, v) in enumerate(filters))
    return f"""    <div class="tools rv">
      <div class="search"><svg><use href="#search"/></svg>
        <input id="listingSearch" type="search" placeholder="{placeholder}" aria-label="{placeholder}"></div>
      <div class="filters" id="filters">{btns}</div>
      <div class="count"><b id="listCount">{total}</b> results</div>
    </div>"""

# ---------- HOTEL ----------
PAGES['hotel.html'] = ('Hotels', 'Hotels in Abidjan — capacity, contacts and neighbourhood.', 'deal',
    phero([('index.html','Home'),('good-deal.html','Good Deal'),('','Hotel')], 'Hotels in Abidjan',
          f"{len(HOTELS)} properties across Cocody, Plateau, Marcory and Port-Bouët, with capacity and direct contacts. Book any of them through us and you get our negotiated rate.",
          f'assets/img/dest/deal-hotel.svg') + f"""
<section class="block" data-way>
  <div class="wrap">
{tools([('all','All'),('cocody','Cocody'),('plateau','Plateau'),('marcory','Marcory'),('portbouet','Port-Bouët')], 'Search a hotel or a neighbourhood…', len(HOTELS))}
    <div class="listing">
{chr(10).join(hotel_card(h) for h in HOTELS)}
    </div>
    <p class="empty" id="listEmpty">No hotel matches that search. Try a neighbourhood name, or ask us directly.</p>
  </div>
</section>

<section class="block services" data-way>
  <div class="wrap split">
    <div class="rv">
      <div class="eyebrow">Booking through Sublime CI-USA</div>
      <h2 class="h-lg">One booking,<br>one contact.</h2>
      <p class="lede" style="margin-top:20px">You can call these hotels yourself — the numbers are right there. But when we book, we hold the room against your itinerary, handle the deposit from the US, and you keep a single point of contact for the whole trip.</p>
      <a class="btn btn--go" style="margin-top:22px" href="contact.html">Ask for availability <svg><use href="#arrow"/></svg></a>
    </div>
    <div class="rv" data-d="2"><img style="border-radius:16px" src="assets/img/dest/deal-hotel.svg" alt="Hotel in Abidjan"></div>
  </div>
</section>
""")

# ---------- GASTRONOMIES ----------
PAGES['gastronomies.html'] = ('Gastronomies', 'Restaurants in Abidjan by neighbourhood.', 'deal',
    phero([('index.html','Home'),('good-deal.html','Good Deal'),('','Gastronomies')], 'Where to eat in Abidjan',
          f"{len(RESTOS)} addresses across Plateau, Cocody, Zone 4 and beyond — from lagoon terraces to Italian kitchens and the maquis worth queueing for.",
          f'assets/img/dest/deal-food.svg') + f"""
<section class="block" data-way>
  <div class="wrap">
{tools([('all','All'),('plateau','Plateau'),('cocody','Cocody & Deux Plateaux'),('zone4','Zone 4 & Marcory'),('autre','Elsewhere')], 'Search a restaurant or a street…', len(RESTOS))}
    <div class="listing">
{chr(10).join(resto_card(r) for r in RESTOS)}
    </div>
    <p class="empty" id="listEmpty">No restaurant matches that search. Try a neighbourhood name, or ask us directly.</p>
  </div>
</section>

<section class="block services" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Ivorian classics</div><h2 class="h-lg">What to order,<br>wherever you sit</h2></div></div>
    <div class="srv rv">
      <div class="srv__i"><h3 class="h-sm">Attiéké &amp; grilled fish</h3><p>Cassava couscous with braised tilapia — the dish to order on your first evening.</p></div>
      <div class="srv__i"><h3 class="h-sm">Kedjenou</h3><p>Chicken slow-cooked in a sealed pot with peppers and tomato. Order it ahead.</p></div>
      <div class="srv__i"><h3 class="h-sm">Garba</h3><p>Fried tuna and attiéké, sold from street kiosks. The national snack.</p></div>
      <div class="srv__i"><h3 class="h-sm">Sauce graine</h3><p>Palm nut stew with fish or beef, served over rice. Rich, and worth the nap after.</p></div>
      <div class="srv__i"><h3 class="h-sm">Alloco</h3><p>Fried plantain with chilli onion relish. Ordered as a side, eaten as a meal.</p></div>
      <div class="srv__i srv__i--cta"><h3 class="h-md">Want a food-led itinerary?</h3><p>Markets, maquis and cooking sessions, built into the route.</p>
        <a class="btn btn--onDark" href="contact.html">Tell us <svg><use href="#arrow"/></svg></a></div>
    </div>
  </div>
</section>
""")

# ---------- TRANSPORT ----------
vtc_cards = '\n'.join(f"""      <article class="lcard rv" data-d="{i+1}">
        <div class="lcard__img lcard__img--logo" style="background:#0A3161"><img loading="lazy" src="{logo}" alt="{n}"></div>
        <div class="lcard__b"><h3 class="h-sm">{n}</h3><p class="lp">{d}</p>
          <div class="lcard__f"><a class="btn btn--ghost btn--sm" href="{href}" target="_blank" rel="noopener">{cta} <svg><use href="#arrow"/></svg></a></div></div>
      </article>""" for i, (n, d, href, cta, logo) in enumerate(VTC))

PAGES['transport.html'] = ('Transport', 'Car rental, ride-hailing and private drivers in Côte d\'Ivoire.', 'deal',
    phero([('index.html','Home'),('good-deal.html','Good Deal'),('','Transport')], 'Getting around Côte d\'Ivoire',
          "Whether you are visiting or living here, several options cover your journeys. Here are the main ones, and what each is good for.",
          f'assets/img/dest/deal-transport.svg') + f"""
<section class="block" data-way>
  <div class="wrap split">
    <div class="rv">
      <div class="eyebrow">Option 1</div>
      <h2 class="h-lg">Car rental</h2>
      <p class="lede" style="margin-top:18px">For maximum freedom, rent a vehicle from a certified agency.</p>
      <ul class="ticks">
        <li>Freedom, autonomy and flexibility to explore the country at your own pace</li>
        <li>Access to places well off the usual routes</li>
        <li>Comfort and convenience, and a schedule that is entirely yours</li>
      </ul>
      <a class="btn btn--go" style="margin-top:22px" href="contact.html">Ask us to arrange it <svg><use href="#arrow"/></svg></a>
    </div>
    <div class="rv" data-d="2"><img style="border-radius:16px" src="assets/img/dest/deal-transport.svg" alt="Car rental in Côte d'Ivoire"></div>
  </div>
</section>

<section class="block services" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Option 2</div><h2 class="h-lg">Ride-hailing (VTC)</h2>
      <p class="lede">For more comfort, tighter regulation, drivers who know the city, and the ability to book at any hour, use a ride-hailing service. Three platforms operate in Abidjan.</p></div></div>
    <div class="listing listing--3">
{vtc_cards}
    </div>
  </div>
</section>

<section class="block" data-way>
  <div class="wrap split">
    <div class="rv"><div class="eyebrow">Option 3</div>
      <h2 class="h-lg">Private driver,<br>arranged by us.</h2>
      <p class="lede" style="margin-top:18px">For airport transfers and excursions we work with drivers we know, insured and reachable on one number for the whole trip. It is the option most of our travelers end up taking outside Abidjan, where apps thin out.</p>
      <a class="btn btn--go" style="margin-top:22px" href="contact.html">Arrange transport <svg><use href="#arrow"/></svg></a></div>
    <div class="rv" data-d="2"><img style="border-radius:16px" src="assets/img/dest/cat-beach.svg" alt="Road in Côte d'Ivoire"></div>
  </div>
</section>
""")

# ---------- GOOD DEAL : page d'aiguillage ----------
PAGES['good-deal.html'] = ('Good Deal', 'Hotels, gastronomy and transport in Côte d\'Ivoire.', 'deal',
    phero([('index.html','Home'),('','Good Deal')], 'Good Deal',
          "Where to sleep, what to eat, how to get around. Three directories, all of them addresses we use ourselves.",
          'assets/img/dest/deal-hotel.svg') + f"""
<section class="block" data-way>
  <div class="wrap">
    <div class="cards">
      <a class="card rv" data-d="1" href="hotel.html">
        <div class="card__img" style="background-image:url('assets/img/dest/deal-hotel.svg')"></div>
        <span class="card__tag">{len(HOTELS)} properties</span>
        <div class="card__body"><h3 class="h-md" data-i18n="nav.hotel">Hotel</h3>
          <p>Cocody, Plateau, Marcory, Port-Bouët — capacity, contacts and neighbourhood for each one.</p>
          <span class="more">Browse hotels <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card rv" data-d="2" href="gastronomies.html">
        <div class="card__img" style="background-image:url('assets/img/dest/deal-food.svg')"></div>
        <span class="card__tag">{len(RESTOS)} addresses</span>
        <div class="card__body"><h3 class="h-md" data-i18n="nav.gastro">Gastronomies</h3>
          <p>Lagoon terraces, Italian kitchens, maquis and the classics to order on your first night.</p>
          <span class="more">Browse restaurants <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card card--green rv" data-d="3" href="transport.html">
        <div class="card__img" style="background-image:url('assets/img/dest/deal-transport.svg')"></div>
        <span class="card__tag">3 options</span>
        <div class="card__body"><h3 class="h-md" data-i18n="nav.transport">Transport</h3>
          <p>Car rental, ride-hailing apps, and private drivers arranged through us.</p>
          <span class="more">See the options <svg><use href="#arrow"/></svg></span></div></a>
    </div>
  </div>
</section>
""")


# ---------- 404 ----------
PAGES['404.html'] = ('Page not found', 'This page does not exist.', 'home', """
<section class="phero" style="text-align:center">
  <div class="phero__bg" style="background-image:url('https://ciusatourism.com/wp-content/uploads/2025/03/image-AM-423-424-page-72-73_0-1024x649.jpg')"></div>
  <svg class="phero__plane" aria-hidden="true"><use href="#plane"/></svg>
  <div class="wrap">
    <div class="eyebrow eyebrow--light eyebrow--center">Error 404</div>
    <h1 class="h-xl">This route<br>doesn't exist.</h1>
    <p class="lede" style="color:rgba(255,255,255,.74);margin:20px auto 30px">The page you were looking for has moved or never existed. The ones below definitely do.</p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center">
      <a class="btn btn--go" href="index.html">Back to home <svg><use href="#arrow"/></svg></a>
      <a class="btn btn--onDark" href="destinations.html">See destinations</a>
      <a class="btn btn--onDark" href="contact.html">Contact us</a>
    </div>
  </div>
</section>
""")


# ============================================================ DESTINATIONS



def place_card(p, i):
    name, img = p['name'], cover(p['img'])
    dist, desc = pick(p['dist']), pick(p['desc'])
    tags = ''.join(f'<li>{pick(t)}</li>' for t in p['tips'])
    flip = ' place--flip' if i % 2 else ''
    return f"""      <article class="place{flip} rv">
        <div class="place__media"><img loading="lazy" src="{img}" alt="{name}">
          <span class="place__dist">{dist}</span></div>
        <div class="place__body">
          <h3 class="h-md">{name}</h3>
          <p>{desc}</p>
          <ul class="ticks ticks--sm">{tags}</ul>
          <a class="btn btn--ghost btn--sm" href="{slug_of(name)}">Discover {name} <svg><use href="#arrow"/></svg></a>
        </div>
      </article>"""


def faq_block(items):
    return '\n'.join(f"""      <div class="acc__i"><button class="acc__q">{pick(q)}<span>+</span></button>
        <div class="acc__a"><p>{pick(a)}</p></div></div>""" for q, a in items)


def destination_page(key, title, sub, intro_h, intro_p, places, faqs, hero, cta):
    return (phero([('index.html', 'Home'), ('destinations.html', 'Destinations'), ('', title)],
                  title, sub, hero) + f"""
<section class="block" data-way>
  <div class="wrap split">
    <div class="rv">
      <div class="eyebrow">{title}</div>
      <h2 class="h-lg">{intro_h}</h2>
      <p class="lede" style="margin-top:20px">{intro_p}</p>
      <a class="btn btn--go" style="margin-top:24px" href="contact.html">{cta} <svg><use href="#arrow"/></svg></a>
    </div>
    <div class="rv" data-d="2"><img style="border-radius:16px" src="{places[0]['img']}" alt="{places[0]['name']}"></div>
  </div>
</section>

<section class="block services" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">{len(places)} places</div>
      <h2 class="h-lg">Where we take<br>our travellers<svg class="flyin"><use href="#plane"/></svg></h2></div></div>
    <div class="places">
{chr(10).join(place_card(p, i) for i, p in enumerate(places))}
    </div>
  </div>
</section>

<section class="block" data-way>
  <div class="wrap" style="max-width:900px">
    <div class="head rv"><div><div class="eyebrow">Good to know</div><h2 class="h-lg">Frequently asked</h2></div></div>
    <div class="acc rv">
{faq_block(faqs)}
    </div>
  </div>
</section>
""")


PAGES['destination-beaches.html'] = ('Beaches & coastline', "The Ivorian coastline, from Grand-Bassam to San Pedro.", 'dest',
    destination_page('beach', 'Beaches &amp; coastline',
        "Five hundred kilometres of Atlantic, lagoons behind the dunes and a coast "
        "road that makes most of it reachable in a day.",
        "From lagoon to ocean,<br>east to west.",
        "The coast runs from the Ghanaian border to Liberia. To the east, the lagoons "
        "and coconut groves of Assinie and Grand-Bassam, an hour or two from Abidjan. "
        "To the west it turns wilder, down to Sassandra and San Pedro. Each stretch "
        "has its own character, and you can chain them or keep just one.",
        BEACHES, BEACH_FAQ, 'assets/img/dest/deal-food.svg',
        'Build a coastal itinerary'))

PAGES['destination-culture.html'] = ('Cultural trips', "Festivals, masks, crafts and heritage in Côte d'Ivoire.", 'dest',
    destination_page('culture', 'Cultural trips',
        "Around sixty languages, mask traditions that are still alive, recognised "
        "crafts and festivals that bring the whole country together.",
        "Living traditions,<br>not a museum.",
        "Côte d'Ivoire has more than sixty cultural groups, and it shows in "
        "everything: the music, the cloth, the masks, the food. Our cultural trips "
        "are built around real encounters — craft workshops, markets, ceremonies "
        "when the village calendar allows — with Ivorian guides who explain the "
        "context and the etiquette.",
        CULTURE, CULTURE_FAQ, 'assets/img/dest/cat-culture.svg',
        'Build a cultural trip'))

PAGES['destination-eco.html'] = ('Adventure & ecotourism', "National parks, primary rainforest and the western highlands.", 'dest',
    destination_page('eco', 'Adventure &amp; ecotourism',
        "Two World Heritage parks, one of the last primary rainforests in West "
        "Africa, and a mountain range in the west.",
        "From primary forest<br>to eighteen mountains.",
        "The country holds three environments within a short distance: the rainforest "
        "of the south-west, the savanna of the north-east, and the western highlands "
        "around Man. We work in small groups, with local guides and community "
        "accommodation — which is what supports the surrounding villages, and "
        "therefore what protects the parks.",
        ECO, ECO_FAQ, 'assets/img/dest/cat-eco.svg',
        'Build a nature trip'))



# ============================================================ PAGES LIEU
from places import PLACES

CAT_INFO = {
    'beach':   ('Beaches &amp; coastline', 'destination-beaches.html'),
    'culture': ('Cultural trips', 'destination-culture.html'),
    'eco':     ('Adventure &amp; ecotourism', 'destination-eco.html'),
}


def _e(v):
    return v[0] if isinstance(v, tuple) else v


def place_page(pl):
    cat_name, cat_page = CAT_INFO[pl['cat']]
    paras = ''.join(f'<p>{x.strip()}</p>' for x in _e(pl['intro']).split('\n\n'))

    see = '\n'.join(f"""      <div class="feat rv" data-d="{min(i, 3)}">
        <h3 class="h-sm">{_e(t)}</h3><p>{_e(x)}</p></div>""" for i, (t, x) in enumerate(pl['see']))

    events = ''
    if pl['events']:
        ev = '\n'.join(f"""      <div class="feat feat--wide rv">
        <h3 class="h-md">{_e(t)}</h3><p>{_e(x)}</p></div>""" for t, x in pl['events'])
        events = f"""
<section class="block" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Festivals &amp; events</div>
      <h2 class="h-lg">When to be there</h2></div></div>
    <div class="feats feats--one">
{ev}
    </div>
  </div>
</section>"""

    facts = '\n'.join(f"""        <div><span>{_e(k)}</span><b>{_e(v)}</b></div>"""
                      for k, v in pl['facts'])

    others = [o for o in PLACES if o['cat'] == pl['cat'] and o['slug'] != pl['slug']][:3]
    near = '\n'.join(f"""      <a class="card rv" data-d="{i + 1}" href="place-{o['slug']}.html">
        <div class="card__img" style="background-image:url('{o['img']}')"></div>
        <span class="card__tag">{_e(o['tag']).split(' · ')[-1]}</span>
        <div class="card__body"><h3 class="h-md">{o['name']}</h3>
          <p>{_e(o['lede'])}</p>
          <span class="more">Explore <svg><use href="#arrow"/></svg></span></div></a>"""
                      for i, o in enumerate(others))

    return (phero([('index.html', 'Home'), ('destinations.html', 'Destinations'),
                   (cat_page, cat_name), ('', pl['name'])],
                  pl['name'], _e(pl['lede']), pl['img']) + f"""
<section class="block" data-way>
  <div class="wrap split">
    <div class="rv">
      <div class="eyebrow">{_e(pl['tag'])}</div>
      <div class="prose">{paras}</div>
      <a class="btn btn--go" style="margin-top:26px" href="contact.html">Add {pl['name']} to my trip <svg><use href="#arrow"/></svg></a>
    </div>
    <div class="rv" data-d="2">
      <img style="border-radius:16px" src="{pl['img']}" alt="{pl['name']}">
      <div class="facts">
{facts}
      </div>
    </div>
  </div>
</section>

<section class="block services" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">What to see</div>
      <h2 class="h-lg">On the ground<svg class="flyin"><use href="#plane"/></svg></h2></div></div>
    <div class="feats">
{see}
    </div>
  </div>
</section>
{events}
<section class="block" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">Nearby</div>
      <h2 class="h-lg">Often combined with</h2></div>
      <a class="btn btn--ghost" href="{cat_page}">All of {cat_name} <svg><use href="#arrow"/></svg></a></div>
    <div class="cards">
{near}
    </div>
  </div>
</section>
""")


for _pl in PLACES:
    PAGES[f"place-{_pl['slug']}.html"] = (
        _pl['name'], _e(_pl['lede'])[:155], 'dest', place_page(_pl))

# ============================================================ VERSION FR
# Les pages anglaises sont générées à la racine, les françaises dans fr/.
# Le sélecteur EN/FR du header navigue de l'une à l'autre.

def to_french(html, page):
    from lang_fr import all_pairs
    for a, b in all_pairs():
        html = html.replace(a, b)

    # chemins : depuis fr/, les ressources sont un cran au-dessus
    html = re.sub(r'(href|src)="(assets/|api/)', r'\1="../\2', html)
    # liens internes : rester dans fr/
    html = html.replace('href="./"', 'href="./"')
    # sélecteur de langue
    tgt = ('' if page == 'index.html' else page[:-5]) if CLEAN else page
    html = html.replace('<a class="langs__a on" href="#" data-lang="en" aria-current="page">EN</a>',
                        f'<a class="langs__a" href="../{tgt}" data-lang="en">EN</a>')
    frlink = 'fr/' if (CLEAN and page == 'index.html') else f'fr/{tgt}'
    html = html.replace(f'<a class="langs__a" href="{frlink}" data-lang="fr">FR</a>',
                        '<a class="langs__a on" href="#" data-lang="fr" aria-current="page">FR</a>')
    html = html.replace('<html lang="en">', '<html lang="fr">')

    # le <title> n'est pas un nœud de texte : il passe à travers le
    # remplacement général, on le traduit explicitement
    import re as _re
    m = _re.search(r'<title>(.*?) — ', html)
    if m:
        for a, b in all_pairs():
            if a == m.group(1):
                html = html.replace(f'<title>{a} — ', f'<title>{b} — ', 1)
                break
    return html


def add_hreflang(html, page, lang):
    """Indique à Google que les deux versions sont équivalentes."""
    base = 'https://ciusatourism.com/'
    tags = ('<link rel="alternate" hreflang="en" href="' + base + page + '">\n'
            '<link rel="alternate" hreflang="fr" href="' + base + 'fr/' + page + '">\n'
            '<link rel="alternate" hreflang="x-default" href="' + base + page + '">\n')
    return html.replace('<link rel="stylesheet"', tags + '<link rel="stylesheet"', 1)


# Image affichée quand on colle le lien dans un e-mail, WhatsApp, Facebook,
# LinkedIn. Format JPG obligatoire : plusieurs plateformes ignorent le WebP.
OG_IMAGE = {
    'event-two-cities.html': 'assets/img/dest/event-two-cities.jpg',
    'blog.html':             'assets/img/dest/blog-passport.jpg',
}
OG_DEFAULT = 'assets/img/og-default.jpg'

OG_SIZE = {
    'assets/img/dest/event-two-cities.jpg': (1500, 703),
    'assets/img/dest/blog-passport.jpg': (1200, 800),
    'assets/img/og-default.jpg': (1200, 630),
}


def add_og(html, page, lang):
    """Aperçu du lien : titre, texte et image. Sans ces balises, un lien
    partagé n'affiche qu'une URL nue."""
    base = 'https://ciusatourism.com/'
    url = base + ('fr/' if lang == 'fr' else '') + ('' if page == 'index.html'
          else (page[:-5] if CLEAN else page))
    rel = OG_IMAGE.get(page, OG_DEFAULT)
    img = base + rel
    w, h = OG_SIZE.get(rel, (1200, 630))

    m = re.search(r'<title>(.*?)</title>', html, re.S)
    title = m.group(1).strip() if m else 'Sublime CI-USA'
    m = re.search(r'<meta name="description" content="(.*?)">', html, re.S)
    desc = m.group(1).strip() if m else ''

    tags = (f'<meta property="og:type" content="website">\n'
            f'<meta property="og:site_name" content="Sublime CI-USA">\n'
            f'<meta property="og:locale" content="{"fr_FR" if lang == "fr" else "en_US"}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{img}">\n'
            f'<meta property="og:image:width" content="{w}">\n'
            f'<meta property="og:image:height" content="{h}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{title}">\n'
            f'<meta name="twitter:description" content="{desc}">\n'
            f'<meta name="twitter:image" content="{img}">\n')
    return html.replace('<link rel="preconnect"', tags + '<link rel="preconnect"', 1)


def build_fr():
    """Les pages françaises vont dans fr/. Elles référencent ../assets et
    /api : rien n'est dupliqué, il n'y a qu'un seul jeu de ressources."""
    fr_dir = ROOT / 'fr'
    fr_dir.mkdir(exist_ok=True)
    for fname in PAGES:
        src = (ROOT / fname).read_text(encoding='utf-8')
        out = to_french(src, fname)
        out = re.sub(r'\s*<meta (?:property="og:|name="twitter:)[^>]*>', '', out)
        out = add_og(out, fname, 'fr')
        (fr_dir / fname).write_text(out, encoding='utf-8')
    print(f'✓ fr/ : {len(PAGES)} pages')


def check_fr():
    """Signale les phrases anglaises qui n'ont pas de traduction."""
    import re as _re
    from lang_fr import all_pairs
    known = {a for a, _ in all_pairs()}
    misses = {}
    for fname in PAGES:
        html = (ROOT / 'fr' / fname).read_text(encoding='utf-8')
        body = _re.sub(r'<(script|style|svg)[^>]*>.*?</\1>', '', html, flags=_re.S)
        for txt in _re.findall(r'>([^<>{}]{25,})<', body):
            t = txt.strip()
            if not t or t in known:
                continue
            # heuristique : mots typiquement anglais
            if _re.search(r'\b(the|and|with|your|from|that|this|when|what|our|you|we|are|is)\b', t, _re.I):
                misses.setdefault(fname, []).append(t[:90])
    # les méta-descriptions ne sont pas dans le corps : on les vérifie à part
    for fname in PAGES:
        def d(path):
            m = _re.search(r'name="description" content="([^"]*)"',
                           (ROOT / path).read_text(encoding='utf-8'))
            return m.group(1) if m else ''
        en_d, fr_d = d(fname), d('fr/' + fname)
        if en_d and en_d == fr_d:
            misses.setdefault(fname, []).append('[meta] ' + en_d[:70])

    total = sum(len(v) for v in misses.values())
    print(f'\n--- contrôle FR : {total} segments non traduits ---')
    for f, items in misses.items():
        print(f'\n{f}')
        for i in items[:12]:
            print('   ', i)
    return total



# ============================================================ ÉVÉNEMENT
# Page d'un événement ponctuel. Pour en ajouter un autre, dupliquer le bloc
# et changer les constantes ci-dessous. Le formulaire RSVP est sur la page
# même (section #rsvp) et envoie vers api/rsvp.php : enregistrement hors du
# web, alerte à l'équipe, confirmation à l'invité.

EVENT_FACTS = [
    ('Date', 'Friday, December 11, 2026'),
    ('Time', '6:00 PM – 10:00 PM'),
    ('Venue', 'Glenview Mansion'),
    ('Address', '603 Edmonston Drive<br>Rockville, MD 20851'),
]

_facts = '\n'.join(
    f'        <div><span>{k}</span><b>{v}</b></div>' for k, v in EVENT_FACTS)

PAGES['event-two-cities.html'] = (
    'Two Cities, One Friendship',
    "Rockville, Maryland and Korhogo, Côte d'Ivoire — a celebration of culture "
    "and heritage, December 11, 2026.",
    'home',
    phero([('index.html', 'Home'), ('blog.html', 'Blog &amp; News'),
           ('', 'Two Cities, One Friendship')],
          'Two Cities,<br>One Friendship',
          "Rockville, Maryland and Korhogo, Côte d'Ivoire — an evening of culture, music and heritage. Friday, December 11, 2026.",
          'assets/img/dest/event-two-cities.webp') + f"""
<section class="block block--tight" data-way>
  <div class="wrap">
    <div class="evcard rv">
      <div class="evcard__facts">
{_facts}
      </div>
      <div class="evcard__cta">
        <p>Admission is by invitation. Let us know you are coming so we can plan the evening.</p>
        <a class="btn btn--go" href="#rsvp">RSVP for this event <svg><use href="#arrow"/></svg></a>
      </div>
    </div>
  </div>
</section>

<section class="block" data-way>
  <div class="wrap split">
    <div class="rv">
      <div class="eyebrow">The evening</div>
      <h2 class="h-lg">One evening,<br>two cultures.</h2>
      <div class="prose">
        <p>On December 11, Glenview Mansion in Rockville becomes the meeting point between Maryland and northern Côte d'Ivoire. The evening celebrates what the two communities share and what each brings: music, dance, craft, food and the people who carry them.</p>
        <p>Ivorian rhythms and dance, the woven and painted textiles of the Senufo country, and a table that puts the two cuisines side by side. It is a cultural evening before it is a formal one — come to meet people.</p>
      </div>
      <a class="btn btn--go" style="margin-top:26px" href="#rsvp">Reserve your place <svg><use href="#arrow"/></svg></a>
    </div>
    <div class="rv" data-d="2">
      <img class="evposter" src="assets/img/dest/event-two-cities-poster.webp" alt="Two Cities, One Friendship — December 11, 2026, Glenview Mansion, Rockville">
    </div>
  </div>
</section>

<section class="block rsvp" id="rsvp" data-way>
  <div class="wrap rsvp__wrap">
    <div class="head rv"><div><div class="eyebrow">RSVP</div>
      <h2 class="h-lg">Will you join us?</h2>
      <p class="lede">It takes a minute. You will receive a confirmation by email right away.</p></div></div>
    <div class="alert alert--ok" id="rsvpOk" role="status"></div>
    <div class="alert alert--ko" id="rsvpKo" role="alert"></div>
    <form class="form rsvp__form rv" id="rsvpForm" novalidate
      data-ok-yes="Thank you — your place is confirmed. A confirmation is on its way to your inbox."
      data-ok-no="Thank you for letting us know. We hope to see you at a future event."
      data-err-fields="Please check the highlighted fields."
      data-err-rate="Too many attempts. Please try again in an hour, or email tourism@ambaciusa.org."
      data-err-server="Something went wrong on our side. Email tourism@ambaciusa.org and we will add you to the list."
      data-err-net="Could not reach the server. Check your connection, or email tourism@ambaciusa.org."
      data-sending="Sending…">
      <input type="hidden" name="lang" value="en">
      <div class="field field--choice" id="attField"><span class="lbl">Can you attend?</span>
        <div class="choice">
          <label><input type="radio" name="attending" value="yes" required><span>Yes, I'll be there</span></label>
          <label><input type="radio" name="attending" value="no"><span>Sorry, can't make it</span></label>
        </div><div class="msg">Please choose one.</div></div>
      <div class="row2">
        <div class="field"><label for="rv-name">Full name</label><input id="rv-name" name="name" autocomplete="name" required><div class="msg">Required.</div></div>
        <div class="field"><label for="rv-email">Email</label><input id="rv-email" type="email" name="email" autocomplete="email" required><div class="msg">Enter a valid email address.</div></div>
      </div>
      <div class="row2">
        <div class="field"><label for="rv-phone">Phone <i>(optional)</i></label><input id="rv-phone" type="tel" name="phone" autocomplete="tel"></div>
        <div class="field"><label for="rv-heard">How did you hear about this event?</label>
          <select id="rv-heard" name="heard">
            <option value="">Choose one</option>
            <option value="website">Website</option>
            <option value="friend">Friend</option>
            <option value="newsletter">Newsletter</option>
            <option value="ad">Advertisement</option>
          </select></div>
      </div>
      <div class="field" id="guestsField"><label for="rv-guests">What are the names of people attending?</label>
        <input id="rv-guests" name="guests" placeholder="Including yourself — e.g. Jane Doe, John Doe"></div>
      <div class="field"><label for="rv-comments">Comments and/or questions</label>
        <textarea id="rv-comments" name="comments" rows="4"></textarea></div>
      <div style="position:absolute;left:-9999px" aria-hidden="true">
        <label for="rv-website">Leave this empty</label>
        <input id="rv-website" name="website" type="text" tabindex="-1" autocomplete="off">
        <input class="started" name="started" type="text" tabindex="-1" autocomplete="off" value="">
      </div>
      <button type="submit" class="btn btn--go" style="justify-self:start">Send my RSVP <svg><use href="#arrow"/></svg></button>
      <p class="formNote">We use these details only to organise the evening and will not share them.</p>
    </form>
  </div>
</section>

<section class="block services" data-way>
  <div class="wrap">
    <div class="head rv"><div><div class="eyebrow">The other city</div>
      <h2 class="h-lg">Where Korhogo sits<svg class="flyin"><use href="#plane"/></svg></h2>
      <p class="lede">Korhogo is the capital of northern Côte d'Ivoire and the heart of Senufo country — the region behind the painted cloth, the carving and the weaving you will see at Glenview Mansion.</p></div>
      <a class="btn btn--ghost" href="place-korhogo.html">Discover Korhogo <svg><use href="#arrow"/></svg></a></div>
    <div class="cards">
      <a class="card rv" data-d="1" href="place-korhogo.html">
        <div class="card__img" style="background-image:url('assets/img/dest/korhogo.webp')"></div>
        <span class="card__tag">Northern Côte d'Ivoire</span>
        <div class="card__body"><h3 class="h-md">Korhogo</h3>
          <p>Capital of the north, heart of Senufo country, and home of the painted cloth that became an emblem of the country.</p>
          <span class="more">Explore <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card rv" data-d="2" href="destination-culture.html">
        <div class="card__img" style="background-image:url('assets/img/dest/cat-culture.webp')"></div>
        <span class="card__tag">6 places</span>
        <div class="card__body"><h3 class="h-md">Cultural trips</h3>
          <p>Festivals, mask traditions, craft workshops and markets — the trips built around the culture you will meet that evening.</p>
          <span class="more">See the culture <svg><use href="#arrow"/></svg></span></div></a>
      <a class="card card--green rv" data-d="3" href="contact.html">
        <div class="card__img" style="background-image:url('assets/img/dest/cat-beach.webp')"></div>
        <span class="card__tag">Plan a trip</span>
        <div class="card__body"><h3 class="h-md">Go and see for yourself</h3>
          <p>If the evening makes you want to travel, we build the itinerary — from Washington to Abidjan and up to Korhogo.</p>
          <span class="more">Talk to us <svg><use href="#arrow"/></svg></span></div></a>
    </div>
  </div>
</section>

<section class="block" data-way>
  <div class="wrap" style="max-width:900px">
    <div class="head rv"><div><div class="eyebrow">Good to know</div>
      <h2 class="h-lg">Before you come</h2></div></div>
    <div class="acc rv">
      <div class="acc__i"><button class="acc__q">How do I confirm my attendance?<span>+</span></button>
        <div class="acc__a"><p>Confirm through the RSVP form on this page, listing everyone coming with you so the welcome desk has their names. You can also call <a href="tel:+12404763562">(240) 476-3562</a> or <a href="tel:+12027254992">(202) 725-4992</a>.</p></div></div>
      <div class="acc__i"><button class="acc__q">Where exactly is Glenview Mansion?<span>+</span></button>
        <div class="acc__a"><p>603 Edmonston Drive, Rockville, MD 20851, inside Rockville Civic Center Park. On-site parking is available in the park.</p></div></div>
      <div class="acc__i"><button class="acc__q">Can I bring guests?<span>+</span></button>
        <div class="acc__a"><p>Yes — list them by name in the RSVP form so we can account for them.</p></div></div>
      <div class="acc__i"><button class="acc__q">Who do I contact with a question?<span>+</span></button>
        <div class="acc__a"><p>Write to <a href="mailto:tourism@ambaciusa.org">tourism@ambaciusa.org</a>, or leave your question in the comments box at the end of the RSVP form.</p></div></div>
    </div>
  </div>
</section>
""")

# ============================================================ SITEMAP
SITE = 'https://ciusatourism.com'
PRIORITY = {'index.html': '1.0', 'destinations.html': '0.9', 'hotel.html': '0.9',
            'event-two-cities.html': '0.9',
            'destination-beaches.html': '0.85', 'destination-culture.html': '0.85',
            'destination-eco.html': '0.85',
            'gastronomies.html': '0.9', 'contact.html': '0.8',
            'transport.html': '0.8', 'good-deal.html': '0.7',
            '404.html': None}


def sitemap(pages):
    import datetime
    today = datetime.date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for f in pages:
        prio = PRIORITY.get(f, '0.7')
        if prio is None:
            continue
        for prefix in ('', 'fr/'):
            loc = SITE + '/' + prefix + ('' if f == 'index.html' else f)
            alt = ''.join(
                f'\n    <xhtml:link rel="alternate" hreflang="{lg}" href="{SITE}/{px}{"" if f == "index.html" else f}"/>'
                for lg, px in (('en', ''), ('fr', 'fr/')))
            out.append(f'  <url>\n    <loc>{loc}</loc>{alt}\n    <lastmod>{today}</lastmod>'
                       f'\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n  </url>')
    out.append('</urlset>')
    return '\n'.join(out) + '\n'


# ============================================================ WRITE
if '--php' not in sys.argv:
    for fname, (title, desc, cur, body) in PAGES.items():
        html = clean_links(localize(head(title, desc, cur) + header(cur) + body + FOOTER))
        html = prefer_photos(html)
        frpath = 'fr/' if (CLEAN and fname == 'index.html') else 'fr/' + (fname[:-5] if CLEAN else fname)
        html = html.replace('__FRPATH__', frpath)
        html = add_hreflang(html, fname, 'en')
        html = add_og(html, fname, 'en')
        (ROOT / fname).write_text(html, encoding='utf-8')
        print('✓', fname, len(html) // 1024, 'kB')

(ROOT / 'sitemap.xml').write_text(sitemap(PAGES.keys()), encoding='utf-8')
print('✓ sitemap.xml')

# ============================================================ MODE PHP
# python3 build.py --php  génère une version .php avec partials/
# Le HTML produit est identique ; seuls l'en-tête et le pied de page
# sont sortis dans partials/header.php et partials/footer.php.

def build_php():
    import shutil
    php_dir = ROOT / 'php'
    if php_dir.exists():
        shutil.rmtree(php_dir)
    (php_dir / 'partials').mkdir(parents=True)

    # --- header.php : tout ce qui précède le contenu de la page ---
    sample_head = head('__TITLE__', '__DESC__', '__CUR__')
    sample_hdr = header('__CUR__')

    hdr = sample_head + sample_hdr
    hdr = hdr.replace('__TITLE__', "<?= htmlspecialchars($page_title ?? 'Sublime CI-USA') ?>")
    hdr = hdr.replace('__DESC__', "<?= htmlspecialchars($page_desc ?? '') ?>")
    # état actif de la navigation, calculé en PHP
    hdr = hdr.replace(' class="nav__item current"', ' class="nav__item"')
    for name in ('home', 'faq', 'dest', 'deal', 'contact'):
        hdr = hdr.replace(
            f'<div class="nav__item"><a class="nav__link" href="{NAV_HREF[name]}"',
            f'<div class="nav__item<?= ($current ?? \'\') === \'{name}\' ? \' current\' : \'\' ?>">'
            f'<a class="nav__link" href="{NAV_HREF[name]}"', 1)
    hdr = hdr.replace('body data-page="__CUR__"', "body data-page=\"<?= htmlspecialchars($current ?? '') ?>\"")
    hdr = hdr.replace('__CUR__', '')

    header_php = ("<?php\n"
                  "/* partials/header.php — variables attendues :\n"
                  "     $page_title  titre de l'onglet\n"
                  "     $page_desc   meta description\n"
                  "     $current     home | faq | dest | deal | contact\n"
                  "*/\n?>\n") + hdr

    footer_php = "<?php /* partials/footer.php */ ?>\n" + FOOTER

    (php_dir / 'partials' / 'header.php').write_text(
        clean_links_php(localize(header_php)), encoding='utf-8')
    (php_dir / 'partials' / 'footer.php').write_text(
        clean_links_php(localize(footer_php)), encoding='utf-8')

    # --- pages ---
    for fname, (title, desc, cur, body) in PAGES.items():
        name = fname[:-5]
        page = (f"<?php\n"
                f"$page_title = {php_str(title)};\n"
                f"$page_desc  = {php_str(desc)};\n"
                f"$current    = '{cur}';\n"
                f"include __DIR__ . '/partials/header.php';\n"
                f"?>\n"
                + clean_links_php(localize(body)) +
                "\n<?php include __DIR__ . '/partials/footer.php'; ?>\n")
        (php_dir / (name + '.php')).write_text(page, encoding='utf-8')
        print('✓ php/' + name + '.php')

    # --- assets et configuration ---
    for item in ('assets', 'api', 'storage', '.htaccess', 'robots.txt', 'sitemap.xml', '.well-known'):
        src = ROOT / item
        if not src.exists():
            continue
        dst = php_dir / item
        shutil.copytree(src, dst) if src.is_dir() else shutil.copy(src, dst)

    print('\n→ dossier php/ prêt : ' + str(php_dir))


NAV_HREF = {'home': 'index.html', 'faq': 'faq.html', 'dest': 'destinations.html',
            'deal': 'good-deal.html', 'contact': 'contact.html'}


def php_str(v):
    return "'" + v.replace('\\', '\\\\').replace("'", "\\'") + "'"


def clean_links_php(html):
    """href="destinations.html" -> href="destinations.php" (index -> ./)"""
    def sub(m):
        page = m.group(2)
        return f'{m.group(1)}{"./" if page == "index" else page + ".php"}{m.group(3)}"'
    return re.sub(r'(href=")(?!https?:|mailto:|tel:|#|/)([A-Za-z0-9._-]+)\.html((?:#[^"]*)?)"', sub, html)


if '--fr' not in sys.argv or True:
    build_fr()

if '--check-fr' in sys.argv:
    check_fr()

if '--php' in sys.argv:
    build_php()
