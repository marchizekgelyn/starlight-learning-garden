# ATLAS Super Calculator v3.0 — Standalone Edition

**Prepared for Marc Lavoie · November 20, 2026**

A self-contained, visual mathematics calculator application built with HTML5, CSS3, ECMAScript modules and the HTML Canvas 2D API. **It is intentionally separate from ATLAS Math Academy.** Codex can integrate the entire application or individual pure-function modules later. No math-academy pages, curriculum files or website-specific integration code are included here.

## Launch the application

### Windows

1. Unzip the archive to a normal folder.
2. Install Python 3 if it is not already installed.
3. Double-click **`run_windows.bat`**. This starts a local web server on **http://127.0.0.1:8765** and attempts to open the URL in your default browser.
4. Select a workspace in the sidebar. All math runs in your browser, not a remote server.
5. Close the command window to stop the server.

### macOS / Linux

Run `./run_mac_linux.sh` and navigate to `http://127.0.0.1:8765`.

### Alternative local server

Run `python3 -m http.server 8765 --bind 127.0.0.1` from the extracted folder, or `npm run serve` (Node is needed only to launch this shortcut). Then browse to `http://127.0.0.1:8765`.

> **Why a server?** Modern browsers restrict JavaScript ES module imports and local JSON fetch requests in `file://` documents. A local HTTP server is a browser requirement, **not a backend service**. There are no network APIs, package installation steps, npm runtime dependencies, analytics scripts, login, or external CDNs.

## What is inside

- **Scientific calculator**: fully clickable 42-key expression keypad, precedence, parentheses, percentages, powers, logarithms, trigonometry, factorials, combinations and permutations, complex numbers, common financial functions, Ans memory and exportable local history.
- **Interactive graphing**: up to four Cartesian functions, polar graphs `r(theta)`, parametric curves `x(t), y(t)`, and numerical 3D surface wireframes `z=f(x,y)`, including pan/zoom, rotation, reset and PNG export. Graphs are drawn entirely in browser Canvas.
- **22 financial calculators**: 12 original ATLAS financial modes plus 10 new advanced modes, including simple and compound interest, effective APY, continuous interest, savings goals, loans, mortgage estimates, debt payoff, NPV, IRR, vehicle loans, interest comparisons, refinance break-even, loan rate solving, retirement purchasing power, the rule of 72, discounts, business break-even and depreciation. CSV export for generated payment tables/cash-flow series.
- **25 guided math operations**: algebraic root solving, quadratics, numerical and symbolic calculus, matrix operations, regression, descriptive statistics, probability distributions, exact fractions, integer math, number bases, date arithmetic, percentages and more.
- **12 conversion families**: length, area, volume, mass, time, speed, energy, power, pressure, data, temperature, angles.
- **11 geometry shapes**: area, surface area, perimeter, diagonal and volume where relevant.
- **532 bundled high-resolution mathematical diagrams**: an offline, searchable and filterable illustrated formula/reference atlas covering Grades 1–8, Algebra I/II, Geometry, Precalculus and Calculus I/II. The images are repurposed, original assets from the previously generated ATLAS Math Academy v2.0, deliberately **not** a dependency on that website.
- **Responsive command-center UI**: mobile navigation, keyboard guidance, contextual descriptions, calculation feedback, command search (Ctrl+K), local browser history and an on-screen help guide.

## Keyboard shortcuts

| Key | Behavior |
|---|---|
| `Enter` | Evaluate the current expression or active advanced-calculation form |
| `Tab` | Move to the next field, for example **principal → APR → years** |
| `Shift` + `Tab` | Move to the previous field |
| `Esc` | Clear scientific expression when focused; close open search/diagram modal |
| `Ctrl` + `K` / `⌘` + `K` | Search calculator commands and navigate directly |
| `Ctrl` + `Enter` | Plot a graph from the multi-line graph input without inserting a newline |

### Examples

| Problem | Direct scientific expression or calculator path | Expected result |
|---|---|---|
| Compound interest: $10k, 5% APR, monthly, 10 years | `compoundinterest(10000,5,10,12)` | Approximately **$16,470.09** |
| Fixed mortgage: $240k, 6.5%, 30 years | `loanpmt(240000,6.5,30)` | Approximately **$1,516.96/month**, P&I only |
| Derivative at x=2 | Calculus → Symbolic derivative, `x^3+2*x`, point `2` | **14** |
| Integrate sine from 0 to π | Calculus → Definite integral, `sin(x)`, bounds `0`, `pi` | Approximately **2** |
| Matrix inversion | Linear Algebra → Matrix, `1,2;3,4` + `inverse` | `[[-2,1],[1.5,-0.5]]` |
| Fraction sum | Exact Math → Fractions, `7/12 + 5/18` | **31/36**, exactly |
| Savings payment plan | Finance → Savings & recurring contributions | Growth series and total interest |

## Folder layout

```
ATLAS_Super_Calculator_v3.0/
├── index.html                    Standalone HTML application
├── css/app.css                   Responsive dark-blue interface
├── js/
│   ├── app.js                    UI orchestration & workspaces
│   ├── math-engine.js            Safe expression parser & scientific functions
│   ├── calculus.js               Symbolic & numerical calculus
│   ├── advanced.js               Probability, stats, units, matrices, exact fractions, etc.
│   ├── finance.js                Base financial mathematics
│   ├── finance-plus.js           Expanded financial calculators
│   ├── graph.js                  Legacy Cartesian graph component (kept as reference)
│   └── graph-viz.js              New Canvas 2D, polar, parametric and 3D plots
├── assets/
│   ├── atlas-mark.svg            App identity icon
│   └── visuals/*.png             Bundled reference diagrams (532 assets)
├── data/visual-library.json      Searchable diagram index
├── docs/                         Technical docs, user guide, Codex handoff
├── tests/                        Automated Node regression suite
├── run_windows.bat
├── run_mac_linux.sh
└── package.json                  Development test/run commands only
```

## Run tests

Requires Node.js 20+ **only for development/tests**, not to use the app:

```shell
cd ATLAS_Super_Calculator_v3.0
npm test
```

Test coverage spans numerical benchmarks, finance, distributions, matrices, security rejection checks, functional defaults for all guided tools, and required app sections. See `docs/QA_REPORT.md` for the actual verified test count and browser-test limitations.

## Accuracy and safety boundaries

This is a powerful local math calculator, **not a claim of universal symbolic computation**. It does not support every branch of abstract mathematics, formal proof, high-precision transcendental arithmetic, or arbitrary indefinite integration. Polynomial antiderivatives are symbolic; other definite integrals are evaluated numerically. Symbolic differentiation supports selected elementary functions. Graphing and 3D rendering use numerical samples. Financial projections use modeled constant rates and assumed payment timing; APR-to-APY results exclude fees. Read the module-specific notes for sampling/precision limits, and independently verify consequential calculations.

For financial decisions, confirm rates, charges, amortization conventions and tax treatment against actual lending or account documents. No financial institution connection is provided.

## Code provenance

The math expression engine, calculus engine and initial finance engine are adapted from the original ATLAS Math Academy v2.0 project generated earlier in this conversation. The expanded finance/math modules, graphing renderer and UI are engineered as an independent application. All bundled visual assets are the ATLAS-generated educational images from that previous deliverable. The package does not bundle third-party proprietary code or fonts and has no runtime dependencies.

© 2026 Marc Lavoie · ATLAS Super Calculator
