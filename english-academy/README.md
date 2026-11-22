# ATLAS English & Reading Academy v4.0 — Preschool to College

**Complete self-contained HTML, CSS and JavaScript learning application** · Original Grade PK–College II coursework · 25.44 MiB of *additional* v4 learning content (uncompressed) · Existing v1, v2 and v3 materials preserved.

## Start here

1. Extract the **whole ZIP**. Do not open files from inside the ZIP.
2. Open **`source/index.html`** in Chrome or Microsoft Edge for the original academy. Choose the **NEW College Reading Pathway 4.0** in its left navigation.
3. Or open **`source/reading-pathway.html`** to go directly to the new course. It runs locally without a server, login, paid library or network connection.
4. Choose a reading level, then a lesson. **Read the text → study the worked lessons → answer the 10 objective questions → write an original paragraph/paper → request a parent/teacher review.**
5. For college-level reading practice, select **College I** and **College II**, work across subjects, and complete the four independent college transfer challenges.
6. Export your local progress from the top bar. Store the exported JSON privately; it can contain a child's writing.

## New in v4: instructional scale

| New material | Count |
|---|---:|
| Learning levels | 16 (preschool, K, grades 1–12, College I/II) |
| Guided reading units | 1,024 (64 per level) |
| Readings | 3,072 (3 paired/related texts per unit) |
| Machine-scored reading-comprehension questions | 10,240 |
| Paragraph, short-answer, and extended writing assignments | 3,072 |
| Individual skills instruction cards/worked mini-lessons | 9,920 |
| Separate college transfer passages with first-attempt scoring | 4 |
| Added v4 lesson content alone | 26,672,912 bytes = 25.44 MiB |
| Reading words across the 16 adapted corpora | approximately 1.1 million occurrences |

**How content was developed:** The materials are originally constructed, illustrative **fictional educational cases**. A curriculum generator adapts 64 distinct case scenarios across 16 levels. Many readings share an underlying scenario and patterned instructional language; **3,072 texts does not imply 3,072 independently researched or teacher-authored source works**. The size requirement was met with source passages, source comparisons, worked explanations, vocabulary, distinct answer keys, writing rubrics, and transfer tasks, rather than blank padding. The four capstone reading passages are separate, original texts. No third-party copyrighted readings are reproduced.

The source records, dates, quantities, and anecdotes are **hypothetical** and must not be presented as real-world facts. Advanced research claims should be practiced with independently verified academic sources in addition to this offline course.

## Reading pathway and desired outcome

This curriculum teaches early literacy and word recognition, literal comprehension, sequencing, main ideas, contextual vocabulary, evidence identification, source comparison, rhetoric, interpretation, argumentative writing, and methodological critique. Later stages increasingly demand qualification of claims, rival interpretations and multi-text synthesis.

**The goal is independently demonstrated college-level reading proficiency.** Completing 1,024 units or reaching an internal score cannot guarantee that outcome. The built-in *practice* milestone requires **at least eight units from College I and eight from College II** with 80% or higher on objective questions **and** a human-reviewed writing response; coverage must include **at least four subject domains**, plus **two separate college transfer challenges with 80%+ on their first attempt**. The dashboard calls this an *internal practice threshold*, not an accredited standard, grade placement, diagnostic reading score, or college credit. Confirm readiness using unfamiliar college texts and a qualified reader/teacher (and, when appropriate, an established reading assessment).

For preschool and kindergarten, reading is parent-assisted: phonemic awareness, pointing, shared reading, oral retellings and drawings are age-appropriate. Do not make very young children type a page-long paper.

## Answer scoring

- **Objective:** 10 keyed 4-option multiple-choice questions per v4 unit, scored exactly (0–100% in 10-point increments). After submission, the correct answer and explanation appear for every question. Best score and latest score are stored separately. The four separate college transfer challenges contain five keyed questions each.
- **Writing:** Three writing tasks per unit, with the source linked in the same screen, worked model responses hidden in a disclosure, and a five-dimension rubric (understanding 25%, evidence 25%, reasoning 20%, organization 15%, language 15%). Drafts are saved locally.
- **Human review:** Parent/teacher can mark a response as reviewed, give an independent numerical score, and leave feedback. A checkbox is an honor-system record, not authentication.
- **Existing v3 paper evaluator:** The button **Open in v3 paper evaluator** copies the draft and assignment into the v3 paper studio. Its heuristics are provisional and may mistake unusual valid answers for errors. It must not be mistaken for guaranteed accuracy. Human review remains necessary.
- **College transfer tests:** The first attempt score cannot be overwritten by a later practice retake; the highest and latest scores can still be viewed.

## Integration for Codex

- `source/reading-pathway.html`: new course entry point.
- `source/pathway-v4/pathway.css`: dedicated responsive visual design.
- `source/pathway-v4/pathway.js`: offline lesson navigation, scoring, writing, parent-review workflow, dashboard, local data export/import and optional cross-studio handoff.
- `source/pathway-v4/content/level_*.js`: 16 lazy-loaded curriculum scripts (educational materials exceed 20 MiB).
- `source/pathway-v4/manifest.js` and `manifest.json`: exact levels and metrics.
- `source/pathway-v4/capstones.js`: four separate cold-reading practice tests and essay prompts.
- `source/studio.js`: link to v4 course from preserved v3 homepage and sidebar and a deep link into the v3 paper editor.
- `tools/build_reading_pathway_v4.py`: reproducible Python content generator (standard library only).
- `docs/V4_READING_CURRICULUM_INDEX.csv`: per-unit searchable source inventory.
- `docs/V4_ARCHITECTURE_AND_LEARNING_PROGRESSION.md`: expanded technical/course notes.
- `tests/validate_v4.py`: source integrity, size, keys, ground-truth quotes and counts.
- `tests/browser_smoke_v4.py`: Chromium-simulated UI test for complete reading, marking, writing, parent review and independent transfer quiz.

Original `classic.html`, v2 `studio-data`, v3 assessment engine, 1,536 SVG drawings, and all original test tools stay intact. The source files do not make remote requests. If you integrate this into a shared website, protect student writing rather than storing identifiable essays in a shared/browser kiosk.

## Verification

From the extracted project root:

```shell
node tests/validate_v1.js
node tests/validate_v2.js
python tests/validate_v2.py
node tests/validate_v3.js
python tests/validate_v4.py
python tests/browser_smoke_v4.py
```

The browser smoke test uses the real course scripts injected into a test page because direct local-file navigation was restricted in this build environment. The actual `file://` double-click launch and deployment into the full ATLAS website should be manually verified on the destination machine. A validity study using human-graded student papers is also still needed before making academic accuracy claims.
