# ATLAS English Academy 2.0 — architecture and integration plan

## Runtime layers

1. **Static platform:** `source/index.html` mounts `studio.css`, `studio-data/manifest.js`, `writing_engine.js`, `visuals.js`, and `studio.js`.
2. **Curriculum discovery:** `manifest.js` indexes 1,536 lesson IDs and 16 levels but does not load full lesson bodies. Grade and strand selectors filter the index.
3. **Lazy lesson loading:** `loadLevel()` injects a local `<script src="studio-data/level_X.js">` and caches it in `window.ATLAS_STUDIO_LEVELS`. `file://` works in typical desktop browsers without requiring fetch/CORS for bundled JSON.
4. **Lesson interface:** `studio.js` renders original passage, art asset, glossary, mentor panels, 15 exercises, and feedback. Event delegation handles responses and navigation.
5. **Grader:** `writing_engine.js` is a pure UMD module. `grade(question,answer)` and `gradeLesson(lesson,answers)` are deterministic and can be tested with Node.js. It exposes `proofread(text)` for conservative edits. Writing results include machine-readable metric and rubric evidence.
6. **Storage:** `localStorage['atlas-english-academy-studio-v2']` stores draft answers, best scores, separate teacher review scores, and a stand-alone essay lab draft. The classic course has its own `atlas-english-academy-v1` key. No cloud writes occur in core mode.
7. **Local AI adapter (optional):** Browser `POST http://127.0.0.1:8798/review` to `local_review_server.py`. Adapter supports Ollama loopback chat (port 11434) and LM Studio's local compatible completion API (port 1234). It is intentionally separate from core grading.

## Recommended integration into larger ATLAS website

The safest path is a dedicated route `/english-academy/` containing the **complete `source/` directory**, preserving original relative paths.

**Option A — iframe** (avoids style collisions with other ATLAS tabs):

```html
<section id="atlas-english" aria-labelledby="atlas-english-title">
  <h2 id="atlas-english-title">ATLAS English & Reading Academy</h2>
  <iframe src="/english-academy/index.html" title="ATLAS English Academy"
          loading="lazy" style="border:0;width:100%;min-height:900px"></iframe>
</section>
```

**Option B — dedicated navigation:** Open `/english-academy/index.html` as a route or tab. For same-document embedding, isolate CSS or refactor the app root and stylesheet selectors before combining with the existing global navigation.

Do not blindly append Studio CSS to unrelated ATLAS pages; `body`, typography and button selectors would override host styles. Prefer iframe or dedicated route.

## Data schema

- `studio-data/manifest.json`: `levels`, `strands`, `lessonIndex`, counts and version.
- `studio-data/level_<id>.json`: `{level,levelName,lessons:[...]}`.
- `lessons[]`: `{id,level,levelName,strand,strandName,unit,title,objective,reading,mentor,glossary,writingPlan,art,questions}`.
- `questions[]`: `{id,type,prompt,points,skill,reason,answer,alternatives?,options?,steps?,keywords?,concepts?,expectedEvidence?,referenceText?,rubric?,sample?,minimumWords?}`.

Question types: `mcq`, `fill`, `short`, `edit`, `order`, `essay`. An essay rubric has dimension keys `task`, `reason`, `evidence`, `organization`, `style`, `integrity` and additive weights summing to 1.0.

**Question identity:** Unique within each lesson; use `{lessonId}:{questionId}` globally. Generated question IDs are `q01..q15`.

## Independent scorer interface

```javascript
const item = ATLAS_WRITING_ENGINE.grade(question, studentAnswer);
// {score,max,percent,kind,confidence,message,details,report?,reviewRequired}

const lesson = ATLAS_WRITING_ENGINE.gradeLesson(lessonData, answersByQuestionId);
// includes an objectivePercent separate from a combined provisional percent

const revisions = ATLAS_WRITING_ENGINE.proofread(studentText);
// {changed,revised,changes,count,note}; always ask before applying
```

## Security and privacy considerations

- All student strings are escaped before inclusion in HTML templates. Treat curriculum JSON and imported progress as data, not instructions.
- Import only known lesson IDs and known question IDs, bounded response values, and sane numeric scores. Do not use `eval` or dynamic JavaScript from user text.
- `local_review_server.py` binds only to loopback, validates origin, caps request size and paper length, avoids logging student text, and excludes cloud credentials. It has **no authentication** because it is deliberately local only; do not expose it on a public interface without adding authentication, TLS, quota controls, a privacy notice and retention rules.
- LLM-assisted analysis should treat student text as untrusted data. A student's paper may attempt prompt injection; the included server attempts to constrain the model but does not guarantee that all prompt injections are prevented.
- Local browser progress is not encrypted. Shared devices require appropriate privacy practices; do not claim compliance with student-data privacy laws merely from local storage.
- Avoid rendering arbitrary AI model output as HTML. The studio escapes all model response strings.

## Extension backlog for Codex

- Expand handcrafted passage variety and introduce distinct phonics fluency diagnostics, morphology families, paragraph genres, fiction and poetry close readings, college research methods, and source citation models.
- Introduce a human feedback workflow with rubric comment text and audit trails rather than numeric overrides alone.
- Add optional teacher classes with permissions and protected identity only with a secure backend and appropriate student privacy governance.
- Add an accessible writing diff view and student-accepted suggestion tracking.
- Add tests in Edge/Firefox/Chrome on actual user devices; this build's headless browser navigation was blocked by the test environment.
- Consider a local full-text search index, WCAG audit and screen-reader usability study, standards alignment authored and verified by educators, and validated age-appropriate fluency/phonemic awareness assessments.
