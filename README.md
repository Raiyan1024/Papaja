# Papaja — Tailoring website preview

A responsive, single-page tailoring site with Bangla/English switching, an illustrated catalogue of blazers, shirts, trousers and suits, and an in-browser editing panel. The editor can save a draft in the current browser and export a standalone public HTML file.

## Live preview and launch status

This repository is public, so GitHub Pages is a suitable free static host. The included GitHub Actions workflow publishes `index.html` **and `assets/`** to Pages when changes reach `main` (or when manually started from the Actions tab). Once the workflow has run successfully, the project site should be available at:

**https://raiyan1024.github.io/Papaja/**

The site is still a design preview. Before advertising it, add the real business name, address, phone/WhatsApp number, opening hours, tailor details, and genuine garment photographs using the editor. Confirm all copy and service claims with the business owner. No inquiry form or order collection is enabled; a WhatsApp link appears only after a valid business number is added.

## The catalogue

`assets/catalog/` holds 24 studio-style garments — 6 blazers, 6 shirts, 6 trousers, 6 suits — shown in the **Choose your starting point** section with category filters (Everything / Blazers / Shirts / Trousers / Suits). Item names and descriptions are bilingual and switch with বাংলা / EN.

- Every image is **800 × 1120 px**, the same dark studio background, so the grid stays even.
- Filenames are stable, e.g. `assets/catalog/blazer-navy-double.png`, `suit-charcoal.png`, `pants-olive.png`.
- **To use a real photo instead:** export your photograph at 5:7 (e.g. 1000 × 1400) and save it over the same filename in `assets/catalog/`. No HTML change is needed. Keep a copy of the illustration elsewhere if you may want it back.
- **To add or remove items:** edit `tools/catalog.json`, then run the generator (below). Adding a row needs only `file`, `cat`, `art`, `pal` and the English/Bangla name and description; the catalogue JSON embedded in `index.html` is regenerated from that file when you re-run `tools/build_catalog.py`.

### Regenerating the artwork

The illustrations are vector drawings rendered to PNG, so they stay sharp and can be recoloured or reshaped in code.

```sh
pip install resvg-py          # one-time
python3 tools/gen_catalog.py  # redraws every PNG in assets/catalog/
python3 tools/build_catalog.py  # re-embeds the item list into index.html
```

`tools/gen_catalog.py` holds the garment shapes (`jacket`, `shirt`, `trousers`, `suit`) and the fabric palettes (`NAVY`, `CHAR`, `CAMEL`, …). Colours are one-line changes there and affect every item that uses that palette.

Photographs or AI renders are better than illustrations for a real shop. When you have them, replace the PNGs file-for-file — the layout, filters and bilingual labels keep working.

## Local preview

Open `index.html` directly in a modern browser, or run a local static server from this folder, for example:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Editing and publishing

1. Open **Edit website** in the lower-right corner.
2. Apply business details and translated text; upload photos to the matching slots. All 24 catalogue slots appear in the **Photo position** list.
3. **Save in this browser** keeps an editable draft only in that browser. It is not a backup or a public deployment.
4. Commit updated `index.html` to `main` (or download **public HTML** and replace `index.html`) to publish through GitHub Pages. The exported file omits the editor, but keep the original source file in this repository for future edits.
5. Check the Actions tab for the **Deploy website to GitHub Pages** workflow and wait for a successful run.

The browser editor resizes and embeds uploaded images in the exported HTML. Use photos you have permission to publish, and note that image data increases the HTML file size dramatically — 24 embedded photos can push one file into the tens of megabytes. For a large real catalogue, prefer replacing the files in `assets/catalog/` and committing them, so the page still loads quickly. Do not upload sensitive customer information.
