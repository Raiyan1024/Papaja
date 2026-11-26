# Deploy Papaja to Cloudflare Pages (free of cost, "perfectly")

Your site is static (`index.html` + `assets/`), so Cloudflare Pages can serve it with
**no build step at all**. This guide covers the free-tier setup end to end, with the
limits from Cloudflare's current docs.

## 1. Create a Cloudflare account (free)

- Go to https://dash.cloudflare.com and sign up. No credit card is required for the
  free Pages plan.

## 2. Create a Pages project

### Option A — from your GitHub repo (recommended)

1. In the Cloudflare dashboard: **Workers & Pages → Create → Deploy a Pages site →
   Connect GitHub**.
2. Authorize Cloudflare, then pick the repo `raiyan1024/Papaja`.
3. **Production branch:** `main`.
4. **Build settings:** leave the build command **empty** — Papaja is a static site;
   Pages serves the files as they are. (If you ever add a build step, e.g.
   `python3 tools/build_catalog.py` before serving, set it as the command and Pages
   runs it before each deploy.)
5. Click **Create project**. Every push to `main` triggers a new deploy.

### Option B — upload directly (no GitHub)

1. Package the site: `zip -r papaja.zip index.html assets tools README.md`
   (adjust as needed; the free tier allows 20,000 files per site and 25 MiB per
   asset — Papaja's ~60 files are far below that).
2. In the dashboard: **Create → Deploy a Pages site → Upload**, choose the zip.

## 3. What you get on the free tier (current 2026 numbers)

From Cloudflare Pages limits and pricing docs (read 2026-10-22/29):

- **$0 forever** — no credit card.
- **Unlimited static bandwidth** — serving `index.html`, CSS, JS and the
  `assets/catalog/*.png` files never charges anything.
- **500 builds per month**, one build at a time, 20-minute build timeout.
- **Custom domains: 100 per project**; add your domain in the project's *Domains* tab.
- **HTTPS is automatic** — a certificate is issued for your custom domain.
- **100 projects** max per account, **unlimited preview deployments** (one per PR).

## 4. Add your custom domain "perfectly"

Two setups, both free:

1. **Your domain is at Cloudflare** (recommended): the domain is already in your
   Cloudflare DNS. Just add it to the Pages project under *Domains* and approve the
   verification email. Done — HTTPS is automatic. (You also get Cloudflare's proxy
   protection and CDN, which many people don't realize they're getting for free.)
2. **Your domain is at another registrar** (e.g. Namecheap, Google Domains):
   - Add the domain to the Pages project first (shows you a `*.pages.dev` URL).
   - At your registrar, add a **CNAME** record for your domain → the
     `<project>.pages.dev` hostname. Point the A-record variant to Cloudflare
     `192.0.2.1`/`198.51.100.1` if you want proxied hosting instead.
   - Cloudflare issues the HTTPS certificate automatically; you usually don't touch
     anything else.

Tip for the "many changes" phase: open a PR in `raiyan1024/Papaja` — Cloudflare
Pages creates a **unique preview URL per PR** so you can test edits before merging
to `main`.

## 5. When you outgrow the free tier

- **Over 500 builds/month:** run builds in GitHub Actions and deploy with
  `wrangler` (see below) — or, more simply, the $20/month Cloudflare Pro plan.
- **Dynamic features** (an API route, SSR, middleware): use **Pages Functions**
  (backed by the Workers free plan: 100,000 requests/day, 10 ms CPU each) or
  Workers Static Assets.

## 6. Alternative free-tier tools (quick alternatives if you want)

- **GitHub Pages** — Papaja is already public on GitHub (`https://raiyan1024.github.io/Papaja/`)
  and the repo ships a GitHub Actions workflow (`.github/workflows/deploy-pages.yml`)
  that publishes `index.html` and `assets/` on pushes to `main`. Zero setup.
- **`wrangler` direct upload** — after installing `npm i -g wrangler`:
  ```sh
  wrangler init papaja-static   # or any name
  # upload the zip with:
  npx wrangler pages deploy papaja/   # or: npx wrangler pages deploy <zip-dir>
  ```

## Sources

- Cloudflare Pages limits: https://developers.cloudflare.com/pages/platform/limits/
- Cloudflare Pages product page: https://www.cloudflare.com/products/pages
- Cloudflare Pages free-tier round-up:
  https://temps.sh/blog/cloudflare-pages-free-tier-limits-2026
