# Tools (not part of the live site)

- `art/logo_mix.py` — draws the animated THOMAS logo (family + houseplants woven into the letters). `build('css')` gives the inline SVG used on the home page; `build('frame', t)` gives one frame for the GIF. Needs the Jost Bold font file (`@fontsource/jost`) for the letter outlines.
- `art/family_table.py` — draws the family-around-the-table illustration used on the Thanksgiving page and the menu GIF.
- `art/render_menu_gif.py` — renders the Thanksgiving menu (from `menu-canvas/Main.dc.html`) into the emailable animated GIF.
- `menu-canvas/Main.dc.html` — source of the "Pass the Papadam" menu design.
- `../worker/worker.js` — the Cloudflare Worker (`thomas-family-api`) behind dish claims (`/claims`, `/claim`) and the guest chat (`/ask`). Its `KNOWLEDGE` text and `EVENTS` dish list must match `assets/data.js`; redeploy after changing them.
