# Build the Mamitrasa landing page

## Context

Mamitrasa is my small honey business. It sells genuine wild honey harvested from the Baduy forest (Lebak, Banten, Indonesia) directly to end consumers, about 50–100 bottles a month. I have no marketing budget. Most visitors will arrive on a phone from my TikTok account (@mamitrasa7), from friends' WhatsApp shares, or from searching "madu baduy".

Indonesia has a lot of fake and blended honey, so buyers distrust every "asli" (genuine) claim. The brand's positioning is **proof, not claims**: show the forest, the harvest, real buyers and (later) lab results.

## Goal

Build a single, mobile-first landing page that turns a visitor into a WhatsApp or TikTok Shop order in one visit.

- Primary action: **"Pesan via WhatsApp"**, repeated after sections and in a sticky bottom bar on mobile.
- Secondary action: **"Beli di TikTok Shop"**.
- All visible copy is in Bahasa Indonesia (provided below). Code, comments and README are in English.

## Technical requirements

- Static site: plain HTML, CSS and a small amount of vanilla JS. No framework and no build step unless you have a strong reason, in which case explain it first.
- All core content and the WhatsApp links must work with JavaScript disabled. Generate the final HTML statically.
- **One place for business details.** Put every value I will need to change in a single, clearly commented config file or block, and have the page use it. This includes the WhatsApp number, prices, product sizes, TikTok Shop links, payment methods, couriers, COD areas, delivery estimates, shelf life, owner name, and the halal/PIRT/lab result numbers. If that needs a tiny build script to stay JS-free at runtime, keep it dependency-free, for example a single Node or Python script, and document it.
- Unfilled values show as visible placeholders like `[harga]` so nothing looks finished by accident. Trust badges for certifications I don't have yet (halal, lab test) must be hidden until their config value is filled.
- Mobile-first and responsive. Design at 360–414 px wide first, and make it look good on desktop too.
- Fast on a budget phone with a slow connection. Target a Lighthouse score of 90+ on mobile for Performance, Accessibility, Best Practices and SEO. Use responsive images, WebP with fallback, `loading="lazy"` below the fold, system fonts or at most one self-hosted web font, and no heavy third-party scripts.
- TikTok video embed: use a click-to-load facade, showing a thumbnail plus play button that loads the official embed only on tap, so the TikTok script doesn't slow the first load.
- Accessible: semantic HTML landmarks, alt text on every image, visible focus states, AA colour contrast, and tap targets of at least 44 px.
- Deployable to GitHub Pages or Cloudflare Pages with no server. Include the deploy steps in the README.

## Visual direction

Warm, natural and honest, not slick. The palette is honey amber and forest green on an off-white background, with dark brown or near-black text. Use generous whitespace and real photos as the hero of every section. Create simple placeholder images (solid colour blocks with a label like "FOTO: madu dituang, hutan di belakang") in `/images/placeholders/` so the layout is complete before I add real photos. Each placeholder should be easy to replace by filename.

## WhatsApp links

Build each link as `https://wa.me/62<number>?text=<url-encoded message>`. Every button gets its own pre-filled message ending in a source code, so I can see which button produced an order:

| Button | Message |
| --- | --- |
| Hero | Halo Mamitrasa, saya mau pesan madu. (WEB-A) |
| Product card 1 | Halo Mamitrasa, saya mau pesan [ukuran 1]. (WEB-P1) |
| Product card 2 | Halo Mamitrasa, saya mau pesan [ukuran 2]. (WEB-P2) |
| Family bundle | Halo Mamitrasa, saya mau Paket Stok Keluarga. (WEB-P3) |
| Gift set | Halo Mamitrasa, saya mau Paket Hadiah. (WEB-P4) |
| Mid-page buttons | Halo Mamitrasa, saya mau pesan madu. (WEB-M) |
| FAQ "chat kami" | Halo Mamitrasa, saya mau tanya dulu. (WEB-Q) |
| Final button and sticky bar | Halo Mamitrasa, saya mau pesan. (WEB-Z) |

Product names and sizes in these messages come from the config.

## Page structure and copy

Build these sections in this order. Use the copy exactly as written; anything in [brackets] comes from the config.

### 1. Hero
- Headline (h1): **Madu Hutan Baduy, Dipanen Langsung untuk Keluarga Anda**
- Subheadline: Kami ke hutan sendiri, bersama para pemanen setempat. Lihat prosesnya, dari sarang sampai ke botol Anda.
- Image: honey pouring, forest behind (placeholder).
- Buttons: "Pesan via WhatsApp" (primary, WEB-A) and "Beli di TikTok Shop" (secondary).

### 2. Trust strip
Short badges with simple inline SVG icons:
- Dipanen langsung dari hutan Baduy
- Halal MUI No. [nomor], shown only when configured
- COD untuk [area COD]
- Botol pecah di jalan? Kami ganti

### 3. From the forest
- Heading: **Dari Hutan Baduy, Bukan dari Pabrik**
- Text: Madu Mamitrasa berasal dari lebah liar di hutan Baduy, Lebak, Banten. Kami bekerja langsung dengan para pemanen, memanen secukupnya, dan membotolkannya tanpa campuran apa pun. Setiap panen kami rekam dan bagikan di TikTok @mamitrasa7.
- 3–4 photos in a swipeable row on mobile, plus the TikTok video facade.
- Link: "Lihat video lainnya di TikTok" → https://www.tiktok.com/@mamitrasa7

### 4. Why it's genuine
- Heading: **Kenapa Warna dan Rasanya Bisa Berbeda?**
- Text: Lebah hutan mengambil nektar dari bunga yang berbeda-beda di setiap musim. Karena itu, warna, kekentalan dan rasa madu kami bisa berubah dari panen ke panen. Bagi kami, itu tanda madu alami, bukan buatan pabrik.
- Small print: Cara sederhana di rumah hanya petunjuk awal. Bukti paling pasti adalah uji laboratorium.
- If a lab result is configured, show a "Lihat hasil uji lab" link or image. Otherwise hide it.
- Button: "Pesan via WhatsApp" (WEB-M).

### 5. Products and prices
One card per product from the config, each with a photo, name, volume, price in `Rp 99.000` format, a one-line description, and its own WhatsApp button:
- [Ukuran 1] — Cocok untuk mencoba.
- [Ukuran 2] — Pilihan favorit keluarga. Mark this card "Terlaris".
- Paket Stok Keluarga (2–3 botol) — Lebih hemat per botol.
- Paket Hadiah — Kemasan rapi untuk orang tua atau sahabat.

Optionally include a TikTok Shop link per product if configured.

### 6. Buyer reviews
- Heading: **Kata Mereka yang Sudah Mencoba**
- 3–6 review cards from the config: a short quote, name and city, and an optional photo or screenshot. Create 3 clearly fake placeholder entries marked "CONTOH — ganti dengan ulasan asli" that never render without that label.
- Button: "Pesan sekarang" (WEB-M).

### 7. How to order
- Heading: **Pesan dalam 3 Langkah**
  1. Klik tombol WhatsApp dan pilih ukuran.
  2. Kirim alamat lengkap; kami hitung ongkirnya.
  3. Bayar via [metode pembayaran], madu langsung kami kirim.
- Pengiriman: [kurir] ke seluruh Indonesia, [estimasi] untuk Jabodetabek.
- Button: "Pesan via WhatsApp" (WEB-M).

### 8. FAQ
Use an accordion built with native `<details>`/`<summary>`:
- **Kenapa madunya bisa mengkristal?** Itu proses alami pada madu murni, terutama di suhu dingin. Rendam botol di air hangat untuk mencairkannya.
- **Bagaimana cara menyimpannya?** Di suhu ruang, tertutup rapat, jauh dari sinar matahari langsung. Tidak perlu kulkas.
- **Boleh untuk anak-anak?** Boleh untuk anak di atas 1 tahun. Madu tidak dianjurkan untuk bayi di bawah 1 tahun.
- **Berapa lama madu bisa disimpan?** [masa simpan]
- **Apakah bisa COD?** Bisa untuk [area COD].
- **Bagaimana jika botol pecah?** Kirim foto/video unboxing, kami ganti.

End with "Masih ada pertanyaan? Chat kami" (WEB-Q).

### 9. Owner's story and footer
- Heading: **Tentang Mamitrasa**
- Owner photo (placeholder) and text: Saya [nama pemilik], pemilik Mamitrasa. Saya sendiri yang datang ke hutan Baduy dan bekerja langsung dengan para pemanen. Tujuan saya sederhana: keluarga di kota bisa menikmati madu hutan asli, dan para pemanen mendapat harga yang adil.
- Big final button: **Pesan Madu Mamitrasa Sekarang** (WEB-Z).
- Footer: WhatsApp number, TikTok link, area or address, and "© [tahun] Mamitrasa Tradisional Indonesia". Show the ® symbol only if `trademarkRegistered` is true in the config; it defaults to false.

### Sticky bar (mobile only)
A fixed bottom bar with "Pesan via WhatsApp" (WEB-Z). It hides while the hero buttons are on screen, using IntersectionObserver as a progressive enhancement, and must not cover the footer's final button. It is hidden on desktop.

## SEO and sharing

- `<html lang="id">`
- Title: `Madu Hutan Baduy Asli — Mamitrasa`
- Meta description: `Madu hutan Baduy dipanen langsung dan direkam prosesnya. Pesan via WhatsApp, COD Banten & Jakarta, kirim ke seluruh Indonesia.`. Build the COD areas part from the config.
- Open Graph and Twitter card tags, with a 1200×630 share image placeholder at `/images/og-image.jpg`.
- Canonical URL from the config.
- JSON-LD: `Organization`, plus `Product` entries with `offers` (price in IDR) for each product. Don't include ratings or reviews markup.
- Favicon and apple-touch-icon placeholders.
- `robots.txt` and `sitemap.xml`.

## Content rules

- **No health or cure claims anywhere**, in visible text, alt text, meta tags or JSON-LD. Do not write that honey cures, treats or prevents any disease, or "meningkatkan imun"-style medical promises. These breach Indonesian food labelling rules (BPOM). If you think some copy needs a benefit line, use neutral wording like "teman sarapan dan minuman hangat keluarga".
- Don't invent facts: no fake numbers of customers, years in business, ratings or certifications.

## Deliverables

1. The site files, ready to deploy.
2. The config file with every editable value, commented in English.
3. `README.md` covering how to edit the config, how to replace each placeholder image (with a list of filenames, recommended sizes and what photo to take for each), how to preview locally, and how to deploy to GitHub Pages and to Cloudflare Pages.
4. A short report at the end listing every placeholder still to fill and the Lighthouse scores you measured, or say plainly if you couldn't run Lighthouse.

## How to work

1. First, propose the file structure and the config schema in a few lines, then proceed without waiting unless something is truly ambiguous.
2. Build section by section, checking the page at 375 px and 1280 px wide as you go.
3. Before finishing, verify that every WhatsApp button opens the right pre-filled message, that the page works with JS disabled, and that no health claims slipped in.
