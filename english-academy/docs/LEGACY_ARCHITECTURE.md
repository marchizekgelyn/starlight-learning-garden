# Architecture and Codex Integration Guide

## Design contract

This release is a static, client-side, offline-capable web application made with HTML5, CSS3, and vanilla JavaScript. There is no dependency on external JavaScript packages, remote fonts, CDNs, database engines, API keys, or network connectivity.

The entry point loads four files in order:

```html
<link rel="stylesheet" href="styles.css">
<script src="data.js"></script>
<script src="grader.js"></script>
<script src="app.js"></script>
```

`data.js` exposes `window.ATLAS_CONTENT`; `grader.js` exposes `window.ATLAS_GRADER`; `app.js` renders the application. Content also exists in structured JSON. These files should remain adjacent or have their URLs adjusted consistently.

## Integrate into ATLAS website

**Option 1 — independent tab (low risk):** Keep the `source/` directory intact as `/english-academy/` and link to `/english-academy/index.html` from the ATLAS navigation. This requires no changes to the existing root app.

**Option 2 — embedded view:** Render a child iframe that points to `/english-academy/index.html` and gives it an accessible name. Provide generous height and independent scroll control. Be aware that localStorage is origin-scoped; two tabs on the same origin share the same academy progress.

**Option 3 — native integration:** Embed the source modules inside ATLAS, namespace CSS to avoid selectors colliding with the parent design, and replace `#app` plus startup initialization with an ATLAS route. `app.js` currently owns page-level clicks, input events, header, and navigation, so refactoring it into an independent mount/unmount module is required before integrating it into a host that already owns those events. Do **not** paste the entire JS and CSS into unrelated global files and assume there will be no conflicts.

## Data schema

`metadata` holds counts/version/warnings, `levels` defines ordered learning levels, `strands` contains subject definitions, and `lessons` contains curriculum units.

Each lesson has:

```json
{
  "id": "4-vocab",
  "level": "4",
  "strand": "vocab",
  "index": 3,
  "title": "Use prefixes, suffixes, and common roots",
  "objective": "Learners will ...",
  "instruction": "Original instruction and worked examples",
  "passage": "Original reading passage",
  "glossary": [{"term": "...", "definition": "..."}],
  "questions": []
}
```

Each lesson has ten question types: 4 `mcq`, 2 `fill`, 2 `short`, 1 `order`, 1 `essay`. Questions include a stable ID, prompt, point value, and grading/reference data appropriate for the type. Each lesson currently totals **100 possible points**.

Use `source/build_content.py` to edit source scope, cases, instruction, and exercise generation. Rerun it with Python 3.10+ to regenerate `source/data.js` and `source/curriculum.json`. **Do not edit generated data.js directly**, or changes can be overwritten. A future human-authored content system can supply equivalent lesson objects without changing the frontend.

## Scoring design

- **MCQ:** 10 or 0 for the exact option ID.
- **Fill-in:** 10 for normalized expected terms or listed alternatives; 7 for a permitted one-edit near match, else zero.
- **Ordering:** 10 for correct order; partial positional credit only if all three distinct event IDs are used once.
- **Short:** 75% reference keyword coverage, 20% suggested answer length, 5% sentence punctuation.
- **Extended writing:** 35% reference keyword coverage, 30% suggested length, 20% structural markers, 15% sentence-ending heuristics.

Keyword scoring is explicitly **provisional**, and many legitimate paraphrases may score poorly. Text containing the right words can score undeservedly. Treat the combined total as a learning indicator rather than a certified proficiency test. The objective-only percentage is shown separately.

`source/grader.js` is dependency-free and exports both to CommonJS and the browser. `grade(question, answer)` returns score, max, confidence level, message, and detailed feedback. `gradeLesson(lesson, answers)` returns item grades and lesson summary.

## Learner state and exports

- Browser key: `atlas-english-academy-v1`.
- JSON structure: `{schema:1,drafts:{[lessonId]:{[questionId]:answer}},attempts:{[lessonId]:{count,best,lastResult,at}},theme,size}`.
- Exports: JSON document with `kind`, `version`, `exportedAt`, and `data`.
- Imports validate known lesson IDs and question IDs, bound text length, and sanitize grade summaries.

There is no registration or hosted account synchronization. Import/export is manual. Backups contain student answers and should be kept private.

## Future expansion milestones

1. Teacher dashboard and scoring override for open responses, including teacher notes and explicit discrepancy review.
2. Fully unique long-form readings and literary genres at each grade, with richer decodable progression in early grades.
3. Phonemic awareness activities with guided audio prompts, early learner visuals, phonics inventories, high-frequency word decks, and accessible text-to-speech controls.
4. Interactive paragraph editor with sentence annotation, revision comparisons, grammar examples, and source highlighting.
5. Diagnostic skills assessment, configurable mastery thresholds, and adaptive placement without penalizing emergent readers.
6. Optional securely hosted AI evaluation of essays, grounded in explicit human-edited rubrics, calibrated on representative samples, with teacher override, transparent confidence, privacy/consent, rate limiting, and no keys in frontend code.
7. Audio capture/pronunciation feedback with consent; captions and controls for speech-related access needs.
8. Human-reviewed standards mapping by grade and jurisdiction, expanded reading/library collections, citation exercises, and accessible instructor guides.
9. Accessibility audit against WCAG, including assistive technology testing with real devices and browsers.
10. Scalable multi-tenant back-end only if classroom account features become necessary, with student-data protections and retention policies.

## Test command

Run `node tests/validate.js` from this project folder. This verifies scope and counts, stable IDs, distinct MCQ answers, each objective answer key, grading constraints, and a simulated app lifecycle (render, navigation, submit, saving).

The browser smoke run with headless Chromium was blocked by administrator navigation restrictions in the build environment. The automated Node lifecycle test passed; manual device/browser accessibility QA is recommended before any classroom deployment.
