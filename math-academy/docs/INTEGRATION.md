# Integration — ATLAS Math Academy v2.0

This is a standalone static app under one directory. Upload that entire directory into the target web repository, ideally at `math-academy/`. Link your existing navigation to `./math-academy/index.html` or the relevant absolute site URL. The app uses relative imports and fetch paths; maintain `js/`, `css/`, `data/`, `assets/`, and `books/` under the same root. **Do not drop only `index.html` into an arbitrary existing page.**

Example ATLAS navigation:

```html
<a href="/math-academy/">Math Academy</a>
<a href="/math-academy/#finance">Interest &amp; Finance Calculator</a>
<a href="/math-academy/#visuals">Visual Math Atlas</a>
<a href="/math-academy/books/">Mathematics Textbooks</a>
```

For GitHub Pages project repositories, use a repository-relative navigation path rather than assuming your content is mounted at the site root. A site-root-relative `/math-academy/` link is suitable only when the site is hosted at the domain root.

## Static web serving

Modern browsers generally disallow local ES module imports or fetches under `file://`; run a local HTTP server or deploy to a web host. For Windows, the supplied `run_windows.bat` uses Python. For manual serving: `python -m http.server 8000 --bind 127.0.0.1`. This server is for local development, not an authenticated production backend.

## Integration safety

- No code from the target ATLAS site needs to be overwritten. Add navigation only.
- CSS is inside `css/styles.css` and scoped to this standalone page. If you embed it directly into another page, a CSS namespace and conflict audit are required.
- No external dependencies, API keys, or network calls are needed.
- Browser local storage uses keys prefixed with `atlas-math-`; the original completion IDs remain valid.
- The app is educational; amounts, rates and interest are never transmitted to remote services.
