# kvsecure.com

Static launch site for `kv-secrets`, the local encrypted vault and brokered
credential boundary for AI-assisted development.

The public story to preserve:

- kv stores secrets in a local encrypted vault.
- AI agents should use brokered tools first: `kv_api`, `kv_query`, and `kv_ssh`.
- `kv run` is useful but higher risk because selected secrets can enter a
  subprocess environment.
- Team vaults, cloud sync, billing, and managed organization controls are
  future or private-beta language until production evidence exists.

Avoid absolute or stale claims:

- do not use overstated encryption marketing
- do not claim concrete team prices
- do not publish stale versions or stale verification counts
- do not make absolute product-wide promises that agents can never receive secrets
- do not present future sync or managed sharing work as generally available

## Files

- [index.html](index.html) — homepage and interactive credential-boundary demo
- [guide.html](guide.html) — practical guide
- [faq.html](faq.html) — plain-language product and security answers
- [feedback.html](feedback.html) — feedback page
- [styles.css](styles.css) — shared visual system
- [site.js](site.js) — mobile nav, FAQ accordion, copy button, reveal states, and hero demo mode switching
- [CNAME](CNAME) — GitHub Pages custom domain

## Local Verification

Run these before publishing site edits:

```bash
node --check site.js
python3 tools/check_site.py
python3 -m http.server 8123
```

Then check:

- `/`
- `/guide.html`
- `/faq.html`
- `/feedback.html`
- `/styles.css`
- `/site.js`

For HTML structure, asset references, and stale claims, use the checklist in
[.graft](.graft) plus `python3 tools/check_site.py`. For hero or layout changes,
do a browser visual review at desktop and mobile widths, including both hero
demo modes: `Normal path` and `With kv`.

## Deployment Note

The site is published through GitHub Pages for `kvsecure.com`. After pushing,
verify the live site with a cache-busted URL if needed:

```text
https://kvsecure.com/?v=<commit>
```
