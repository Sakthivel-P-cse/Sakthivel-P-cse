# GitSkins README builder UI scrape reference

This folder now contains the rendered HTML and a full-page screenshot supplied from Firefox, plus a compact DOM summary.

- `live-preview.html`: rendered README preview markup copied from Firefox DevTools.
- `dom-summary.json`: headings, image URLs, links and CSS classes extracted from that markup.
- `firefox-fullpage.png`: full-page builder screenshot (907 × 4202 px).
- `scrape.json`: page/preview inventory and capture limits.
- `reference.png`: earlier screenshot supplied in chat.
- `rea-attempt.md` and `rea-scenario.json`: REA attempt notes and the safe scenario; REA's isolated Chromium hit a TLS certificate authority error.

The Firefox capture is a rendered HTML snapshot, not a live browser session. It shows GitSkins' **Anthony Fu (@antfu) sample preview**, with a placeholder About Me sentence, rather than Sakthivel's personalized profile. It contains no page stylesheet or computed-style values. Use the screenshot for visual details and the HTML for structure, text and image URLs.
