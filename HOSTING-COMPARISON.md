# Free hosting comparison for Papaja (static website)

Papaja is a static site — plain `index.html` + `assets/` + `tools/`. Any host that
serves static files works; it needs no build step, no database and no credit card.

Findings below are the 2026 free tiers of the five largest hosts. Sources are listed
at the end.

## Comparison table (current 2026 limits)

| Host | Cost today | Free bandwidth | Build limits | Custom domain + HTTPS | Functions on free | Best for |
|---|---|---|---|---|---|---|
| **Cloudflare Pages** | $0 | Unlimited for static assets | 500 builds/month, 1 concurrent, 20-min timeout | Custom domains: 100 per project, free HTTPS | Pages Functions → Workers free: 100,000 req/day, 10 ms CPU each | Best raw traffic: static sites, no bandwidth caps |
| GitHub Pages | Free forever | ~1 GB site; soft 100 GB/mo | Soft 10 builds/hour | Custom domain + free auto-HTTPS | None (static only) | Code already in a GitHub repo (Papaja is) |
| Netlify | Free tier | ~15 GB effective (300 credits/mo, 20 credits/GB) | 15 credits per production deploy, ~20 deploys/mo | Custom domain + free HTTPS | Serverless only | Forms, deploy previews, Jamstack plugins |
| Vercel (Hobby) | Free tier | 100 GB Fast Data Transfer/mo | Included builds | Custom domain + free HTTPS | 1,000,000 function invocations/mo | Next.js apps; non-commercial use only |
| Render | Free tier | 5 GB pooled per workspace | — | Custom domain + free HTTPS | — | Full-stack apps with always-on servers |

### The numbers that matter for a static site like Papaja

- **Cloudflare Pages** — the only free host with **no bandwidth cap** for static
  assets (stork.ai / temps.sh, 2026 reads). If your storefront can get visitors, this
  is the choice that never asks you to pay.
- **GitHub Pages** — Papaja is already a public GitHub repo (`raiyan1024/Papaja`), so
  this is the zero-setup option; it already ships with the repo's
  `.github/workflows/deploy-pages.yml` publishing `index.html` and `assets/` on
  pushes to `main`. Caveat: it is "not intended for … online business … e-commerce"
  on the free tier.
- **Netlify / Vercel** — capped at ~15–100 GB/month; fine for a storefront, but watch
  the credits. Vercel's free tier is limited to personal, non-commercial use — a
  commercial storefront should use Cloudflare or GitHub Pages on the free tier.
- **Functions** — you don't need any for Papaja today. If you later add a real
  ordering form, Cloudflare Workers free (100,000 requests/day) is the cheapest place
  to put it; both Netlify and Vercel also have free serverless quotas.

## Recommendation

For a static storefront that may get real traffic:

1. **Cloudflare Pages** — free, unlimited static bandwidth, custom domain and HTTPS
   included, global CDN via Cloudflare.
2. Or **GitHub Pages** — already free and already wired up in the repo via
   `.github/workflows/deploy-pages.yml`.

Both are free of cost and both give you a real domain, HTTPS and a public URL. See
`DEPLOY-ON-CLOUDFLARE.md` for the step-by-step Cloudflare setup for Papaja.

## Sources

- Cloudflare Pages 2026 free tier, limits & pricing:
  https://developers.cloudflare.com/pages/platform/limits/ (read 2026-10-29),
  https://www.cloudflare.com/products/pages (read 2026-10-22)
- Cloudflare Pages vs Workers free tier: https://temps.sh/blog/cloudflare-pages-free-tier-limits-2026
- Hosting comparison (Netlify vs Vercel vs Cloudflare Pages vs GitHub Pages):
  https://www.stork.ai/blog/how-to-host-a-website-for-free-2026
  https://klymentiev.com/blog/free-hosting-comparison-2026
  https://ecn-apps.com/pages/articles/vercel-vs-netlify-vs-cloudflare-pages-2026.html
  https://guptadeepak.com/tools/top-5-static-site-hosting-jamstack-platforms-2026/
