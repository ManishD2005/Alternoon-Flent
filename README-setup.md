# Keyhole Hunt — setup guide

This folder is everything you need. It's a single static page (`index.html`) — no build step, no framework, no backend server of your own to run.

---

## 1. How the "QR scan" actually works

The in-app "Tap to Scan!" button is just a manual fallback for previewing the flow. In real use, guests scan a **physical QR code** you print and hide at each spot (balcony, kitchen, bedroom) using their phone's normal camera app — not a scanner built into the page.

Each physical QR code encodes a direct link straight to that room's reveal screen, e.g.:

```
https://your-domain.vercel.app/#r1   → The Balcony
https://your-domain.vercel.app/#r2   → The Kitchen
https://your-domain.vercel.app/#r3   → The Bedroom
```

The page already listens for that `#r1` / `#r2` / `#r3` part of the URL and jumps straight to the right screen on load — that's already built in, no extra setup needed on your end.

**What you need to do:**
1. Deploy the site (see step 3 below) and get your real Vercel URL (e.g. `flent-hunt.vercel.app`).
2. Regenerate the 3 QR codes in `/qr-codes` with your real domain instead of the placeholder one (see the regenerate script below, or just tell me your final URL and I'll regenerate them for you).
3. Print them and place them at the balcony, kitchen, and bedroom.

**To regenerate the QR codes yourself** (needs Python):
```bash
pip install qrcode[pil]
python3 regenerate_qr.py https://your-real-domain.vercel.app
```
(`regenerate_qr.py` is included in this folder.)

> Why not an in-page camera scanner? A camera-based scanner (e.g. the `html5-qrcode` library) is possible, but adds camera-permission prompts, HTTPS requirements, and iOS Safari quirks — fragile for guests who just want a quick "aha" moment. The direct-link approach works with zero friction on every phone's built-in camera app.

---

## 2. Making the enquiry form actually submit somewhere

The "Enquire" button on the last screen is wired up to POST to a Google Apps Script "Web App" URL, which appends each submission as a row in a Google Sheet. You just need to create that Sheet + script once (~5 minutes, free, no coding beyond copy-paste):

1. Create a new Google Sheet. Add a header row: `Name | Phone | Email | Submitted At`.
2. In the Sheet, go to **Extensions → Apps Script**.
3. Delete the placeholder code and paste this:

   ```javascript
   function doPost(e) {
     const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
     const data = JSON.parse(e.postData.contents);
     sheet.appendRow([data.name, data.phone, data.email, data.submittedAt]);
     return ContentService.createTextOutput(JSON.stringify({status: 'ok'}))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```

4. Click **Deploy → New deployment**. Choose type **Web app**.
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Click **Deploy**, authorize it (it'll warn you it's an unverified app — that's normal for personal scripts, click through Advanced → Go to project).
6. Copy the **Web app URL** it gives you (ends in `/exec`).
7. Open `index.html`, find this line near the top of the `<script>` block:
   ```javascript
   const SHEETS_ENDPOINT = "PASTE_YOUR_GOOGLE_APPS_SCRIPT_URL_HERE";
   ```
   Replace the placeholder with the URL you copied.
8. Re-deploy (push the change to GitHub — Vercel auto-redeploys).

That's it — every enquiry submission now lands as a new row in your Sheet, and you can set up an email notification rule on the Sheet itself if you want a ping (Tools → Notification rules).

---

## 3. Deploying to GitHub + Vercel

Because this is a single self-contained HTML file, there's nothing to build.

1. Create a new GitHub repo (public or private, doesn't matter).
2. Add just `index.html` (already renamed for you in this folder) to the repo root. That's the only file Vercel needs.
3. Push it:
   ```bash
   git init
   git add index.html
   git commit -m "Keyhole hunt"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
4. Go to [vercel.com](https://vercel.com), click **Add New → Project**, and import that GitHub repo.
5. Vercel will detect it as a plain static site — **Framework Preset: Other**, no build command, no output directory needed. Click **Deploy**.
6. You'll get a URL like `your-repo.vercel.app`. That's your live site.
7. (Optional) Add a custom domain under Project → Settings → Domains.

Once you have that real URL, come back to step 1 and regenerate/print the QR codes with it.

---

## Files in this folder
- `index.html` — the whole app (upload this to GitHub as-is)
- `qr-codes/r1.png`, `r2.png`, `r3.png` — printable QR codes (placeholder domain, regenerate after deploying)
- `regenerate_qr.py` — script to regenerate the QR codes with your real domain
