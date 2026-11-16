# REA browser capture attempt

REA `capture_browser_scenario` launched its owned Chromium 150.0.7871.181 and attempted a read-only GET of the supplied builder URL. Navigation failed before the page state was captured.

Observed network evidence from the partial REA result:

- Request: `GET https://www.gitskins.com/readme-builder?username=Sakthivel-P-Cse&template=community-creative-dev-rt3x`
- Failure: `net::ERR_CERT_AUTHORITY_INVALID`
- DOM/accessibility/screenshot: not captured because initial navigation failed

The identical capture request was not retried. REA `doctor` ran as instructed, but its checks cover REA setup/deep-analysis providers and do not establish that this browser certificate is trusted. The current CUA browser host is unavailable, and no local Chrome process/CDP port was present to attach to.

## Safe next route

Use a browser session that already trusts the site's certificate, open the exact URL there, then attach REA to that session's loopback CDP endpoint and passively inspect the page. Do not disable certificate validation or use an ignore-certificate-errors flag. If no trusted browser session is available, the screenshot and pasted DOM remain the usable design evidence.

A read-only launch scenario is saved in `rea-scenario.json` for a host where the certificate chain is trusted. It requests DOM, accessibility, screenshot, final URL, and network/console/page-error evidence.
