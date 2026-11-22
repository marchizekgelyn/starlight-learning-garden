# QA report — ATLAS Super Calculator v3.0

**Build:** Standalone static calculator · November 20, 2026

## Automated mathematical checks

- **26 of 26** Node.js regression test groups passed.
- Scientific arithmetic, precedence, trigonometric modes, combinatorics, complex values, and rejection of non-mathematical code.
- Mathematical finance benchmarks: monthly-compounded $10,000 at 5% for 10 years ≈ **$16,470.0949769**; $240,000 at 6.5% for 360 months ≈ **$1,516.963256/month** principal and interest.
- Derivative, polynomial antiderivative, numerical definite integral, roots, limits, Taylor series, and summation.
- Matrices, Gaussian solving, eigenvalues, descriptive statistics, least-squares regression.
- Binomial, Poisson and normal-distribution approximations.
- BigInt fractions and base conversion; units, geometry, percentages, and dates.
- The default example was executed for every one of **25 guided advanced mathematical modes** and **22 financial modes**.

## Browser interaction tests

Chromium was used to execute the real user-interface JavaScript in an **in-memory document with module imports rewritten to local data URLs** because the build environment prohibits navigating directly to even localhost addresses. The visual-asset index was locally mocked using the shipped JSON data, not a fabricated index. The actual packaged files remain ordinary ES module files and are not modified by this test setup.

The automated browser test completed successfully with **no JavaScript page errors**, covering:

- 42-keypad initialization; scientific Enter calculation of compound interest.
- All **25 guided math forms** through clickable mode selection and Calculate buttons.
- All **22 finance forms** through actual mode selection and Calculate buttons.
- Cartesian graph render; 3D surface graph render; on-screen graph status.
- 18-at-a-time atlas gallery and modal; local index search.
- Keyboard Ctrl+K command search.
- Responsive phone layout, mobile navigation drawer, and navigation into Finance.

**Limitations:** direct local HTTP navigation and real hosted end-to-end asset requests could not be exercised due to environment policy. Actual production browser hosting, file URLs, iframe embedding, and cross-browser compatibility should be rechecked by Codex in the target deployment.

## Asset audit

- **532 of 532** PNG files pass Python Pillow image verification.
- **532 of 532** gallery metadata records resolve to real local images.
- All referenced HTML script, CSS, favicon and ES module import paths resolve to existing files.
- All **8 JavaScript source files** pass `node --check` syntax validation.
- **13 workspace sections** are present in the standalone `index.html`.

## Reproduce checks

```
node --test tests/*.test.mjs
python3 tests/browser_smoke.py
```

The Chromium smoke test needs Python Playwright installed, a local Chromium executable at `/usr/bin/chromium`, and a browser environment permitting `page.set_content()`. The application itself needs neither Python Playwright nor Node dependencies beyond a local static file server.

## Numerical and product limitations

- The symbolic integrator handles **polynomial indefinite integrals**; it does not perform general computer algebra integration.
- Symbolic differentiation supports an explicit elementary-function subset. Numerical limits, derivatives, integrals and graphs are approximations, not mathematical proofs.
- The polynomial Taylor tool supports degrees 0–8.
- Matrix tools are limited to 8×8 and use binary64 floating point.
- Financial amortization assumes standard periodic compounding and end-of-period payments. Property tax, PMI, HOA, insurance, taxes, fees, inflation, market returns and similar assumptions depend on user-supplied information.
- Interest-rate and investment calculators are educational estimates, not regulated lender disclosures or investment predictions.
- The diagram atlas is an offline reference library; individual visuals are not an interactive proof engine.

**Conclusion:** successfully verified as a substantial standalone calculator prototype with 47 guided form workflows, functional scientific/graphing interaction, an offline diagram atlas and a documented integration contract. Live production deployment and accessibility audit remain future validation steps.
