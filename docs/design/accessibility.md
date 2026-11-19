# Accessibility

The target is WCAG 2.2 AA. The site is not audited yet. This spec replaces the one-line note in `docs/users.md` with checks a reviewer can apply. `docs/design/information-architecture.md` links the same pages. User instruction: "Go ahead and complete the next goals. Deploy multiple agents with similar and relevant skills with gitworktree."

## What the local pages do now

- The document language is English.
- The search field has a visible label, "Search posts".
- The theme control is a button named "Toggle theme". A keyboard user can reach it and activate it.
- Light text is `#1c1915` on `#f7f4ef`. Dark text is `#f7f4ef` on `#1c1915`.
- Post text is escaped, so a title cannot inject an unlabelled control.

## What implementation still needs

- A skip link as the first focusable control. It goes to the main content.
- The theme button exposes whether the current theme is light or dark.
- Images, when a post has them, need alt text that says what they show.
- Focus is visible on links, the search field, and the theme button in both themes.

## Check

A person can move through Home, Search, a post, About, Subscribe, and the 404 page with the keyboard alone. Subscribe has no email field, so there is nothing to submit.
