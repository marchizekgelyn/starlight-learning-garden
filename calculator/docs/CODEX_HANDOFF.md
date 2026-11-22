# Codex integration handoff — standalone ATLAS Super Calculator

## Contract

**The calculator is finished as a separate deployable static web application.** Do not delete or rewrite the existing ATLAS Math Academy website when integrating it. Preserve the calculator's own routes, styling, math modules, media assets, public function interfaces and tests.

### Preferred option: deploy it as a separate folder

1. Copy the entire `ATLAS_Super_Calculator_v3.0` folder into an accessible website path, for example `/super-calculator/`.
2. Ensure the host serves `index.html`, CSS, JS ES modules and the JSON/PNG assets with correct MIME types. No server code is needed.
3. Link to `/super-calculator/` from the academy navigation, or embed the app in an `<iframe>` with an accessible title. If embedding, ensure a generous height or provide a full-screen link. **Avoid duplicating global CSS across the parent page.**
4. Run tests and verify all 13 workspace screens manually in the target browser.

### Optional option: integrate calculation functions, not the UI

Use the exported pure-function interfaces:

```javascript
import { calculate } from './js/math-engine.js';
import { runMethod, METHODS, convertUnit, geometry } from './js/advanced.js';
import { calculateFinance, FINANCE_TOOLS } from './js/finance-plus.js';

calculate('sin(pi/2)'); // 1
await runMethod('derivative', {expression:'x^3+2*x', at:'2'});
calculateFinance('compound', {principal:10000,apr:5,years:10,periodsPerYear:12});
```

All functions use explicit arguments. `runMethod` can return an object or a Promise (the quadratic option currently loads the quadratic solver via a dynamic import); use `await` for uniform handling. Finance result envelope: `{result, rows, note, formula, type}`. The original financial methods are preserved in `finance.js`.

### Graph code

`GraphVisualizer` in `js/graph-viz.js` owns its `<canvas>`, status, hover and legend elements. It is designed as a standalone component. Canvas sampling assumes radians for graph variables. It requires no GPU or WebGL library.

### Asset manifest

`data/visual-library.json` contains 532 records with their relative image paths. Images are in `assets/visuals`. Preserve this file and the directory together. The app renders only the first 18 images in its atlas initially, loading more when requested.

### No backend security scope

- Calculator expressions are parsed by `js/math-engine.js`, not passed to `eval()` or `Function()`.
- Calculator history is stored in the browser's `localStorage`; a user can clear/export it.
- There is no request for login, payments, private records, or server-side computation.
- For public hosting, configure a restrictive Content Security Policy after validating app features on the destination domain.
- Numerical calculations can still be resource-intensive. When adapting for untrusted multi-user use, consider Web Worker timeouts and stronger input/resource limits.

### Acceptance checklist

1. Scientific expression computes `compoundinterest(10000,5,10,12)` → approx `$16,470.09`.
2. Clicking the calculator's number keys inserts at the cursor; Enter calculates; Tab moves focus.
3. Finance selection works; mortgage estimate produces P&I, escrow, extra payment and loan schedule CSV.
4. Cartesian graph plots sine/cosine; polar and parametric modes render; surface plot rotates when dragged.
5. Algebra, Calculus, Linear Algebra, Statistics and Probability forms work by Enter and click.
6. Converter source/destination swap works; geometry controls render diagrams.
7. Visual Atlas loads local diagrams by grade/topic and opens larger modal.
8. Command search Ctrl+K finds advanced functions, keyboard accessibility works.
9. Sidebar collapses on phone layouts; no horizontal overflow in main content.
10. `npm test` passes. Also do real manual browser testing after deployment (not available in the original build environment).

### Known limits

Calculator v3.0 is not a general-purpose symbolic CAS on the level of Mathematica or Maple, and does not make every mathematical question solvable. It includes targeted school-through-Calculus-II and applied calculator workflows, with safe numerical fallback and clear error handling. Date calculations omit official holidays; currency FX conversion intentionally requires a separate authoritative rate source.
