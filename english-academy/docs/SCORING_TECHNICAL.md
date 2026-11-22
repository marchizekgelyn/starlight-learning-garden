# Scoring engine — transparent mechanics and limitations

## Correct-answer exercises

- **Multiple choice:** compares selected option ID with the authored option ID. Full points for correct; otherwise zero with explanation.
- **Fill-in:** case-, punctuation-, accent-, and whitespace-normalized compare against authored answers and explicit alternatives. No uncertain edit-distance credit.
- **Order:** awards fractional credit based on each item in its correct position, but only when all positions are uniquely and validly filled.
- **Sentence edit:** accepted exemplar or authored alternatives receive full points; normalized lexical matches that miss capitalization/punctuation receive up to 60% partial credit; other responses zero.

These outcomes are called **verified against the authored key**, not proof that a question is pedagogically perfect or that there is no other legitimate interpretation.

## Provisional writing rubric

| Rubric criterion | Default weight | Indicators, not verified judgments |
|---|---:|---|
| Task focus | 18% | Covered reference-concept clusters and minimum-word target |
| Reasoning | 22% | Causal connectives, hedging, sentence development |
| Evidence | 24% | Content-token overlap with authored evidence anchors; direct quotation presence |
| Organization | 16% | Paragraphs, transitions, sentences |
| Style | 12% | Long sentences, missing ending marks, initial lowercase and selected mechanical warnings |
| Independent explanation | 8% | Excessive exact copied n-grams, repeated wording, copied model examples |

The provisional score may be capped when a response is severely underlength, lacks recognizable concept and evidence references, repeats content excessively, or closely resembles its model/source. The local model can offer a separately displayed semantic critique but does not replace this rubric.

**Do not interpret the weighted score as an objective measure of writing quality.** These signals can be gamed, can miss legitimate paraphrases, may discourage certain valid writing styles, and cannot evaluate original insight, accurate citations, text interpretation, dialect appropriateness or fact-checking. The concept term banks are formative scaffolds, not exhaustive semantic equivalence dictionaries.

## Independent human judgment

A teacher/reviewer can enter a separate 0–100% score per lesson writing answer, stored in `saved.manual`. This does not alter the local machine score. A production instructional product should additionally support reasoned rubric comments, versioning and restricted access.

## Paper correction without source material

When the user pastes an arbitrary paper with no source passage, the UI **intentionally withholds an overall numeric grade**. It can still provide mechanical and organizational warnings and optional edits. Providing a reference source allows an approximate comparison with up to three textual anchors; this is still provisional, and does not establish factual correctness.

## Conservative local proofreader

`proofread(text)` proposes a small set of high-confidence mechanical fixes: spelling of certain common words; missing apostrophes in selected contractions; standalone `i`; whitespace before punctuation; repeated function words; extra consecutive spaces. Each proposal carries a before/after text pair and rule label. The student must deliberately choose to apply the new text; otherwise the original draft is unchanged.

It is **not a complete grammar checker**, spell checker, or semantic paper reviser. Avoid broad autocorrections for grammar items with contextual exceptions (their/there, affect/effect, whom/who, etc.) unless a true language parser validates the context.

## Verification strategy

`tests/validate_v2.js` checks all 23,040 new items and exercises correct-answer keys plus behavior on repeated/copy-stuffed and reasonable writing samples. `tests/validate_v2.py` checks all content, lesson counts, references and XML SVG syntax. Run both before Codex changes the generator, schema or evaluator. Human content QA across reading levels remains desirable.
