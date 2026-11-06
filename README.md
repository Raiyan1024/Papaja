# Papaja — Tailoring website preview

A responsive, single-page tailoring site with Bangla/English switching, scout-uniform/suit/blazer filters, and an in-browser editing panel. The editor can save a draft in the current browser and export a standalone public HTML file.

## Live preview and launch status

This repository is public, so GitHub Pages is a suitable free static host. The included GitHub Actions workflow publishes `index.html` to Pages when changes reach `main` (or when manually started from the Actions tab). Once the workflow has run successfully, the project site should be available at:

**https://raiyan1024.github.io/Papaja/**

The site is still a design preview. Before advertising it, add the real business name, address, phone/WhatsApp number, opening hours, tailor details, and genuine garment/workshop photographs using the editor. Confirm all copy and service claims with the business owner. No inquiry form or order collection is enabled; a WhatsApp link appears only after a valid business number is added.

## Local preview

Open `index.html` directly in a modern browser, or run a local static server from this folder, for example:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Editing and publishing

1. Open **Edit website** in the lower-right corner.
2. Apply business details and translated text; upload photos to the matching slots.
3. **Save in this browser** keeps an editable draft only in that browser. It is not a backup or a public deployment.
4. Commit updated `index.html` to `main` (or download **public HTML** and replace `index.html`) to publish through GitHub Pages. The exported file omits the editor, but keep the original source file in this repository for future edits.
5. Check the Actions tab for the **Deploy website to GitHub Pages** workflow and wait for a successful run.

The browser editor resizes and embeds uploaded images in the exported HTML. Use photos you have permission to publish, and note that image data increases the HTML file size. Do not upload sensitive customer information.
