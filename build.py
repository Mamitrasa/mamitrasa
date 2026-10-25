#!/usr/bin/env python3
"""Generate the static Mamitrasa landing page from config.toml.

Usage:  python3 build.py

Writes index.html, sitemap.xml and robots.txt next to this file, and creates
any missing placeholder images. Needs Python 3.11+ and nothing else.
"""
import datetime
import html
import json
import re
import textwrap
from pathlib import Path
from urllib.parse import quote
import tomllib

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"
PLACEHOLDERS = IMAGES / "placeholders"
cfg = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))
biz, shop, certs = cfg["business"], cfg["shop"], cfg["certificates"]
products, reviews, video = cfg["products"], cfg.get("reviews", []), cfg["video"]

e = html.escape
unfilled = []  # names of placeholders that are still showing


# ---------------------------------------------------------------- helpers
def plain(value, name):
    """Plain-text value, or a bracketed placeholder (for attributes/URLs)."""
    value = str(value).strip()
    if value:
        return value
    if name not in unfilled:
        unfilled.append(name)
    return f"[{name}]"


def ph(value, name):
    """HTML value, or a visibly highlighted placeholder."""
    value = str(value).strip()
    if value:
        return e(value)
    if name not in unfilled:
        unfilled.append(name)
    return f'<mark class="ph">[{e(name)}]</mark>'


def rupiah(n):
    return "Rp " + f"{int(n):,}".replace(",", ".")


def wa_number():
    digits = re.sub(r"\D", "", biz["whatsapp"])
    digits = re.sub(r"^(62|0)", "", digits)
    return digits


def wa(text):
    num = wa_number() or plain("", "nomor WhatsApp")
    return f"https://wa.me/62{num}?text={quote(text)}"


def product_label(i):
    p = products[i]
    return p["wa_item"].strip() or "pesan " + plain(p["volume"], p["volume_hint"])


def wa_link(code, i=None):
    if code == "WEB-A" or code == "WEB-M":
        msg = "Halo Mamitrasa, saya mau pesan madu."
    elif code == "WEB-Q":
        msg = "Halo Mamitrasa, saya mau tanya dulu."
    elif code == "WEB-Z":
        msg = "Halo Mamitrasa, saya mau pesan."
    else:
        msg = f"Halo Mamitrasa, saya mau {product_label(i)}."
    return wa(f"{msg} ({code})")


def tiktok_shop(url=""):
    return (url or biz["tiktok_shop_url"] or biz["tiktok_profile_url"]).strip()


if not biz["tiktok_shop_url"].strip():
    unfilled.append("link TikTok Shop")

SITE = biz["site_url"].strip().rstrip("/")
if not SITE:
    unfilled.append("site_url")
SITE_OR_PH = SITE or "https://[site_url]"

# ---------------------------------------------------------------- images
# slot: (width, height, placeholder colour, label, alt text)
SLOTS = {
    "hero": (1200, 900, "#F1D58A", "FOTO: madu dituang, hutan di belakang",
             "Madu dituang dari botol, dengan hutan Baduy di belakangnya"),
    "forest-1": (800, 1000, "#BFD3B5", "FOTO: pemanen di hutan Baduy",
                 "Pemanen madu di dalam hutan Baduy"),
    "forest-2": (800, 1000, "#F1D58A", "FOTO: sarang lebah liar",
                 "Sarang lebah liar di hutan"),
    "forest-3": (800, 1000, "#BFD3B5", "FOTO: proses panen madu",
                 "Proses panen madu langsung dari sarang"),
    "forest-4": (800, 1000, "#F1D58A", "FOTO: madu dibotolkan",
                 "Madu dituang ke dalam botol"),
    "video-thumb": (540, 960, "#D9C9A3", "FOTO: tangkapan layar video TikTok",
                    "Cuplikan video panen madu di TikTok Mamitrasa"),
    "product-1": (800, 800, "#F1D58A", "FOTO: botol ukuran 1",
                  "Botol madu Mamitrasa ukuran pertama"),
    "product-2": (800, 800, "#E8C468", "FOTO: botol ukuran 2",
                  "Botol madu Mamitrasa ukuran kedua"),
    "product-3": (800, 800, "#BFD3B5", "FOTO: paket stok keluarga",
                  "Paket stok keluarga berisi beberapa botol madu"),
    "product-4": (800, 800, "#D9C9A3", "FOTO: paket hadiah",
                  "Paket hadiah madu dengan kemasan rapi"),
    "owner": (800, 1000, "#BFD3B5", "FOTO: pemilik di hutan Baduy",
              "Pemilik Mamitrasa bersama pemanen di hutan Baduy"),
}


def make_placeholder(slot):
    w, h, colour, label, _ = SLOTS[slot]
    path = PLACEHOLDERS / f"{slot}.svg"
    if path.exists():
        return
    head, _, body = label.partition(": ")
    lines = [head + ":"] + textwrap.wrap(body, 22)
    size = round(w / 16)
    y0 = h / 2 - (len(lines) - 1) * size * 0.6 - size * 0.4
    tspans = "".join(
        f'<tspan x="{w // 2}" y="{y0 + k * size * 1.25:.0f}">{e(t)}</tspan>'
        for k, t in enumerate(lines))
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="{colour}"/>'
        f'<rect x="12" y="12" width="{w - 24}" height="{h - 24}" fill="none" '
        f'stroke="#3B2A1A" stroke-opacity=".35" stroke-width="3" stroke-dasharray="14 10"/>'
        f'<text text-anchor="middle" font-family="sans-serif" font-size="{size}" '
        f'font-weight="700" fill="#3B2A1A">{tspans}</text>'
        f'<text x="{w // 2}" y="{h - 40}" text-anchor="middle" font-family="monospace" '
        f'font-size="{round(w / 36)}" fill="#3B2A1A">ganti dengan images/{slot}.jpg</text></svg>\n')
    path.write_text(svg, encoding="utf-8")


def find(name):
    return next((f"images/{name}{ext}" for ext in (".jpg", ".jpeg", ".png", ".webp")
                 if (IMAGES / f"{name}{ext}").exists()), None)


def img(slot, sizes="100vw", eager=False, cls=""):
    """<picture> for a slot: real photo if present in images/, else placeholder.

    Looks for images/<slot>.webp and images/<slot>.jpg (or .jpeg/.png).
    An optional images/<slot>-640.webp / -640.jpg adds a smaller srcset entry.
    """
    w, h, _, _, alt = SLOTS[slot]
    make_placeholder(slot)
    webp = f"images/{slot}.webp" if (IMAGES / f"{slot}.webp").exists() else None
    webp_small = f"images/{slot}-640.webp" if (IMAGES / f"{slot}-640.webp").exists() else None
    fallback = find(slot)
    if fallback and fallback.endswith(".webp"):
        fallback = None
    jpg_small = find(f"{slot}-640")
    src = fallback or webp or f"images/placeholders/{slot}.svg"
    srcset_jpg = f'{jpg_small} 640w, {fallback} {w}w' if (jpg_small and fallback) else ""
    attrs = (f'width="{w}" height="{h}" alt="{e(alt)}" decoding="async" '
             + ('fetchpriority="high"' if eager else 'loading="lazy"'))
    cls_attr = f' class="{cls}"' if cls else ""
    if srcset_jpg:
        attrs += f' srcset="{srcset_jpg}" sizes="{sizes}"'
    source = ""
    if webp:
        srcset = f"{webp_small} 640w, {webp} {w}w" if webp_small else webp
        source = f'<source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
    return f'<picture{cls_attr}>{source}<img src="{src}" {attrs}></picture>'


# ---------------------------------------------------------------- icons
def icon(path):
    return ('<svg class="icon" viewBox="0 0 24 24" width="24" height="24" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true" focusable="false">{path}</svg>')


ICON_LEAF = icon('<path d="M11 20A7 7 0 0 1 4 13c0-6 6-9 16-9 0 10-3 16-9 16z"/><path d="M4 21c2-6 6-9 11-11"/>')
ICON_CHECK = icon('<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>')
ICON_COD = icon('<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 10v4M18 10v4"/>')
ICON_BOX = icon('<path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>')
ICON_WA = icon('<path d="M3 21l1.6-4.8A8.5 8.5 0 1 1 8 19.5z"/><path d="M9 9c0 3 3 6 6 6l1-1.500-2-1-1 .8C12 12.800 11.200 12 10.800 11l.8-1-1-2z"/>')
ICON_TT = icon('<path d="M14 3v11.500a3.500 3.500 0 1 1-3.500-3.500"/><path d="M14 3c.4 2.500 2 4 5 4.200"/>')
ICON_PLAY = ('<svg viewBox="0 0 64 64" width="64" height="64" aria-hidden="true" focusable="false">'
             '<circle cx="32" cy="32" r="30" fill="#2F5D3A" fill-opacity=".92"/>'
             '<path d="M26 20l20 12-20 12z" fill="#fff"/></svg>')


def btn(label, href, kind="primary", icon_svg="", extra=""):
    external = ' target="_blank" rel="noopener"' if "wa.me" in href or "tiktok" in href else ""
    return f'<a class="btn btn-{kind}" href="{e(href)}"{external}{extra}>{icon_svg}{e(label)}</a>'


def wa_btn(label, code, i=None, extra=""):
    return btn(label, wa_link(code, i), "primary", ICON_WA, extra)


# ---------------------------------------------------------------- sections
def trust_strip():
    items = [(ICON_LEAF, "Dipanen langsung dari hutan Baduy")]
    if certs["halal_number"].strip():
        items.append((ICON_CHECK, f"Halal MUI No. {e(certs['halal_number'].strip())}"))
    if certs["pirt_number"].strip():
        items.append((ICON_CHECK, f"PIRT No. {e(certs['pirt_number'].strip())}"))
    if certs["nkv_number"].strip():
        items.append((ICON_CHECK, f"NKV No. {e(certs['nkv_number'].strip())}"))
    items.append((ICON_COD, f"COD untuk {ph(shop['cod_areas'], 'area COD')}"))
    items.append((ICON_BOX, "Botol pecah di jalan? Kami ganti"))
    lis = "".join(f"<li>{ic}<span>{txt}</span></li>" for ic, txt in items)
    return f'<section class="trust" aria-label="Jaminan Mamitrasa"><ul class="container">{lis}</ul></section>'


def forest():
    vid = video["tiktok_video_url"].strip()
    m = re.search(r"/video/(\d+)", vid)
    vid_id = m.group(1) if m else ""
    href = vid or biz["tiktok_profile_url"]
    data = f' data-video-id="{vid_id}" data-cite="{e(vid)}"' if vid_id else ""
    facade = (
        f'<a class="facade" href="{e(href)}" target="_blank" rel="noopener"{data}>'
        f'{img("video-thumb", sizes="(min-width: 768px) 300px, 70vw")}'
        f'<span class="play">{ICON_PLAY}</span>'
        f'<span class="facade-label">Tonton video panen</span></a>')
    photos = "".join(f'<li>{img(f"forest-{n}", sizes="(min-width: 768px) 25vw, 70vw")}</li>'
                     for n in range(1, 5))
    return f'''<section class="section" id="hutan" aria-labelledby="h-hutan">
<div class="container">
<h2 id="h-hutan">Dari Hutan Baduy, Bukan dari Pabrik</h2>
<p class="lead">Madu Mamitrasa berasal dari lebah liar di hutan Baduy, Lebak, Banten. Kami bekerja langsung dengan para pemanen, memanen secara tradisional agar koloni lebah dan hutan tetap lestari, dan membotolkannya tanpa campuran apa pun, dengan pengawasan dan bimbingan oleh dinas KPKP (Ketahanan Pangan, Kelautan, dan Pertanian) DKI Jakarta.</p>
<div class="forest-media">
<div class="video">{facade}</div>
<ul class="photos" role="group" aria-label="Foto panen madu, geser untuk melihat lainnya" tabindex="0">{photos}</ul>
</div>
<p><a class="textlink" href="{e(biz["tiktok_profile_url"])}" target="_blank" rel="noopener">Lihat video lainnya di TikTok</a></p>
</div>
</section>'''


def genuine():
    lab = ""
    if certs["lab_result_url"].strip():
        who = f' ({e(certs["lab_name"].strip())})' if certs["lab_name"].strip() else ""
        lab = (f'<p><a class="textlink" href="{e(certs["lab_result_url"].strip())}" '
               f'target="_blank" rel="noopener">Lihat hasil uji lab</a>{who}</p>')
    return f'''<section class="section alt" id="asli" aria-labelledby="h-asli">
<div class="container narrow">
<h2 id="h-asli">Kenapa Warna dan Rasanya Bisa Berbeda?</h2>
<p class="lead">Lebah hutan mengambil nektar dari bunga yang berbeda-beda di setiap musim. Karena itu, warna, kekentalan dan rasa madu kami bisa berubah dari panen ke panen. Bagi kami, itu tanda madu alami, bukan buatan pabrik.</p>
<ul class="checks" aria-label="Keunggulan madu Mamitrasa">
<li>100% madu hutan asli</li>
<li>Bukan madu ternak</li>
<li>Tanpa campuran</li>
<li>Tanpa tambahan gula</li>
<li>Tanpa rekayasa</li>
</ul>
<p class="small">Cara sederhana di rumah hanya petunjuk awal. Bukti paling pasti adalah uji laboratorium.</p>
{lab}
<p>{wa_btn("Pesan via WhatsApp", "WEB-M")}</p>
</div>
</section>'''


def product_cards():
    out = []
    for i, p in enumerate(products):
        n = i + 1
        price = rupiah(p["price"]) if p["price"] else ph("", "harga")
        badge = f'<span class="badge">{e(p["badge"])}</span>' if p["badge"].strip() else ""
        shop_link = ""
        if p["tiktok_url"].strip():
            shop_link = btn("Beli di TikTok Shop", p["tiktok_url"].strip(), "secondary", ICON_TT)
        out.append(f'''<li class="card">{badge}
{img(f"product-{n}", sizes="(min-width: 768px) 25vw, 90vw")}
<div class="card-body">
<h3>{e(p["name"])}</h3>
<p class="vol">{ph(p["volume"], p["volume_hint"])}</p>
<p class="price">{price}</p>
<p>{e(p["description"])}</p>
<div class="stack">{wa_btn("Pesan via WhatsApp", f"WEB-P{n}", i)}{shop_link}</div>
</div></li>''')
    return f'''<section class="section" id="produk" aria-labelledby="h-produk">
<div class="container">
<h2 id="h-produk">Pilih Madu Anda</h2>
<ul class="cards">{"".join(out)}</ul>
<p class="center">{btn("Beli di TikTok Shop", tiktok_shop(), "secondary", ICON_TT)}</p>
</div>
</section>'''


def review_section():
    if not reviews:
        return ""
    cards = []
    for r in reviews[:6]:
        label = ('<p class="sample">CONTOH — ganti dengan ulasan asli</p>'
                 if r.get("sample", True) else "")
        photo = ""
        if r.get("photo", "").strip():
            photo = (f'<img class="rv-photo" src="{e(r["photo"].strip())}" width="96" height="96" '
                     f'alt="Foto dari {e(r["name"])}" loading="lazy" decoding="async">')
        cards.append(f'''<li class="card review">{label}{photo}
<blockquote><p>{e(r["quote"])}</p></blockquote>
<p class="who"><strong>{e(r["name"])}</strong>, {e(r["city"])}</p></li>''')
    return f'''<section class="section alt" id="ulasan" aria-labelledby="h-ulasan">
<div class="container">
<h2 id="h-ulasan">Kata Mereka yang Sudah Mencoba</h2>
<ul class="cards reviews">{"".join(cards)}</ul>
<p class="center">{wa_btn("Pesan sekarang", "WEB-M")}</p>
</div>
</section>'''


def how_to_order():
    return f'''<section class="section" id="cara-pesan" aria-labelledby="h-pesan">
<div class="container narrow">
<h2 id="h-pesan">Pesan dalam 3 Langkah</h2>
<ol class="steps">
<li>Klik tombol WhatsApp dan pilih ukuran.</li>
<li>Kirim alamat lengkap; kami hitung ongkirnya.</li>
<li>Bayar via {ph(shop["payment_methods"], "metode pembayaran")}, madu langsung kami kirim.</li>
</ol>
<p><strong>Pengiriman:</strong> {ph(shop["couriers"], "kurir")} ke seluruh Indonesia, {ph(shop["delivery_estimate_jabodetabek"], "estimasi")} untuk Jabodetabek.</p>
<p>{wa_btn("Pesan via WhatsApp", "WEB-M")}</p>
</div>
</section>'''


def faq():
    qa = [
        ("Kenapa madunya bisa mengkristal?",
         "Itu proses alami pada madu murni, terutama di suhu dingin. Rendam botol di air hangat untuk mencairkannya."),
        ("Bagaimana cara menyimpannya?",
         "Di suhu ruang, tertutup rapat, jauh dari sinar matahari langsung. Tidak perlu kulkas."),
        ("Boleh untuk anak-anak?",
         "Boleh untuk anak di atas 1 tahun. Madu tidak dianjurkan untuk bayi di bawah 1 tahun."),
        ("Berapa lama madu bisa disimpan?", ph(shop["shelf_life"], "masa simpan")),
        ("Apakah bisa COD?", f"Bisa untuk {ph(shop['cod_areas'], 'area COD')}."),
        ("Bagaimana jika botol pecah?", "Kirim foto/video unboxing, kami ganti."),
    ]
    items = "".join(
        f'<details><summary>{e(q)}</summary><p>{a if "<mark" in a else e(a)}</p></details>'
        for q, a in qa)
    return f'''<section class="section alt" id="faq" aria-labelledby="h-faq">
<div class="container narrow">
<h2 id="h-faq">Pertanyaan yang Sering Ditanyakan</h2>
{items}
<p class="center">Masih ada pertanyaan? <a class="textlink" href="{e(wa_link("WEB-Q"))}" target="_blank" rel="noopener">Chat kami</a></p>
</div>
</section>'''


def about_and_footer(year):
    reg = "®" if biz["trademark_registered"] else ""
    num = wa_number()
    num_txt = f"+62 {e(num)}" if num else ph("", "nomor WhatsApp")
    nkv = f' · NKV No. {e(certs["nkv_number"].strip())}' if certs["nkv_number"].strip() else ""
    pirt = f' · PIRT No. {e(certs["pirt_number"].strip())}' if certs["pirt_number"].strip() else ""
    halal = f' · Halal MUI No. {e(certs["halal_number"].strip())}' if certs["halal_number"].strip() else ""
    return f'''<section class="section" id="tentang" aria-labelledby="h-tentang">
<div class="container about">
<div>{img("owner", sizes="(min-width: 768px) 400px, 90vw")}</div>
<div>
<h2 id="h-tentang">Tentang Mamitrasa</h2>
<p class="lead">Saya {ph(biz["owner_name"], "nama pemilik")}, pemilik Mamitrasa. Saya sendiri yang datang ke hutan Baduy dan bekerja langsung dengan para pemanen. Tujuan saya sederhana: keluarga di kota bisa menikmati madu hutan asli, dan para pemanen mendapat harga yang adil.</p>
<p id="final-cta">{wa_btn("Pesan Madu Mamitrasa Sekarang", "WEB-Z", extra=' data-final-cta')}</p>
</div>
</div>
</section>
</main>
<footer class="footer">
<div class="container">
<p><strong>Mamitrasa</strong></p>
<ul>
<li>WhatsApp: <a href="{e(wa_link("WEB-Z"))}" target="_blank" rel="noopener">{num_txt}</a></li>
<li>TikTok: <a href="{e(biz["tiktok_profile_url"])}" target="_blank" rel="noopener">{e(biz["tiktok_handle"])}</a></li>
<li>{ph(biz["address"], "alamat/area")}</li>
</ul>
<p class="small">© {year} {e(biz["legal_name"])}{reg}{halal}{pirt}{nkv}</p>
</div>
</footer>'''


# ---------------------------------------------------------------- head / SEO
def head(year):
    cod = shop["cod_areas"].strip()
    desc = ("Madu hutan Baduy dipanen langsung dan direkam prosesnya. Pesan via WhatsApp, "
            + (f"COD {cod}, " if cod else "") + "kirim ke seluruh Indonesia.")
    title = "Madu Hutan Baduy Asli — Mamitrasa"
    og_img = f"{SITE_OR_PH}/images/og-image.jpg"
    canon = f'<link rel="canonical" href="{e(SITE)}/">' if SITE else ""
    og_url = f'<meta property="og:url" content="{e(SITE)}/">' if SITE else ""

    org = {"@context": "https://schema.org", "@type": "Organization",
           "name": "Mamitrasa", "legalName": biz["legal_name"],
           "sameAs": [biz["tiktok_profile_url"]]}
    if SITE:
        org["url"] = SITE + "/"
        org["logo"] = f"{SITE}/images/logo.png"
    if wa_number():
        org["contactPoint"] = {"@type": "ContactPoint", "telephone": f"+62{wa_number()}",
                               "contactType": "customer service", "availableLanguage": "id"}
    ld = [org]
    for i, p in enumerate(products):
        if not p["price"]:
            continue  # no price yet: skip, never publish a Product without an offer
        item = {"@context": "https://schema.org", "@type": "Product",
                "name": f"{p['name']} {p['volume']}".strip(),
                "description": p["description"],
                "brand": {"@type": "Brand", "name": "Mamitrasa"},
                "offers": {"@type": "Offer", "priceCurrency": "IDR", "price": str(p["price"]),
                           "availability": "https://schema.org/InStock"}}
        real = find(f"product-{i + 1}")
        if SITE and real:
            item["image"] = f"{SITE}/{real}"
        if SITE:
            item["offers"]["url"] = SITE + "/#produk"
        ld.append(item)
    ld_html = "".join(
        '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
        + "</script>" for o in ld)

    css = (ROOT / "assets/style.css").read_text(encoding="utf-8")
    return f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#1F4A2E">
{canon}
<meta property="og:type" content="website">
<meta property="og:locale" content="id_ID">
<meta property="og:site_name" content="Mamitrasa">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
{og_url}
<meta property="og:image" content="{e(og_img)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{e(og_img)}">
<link rel="icon" href="images/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
{ld_html}
<style>{css}</style>
</head>'''


def build():
    year = biz["year"].strip() or str(datetime.date.today().year)
    js = (ROOT / "assets/main.js").read_text(encoding="utf-8")
    hero = f'''<section class="hero" aria-labelledby="h-hero">
<div class="container hero-grid">
<div class="hero-text">
<h1 id="h-hero">Madu Hutan Baduy, Dipanen Langsung untuk Keluarga Anda</h1>
<p class="lead">Kami ke hutan sendiri, bersama para pemanen setempat. Lihat prosesnya, dari sarang sampai ke botol Anda.</p>
<div class="stack hero-actions" id="hero-actions">{wa_btn("Pesan via WhatsApp", "WEB-A")}{btn("Beli di TikTok Shop", tiktok_shop(), "secondary", ICON_TT)}</div>
</div>
<div class="hero-img">{img("hero", sizes="(min-width: 900px) 540px, 100vw", eager=True)}</div>
</div>
</section>'''
    body = f'''<body>
<a class="skip" href="#utama">Lewati ke konten utama</a>
<header class="topbar"><div class="container"><a class="brand" href="./"><picture><source type="image/webp" srcset="images/logo-header.webp"><img src="images/logo-header.png" width="312" height="120" alt="Mamitrasa, Tradisional Indonesia" decoding="async" fetchpriority="high"></picture></a></div></header>
<main id="utama">
{hero}
{trust_strip()}
{forest()}
{genuine()}
{product_cards()}
{review_section()}
{how_to_order()}
{faq()}
{about_and_footer(year)}
<div class="sticky-bar" id="sticky-bar">{wa_btn("Pesan via WhatsApp", "WEB-Z")}</div>
<script>{js}</script>
</body>
</html>
'''
    (ROOT / "index.html").write_text(head(year) + "\n" + body, encoding="utf-8")
    today = datetime.date.today().isoformat()
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{e(SITE_OR_PH)}/</loc><lastmod>{today}</lastmod></url>\n</urlset>\n",
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_OR_PH}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    build()
    print("Built index.html, sitemap.xml, robots.txt")
    if unfilled:
        print("Still unfilled (shown as placeholders / fallbacks):")
        for name in unfilled:
            print(f"  - {name}")
