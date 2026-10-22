"""AIM logo as an inline, animatable SVG (traced from images/brand/logo-mark.png)."""
SW = 'M18 356 Q228 150 440 318 L417 338 Q228 186 18 356 Z'   # swoosh shape
SWC = 'M18 356 Q228 168 429 328'                               # swoosh centre line

def aim_logo(uid, cls='', label=None):
    a = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true" focusable="false"'
    return (f'<svg class="aim {cls}" viewBox="0 0 640 375" {a}>'
      f'<defs><linearGradient id="lgg{uid}" x1="0" x2="1"><stop offset=".25" stop-color="var(--lg-navy)"/><stop offset=".55" stop-color="var(--lg-teal)"/></linearGradient>'
      f'<mask id="lgm{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="640" height="375"><rect width="640" height="375" fill="#fff"/><path d="{SWC}" fill="none" stroke="#000" stroke-width="44"/></mask>'
      f'<mask id="lgd{uid}" maskUnits="userSpaceOnUse" x="0" y="0" width="640" height="375"><path class="lg-draw" pathLength="1" d="{SWC}" fill="none" stroke="#fff" stroke-width="60"/></mask></defs>'
      f'<g mask="url(#lgm{uid})">'
      f'<path class="lg-a" d="M226 84 L364 354 L313 354 L206 141 L135 262 L106 276 Z"/>'
      f'<rect class="lg-i" x="342" y="88" width="44" height="200"/></g>'
      f'<path class="lg-m" d="M398 88 L413 88 L503 250 L586 88 L620 88 L620 354 L574 354 L574 142 L483 320 L398 156 Z"/>'
      f'<g mask="url(#lgd{uid})"><path class="lg-s" d="{SW}" fill="url(#lgg{uid})"/></g>'
      f'<circle class="lg-dot" cx="365" cy="43" r="24"/>'
      f'<circle class="lg-ring" cx="365" cy="43" r="24"/>'
      '</svg>')
