# Accessibility

Platform: Web (local HTML preview). Target: **WCAG 2.2 Level AA**.

This spec replaces the one-line note in `docs/users.md` with checks a reviewer can apply. Page inventory matches `docs/design/information-architecture.md`. Local preview checks that a unit test can make are recorded in `docs/design/accessibility-audit.md`.

A finished human browser and screen-reader audit is **optional for Stage 3** (feature-complete / staging). It is not required to close this Stage 2 design-system task. Venkat has not accepted a human audit.

## Palette and contrast

| Theme | Text | Background | Notes |
| --- | --- | --- | --- |
| Light | `#1c1915` | `#f7f4ef` | Primary body text and chrome |
| Dark | `#f7f4ef` | `#1c1915` | Inverted pair; same relative contrast |

Calculated contrast for the pair is about **15.96:1**, which meets WCAG 2.2 AA for normal text (4.5:1) and large text (3:1), and for non-text UI components / focus indicators (3:1 against adjacent colours). Do not introduce a second brand palette without a design review (`docs/design/brand-identity.md`).

UI chrome (borders, focus ring against page background) must keep at least **3:1** contrast with adjacent colours in both themes (SC 1.4.11).

## Skip link

- The first focusable control on every page is a skip link.
- Visible label: **Skip to content** (or equivalent plain language).
- `href="#main"`. It appears before `<nav>`.
- On focus, the skip link must become visible (not `display: none` / permanently off-screen without a focus reveal).
- Activating it moves keyboard focus to `<main id="main">`.

Maps to SC 2.4.1 Bypass Blocks.

## Focus ring

Every interactive control that receives keyboard focus must show a visible focus indicator in both themes (SC 2.4.7 Focus Visible). Spec for Stage 2:

| Property | Requirement |
| --- | --- |
| Trigger | `:focus-visible` on links, buttons, and form controls (including the search field and theme toggle) |
| Shape | Solid outline (or equivalent box-shadow ring) around the control |
| Thickness | At least **2px** |
| Contrast | Focus indicator contrasts at least **3:1** with the adjacent background in the active theme |
| Obscuring | Focused control must not be fully hidden by sticky chrome or overlays (SC 2.4.11 Focus Not Obscured Minimum) |
| Skip link | Same ring rules apply when the skip link is focused |

Do not remove the outline without replacing it with a style that meets the table above.

## Heading order

- Exactly **one** `h1` per page.
- Index (`/`): `h1` is **Agents Blog** (including when the post list is empty).
- Search, About, Subscribe, 404: one `h1` naming that page.
- Post page: `h1` is the post title; body headings start at `h2` and do not skip levels.
- Do not use heading elements for styling alone.

Maps to SC 1.3.1 Info and Relationships and 2.4.6 Headings and Labels.

## Alt text (future media)

When a post or page includes an image (or other non-text media):

- Decorative images: empty `alt=""` and no redundant caption that only repeats the same decoration.
- Informative images: `alt` describes what the image shows in plain language (not "image of…" unless needed for clarity).
- Complex diagrams: short `alt` plus a longer text description adjacent in the page or linked.
- Do not rely on colour alone to convey meaning in diagrams (SC 1.4.1).

Images are not in the current fixture; this rule applies when media lands in content.

## Shared chrome (all reader pages)

Expected focusable order before page-specific content:

1. Skip link → `#main`
2. Primary navigation: Home, Search, About, Subscribe, Privacy
3. Theme control: button named **Toggle theme**, with `aria-pressed` reflecting the active theme; Space/Enter toggles
4. `<main id="main">` content for that page

Document language is English (`html lang="en"`). Post titles and bodies are escaped so author text cannot inject unlabelled controls.

## Keyboard paths

A keyboard-only user must be able to complete each path without a pointer. Subscribe has no email field, so there is nothing to submit.

### Home (`/`)

1. Tab to skip link → Enter → focus lands in `#main`.
2. Tab through nav links, then Toggle theme (Space/Enter toggles; `aria-pressed` updates).
3. In main: read `h1` "Agents Blog", then post list links (or empty-state copy). Enter on a post link opens that post.

### Search (`/search.html`)

1. Skip link → main.
2. Tab to labelled search field (**Search posts**, `for="search-query"`).
3. Type a query; Tab to any submit control if present, or rely on the documented search activation for the build.
4. Results (if any) are reachable as links in focus order after the field.

### Post (`/posts/{slug}.html`)

1. Skip link → main.
2. `h1` is the post title; body content follows in reading order.
3. In-post links and tag links (if present) are in the tab order after the title/body start.
4. Escaped content: no unexpected interactive nodes from author markup.

### About (`/about.html`)

1. Skip link → main.
2. Single `h1` for About; body links (if any) follow in document order.

### Subscribe (`/subscribe.html`)

1. Skip link → main.
2. Single `h1` for Subscribe; instructional copy only.
3. No email input and no submit control in Stage 2. Keyboard path ends after reading main content and leaving via nav.

### 404 (`/404.html`)

1. Skip link → main.
2. Single `h1` for the missing-page message.
3. A link back to Home (or equivalent) is in the tab order inside main.

## Target size and pointer

Interactive targets meet at least **24×24 CSS pixels** with adequate spacing, or an equivalent exception under SC 2.5.8 Target Size (Minimum). Prefer at least **44×44** CSS pixels for primary nav and the theme button when layout allows.

## What Stage 2 design closes vs Stage 3 audit

| Item | Stage 2 (this spec) | Stage 3 (optional human audit) |
| --- | --- | --- |
| WCAG 2.2 AA target and design rules | Required | Confirm in browser |
| Skip link, headings, labels, contrast pair, keyboard paths | Specified here | Walk with keyboard + screen reader |
| Focus ring in CSS for both themes | Specified; implement with templates | Verify 2.4.7 / 2.4.11 visually |
| Image alt for future media | Rule stated | Check when images exist |
| Venkat-accepted human audit | Not required to close this task | Optional |

## Compliance mapping (design intent)

| Area | WCAG 2.2 AA |
| --- | --- |
| Language, structure, headings | 1.3.1, 2.4.6, 3.1.1 |
| Contrast (text and UI) | 1.4.3, 1.4.11 |
| Skip link | 2.4.1 |
| Focus visible / not obscured | 2.4.7, 2.4.11 |
| Keyboard operable | 2.1.1, 2.1.2 |
| Target size | 2.5.8 |
| Name, role, value (theme button) | 4.1.2 |
| Text alternatives (future media) | 1.1.1 |
