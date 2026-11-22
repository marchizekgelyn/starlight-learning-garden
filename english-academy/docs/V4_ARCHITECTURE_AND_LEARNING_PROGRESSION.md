# ATLAS English Academy v4: architecture, teaching sequence and assessment integrity

## Why the curriculum is arranged as a pathway

A child should move from attention to sound and print through decoding and word meaning, connected comprehension, evidence-based inference, multi-text comparison, academic disciplinary reading, and independent critique. Reading more pages is not by itself proof of comprehension. The v4 interface therefore teaches a technique explicitly, demonstrates a worked example in a particular case, asks objective source-grounded questions, and asks the student to apply the technique in their own words.

### Learning progression

| Stage | Essential habits | Practice and evidence |
|---|---|---|
| Preschool–K | Shared attention, phonemic awareness, print direction, letter names, oral vocabulary, adult read-aloud | Say/point to a word, choose a beginning sound, identify a question mark, draw or orally retell |
| Grades 1–2 | Decoding, high-frequency words, literal details, events in order | Short narrated cases and parent support, direct-detail comprehension, sentence writing |
| Grades 3–5 | Connected paragraphs, main idea and supporting facts, context clues, inference | Close reading across related texts, vocabulary in context, evidence-marked responses |
| Grades 6–8 | Purpose, perspective, reliability, cause vs. correlation, data interpretation, argument structure | Compare two interpretations, cite source limitations and write defensible explanations |
| Grades 9–12 | Complex syntax, rhetoric, authorial choices, statistical and historical reasoning, source reliability | More substantial multi-document reading, contrasting claims, longer paper responses |
| College I | Critical synthesis, qualifications, methodological limitations, disciplinary vocabulary | Source comparisons, causal vs normative argument, close reading and independent critique |
| College II | Counterfactual thinking, methodological validity, rhetorical scrutiny, interpretation across genres | Independent transfer passages, source-based analytical writing, human review of complex argument |

This is a broad learning sequence, not a normed or validated grade-band placement instrument. A child can move at an individualized pace. Gaps in phonics, word recognition and fluency need explicit support even if an older student is strong in conceptual reasoning.

## Scope and data architecture

The new course contains 64 case scenarios in eight subject domains—Ecology, History, Engineering, Community, Technology, Literature, Science and Argument. They are intentionally *constructed* examples, not purported accounts of actual towns or studies. Every case is adapted to 16 developmental levels, generating 1,024 units.

Each unit contains three related reading texts: a starting document, an alternative perspective, and an evidence packet. In early grades, a document is a short read-aloud or fact card; in higher grades it becomes an extended close-reading exercise. Every unit also includes a vocabulary set, between five and twelve instructional cards, annotated evidence anchors, 10 keyed objective checks, three original writing exercises, six transfer prompts and a transparent five-dimension writing rubric.

Content is stored in scripts rather than fetched as JSON. `window.ATLAS_PATHWAY_CONTENT[level]` is lazy-loaded by grade. A standalone HTML file can therefore be launched offline without `fetch` restrictions under `file://`. Content is never read dynamically with `eval` at runtime; dynamically appended `<script>` tags load the packaged static files. The browser test harness injects them because direct file navigation is restricted there.

The original v1/v2/v3 site remains available. The v4 pathway has a distinct localStorage key (`atlas-reading-pathway-v4`) so data from the original v3 studio is not overwritten. Only on explicit learner action does a writing draft transfer to the older v3 paper editor via its existing localStorage schema.

## Grading design and limitations

Ten objective choices are scored by a fixed answer index. After submission the system reveals which choice was correct and a human-readable rationale. Unit mastery targets 80%, but multiple-choice completion alone does not prove transferable proficiency. Highest and latest scores are separate, and an adult reading assessment is recommended for actual placement.

For free-form paragraphs, one-page papers and spoken retellings, the new module does not invent a validated semantic score. It supplies assignment-specific requirements and model answers and routes writing to the preserved v3 formative diagnostics if requested. The adult reviewer records a separate score and comments. Correct, succinct, creative or dialect-influenced writing must not be penalized by naive length/keyword heuristics.

Four separate capstone passages are not present in the 64-unit teaching bank. They ask the learner to interpret an unfamiliar research report, evaluate historical source bias, analyze narrator reliability and critique a statistical public-service dashboard. A first-attempt score is stored immutably by normal UI actions; retakes are reported but are not credited toward first-attempt readiness.

Internal college practice requires: 8 reviewed/80%+ units from College I, 8 reviewed/80%+ units from College II, four or more domains across qualifying units, and two distinct independent challenge first attempts at 80% or better. **This threshold is a program milestone only**, not evidence of validated college placement or reading age. Obtain qualified human assessment and samples of true unfamiliar college texts before asserting the learner has attained that level.

## Known constraints and next research steps

1. Many lessons are systematic adaptations of the same curated 64 fictional case stems. They are practice resources, not 1,024 independently authored fiction or nonfiction works. Additional authentic genre diversity, poetry, historical primary sources with verified provenance and longer carefully edited college essays should be added before an accredited curriculum claim.
2. The earliest reading passages are designed for adult co-reading, not strict controlled-phonics decodability, and do not substitute for a verified scope-and-sequence phonics curriculum.
3. The offline scoring system cannot establish plagiarism, factual accuracy, or human-grade equivalence for arbitrary written responses.
4. The college transfer passages are original and valuable practice, but not standardized, externally normed or psychometrically calibrated.
5. Progress is stored in browser localStorage without authentication or encryption. Do not treat that record as authoritative in a multi-user or compliance-regulated educational environment. Export backups privately.
6. Validate with actual students: accessibility testing; teacher-rated essays with inter-rater agreement; out-of-sample passages; and grade-stratified error analysis. Do not invent a grading-accuracy percentage from software unit tests.

## Testing and integration checklist

- Read `source/reading-pathway.html` and navigate from v3 `source/index.html` using the sidebar and homepage feature.
- Verify `PK`, `4`, `C1`, `C2` can load lazily; all levels contain 64 complete records.
- Answer 10 objective items, submit and confirm both score and explanations. Retake and verify best-vs-last history is preserved.
- Enter and save writing, record an independent parent/teacher review, and export/import a JSON backup.
- Use the explicit button to send an essay to the v3 paper review and check that the source passage and prompt survive the handoff.
- Complete a capstone first attempt, retake it, verify the first score is preserved.
- Test opening under `file://` and under your intended hosting origin; review CSP and any larger request limits if integrating with an existing web framework.
