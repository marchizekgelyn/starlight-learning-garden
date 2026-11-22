# ATLAS English Academy 3.0 — Verification Report

**Build date:** 2026-11-21. **Source:** uploaded ATLAS English Academy v2.0 ZIP. **Platform:** standalone HTML/CSS/vanilla JS, optional loopback-only Python review service.

## Completed automated checks

1. Original v1 validation: **192 lessons, 1,920 assignments**, 1,344 objective answer keys, UI smoke simulation — passed.
2. Preserved v2 validation: **1,536 lessons, 23,040 exercises**, verified reference keys, six-dimension essay shape and repetition controls — passed.
3. v2 Python data check: 16 levels × 96 lessons, 12 strands, all 1,536 SVGs valid XML — passed.
4. New v3 assignment generation: **1,536 × 8 = 12,288 new writing prompts**, unique IDs, checklists, response level, parent verification and evidence anchors — passed.
5. v3 assessment regression tests: bounded score [0,100], grade profiles, synthetic reasonable/irrelevant/repetitive examples, no unsupported source grade, sentence segmentation, cautious proofreading, parent calibration function — passed.
6. Browser smoke in Chromium with actual scripts supplied via an injected test page: home, navigation, lazy lesson/task data, writing task selection, paragraph submission, displayed estimate and rubric, independent parent score, grade change, page mode — passed with **no JavaScript page errors**.
7. Local review adapter Python syntax compilation — passed.

## Important test limitations

The Chromium environment blocks direct navigation to `file://` URLs. As a workaround, the browser smoke test injected the original stylesheet and application scripts into a page and simulated the local lazy script loader using the unmodified data contents. It is a useful interaction test but **not proof that a double-click launch works on every Windows machine**. No external network, remote AI model or localhost Ollama/LM Studio was started. The local model's semantic response quality was not measured.

There is **no real human-graded benchmark**, no independently rated student paper set, no measured mean absolute error against expert teachers, and no external validation of fairness. Synthetic regression results cannot establish grade accuracy. Accuracy must be measured with permissioned, representative papers scored by qualified readers as described in `docs/ASSESSMENT_ARCHITECTURE_V3.md`.

The content volume is generated assessment specifications and not evidence that every writing prompt was individually reviewed by a specialist teacher. Before use in high-stakes education, audit the prompts and source anchors for grade appropriateness and fairness.

## Build consistency

The archive includes a SHA-256 manifest covering files inside the release and is verified using ZIP CRC integrity. All v1 and v2 source files needed for the standalone application are retained.
