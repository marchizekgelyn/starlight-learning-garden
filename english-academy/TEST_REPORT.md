# ATLAS English & Reading Academy v2.0 — Validation Report

## Results

- **PASS:** 1,536 new lesson objects generated at 16 levels across 12 instructional strands.
- **PASS:** 23,040 new exercise objects checked for IDs, schemas, answer keys and consistent expected values.
- **PASS:** Question-type counts: 10,752 multiple choice; 4,608 fill-ins; 3,072 short responses; 1,536 sentence-editing; 1,536 sequencing; 1,536 essays.
- **PASS:** 1,536 local SVG illustrations are well-formed XML and match their lessons.
- **PASS:** The earlier v1 content is preserved (192 lessons and 1,920 assignments). The original tests also pass.
- **PASS:** Objective answer keys, selected invalid alternatives, essay scoring guardrails, provisional score labels, and simulated app navigation/rendering/progress and interactive learning diagrams pass automated Node tests.
- **PASS:** Node.js syntax parsing for the new JavaScript and Python compilation for generator and optional local review adapter.
- **PASS:** Sample generated SVG images rendered into raster previews and reviewed for legibility, including emergent-literacy flashcards.
- **NOT VERIFIED:** A real Chrome/Chromium end-to-end launch and interactive browser walk-through. The container's browser navigations were blocked by `net::ERR_BLOCKED_BY_ADMINISTRATOR`. Automated tests used a DOM simulation rather than a browser engine. Users should test on Edge/Chrome/Firefox after extracting.
- **NOT VERIFIED:** An external live Ollama or LM Studio inference session. It is an optional integration whose server code is included, but not a guarantee of model-specific performance.

## Content and grading limitations

This is a working new instructional application, not a claim of accreditation, educational standards certification, or an exhaustive coverage of every possible English syllabus. The 96 newly authored lesson scenarios are reused with differentiated text and exercises at 16 levels, so not every item is a completely independent authored idea. Exact-answer grading can be verified against reference keys; extended writing scores are rule-based and **provisional**. Essays still require human review for correctness, argument quality, appropriate voice, citations, and originality. The optional local LLM critique does not make any grading guarantee.

## Reproduce test suite

```bash
python tests/validate_v2.py
node tests/validate_v2.js
node tests/validate_v1.js
node --check source/studio.js
node --check source/writing_engine.js
python -m py_compile tools/build_v2.py source/local_review_server.py
```

All tests above were run successfully during packaging. The ZIP integrity and SHA-256 manifest are checked separately when the archive is built.
