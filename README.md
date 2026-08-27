# kroster.github.io

Personal academic website. Jekyll + the [Minimal Mistakes](https://mademistakes.com/work/jekyll-themes/minimal-mistakes/)
theme, pulled in as a remote theme so there is no theme code to maintain in this repo.

---

## 1. Put it online

1. On GitHub, create a **new empty public repository named exactly `kroster.github.io`**
   (the name has to match your username for the URL to be `https://kroster.github.io`).
2. In this folder, run:

   ```bash
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/KRoster/kroster.github.io.git
   git push -u origin main
   ```

3. In the repo on GitHub: **Settings → Pages → Build and deployment**. Set
   *Source* to **Deploy from a branch**, branch **main**, folder **/ (root)**. Save.
4. Wait a minute or two, then open <https://kroster.github.io>.

GitHub builds the site for you every time you push. You don't need Ruby or Jekyll
installed unless you want to preview changes locally first (see section 6).

## 2. Two things to swap in

Replace these files, keeping the filenames:

| File | What it should be |
| --- | --- |
| `assets/images/profile.jpg` | Your headshot. **Square** — crop it to a 1:1 ratio, ~600×600px. Shown at 200px in the left column of the About page, straddling the bottom edge of the banner. |
| `assets/images/banner.jpg` | **Already done** — see "The banner" below. Only swap it if you'd rather use a photo. Wide, ~2400×600px; it is cropped to a 320px-tall strip and the photo sits over its left third, so keep anything important out of the left. No text is drawn on it. |
| `assets/files/cv.pdf` | Your CV. The CV page embeds whatever is at this path. |

To grab your headshot off LinkedIn: open your profile, click the photo, then right-click →
*Save image as*.

## 3. The banner

`assets/images/banner.jpg` isn't stock decoration — it's your own subject matter.
`tools/banner_gen.py` simulates an ensemble of stochastic SIR epidemics (tau-leaping)
and draws them on a faint grey ground: ~150 dark blue wild-type trajectories, then a
drug-resistant strain seeded later and drawn in the site's accent red, emerging and
spreading through a handful of runs. The left third is deliberately quiet, because
that's where your photo and name sit.

To regenerate it — a different random draw, other colours, a taller strip:

```bash
pip install numpy matplotlib
python tools/banner_gen.py
```

The knobs are at the top of the file: `W`/`H`, `BG_TOP`/`BG_BOTTOM`, `WILD`,
`RESISTANT`, and the seed passed to `default_rng` (change it for a different-looking
ensemble). It overwrites `assets/images/banner.jpg` in place.

## 4. Adding a publication

Everything lives in **`_data/publications.yml`** — one file, used by both the
Publications page and the Research page, so each paper is written once.

Add a new block at the **top** of that file:

```yaml
- id: aje2027-something          # any unique short label
  authors: "Oliveira Roster K, Someone A, Grad YH"
  title: "The title of the paper"
  journal: "American Journal of Epidemiology"
  year: 2027
  pmid: "12345678"               # optional, becomes a PubMed link
  pmcid: "PMC1234567"            # optional, becomes a full-text link
  url: "https://doi.org/..."     # optional, used instead of the PubMed link
  note: "*equal contribution"    # optional
  themes: [t2]                   # optional, see below
```

Notes:

- Your name is bolded automatically wherever `Oliveira Roster K` appears.
- The Publications page numbers the list **counting down the page**, so the newest
  paper always has the highest number. Nothing to renumber by hand.
- Italics inside a title (species names, for instance) go in as HTML:
  `<em>Neisseria gonorrhoeae</em>`.
- `themes` decides which sections of the Research page also cite the paper:
  `t1` antibiotic deployment, `t2` surveillance design, `t3` forecasting in
  low-data settings, `t4` drivers of changing burden. Leave it out for papers
  that belong to none of them — they still appear in the full list.

## 5. Editing the pages

| Page | File |
| --- | --- |
| About (home) | `index.md` |
| Research | `_pages/research.md` |
| Publications | `_pages/publications.md` |
| CV | `_pages/cv.md` |
| Navigation bar | `_data/navigation.yml` |
| Name, sidebar links, site title | `_config.yml` |
| Fonts and colours | `assets/css/main.scss` |

The pages are Markdown: `**bold**`, `*italic*`, `[link text](https://url)`,
`## Heading`. The block between the `---` lines at the top of each file is
configuration, not content.

To add a page, copy an existing file in `_pages/`, change its `title` and
`permalink`, and add an entry to `_data/navigation.yml`.

## 6. Previewing locally (optional)

Only if you want to see changes before pushing. Needs Ruby.

```bash
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>. Changes to Markdown files show up on reload;
changes to `_config.yml` need a restart.

## 7. Design notes

- **Typeface and accent follow Owlstown's "Blazer" preset** — the platform
  robertavaltorta.com is built on. That means **Inter** (loaded from Google Fonts in
  `_includes/head/custom.html`) with a **red accent, `#f44336`**.
- Body text is near-black (`#1c1e21`). All colour and font values are Sass variables
  near the top of `assets/css/main.scss`, above the theme import, so they change in one
  place: `$sans-serif` for the typeface, `$primary-color` / `$link-color` for the accent.
  Owlstown's other presets are Lato (Argyle, blue `#0b8bf2`; Jersey, cyan `#03a9f4`),
  IBM Plex Sans (Corduroy, `#ffc107`), Chivo (Goggles, `#607d8b`), Alegreya (Duffel,
  `#4caf50`), Eczar (Flannel, `#795548`), Cardo (Hoodie, `#607d8b`), Libre Baskerville
  (Inkpen, `#2196f3`) and Inconsolata (Elbowpatch, `#673ab7`).
- **About page** follows robertavaltorta.com: a banner with no text over it, then two
  columns. The left column holds the photo — square, centred in its column, pulled up to
  overlap the banner by exactly half its height — with the name, role and three links
  beneath it; the right column holds the prose. Below 768px the two columns stack.
  The photo size and its pull-up are the paired variables `$profile-photo` /
  `$profile-photo-pull` (and the `-small` pair for phones); if you change one, change its
  partner to half the value, negated. `$profile-column` and `$profile-gutter` set the
  left column's width and the space beside it.
- The other pages keep the left author sidebar so your links follow the reader.
- In publication lists, co-authors are set in grey and your own name in solid black,
  so your papers are scannable at a glance.
