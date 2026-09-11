# TheGateKeeper.art

A single-page site for a one-off sculptural metal art workshop. Plain HTML + CSS + JS,
no build step, no dependencies. Drop the folder on any static host (Netlify, Cloudflare
Pages, GitHub Pages, or just upload via FTP to the domain).

```
index.html          the whole page
css/style.css       all styling (design tokens at the top)
js/main.js          nav, gallery filter, lightbox, form
assets/             placeholder graphics — replace these
tools/make_placeholders.py   regenerates the placeholders if you want more
```

## Preview locally

```bash
cd thegatekeeper.art
python3 -m http.server 8080
# open http://localhost:8080
```

## Swapping in the real photos

Every placeholder is just an `<img>` in `index.html`. Two options:

**A. Same filename, different content (no HTML edits)**
Save the photo so it lands on the exact same path, e.g. `assets/hero.svg` → replace with
`assets/hero.jpg` and update that one `src` attribute. Keeping the filename identical and
just changing the extension means editing exactly one word per image.

**B. Add a photo folder** — put real images in `assets/photos/` and repoint each `src`:

```html
<img src="assets/photos/iron-widow.jpg" alt="Iron Widow — welded steel spider sculpture" ...>
```

### What goes where

| Slot | File | Subject | Ratio |
|---|---|---|---|
| Hero | `assets/hero.svg` | The signature piece — best-lit, strongest silhouette | 4:3 |
| 01 | `assets/gallery-01.svg` | Iron Widow (spider) | 4:3 |
| 02 | `assets/gallery-02.svg` | The Mincer (grinder + forks + chain) | 4:3 |
| 03 | `assets/gallery-03.svg` | Loom Raider (loom → car) | 4:3 |
| 04 | `assets/gallery-04.svg` | Spanner Fish | 4:3 |
| 05 | `assets/gallery-05.svg` | The GateKeeper (name piece) | 4:3 |
| 06 | `assets/gallery-06.svg` | Rust & Rivets — also reused in the Workshop section for a maker photo | 4:3 |
| 07 | `assets/gallery-07.svg` | Gearling (small piece) | 4:3 |
| 08 | `assets/gallery-08.svg` | The Gate (large / outdoor) | 4:3 |
| 09 | `assets/gallery-09.svg` | Copper Moth (small creature) | 4:3 |

Also update `assets/og.svg` (the link preview image shown on Facebook/WhatsApp) — ideally swap
this for a JPG/PNG at 1200×630 and update the `og:image` URL in `<head>`.

**Shooting tips:** plain dark backdrop, one hard light from the side, shoot slightly below the
piece so it reads as monumental. Export 1200×900 at ~150–250 KB each.

## Editing content

- **Titles/descriptions** — each piece is a `<figure class="piece" data-cat="...">` block.
  `data-cat` must be one of `creatures`, `machines`, `curiosities` to match the filter buttons.
- **Colours** — everything comes from the `:root` block at the top of `css/style.css`
  (`--copper`, `--brass`, `--iron-*`).
- **Email address** — appears in `index.html` (contact card + footer + JSON-LD) and as
  `MAILTO` in `js/main.js`.
- **Categories** — add a button in `.filters` with a matching `data-filter`, and use the same
  value in `data-cat` on the pieces.

## Contact form

By default it composes a `mailto:` link — zero setup, and nothing is stored. If you'd rather
have it post silently, sign up at Formspree (free tier is fine for a hobby site) and set:

```js
// js/main.js, near the top of section 6
var FORM_ENDPOINT = "https://formspree.io/f/yourid";
```

## Deploying to TheGateKeeper.art

Any static host works:

- **Netlify / Cloudflare Pages** — drag the folder onto their dashboard, point the domain's
  nameservers or add the CNAME they give you.
- **Existing hosting / cPanel** — upload the contents of this folder into `public_html`.
- **GitHub Pages** — push the folder to a repo, enable Pages on the branch root, add the
  custom domain in settings.

The DNS record should point `thegatekeeper.art` at the host; `www` usually gets a CNAME to the
same place plus a redirect rule.

## Preview screenshots

`preview/preview-full.png` and `preview/preview-top.png` are headless renders of the current
build (placeholders still in place) — handy as a "before" reference. Delete the folder once the
real photos are in.

## Accessibility & performance notes

- Alt text on every image — rewrite these to describe the actual sculpture.
- Lightbox is keyboard-accessible (Esc closes, focus returns to where you were).
- Honours `prefers-reduced-motion`.
- No JS frameworks, one stylesheet, system-font fallbacks — the whole page is ~40 KB of code
  plus images.
