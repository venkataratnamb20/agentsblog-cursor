# Performance budgets

These checks are transfer budgets for the local static preview. They
measure bytes and request hosts on pages written by
`agentsblog.build.build_site`. They are not a lab run and they are not
field Core Web Vitals. LCP, INP, and CLS are not measured. There is
no public host, no analytics vendor, and no real-user monitoring, so
field data is not collected.

An analytics beacon is not allowed on the built pages. Venkat must
approve any RUM vendor before one is added. That approval is separate
from these local budgets.

## Limits

The preview stays small enough for a later consent banner and a little
more CSS. The numbers below are file sizes on disk after a build, not
compressed transfer sizes from a CDN.

| Check | Limit |
| --- | --- |
| `index.html` | 20000 bytes |
| `assets/site.css` | 8000 bytes |
| External scripts | No `<script src=` in built HTML |
| Font stylesheets | No `fonts.googleapis.com` and no `cdn.` host |

`tests/unit/test_performance_budgets.py` builds one published post and
one draft into a temporary directory and checks those limits. Drafts
stay out of the published pages. The test does not call a browser, a
lab tool, or a field collector.

## What this does not claim

- LCP (Largest Contentful Paint) is not measured.
- INP (Interaction to Next Paint) is not measured.
- CLS (Cumulative Layout Shift) is not measured.
- Lab data from Lighthouse or WebPageTest is not collected.
- Field data is not collected.

A green unit test means the local preview stayed inside the byte and
request budgets above. It does not mean the public site meets a Core
Web Vitals target.
