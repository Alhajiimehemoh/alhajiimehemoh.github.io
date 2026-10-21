# Site guide

## Rebuild after any change
    python3 build.py
Needs Python 3 with `openpyxl` and `reportlab` (`pip install openpyxl reportlab`). To refresh the PDFs: `python3 tools/make_pdfs.py` (needs playwright). To check links: `python3 tools/check_links.py`.

## Switch features on: edit site_config.py
| Setting | What it turns on |
|---|---|
| FORMSPREE_ID | Contact and quote forms send to your email (create a free form at formspree.io) |
| BOOKING_URL | "Book a call" opens your Calendly / Google Calendar page |
| LINKEDIN, GITHUB, TIKTOK, YOUTUBE | Social links in the footer |
| ANALYTICS_PROVIDER, ANALYTICS_ID | Cookie-free analytics (GoatCounter or Plausible) |
| GOOGLE_BUSINESS_URL | "Find me on Google Maps" link |
| CERTIFICATIONS, PARTNER_LOGOS | Certifications section, partner logos (only with permission) |
| CASE_RESULTS, CASE_VIDEOS, TUTORIAL_VIDEOS | Result box and video on case studies, videos on Resources |
| KRIO_ENABLED | Krio toggle. Review lang/kri.json with a Krio speaker first |

## Add a note
Open `admin.html` on the site (or locally), write the note, copy the JSON into `notes.json`, run `python3 build.py`, commit.

## Add screenshots
Put anonymised images in `images/cases/<case-name>/` (e.g. `images/cases/case-epi-dashboard/overview.png`). No patient or staff names, IDs or phone numbers.

## Outside steps only you can do
1. Google Search Console: add the site, then submit `sitemap.xml`.
2. Google Business Profile: create it, then paste the link in site_config.py.
3. Formspree, Calendly, analytics accounts: create and paste the IDs.
4. Custom domain (later): buy it, add a CNAME file, set DNS, enable HTTPS in repo Settings > Pages.

## Automatic checks
`.github/workflows/check.yml` rebuilds the site and checks local links on every push.
