# ATLAS Math Academy — Version 2.0

**Expanded working source package for Marc Lavoie · November 20, 2026**

**Scope:** Grades 1–8, Algebra I, Geometry, Algebra II, Precalculus, Calculus I, Calculus II, including real-world financial mathematics.

This package **expands the uploaded v1.0 codebase**, preserves all 145 earlier lessons and their existing completion IDs, and adds **716 newly structured lessons**, **716 matched high-resolution visual illustrations**, **14 offline study textbooks**, **one 146-formula compendium**, and a **30-chapter finance guide**.

## Launch

1. Extract `ATLAS_Math_Academy_v2.0_Marc_Lavoie.zip` fully. **Do not run the app from inside the compressed archive.**
2. Windows: double-click `run_windows.bat` (requires Python 3, used only for local HTTP hosting).
3. macOS/Linux: run `./run_mac_linux.sh` from the extracted directory (requires Python 3).
4. Open `http://127.0.0.1:8000/` in a modern browser. The Windows launcher opens this address automatically.
5. Or deploy the directory to static web hosting (for example `math-academy/` in a GitHub Pages repository) and open that path in your browser.

The main app uses JavaScript ES modules and fetches the visual index, so direct `file://` browsing may fail. The HTML textbooks under **`books/` are independently readable offline even without a local server**.

No backend, npm install, cloud account, CDN, service key or remote data source is required.

## What is included

| Module | Content and capability |
| --- | --- |
| Learn | **861 total lessons**: 145 original plus 716 supplemental topics, arranged in 14 learning tracks, with worked examples, multi-step solutions, hints, individual practice checks, saved progress and visual previews |
| Practice Arena | Question pool from the selected grade curriculum plus generated fluency drills; immediate numeric feedback, hints, worked steps, session tracking |
| Scientific Calculator | Clickable keypad, safe math AST parser, scientific functions, complex arithmetic, statistics, matrices, symbolic derivatives for supported function classes, root solving and numerical calculus |
| Financial Mathematics | **12 specialized calculators**, including simple interest, discrete compound interest, continuous compounding, APY, fixed-rate loan/mortgage payment and amortization, debt payoff, monthly savings, savings goal, inflation, CAGR, NPV and IRR |
| Finance visualizations | Loan balances, interest paid over time, savings contribution breakdown, interest-rate sensitivity comparisons for compound growth, loans and savings, exportable full amortization CSV |
| Graph Studio | Two-dimensional real Cartesian plotting, function comparison, pan, zoom, numerical data table and guided plotting examples |
| Illustrated Concept Atlas | **716** individually generated 1260 × 780 PNG concept illustrations, searchable by name, subject and track; click to inspect a larger diagram or open its matching lesson |
| Formula Field Manual | **146** searchable formulas including a substantial new finance-math section, with executable examples where mathematically supported |
| Books | 14 standalone, print-styled grade-level HTML study guides, one formula compendium and a 30-chapter financial mathematics handbook |

**Honest scope:** This is a substantially expanded educational platform, but no finite set of lessons or browser-only calculator can literally cover *all* mathematics, solve all symbolic equations or certify financial products. The 861 lessons give **broad grade-level coverage** with many guided examples, not guaranteed alignment with every jurisdiction's learning standards or an exhaustive multi-volume university calculus treatment.

## Financial calculator quick start

Open **Finance Lab** from the top navigation or click **Explore interest tools** on the home screen.

- Choose **Compound interest** and type principal `10000`, APR `5`, years `10`, compounding events `12`. The calculator gives approximately **$16,470.09** total value (rate and time fixed).
- Choose **Simple interest**, principal `10000`, APR `5`, years `3`. Interest = **$1,500.00**; ending balance = **$11,500.00**.
- Choose **Mortgage / loan amortization**. The preset is `$240,000`, APR `6.5`, 30 years, and `$150` extra principal per month. The result includes monthly payment, expected payoff period, total interest, a chart, and a downloadable CSV schedule for **every payment period**.
- Choose **APY / effective annual yield** to convert nominal APR to a comparable annual yield.
- Choose **Savings & recurring contributions** for a starting balance and fixed monthly contribution.
- Choose **Net present value** to discount cash flows, or **Internal rate of return** for a numerical rate that zeroes NPV.

**Rate entry convention:** finance tools take an **annual percentage such as `6.5`**, NOT a decimal fraction such as `0.065`. For example `6.5` means 6.5%.

**Keyboard help:** Press `Tab` to move to the next field, `Shift+Tab` to move backward, and `Enter` to submit the selected calculation. In the scientific expression input, `Enter` calculates and `Esc` clears. Keypad buttons insert at the cursor; `=` evaluates. In practice, `Enter` checks the answer. Use `/` outside text inputs to focus curriculum search.

### Finance functions directly inside the scientific calculator

All functions are **case-insensitive**, and percentage rate arguments use annual percent points:

| Scientific expression | Meaning |
| --- | --- |
| `simpleinterest(10000,5,3)` | Earned simple interest, $1,500 |
| `compoundinterest(10000,5,10,12)` | Ending compound balance with monthly compounding |
| `continuousinterest(10000,5,10)` | Ending value with continuous compounding |
| `apy(6,12)` | Effective annual yield **expressed as a percentage**, about 6.1678 |
| `loanpmt(240000,6.5,30)` | Monthly principal-and-interest mortgage payment |
| `savingsfv(3000,250,4.2,10)` | Opening savings plus end-of-month deposits |
| `financenpv(10,-100,110)` | NPV with 10% annual discount rate and annual cash flows |
| `financeirr(-100,110)` | IRR returned **as a percentage**, 10 |

The dedicated Finance Lab is preferable for large tables, explanations, loan schedules, comparisons and visualizations.

## Learning and visual library

Choose a track from the sidebar. Each detailed supplemental lesson has a concept explanation, a worked example, revealable steps, and an individual check-for-understanding. New lessons are labeled with track indices and preserve the earlier course content. Click the illustration to view its high-resolution PNG.

In **Visual Atlas**, search a topic (such as *fractions*, *derivatives*, *trigonometry*, *interest*, *polynomials*). Filter by track or mathematical category. Select a diagram, then select **Study this lesson** to jump into the matching learning chapter. Only 24 diagrams are inserted into the view at once to avoid loading the complete multi-megabyte library at startup.

**Illustration type:** Visuals are computer-rendered educational schematics, curves, arrays, diagrams, or mathematical data illustrations. Many topic-related drawings illustrate a *family-level mathematical concept*, not a formal proof of every theorem in the title. Consult the worked steps and definitions for mathematically precise claims.

### Textbooks

Open `books/index.html` for a standalone workbook collection with all **861 chapters**. The workbooks do not require JavaScript. Every lesson has its answer hidden behind a disclosure control. The books are styled for screen reading or printing. `books/financial-mathematics.html` explains interest and investing models over 30 chapters.

## Precision, formulas, limitations and risks

- JavaScript `Number` is floating-point, so calculations are approximate. Currency is displayed with two decimals but amortization internally retains floating-point precision; contract-level statements may round differently.
- Scientific parser never passes math text through JavaScript `eval`, `Function` or dynamically loaded code. Supported expressions, not arbitrary programs, are evaluated.
- Symbolic differentiation handles the original engine's supported function set, not arbitrary symbolic algebra. Polynomial indefinite integrals are supported within the documented degree constraint. Numerical limits, root finding and adaptive numerical integrals are not proofs and can fail near singularities or oscillations.
- 2D graphing supports real-valued Cartesian functions, not full 3D, implicit curves or computational geometry.
- Finance calculations model fixed nominal rates and stated payment schedules, ignoring variable rates, dates/day counts, bank fees, insurance, taxes, lending-specific disclosures, market returns, and complex cash-flow conventions. IRR calculations may have multiple roots for nonconventional cash flows.
- Interest-rate comparisons are scenarios **not market forecasts**. Use lender or bank disclosures for actual decisions.
- Progress and calculation history are stored in the browser's `localStorage`; this package makes no network analytics requests and does not send answers or sensitive financial values to a server.

## Project architecture

```
ATLAS_Math_Academy_v2.0/
├── index.html                    # SPA: Learn, Practice, Calculator, Graph, Finance, Visuals, Formulas
├── css/styles.css                # Responsive ATLAS blue command-center design
├── js/app.js                     # Navigation, lessons, history, calculator coordination
├── js/math-engine.js             # Safe parser; additional direct financial functions
├── js/calculus.js                # v1 symbolic and numerical calculus engine
├── js/curriculum.js              # v1 lessons, preserving original identity IDs
├── js/expanded-curriculum.js     # 716 supplemental lesson objects
├── js/reference.js              # Base formulas, practice checks, conversions
├── js/finance.js                # 12 finance mathematical engines
├── js/finance-ui.js             # Finance forms, charts, schedules, sensitivity
├── js/finance-formulas.js       # 52 additional formula references
├── js/visual-atlas.js           # Searchable image browser, pagination and lesson links
├── js/graph.js                  # Interactive Cartesian graph studio
├── assets/visuals/*.png         # 716 mathematical diagrams; 1260×780 each
├── data/visuals.json            # Diagram index and linked lesson identifiers
├── data/curriculum-index.json   # Export of supplemental instructional content
├── books/                       # 14 grade workbooks, 1 finance guide, 1 compendium, index/CSS
├── scripts/                     # Reproducible content/visual/workbook generation
├── tests/                       # Node math, finance and content tests
├── docs/                        # Integration, coverage, financial limitations, QA notes
├── run_windows.bat
└── run_mac_linux.sh
```

### Developers

Node is only required to **run tests or regenerate books**; Python 3 is used only for local serving or generating visual assets. Browser execution requires neither.

```bash
node --check js/app.js
npm test
python scripts/generate_syllabus.py
python scripts/generate_visuals.py
node scripts/generate_workbooks.mjs
node scripts/generate_finance_guide.mjs
```

The visual asset generator is reproducible and requires Pillow and NumPy only if you choose to regenerate the images; these Python packages are **not** required to use the website.

## Testing status

The included tests exercise original scientific functionality, calculus, all finance methods, edge-condition validation, matches between every diagram and its corresponding lesson, and each image file's existence. `npm test` should pass all 17 test groups.

**Browser E2E limitation:** An interactive Playwright navigation attempt was blocked by this authoring environment's network/navigation restrictions (`ERR_BLOCKED_BY_ADMINISTRATOR`). Therefore, I have not completed a full browser click-through/visual-rendering certification; source syntax, mathematical results and structured content were validated independently. The supplied static HTML workbooks are additionally inspectable without the application runtime.

**Version history:** v1.0 source was used as the base. v2.0 app preserves original course categories, math-engine functionality, and matching completion storage keys. Do not delete the original version if you want to preserve an independent backup.
