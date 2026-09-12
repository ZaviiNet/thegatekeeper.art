# TheGateKeeper.art

A single-page site for a one-off sculptural metal art workshop. Plain HTML + CSS + JS,
no build step, no dependencies. Drop the folder on any static host (Netlify, Cloudflare
Pages, GitHub Pages, or plain FTP to the domain).

```
index.html      the whole page
css/style.css   all styling (design tokens at the top)
js/main.js      nav, lightbox, commission form
assets/         the five piece photos + favicon
preview/        headless screenshot of the current build (reference only)
```

## Preview locally

```bash
cd thegatekeeper.art
python3 -m http.server 8080
# open http://localhost:8080
```

## The pieces

| Photo | Piece | Shown as |
|---|---|---|
| `assets/stone.jpg` | steel figure carrying a stone | hero **and** gallery |
| `assets/shark.jpg` | shark built from a pair of grips | gallery |
| `assets/meat.jpg` | meat grinder with forks and chain | gallery |
| `assets/bird.jpg` | bird made from a spanner | gallery |
| `assets/car.jpg` | car built from a loom bobbin | gallery |

The gallery is a **masonry layout** (`column-count` in `css/style.css`), so each photo keeps its
own shape — the two portrait photos are not cropped to match the landscape ones. If you add more
photos of any orientation, they'll just slot in.

### Adding a piece

Copy this block into `<div class="gallery">` in `index.html` and change the four marked values:

```html
<figure class="piece reveal" data-cat="creature">
  <div class="piece__frame">
    <span class="piece__tag">Steel</span>
    <img src="assets/newphoto.jpg" alt="What the sculpture shows, for screen readers" loading="lazy" width="2000" height="1500">
    <div class="piece__zoom" data-lightbox><span>View piece</span></div>
  </div>
  <figcaption class="piece__body">
    <div>
      <h3>Piece name</h3>
      <p>One line about it.</p>
    </div>
    <dl><div>Steel</div></dl>
  </figcaption>
</figure>
```

Set `width`/`height` to the real pixel size of the photo — it stops the page jumping while images
load. Multiple photos per piece aren't supported yet.

## Things worth a second pass

- **The handwritten tags are in shot.** `stone.jpg`, `car.jpg`, `shark.jpg` and `bird.jpg` all have
  a small paper tag visible near the base. They're left in deliberately rather than guessed at —
  if those tags carry the real titles, tell me what they say and I'll use them instead of the
  current descriptive names.
- **Materials are placeholders.** The little caption on each card ("Steel", "Found metal",
  "Wood & metal") is a best guess from the photo — correct them in `index.html`.
- **Photo size.** The five photos are 380–560 KB each (~2.4 MB total). Fine for now; if the site
  needs to be faster, they can be re-exported at 1600px wide / quality 80 to roughly halve that.
- **No maker photo.** The workshop section is text + an info card rather than a portrait of the
  maker. Send one over and I'll drop it in.

## Editing content

- **Colours** — everything comes from the `:root` block at the top of `css/style.css`
  (`--copper`, `--brass`, `--iron-*`).
- **Email address** — appears in `index.html` (contact card, footer, workshop card, JSON-LD) and
  as `MAILTO` in `js/main.js`.
- **Gallery columns** — the three `@media` rules above `.piece` set 1 / 2 / 3 columns.
- **Filter buttons** — removed while the collection is 5 pieces. The `data-cat` attribute is still
  on every figure, and `js/main.js` has a comment marking where to restore the filter code.

## Contact form

By default it composes a `mailto:` link — zero setup, nothing stored. To post silently instead,
sign up at Formspree (free tier is fine) and set:

```js
// js/main.js, section 6
var FORM_ENDPOINT = "https://formspree.io/f/yourid";
```

## Deploying

The site is a private repo at <https://github.com/ZaviiNet/thegatekeeper.art>.

> **GitHub Pages won't serve a private repo on a Free plan** — it needs Pro/Team/Enterprise.
> Two free options: make the repo public and enable Pages, or connect the private repo to
> Cloudflare Pages / Netlify (both auto-deploy on push and handle the custom domain).

Whichever host you pick: point `thegatekeeper.art` at it (the host gives you either nameservers or
a CNAME target), and give `www` a CNAME to the same place plus a redirect to the bare domain.
For GitHub Pages specifically, add a file named `CNAME` at the repo root containing
`thegatekeeper.art`.

## Accessibility & performance notes

- Alt text on every image — rewrite these to describe the actual sculpture.
- Lightbox is keyboard-accessible (Esc closes, focus returns to where you were).
- Honours `prefers-reduced-motion`.
- No frameworks, one stylesheet, system-font fallbacks — about 40 KB of code plus photos.
