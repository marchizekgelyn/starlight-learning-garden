# ATLAS Writing Assessment v3 — Technical Architecture

## Purpose and non-goals

This is a **formative writing tutor**, not a validated automated essay scoring system. It cannot certify correctness, detect plagiarism/authorship, or fairly grade a child's interpretation without human review. More bytes of source code do not establish psychometric validity. The application intentionally reports an uncertain rubric **indicator and estimated range** rather than an authoritative school grade. The local AI option remains a separate fallible second opinion. The adult reviewer has the final say.

## New source and integration

- `source/assessment_v3/engine.js`: UMD/browser + CommonJS, no network. It implements Unicode-aware tokenization, elementary word normalization, sentence segmentation, source-linked evidence proximity checks, reference-concept clusters, repeated 4-gram detection, source 9-gram overlap warnings, conservative possible-negation flags, developmental rubrics, and explicit score uncertainty.
- `source/assessment_v3/proofreading.js`: Opt-in mechanical proofreading rules. It does NOT silently edit content or attempt broad homophone correction; the student controls every application of edits.
- `source/assessment_v3/calibration.js`: Descriptive agreement statistics against **independent** parent/teacher marks. Mean absolute error and bias are not automatically used to alter scores.
- `source/assessment_v3/tasks/level_*.js`: Sixteen offline browser-loadable JavaScript files. Every existing v2 lesson now has eight additional writing tasks. Each task is linked to the original passage and includes a developmentally appropriate prompt, concept groups, passage evidence anchors, checklist, typical pitfalls, success criteria, and parent review questions.
- `tools/build_assessment_v3.py`: Reproducibly regenerates the v3 task code from the preserved v2 JSON corpus.
- `tools/human_review_benchmark.js`: Evaluates **externally annotated**, independent human marks when they exist. The repository deliberately does not fabricate gold-standard teacher scores.
- `source/studio.js`, `source/studio.css`, `source/assessment_v3/assessment.css`: Student editor and responsive interface for the original lessons, the new assignment chooser, paragraph/page mode, uncertainty display, and independent parent marks.
- `source/local_review_server.py`: Optional, loopback-only Ollama or LM Studio rubric critique with excerpt checking. It suppresses ratings not supported by an exact quotation from the student writing; it does **not** validate whether the quotation proves the argument.

## Scoring dimensions

The weight of each rubric dimension varies by grade and is visible through the grading engine. Preschool/early literacy places greater emphasis on showing a comprehensible idea and basic sentence conventions; college-level work emphasizes task relevance, evidence, reasoning and organized argument. The rubric's six dimensions are task completion, evidence, reasoning, organization, conventions and independent expression.

The scoring pipeline is:

1. Read teacher-written prompt, level, optional source passage and anchor expectations.
2. Read the student's response and tokenize without sending data off device.
3. Compare reference idea groups with answer spans and look for recognizably aligned source details; this can miss valid paraphrases.
4. Identify observable writing features (sentences, paragraph structure, possible punctuation problems and redundancy).
5. Screen for substantial repeated passage/model text. A high overlap is a **review prompt**, not a plagiarism accusation.
6. Aggregate six transparent rubric indicators, apply conservative development/repetition caps, and provide a deliberately broad uncertainty range.
7. Show revision suggestions and require adult review for semantic truth, the strength of the explanation, fair interpretation of dialect, and the final academic mark.

## Limitations that cannot be fixed by more word lists

A persuasive but untrue paragraph can contain all the right key terms. A brilliant paraphrase can use none. Keyword or token-based matching, even with more contexts, cannot settle these cases reliably. Model-based semantic evaluation may improve coverage but may hallucinate, favor verbose responses and inherit bias. No dataset of actual teacher-reviewed paragraphs or inter-rater judgments was supplied. Consequently **no quantitative agreement or accuracy percentage is claimed**. If high-stakes numeric grades are required, collect a representative human-rated corpus, evaluate across grades, writing types, reading abilities and dialects, inspect worst-case errors, and introduce a parent-approved calibration and appeals workflow before release.

## Human-rating calibration protocol

1. Obtain permission before collecting children's writing, and remove names, addresses and other personal information from benchmark datasets.
2. Sample at least 100 independent responses per target grade band and writing mode, spanning very weak, average, excellent and unusual-but-valid answers; more are required for sound validation.
3. Have at least two qualified readers score blindly on identical assignment-specific rubrics and record the degree of reader disagreement.
4. Keep a blind holdout set the scorer is not tuned on. Do not modify teacher marks to match machine output.
5. Run `node tools/human_review_benchmark.js /path/to/private_human_reviews.json`, inspect MAE, mean bias, within-ten-point agreement, range coverage, and results by grade.
6. Audit dialect-related false positives, subject-specific vocabulary, special learning needs, concise correct answers, quoted evidence and paraphrases before interpreting the numbers.
7. If disagreement is large or the source has no authoritative answer, report **needs review**, not an apparently exact grade.

## Parents' privacy and confidence

Student drafts, responses, parent scores and assessment history are saved to browser localStorage for this single browser profile. Exports are explicitly initiated by the user. Anyone who can access the browser profile may read this data. Do not deploy the static site to a shared kiosk for identifiable children's writing. Optional local LLM review transfers the paper to the configured loopback service on the same machine, but model implementations and their storage practices must be evaluated separately. No remote model or tracking is bundled.

## Known improvements for a future evidence-based revision

- A genuinely human-labeled, grade-stratified and permissioned benchmark, with adjudicated answers and inter-rater agreement.
- Assignments with teacher-authored acceptable paraphrases, misconceptions and alternate reasoning chains, and verified source provenance.
- A vetted parsing/grammar system for multilingual and dialect-aware suggestions, avoiding unsafe automatic corrections.
- Teacher-selected custom rubric and revision-history comparison per student, with rubric versioning and grade-level adjustments.
- Optional server-based semantic evaluation with independent factual source verification, privacy controls and a human appeal path.
