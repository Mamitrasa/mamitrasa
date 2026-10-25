# Mamitrasa landing page

Static, mobile-first landing page for Mamitrasa (wild honey from the Baduy forest).
Plain HTML/CSS plus a tiny vanilla JS snippet. The page is generated from `config.toml`
by a single dependency-free Python script (Python 3.11+, no packages, no build tooling).

## Files

| File | Purpose |
| --- | --- |
| `config.toml` | **Every business detail you will edit** (WhatsApp, prices, certificates, ...) |
| `build.py` | Generates `index.html`, `sitemap.xml`, `robots.txt` from the config |
| `assets/style.css`, `assets/main.js` | Styles and the small JS (inlined into `index.html` at build) |
| `images/` | Your photos. `images/placeholders/` holds the stand-ins |
| `index.html`, `sitemap.xml`, `robots.txt` | Generated. Commit them, the host serves them as-is |

## Edit the content

1. Open `config.toml` and fill in values (comments explain each one).
2. Run `python3 build.py`. It lists every value that is still a placeholder.
3. Commit and push.

Empty values show as highlighted `[placeholders]` on the page. Halal, PIRT and
lab-result badges stay hidden until their value is filled. The review cards
marked `sample = true` always show the label "CONTOH — ganti dengan ulasan asli".
Real reviews: replace the text, set `sample = false`.

WhatsApp number: digits only, without the leading `0` or `62` (`81234567890`).
Each button's message ends with a source code (WEB-A, WEB-P1..P4, WEB-M, WEB-Q, WEB-Z)
so you can see which button produced an order.

## Replace images

Drop your photo into `images/` using the slot name; the build picks it up
automatically (no config change) and falls back to the placeholder otherwise.
Use `slot.jpg` (or `.png`) as the fallback and optionally `slot.webp` as the
smaller modern version. Optional `slot-640.webp` / `slot-640.jpg` add a smaller
version for slow phones. Then run `python3 build.py`.

| Slot (filename) | Size | Photo to take |
| --- | --- | --- |
| `hero` | 1200×900 | Honey being poured, forest in the background |
| `forest-1` | 800×1000 | Harvesters in the Baduy forest |
| `forest-2` | 800×1000 | Wild bee nest |
| `forest-3` | 800×1000 | The harvest in progress |
| `forest-4` | 800×1000 | Honey being bottled |
| `video-thumb` | 540×960 | Screenshot of your TikTok video (portrait) |
| `product-1`, `product-2` | 800×800 | Each bottle size, clean background |
| `product-3` | 800×800 | Family stock bundle (2–3 bottles) |
| `product-4` | 800×800 | Gift set |
| `owner` | 800×1000 | You, in the forest or with the harvesters |
| `og-image.jpg` | 1200×630 | Share image for WhatsApp/social previews (replace the file) |
| `apple-touch-icon.png` (180×180), `favicon-32.png` | | Logo/icons |

Review photos are optional: put the file anywhere in `images/` and set `photo = "images/review-1.jpg"` in the config.
Compress photos (aim for under 150 KB each) to keep the page fast.

TikTok video: paste the full video URL into `[video] tiktok_video_url`. The thumbnail
loads the official TikTok embed only after a tap.

## Preview locally

```
python3 build.py
python3 -m http.server 8000
```
Open <http://localhost:8000>.

## Deploy

Set `site_url` in `config.toml` first (canonical URL, share tags, sitemap), rebuild and commit.

**GitHub Pages**: push to GitHub, then Settings → Pages → Source: "Deploy from a branch",
branch `main`, folder `/ (root)`. The site is live at `https://<user>.github.io/<repo>/`
(or your custom domain; set `site_url` to match).

**Cloudflare Pages**: Workers & Pages → Create → Pages → Connect to Git, pick the repo.
Framework preset: None. Build command: empty. Build output directory: `/` (root).
Because `index.html` is committed, no build runs on Cloudflare.

## Notes

- Copy contains no health or cure claims. Keep it that way when editing (BPOM rules).
- Lighthouse was not run when this was set up; run it from Chrome DevTools on the deployed URL.
