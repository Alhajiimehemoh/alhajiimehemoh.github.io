# Things only you can fill in or confirm

1. Contact form: create a free form at formspree.io and replace `xxxxabcd` in `build.py` (search "xxxxabcd"), then run `python3 build.py`.
   Until then the form sends the message through WhatsApp.
2. Experience dates: your old site said SLPP started Jan 2021; this version uses Jan 2022 to Sep 2023 (matches Growth Centre ending in 2021). Correct if wrong.
3. Education: "BSc Computer Science (in progress)". Edit the line in `build.py` if you want to name the university.
4. Reported figures kept from your old site: 25% accuracy improvement, 99% availability, 30% online engagement, 200+ students. Add one line on how each was measured, or remove any you cannot support.
5. Project case studies: add anonymised screenshots or a short result per project (for example hours saved per month, number of facilities covered). Never publish patient or staff data.
6. Status labels (In development, Built, In design, Designed): update as projects move on.
7. Third testimonial is anonymous ("IT client, Bo"). Add a name or business if the client agrees.
8. Notes: copy an entry in the NOTES list in `build.py`, then run `python3 build.py`. Add real dates when you publish new posts.

How to edit: change text in `build.py` (all page content) or `style.css` (design), then run `python3 build.py` to regenerate the pages.

## Added in v11: things only you can supply
- Formspree ID, booking link, social URLs, analytics ID, Google Business link (site_config.py)
- Anonymised screenshots, one-line results and demo videos per case study
- Real certifications and partner logos (with permission)
- A named testimonial you have permission to publish (current ones are unverified)
- Dates for notes (notes.json) so RSS and ordering work properly
- Review FAQ answers, the Now page and the capability statement for accuracy
- Krio translations in lang/kri.json must be reviewed before KRIO_ENABLED = True
- Confirm: SLPP start date (Jan 2022), education wording, and the figures 25%, 99%, 30%, 200+
