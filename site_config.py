"""
Your settings. Edit this file, then run:  python3 build.py

Anything left empty is simply hidden or falls back to something safe, so the
site always works. Fill things in as you get them.
"""

# ---- contact form -----------------------------------------------------------
# Create a free form at https://formspree.io and paste its ID here (the part after /f/).
# Example: if your form URL is https://formspree.io/f/xyzabcde  then  FORMSPREE_ID = "xyzabcde"
# Empty = forms send the message through WhatsApp instead.
FORMSPREE_ID = "mkjodord"

# ---- booking ----------------------------------------------------------------
# Calendly / Google Calendar appointment page / Cal.com link for 20-minute calls.
# Empty = the "Book a call" button opens WhatsApp with a ready-made message.
BOOKING_URL = ""

# ---- social links (leave empty to hide) --------------------------------------
LINKEDIN = "https://www.linkedin.com/in/alhajiimehemoh/"   # https://www.linkedin.com/in/...
GITHUB = ""     # https://github.com/Alhajiimehemoh
TIKTOK = ""     # https://www.tiktok.com/@...
YOUTUBE = ""    # https://www.youtube.com/@...

# ---- privacy-friendly analytics (no cookies) ---------------------------------
# provider: "goatcounter" (id = your code, e.g. "alhaji" for alhaji.goatcounter.com)
#           "plausible"   (id = your site domain, e.g. "alhajiimehemoh.github.io")
#           ""            (analytics off)
ANALYTICS_PROVIDER = ""
ANALYTICS_ID = ""

# ---- local search -------------------------------------------------------------
# Paste your Google Business Profile link here after you create it (see GUIDE.md).
GOOGLE_BUSINESS_URL = ""

# ---- Krio language toggle -----------------------------------------------------
# The Krio text in lang/kri.json is a DRAFT. Review and correct it, then set True.
KRIO_ENABLED = False

# ---- credibility sections (empty list = section hidden) -----------------------
# Example: {"name": "Power BI Data Analyst", "issuer": "Microsoft", "year": "2026", "url": ""}
CERTIFICATIONS = []

# Partner or client logos you have permission to show.
# Example: {"name": "RHCI", "image": "images/partners/rhci.png", "url": "https://..."}
PARTNER_LOGOS = []

# One-line result per case study (shown as a highlighted box). Use real, defensible figures only.
# Keys: case-epi-dashboard, case-survey123, case-chw-card-studio, case-dms
CASE_RESULTS = {
    # "case-epi-dashboard": "Monthly EPI reporting now takes X hours instead of Y days.",
}

# Demo video per case study: a YouTube / Vimeo / direct .mp4 link.
CASE_VIDEOS = {
    # "case-epi-dashboard": "https://www.youtube.com/watch?v=...",
}

# Tutorial or explainer videos for the Resources page.
# Example: {"title": "Excel tips for facility staff", "url": "https://www.youtube.com/watch?v=..."}
TUTORIAL_VIDEOS = []

# Screenshots: just drop image files into  images/cases/<case-name>/  (for example
# images/cases/case-epi-dashboard/overview.png). They appear on that case study automatically.
# Use anonymised screenshots only: no patient or staff names, IDs or phone numbers.
