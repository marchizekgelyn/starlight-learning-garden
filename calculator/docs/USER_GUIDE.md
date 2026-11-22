# ATLAS Super Calculator — operator guide

## Scientific keypad

Type a mathematical expression in the top display, or click the 42 keys. `=` or **Enter** runs the expression. `AC` clears all; `DEL` removes the character before the cursor. Click `ANS` to reference the last computed result. `RAD ↺` switches to degrees, useful for `sin(90)`.

Accepted examples include `2^3^2`, `sqrt(144)`, `sin(pi/2)`, `5!`, `ncr(52,5)`, `ln(e)`, `compoundinterest(10000,5,10,12)` and `loanpmt(240000,6.5,30)`. Use explicit multiplication `2*x` when working with symbolic variables.

## Workspaces

### Graphing Studio

Use a function like `sin(x)`; enter multiple functions on separate lines in Cartesian mode. For polar, enter `r(theta)`, e.g. `2+cos(5*theta)`. For parametric, enter x(t) and y(t), e.g. `cos(3*t)` and `sin(2*t)`. For the 3D surface wireframe, enter `sin(sqrt(x^2+y^2))*3`. Click **Plot function**, drag to pan/rotate and scroll to zoom.

### Financial Laboratory

Choose a model in the left panel. The model displays explanatory field labels and reasonable sample defaults. Use **Tab** to move from one number to the next; **Shift + Tab** to reverse, and **Enter** to calculate at any input field. Read interest, payments and total financial outputs on the right. When the method produces periods, export all rows using **Export full CSV**. The plotted chart visualizes the amortization balance or projected financial series.

### Advanced math

Algebra handles quadratics, numerical roots and percentages. Calculus differentiates selected formulas, estimates limits, evaluates integrals, Taylor polynomials and bounded sums. Linear Algebra covers matrices and square systems up to 8×8. Statistics calculates descriptive summaries and histograms, plus least-squares regression. Probability covers exact binomial, Poisson and approximate normal models with confidence intervals. Exact Math includes arbitrary-precision rational numbers and integer calculations.

### Geometry & conversion

Pick a shape and type the dimensions in a consistent unit. Choose one of the 12 measurement dimensions for units and press the swap arrow to reverse direction. Exchange rates are not included because they require fresh external data.

### Visual Formula Atlas

The searchable visual atlas contains 532 high-resolution diagrams from 14 math tracks. It is a reference and visualization gallery, not a dependency on the existing Academy website. Use a learning-track filter and click a diagram for larger viewing.

## Troubleshooting

**The page appears but tools do not respond:** You likely opened the `index.html` file directly. Use `run_windows.bat` or a local HTTP server so browser ES modules load properly.

**Calculator says undefined result or division by zero:** The mathematical expression is outside its real/complex domain, has a singularity, or exceeds machine precision. Refine the expression.

**Integration fails or numerical limit is inconsistent:** Numerical methods cannot prove all limits or detect every internal discontinuity. Split the interval or analytically verify.

**Payment differs from a bank estimate:** Some lenders use daily interest, paid-in-advance timing, fees, compounding conventions, or extra components. The built-in fixed-payment loan model assumes nominal APR divided by payments per year and end-of-period payments. Compare all assumptions.

**No images in the atlas:** Verify `data/visual-library.json` and `assets/visuals/` are present in the same extracted folder, with server access.
