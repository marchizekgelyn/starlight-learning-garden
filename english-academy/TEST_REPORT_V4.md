# ATLAS English Academy v4.0 — test report

- **Corpus size:** `26,672,912` bytes of new instructional source in `source/pathway-v4/content` (**25.44 MiB**, exceeds requested 20 MiB *uncompressed*).
- **Validated new units:** 1,024 (64 at each of 16 stages); 3,072 related readings; 10,240 objective checks; 3,072 writing prompts; 9,920 instruction cards.
- **Original scenario stems:** 64 original hypothetical cases, adapted to learning levels. The material is not 1,024 independently sourced research reports.
- **Objective keys:** Exactly four distinct alternatives, an integer correct-option index, a nonempty explanation and valid evidence links in every new quiz question. Evidence-, limitation- and number-specific keys were validated against included passage text.
- **Full v1/v2/v3 test suites:** Passed after v4 integration. Previous grading-engine probes test software behavior only, not human-scoring accuracy.
- **v4 Chromium UI:** Passed grade-level lazy load, all ten comprehension questions, 100% score and explanation display, student-draft save, human review, dashboard, advanced reading content, separate capstone exam first attempt, and retake preservation.
- **v3 Chromium UI regression:** Passed navigation to the existing paper lab, source-linked assignment load, scoring, human review entry and mode switching. No page script errors were observed.
- **Browser environment constraint:** Ordinary local-file double-click navigation could not be fully tested because the build environment disallows file navigation. Tests injected the exact packaged scripts into Chromium. Manual `file://` and hosted deployment tests should be performed on the destination PC.
- **Validity caveat:** No independently teacher-scored dataset was supplied. Neither the older v3 essay evaluator nor the new v4 learning threshold has been scientifically validated against an accepted college reading-level standard.

**Source archive:** `MANIFEST_SHA256.txt` records each included file's SHA-256 digest, excluding itself.
