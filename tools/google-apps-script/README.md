# Family calendar helper (Google Apps Script)

`Code.gs` runs in Shajan's Google account and lets the site's Rocky chat add events to the Family calendar (add only).
Its deployment URL is stored on the Cloudflare worker as the `CAL_WRITE_URL` secret, and its shared secret as `CAL_WRITE_TOKEN`.
The copy in this repo has the secret blanked out.
