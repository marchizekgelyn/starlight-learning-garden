/* ATLAS English Academy 2.0 | Original visual courseware application.
 * The data loader uses scripts instead of fetch so the curriculum works with file://.
 * No accounts, third-party scripts, external fonts or data collection.
 */
(function(){'use strict';
const M=window.ATLAS_STUDIO_MANIFEST,G=window.ATLAS_WRITING_ENGINE,V=window.ATLAS_VISUALS,A=window.ATLAS_ASSESSMENT_V3,C=window.ATLAS_CALIBRATION_V3;
const host=document.getElementById('studio');
const escape=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
const qs=s=>document.querySelector(s);
if(!M||!G||!V){host.innerHTML='<div class="error-large">Could not load Studio dependencies. Extract the complete ZIP and keep all files together.</div>';return;}
const storeKey='atlas-english-academy-studio-v2';
const fresh=()=>({schema:2,answers:{},history:{},manual:{},paper:{text:'',prompt:'',reference:'',focus:'',taskId:'',lessonId:'',mode:'paragraph'},paperReviews:[],theme:'dark',font:1});
function load(){try{const v=JSON.parse(localStorage.getItem(storeKey)||'null');if(v&&v.schema===2&&v.answers&&v.history&&v.manual)return {...fresh(),...v};}catch(e){}return fresh();}
const saved=load();
saved.paper={...fresh().paper,...(saved.paper||{})};
if(!Array.isArray(saved.paperReviews))saved.paperReviews=[];
const state={view:'home',level:'PK',strand:'all',search:'',lessonId:'PK-phonics-01',feedback:{},lastResults:{},visualId:'evidence',visualStep:0,
              showAll:false,mobile:false,loading:false,loaded:{},taskLoaded:{},paperTaskId:'',storageWarning:false,paperResult:null,localResult:null};
const levels=new Map(M.levels.map(x=>[x.id,x]));const strands=new Map(M.strands.map(x=>[x.id,x]));
const indexById=new Map(M.lessonIndex.map(x=>[x.id,x]));
const levelQuestions={};
const allLessons=()=>window.ATLAS_STUDIO_LEVELS?.[state.level]?.lessons||[];
const curLesson=()=>levelQuestions[state.lessonId]||null;
const selectedProgress=()=>saved.history[state.lessonId]||null;
const answerDraft=()=>saved.answers[state.lessonId]||{};
function persist(){try{localStorage.setItem(storeKey,JSON.stringify(saved));state.storageWarning=false;}catch(e){state.storageWarning=true;}}
function wordCount(text){return G.words(text||'').length;}
function format(n){return Number(n||0).toLocaleString('en-US');}
function shortLabel(id){return levels.get(id)?.name||id;}
function fireNotice(message){const n=qs('#toast');if(!n)return;n.textContent=message;n.classList.add('show');clearTimeout(fireNotice.timeout);fireNotice.timeout=setTimeout(()=>n.classList.remove('show'),4400);}
function setAppearance(){document.body.dataset.theme=saved.theme;document.documentElement.style.setProperty('--reader-scale',String(saved.font||1));}
function loadLevel(id){
 if(!levels.has(id))return Promise.reject(new Error('Unknown learning level'));
 state.level=id;
 if(levelQuestions[`${id}-phonics-01`])return Promise.resolve();
 if(state.loaded[id])return state.loaded[id];
 state.loading=true;
 state.loaded[id]=new Promise((resolve,reject)=>{
  const script=document.createElement('script');script.src=`studio-data/level_${id.toLowerCase()}.js`;
  script.onload=()=>{const d=window.ATLAS_STUDIO_LEVELS?.[id];if(!d||!Array.isArray(d.lessons)){reject(new Error('Level content missing'));return;}
    for(const l of d.lessons){levelQuestions[l.id]=l;for(const q of l.questions||[])q.level=l.level;}state.loading=false;resolve();};
  script.onerror=()=>{state.loading=false;delete state.loaded[id];reject(new Error(`Could not load curriculum for ${id}. Check source/studio-data.`));};
  document.head.appendChild(script);
 });return state.loaded[id];
}
function loadWritingTasks(level){
 if(!levels.has(level))return Promise.reject(new Error('Unknown level'));
 if(window.ATLAS_WRITING_TASKS?.[level])return Promise.resolve(window.ATLAS_WRITING_TASKS[level]);
 if(state.taskLoaded[level])return state.taskLoaded[level];
 state.taskLoaded[level]=new Promise((resolve,reject)=>{
  const script=document.createElement('script');script.src=`assessment_v3/tasks/level_${level.toLowerCase()}.js`;
  script.onload=()=>{const data=window.ATLAS_WRITING_TASKS?.[level];if(!data||!Array.isArray(data.lessons))reject(new Error('Writing task file missing records'));else resolve(data);};
  script.onerror=()=>{delete state.taskLoaded[level];reject(new Error('Could not load writing tasks for '+level));};
  document.head.appendChild(script);
 });return state.taskLoaded[level];
}
function writingData(){return window.ATLAS_WRITING_TASKS?.[state.level];}
function chosenPaperLesson(){const arr=writingData()?.lessons||[];return arr.find(l=>l.id===saved.paper.lessonId)||arr[0]||null;}
function chosenPaperTask(){const l=chosenPaperLesson();return l?.tasks.find(t=>t.id===saved.paper.taskId)||null;}
function paperExercisePicker(){const level=M.levels.find(l=>l.id===state.level);const writing=writingData(),selected=chosenPaperLesson();
 return `<section class="assessment-picker"><div class="v3-eyebrow">ASSIGNMENT STUDIO · VERSION 3</div><h2>Choose a passage-linked writing assignment</h2>
 <p>Each new task has a specific writing goal and grading criteria. Select the child’s level, a reading lesson, and a writing exercise. The original free-writing editor remains available.</p>
 <div class="v3-picker-grid"><label>Learning level <select id="paper-level">${M.levels.map(l=>`<option value="${l.id}" ${state.level===l.id?'selected':''}>${escape(l.name)}</option>`).join('')}</select></label>
 <label>Reading lesson <select id="paper-lesson">${(writing?.lessons||[]).map(l=>`<option value="${escape(l.id)}" ${selected?.id===l.id?'selected':''}>${escape(l.title)}</option>`).join('')||'<option>Loading lessons…</option>'}</select></label>
 <label>Writing task <select id="paper-task-choice">${(selected?.tasks||[]).map(t=>`<option value="${escape(t.id)}" ${saved.paper.taskId===t.id?'selected':''}>${escape(t.title)} · ${t.mode==='page'?'Page':'Paragraph'}</option>`).join('')||'<option>Loading tasks…</option>'}</select></label></div>
 <div class="v3-picker-buttons"><button class="button primary" data-action="choose-paper-task" ${selected?'':'disabled'}>Load this assignment into editor</button>
 <span>${writing?`${writing.lessons.length*8} writing assignments ready for ${escape(level?.name||state.level)}`:'Loading new writing tasks…'}</span></div>
 ${chosenPaperTask()?`<div class="v3-loaded-task"><strong>Selected: ${escape(chosenPaperTask().title)}</strong><p>${escape(chosenPaperTask().successCriteria)}</p>
 <h3>Writing checklist</h3><ul>${chosenPaperTask().checklist.map(x=>`<li>${escape(x)}</li>`).join('')}</ul>
 <details><summary>What a parent should verify</summary><ul>${chosenPaperTask().parentReview.map(x=>`<li>${escape(x)}</li>`).join('')}</ul></details></div>`:''}</section>`;
}
function choosePaperTask(){const lesson=chosenPaperLesson();const id=qs('#paper-task-choice')?.value;const task=lesson?.tasks.find(t=>t.id===id)||lesson?.tasks[0];if(!lesson||!task){fireNotice('Select a loaded lesson and task first.');return;}
 saved.paper.lessonId=lesson.id;saved.paper.taskId=task.id;saved.paper.prompt=task.prompt;saved.paper.reference=lesson.source;
 saved.paper.focus='';saved.paper.mode=task.mode;state.paperResult=null;state.localResult=null;persist();render();fireNotice('Assignment loaded: '+task.title+'. Your essay draft was preserved.');
}
const typeLabels={mcq:'Choose one',fill:'Type a short answer',short:'Explain in writing',edit:'Correct the sentence',order:'Sequence events',essay:'Essay and analysis'};
function navButton(view,label,icon){return `<button type="button" class="nav-item ${state.view===view?'active':''}" data-action="view" data-view="${view}" aria-current="${state.view===view?'page':'false'}"><span class="nav-icon">${icon}</span><span>${escape(label)}</span></button>`;}
function sidebar(){return `<aside class="atlas-sidebar ${state.mobile?'sidebar-open':''}" aria-label="ATLAS section navigation">
    <div class="brand"><div class="brand-glyph">A<span>✦</span></div><div><strong>ATLAS ENGLISH</strong><small>READING & WRITING ACADEMY</small></div></div>
    <div class="sidebar-label">WORKSPACE</div>
    ${navButton('home','Course library','▦')}
    <a class="classic-link" style="display:block;margin:9px 0 13px;color:#95eedb" href="reading-pathway.html">📚 NEW: College Reading Pathway 4.0 →</a>
    ${navButton('lesson','Learning desk','▤')}
    ${navButton('visual','Visual learning labs','◇')}
    ${navButton('paper','Paper correction lab','✎')}
    ${navButton('progress','Learning analytics','◔')}
    ${navButton('guide','Scoring & instructions','?')}
    <div class="side-divider"></div><div class="sidebar-label">QUICK SELECT — LEVEL</div>
    <div class="level-grid-side">${M.levels.map(l=>`<button type="button" class="level-pill ${state.level===l.id?'selected':''}" data-action="level" data-level="${l.id}" title="${escape(l.name)}">${escape(l.id==='PK'?'Pre':l.id==='K'?'K':l.id==='C1'?'C1':l.id==='C2'?'C2':l.id)}</button>`).join('')}</div>
    <div class="sidebar-note"><span class="status-dot"></span><strong>PRIVATE BY DESIGN</strong><p>Offline lessons and grading. Answers stay in this browser unless you export them.</p></div>
    <a href="classic.html" class="classic-link">↗ Open original 1,920 exercises</a>
  </aside>`;}
function toolbar(){return `<header class="toolbar"><button class="icon-button mobile-only" data-action="menu" aria-label="Toggle navigation">☰</button>
 <div class="breadcrumbs">ATLAS / <strong>${escape(({home:'Course library',lesson:'Learning desk',paper:'Writing workshop',visual:'Visual learning labs',progress:'Learner analytics',guide:'Scoring policy'})[state.view])}</strong><span class="header-sep">/</span><span class="toolbar-grade">${escape(shortLabel(state.level))}</span></div>
 <div class="toolbar-actions"><button type="button" class="icon-button" data-action="font" title="Adjust reading size" aria-label="Adjust reading font size">A±</button>
 <button type="button" class="icon-button" data-action="theme" title="Light/dark mode" aria-label="Toggle color scheme">${saved.theme==='dark'?'☼':'☾'}</button>
 <button type="button" class="small-btn" data-action="export">↓ Export</button><button type="button" class="small-btn" data-action="import">↑ Import</button>
 <input type="file" id="backup-file" accept="application/json,.json" hidden aria-label="Select backup file"></div></header>`;}
function stats(){const entries=Object.values(saved.history);const attempts=entries.length,passed=entries.filter(x=>x.best>=80).length;
 const objective=entries.filter(x=>Number.isFinite(x.objectivePercent)).map(x=>x.objectivePercent);
 return {attempts,passed,avg:objective.length?Math.round(objective.reduce((a,b)=>a+b,0)/objective.length):0,pct:Math.round(100*attempts/M.lessonCount)};}
function summaryCards(){const s=stats();return `<div class="metric-row">
   <div class="metric"><span>FULL EXERCISE LIBRARY</span><b>${format(M.combinedAssignmentCount)}</b><small>Original + v2 practice + 12,288 writing tasks</small></div>
   <div class="metric"><span>VISUAL LESSON MAPS</span><b>${format(M.artCount)}</b><small>Original, zoomable SVG diagrams</small></div>
   <div class="metric"><span>MY COMPLETED STUDIOS</span><b>${s.attempts}</b><small>${s.passed} scored at 80% or above</small></div>
   <div class="metric"><span>OBJECTIVE ACCURACY</span><b>${s.avg}%</b><small>Average objective result, not essay grade</small></div>
 </div>`;}
function pickerHTML(){return `<div class="filterbar"><label class="filter"><span>Learning level</span><select id="filter-level">${M.levels.map(l=>`<option value="${l.id}" ${state.level===l.id?'selected':''}>${escape(l.name)}</option>`).join('')}</select></label>
 <label class="filter"><span>English strand</span><select id="filter-strand"><option value="all">All 12 learning strands</option>${M.strands.map(x=>`<option value="${x.id}" ${state.strand===x.id?'selected':''}>${escape(x.name)}</option>`).join('')}</select></label>
 <label class="filter flex"><span>Find a lesson</span><input id="filter-search" type="search" placeholder="Search lesson title, skill, or focus…" value="${escape(state.search)}"></label></div>`;}
function filteredIndex(){const term=state.search.toLowerCase().trim();return M.lessonIndex.filter(l=>l.level===state.level&&(state.strand==='all'||l.strand===state.strand)&&(!term||(`${l.title} ${l.role} ${strands.get(l.strand)?.focus||''}`).toLowerCase().includes(term)));}
function lessonGrid(){const all=filteredIndex();const entries=state.showAll?all:all.slice(0,24);
 return `<div class="lesson-grid" id="lesson-grid">${entries.length?entries.map(l=>{
 const prog=saved.history[l.id];return `<button class="lesson-tile" type="button" data-action="lesson" data-lesson="${l.id}"><div class="tile-art"><img src="${escape(l.art)}" alt="Educational illustration for ${escape(l.title)}" loading="lazy"></div>
 <div class="tile-body"><div class="tile-number">UNIT ${String(l.unit).padStart(2,'0')} <span>${prog?`${Math.round(prog.best)}% BEST`:'15 ASSIGNMENTS'}</span></div>
 <h3>${escape(l.title)}</h3><p>${escape(strands.get(l.strand)?.focus||'Reading and writing')}</p><div class="tile-foot"><span>${escape(l.role)}</span><b>Open →</b></div></div></button>`;}).join(''):'<div class="empty">No matching lessons. Change your filters or search term.</div>'}</div>
 ${all.length>24?`<div class="show-more"><button type="button" class="button secondary" data-action="show-more">${state.showAll?'Show fewer lessons':`Show all ${all.length} matching lessons`}</button></div>`:''}`;}
function home(){return `<div class="hero"><div class="hero-background" aria-hidden="true"><span>A</span><span>e</span><span>✦</span></div><div class="hero-copy"><div class="eyebrow">THE COMPLETE LANGUAGE LEARNING STUDIO · V4.0 + ORIGINAL V3 CONTENT</div>
 <h1>Read with confidence.<br><em>Write with purpose.</em></h1>
 <p>Preschool through college. Follow original reading cases, see evidence visually, practice thousands of assignments, and revise papers with explainable feedback.</p>
 <div class="hero-buttons"><button type="button" class="button primary" data-action="lesson" data-lesson="${state.level}-phonics-01">Start learning <span>→</span></button>
 <button type="button" class="button secondary" data-action="view" data-view="paper">Open writing evaluator</button></div></div>
 <div class="hero-graphic" aria-hidden="true"><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><div class="orbit orbit-three"></div><div class="hero-letter">Aa</div><span class="orbit-tag tag-one">READ</span><span class="orbit-tag tag-two">REASON</span><span class="orbit-tag tag-three">REVISE</span></div></div>
 ${summaryCards()}
 <div class="section-top"><div><div class="eyebrow">EXPLORE THE CURRICULUM</div><h2>Choose a learning pathway</h2><p>One level contains 96 additional lessons, each with 15 practice assignments.</p></div><span class="section-indicator">16 LEVELS / 12 STRANDS</span></div>
 ${pickerHTML()}<div id="filtered-lessons">${lessonGrid()}</div>
 <div class="feature-grid"><a class="feature" style="text-decoration:none;color:inherit" href="reading-pathway.html"><span class="feature-icon">📚</span><h3>NEW: College Reading Pathway v4</h3><p>25+ MiB of new reading lessons, source comparisons, 13,312 new assignments and independent college transfer challenges.</p><b>Open new reading course →</b></a><button class="feature" data-action="view" data-view="visual"><span class="feature-icon">◇</span><h3>Visual language labs</h3><p>See how sentences, stories, arguments and research work with interactive diagrams.</p><b>Explore diagrams →</b></button>
 <button class="feature" data-action="view" data-view="paper"><span class="feature-icon">✎</span><h3>Paper correction lab</h3><p>Paste an essay to analyze structure, reasoning markers, clarity and revision priorities.</p><b>Review your writing →</b></button>
 <button class="feature" data-action="view" data-view="guide"><span class="feature-icon">◎</span><h3>Understand your score</h3><p>Separate verified objective checks from provisional writing estimates and human assessment.</p><b>How it works →</b></button></div>`;}
function feedback(q,r){if(!r)return '';
 const name=r.kind==='writing'?'Provisional writing estimate':r.kind==='objective'?'Objective answer check':'Unanswered';
 return `<div class="feedback-box ${r.kind==='objective'&&r.percent>=99?'correct':''}" role="status"><div class="feedback-header"><b>${escape(name)}</b><strong>${r.score} / ${r.max} pts</strong></div><p>${escape(r.message)}</p>
 ${r.details?.length?`<div class="feedback-notes">${r.details.map(d=>`<p>${escape(d)}</p>`).join('')}</div>`:''}
 ${r.report?reportHTML(r.report,`${state.lessonId}-${q.id}`,q):''}
 ${r.kind==='writing'?`<div class="fixbar"><button class="button small secondary" data-action="fix-question" data-q="${q.id}">Suggest / apply safe mechanical fixes</button><small>Review your draft afterward; this does not validate meaning.</small></div>`:''}
 </div>`;}
function reportHTML(report,id,q){const manual=saved.manual[id];return `<div class="writing-report">
 <div class="report-head"><div><strong>Six-dimension writing diagnostics</strong><p>These indicators do not establish semantic accuracy or authorship. Human review required.</p>${report.estimatedRange?`<div class="v3-uncertainty"><b>Possible rubric-score range: ${report.estimatedRange.low}–${report.estimatedRange.high}%</b><span>Wide range because an offline rules engine cannot verify meaning; this is not a measurement of grading accuracy.</span></div>`:''}</div><div class="report-metrics">${report.metrics.wordCount} words <span>·</span> ${report.metrics.sentenceCount} sentences</div></div>
 <div class="rubric-list">${report.criteria.map(c=>`<div class="rubric-item"><div class="rubric-title"><b>${escape(c.label)}</b><span>${Math.round(c.ratio*100)}% indicator</span></div><div class="meter"><span style="width:${Math.round(c.ratio*100)}%"></span></div><p>${escape(c.why)}</p></div>`).join('')}</div>
 ${report.caps?.length?`<div class="paper-warning">${report.caps.map(s=>`<p>⚠ ${escape(s)}</p>`).join('')}</div>`:''}
 ${report.fixes?.length?`<div class="revision-plan"><h4>Revision priorities</h4><ol>${report.fixes.map(x=>`<li>${escape(x)}</li>`).join('')}</ol></div>`:''}
 ${report.contradictions?.length?`<div class="v3-contradictions"><b>Possible source-meaning conflicts — verify manually</b>${report.contradictions.map(x=>`<p>${escape(x.message)} <q>${escape(x.excerpt)}</q></p>`).join('')}</div>`:''}
 ${report.annotations?.length?`<details class="deep-details"><summary>Sentence-level review (${report.annotations.length})</summary>${report.annotations.map(x=>`<div class="annotation"><b>${escape(x.issue)}</b><blockquote>${escape(x.excerpt)}</blockquote><p>${escape(x.suggestion)}</p></div>`).join('')}</details>`:''}
 ${q?`<div class="teacher-row"><label>Teacher-reviewed score (optional, 0–100%) <input type="number" min="0" max="100" step="1" data-manual-input="${escape(id)}" value="${manual===undefined?'':Number(manual)}" placeholder="Human assessment"></label><button type="button" data-action="manual" data-manual="${escape(id)}" class="button secondary">Save review</button>${manual!==undefined?`<span class="reviewed">Human: ${manual}%</span>`:''}</div>`:''}
 </div>`;}
function questionControl(q,a){const id=escape(q.id),val=escape(a??'');
 if(q.type==='mcq')return `<div class="option-list">${q.options.map(o=>`<label class="option ${a===o.id?'selected':''}"><input type="radio" name="answer-${id}" data-question="${id}" value="${o.id}" ${a===o.id?'checked':''}><span>${escape(o.text)}</span></label>`).join('')}</div>`;
 if(q.type==='fill')return `<input data-question="${id}" class="answer-input" type="text" value="${val}" placeholder="Type an answer, then press Enter to check" spellcheck="true" autocomplete="off">`;
 if(q.type==='edit')return `<textarea data-question="${id}" class="answer-input edit-input" rows="2" placeholder="Rewrite the whole sentence with correct capitals and punctuation">${val}</textarea>`;
 if(q.type==='short'||q.type==='essay')return `<div class="writing-area"><textarea data-question="${id}" rows="${q.type==='essay'?13:5}" class="answer-input long-text" placeholder="Enter your own ideas. Support interpretations with details from the passage…" spellcheck="true">${val}</textarea>
 <div class="editor-status"><span>Target ${q.minimumWords} words</span><span data-word-counter="${id}">${wordCount(a)} words entered</span><span>Auto-saved on this device</span></div></div>`;
 if(q.type==='order')return `<div class="order-controls">${q.answer.map((_,pos)=>`<div class="order-input"><strong>${pos+1}</strong><select data-order="${id}" data-pos="${pos}" aria-label="Position ${pos+1}"><option value="">Choose an event…</option>${q.steps.map((s,i)=>`<option value="${i}" ${String(a?.[pos])===String(i)?'selected':''}>${escape(s)}</option>`).join('')}</select></div>`).join('')}</div>`;
 return '<p>Unsupported exercise type.</p>';
}
function questionHTML(q,i){const a=answerDraft()[q.id];const r=state.feedback[state.lessonId]?.[q.id];return `<article class="question" id="question-${escape(q.id)}">
 <div class="question-meta"><span class="number-badge">${String(i+1).padStart(2,'0')}</span><span>${escape(typeLabels[q.type]||q.type)}</span><span class="q-skill">${escape(q.skill||'language practice')}</span><span class="q-points">${q.points} pts</span></div>
 <h3>${escape(q.prompt)}</h3>${questionControl(q,a)}
 <div class="question-actions"><span class="helper-text">${q.type==='essay'?'Detailed rubric + revision advice':q.type==='short'?'Concept and evidence checks are provisional':q.type==='fill'||q.type==='edit'?'Enter to check': 'Choose your response then check'}</span>
 <button class="button small secondary" type="button" data-action="check" data-q="${q.id}">Check response →</button></div>
 <div id="feedback-${q.id}">${feedback(q,r)}</div></article>`;}
function readingAndMentors(lesson){const paras=lesson.reading.paragraphs;return `<section class="reading-pane" aria-label="Reading passage and instruction">
 <div class="reader-panel"><div class="panel-title"><span class="eyebrow">ORIGINAL READING TEXT</span><div class="read-buttons"><button class="small-btn" data-action="read">♫ Listen</button><button class="small-btn" data-action="stop">◼ Stop</button><button class="small-btn" data-action="print">▤ Print</button></div></div>
 <div class="reader-body"><div class="reading-caption">${escape(lesson.reading.kind)} · ${paras.length} paragraphs</div>
 ${paras.map(p=>`<p>${escape(p)}</p>`).join('')}</div>
 <div class="evidence-note"><b>Important evidence</b><p>${escape(lesson.reading.notice)}</p></div>
 </div>
 <div class="reader-panel teaching-panel"><div class="panel-title"><span class="eyebrow">LESSON COACH</span><span class="mode-label">${escape(lesson.role)}</span></div>
 <div class="mentors">${lesson.mentor.map((m,i)=>`<details class="mentor" ${i<2?'open':''}><summary>${escape(m.title)}</summary><div>${escape(m.body)}</div></details>`).join('')}</div></div>
 <div class="reader-panel"><div class="panel-title"><span class="eyebrow">WRITING MAP</span></div><ol class="writing-outline">${lesson.writingPlan.outline.map(s=>`<li>${escape(s)}</li>`).join('')}</ol>
 <div class="glossary-head">Vocabulary to explore</div>${lesson.glossary.map(g=>`<div class="glossary-row"><b>${escape(g.word)}</b><span>${escape(g.meaning)}</span></div>`).join('')}</div>
 </section>`;}
function resultsBar(lesson){const r=state.lastResults[lesson.id];if(!r)return '';
 return `<section class="score-panel" id="score-panel"><div><span class="eyebrow">CURRENT PRACTICE RESULT</span><h2>${r.percent}% <small>provisional combined practice score</small></h2><p>${r.score}/${r.max} points across ${r.answered}/${lesson.questions.length} answered assignments.</p></div>
 <div class="score-details"><b>${r.objectivePercent===null?'—':r.objectivePercent+'%'}</b><span>Verified objective subset</span><p>${r.objectiveScore}/${r.objectiveMax} objective points</p></div>
 <div class="score-details"><b>${r.writingCount}</b><span>Writing responses requiring human review</span><p>Revise and submit again to improve.</p></div></section>`;}
function lessonView(){const l=curLesson();if(!l)return `<div class="loading"><h2>Preparing your reading studio…</h2><p>Please verify the curriculum files were extracted with the application.</p></div>`;
 return `<div class="lesson-header"><div class="lesson-back"><button class="text-button" data-action="view" data-view="home">← All lessons</button><span> / ${escape(l.levelName)} / ${escape(l.strandName)}</span></div>
 <div class="eyebrow">STUDIO LESSON ${String(l.index).padStart(2,'0')} / 96</div><h1>${escape(l.title)}</h1><p>${escape(l.objective)}</p>
 <div class="lesson-tags"><span>◷ ${l.readingTime} min reading</span><span>✎ ${l.questions.length} assignments</span><span>◈ ${escape(l.stage)}</span><span>◉ Offline scored</span></div></div>
 <div class="art-hero"><img src="${escape(l.art)}" alt="Graphic pathway to study the evidence in ${escape(l.caseTitle)}"></div>
 <div class="lesson-layout">${readingAndMentors(l)}<section class="assignment-pane"><div class="assignment-header"><div><div class="eyebrow">INTERACTIVE ASSIGNMENTS</div><h2>Practice, explain, revise</h2><p>Enter answers; select <strong>Check response</strong> for immediate feedback. Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to grade the full lesson.</p></div><button type="button" class="button primary" data-action="grade">Grade all ↗</button></div>
 ${l.questions.map(questionHTML).join('')}
 ${resultsBar(l)}
 <div class="lesson-end"><button class="button primary" data-action="grade">Submit all and score →</button><button class="button secondary" data-action="clear">Clear current draft</button><button class="button secondary" data-action="next">Next lesson →</button></div></section></div>`;}
function visualView(){const lab=V.labs.find(x=>x.id===state.visualId)||V.labs[0],node=lab.nodes[state.visualStep];return `<div class="eyebrow">INTERACTIVE CONCEPT VISUALIZATIONS</div><h1 class="page-title">Language Visual Lab</h1><p class="intro">Click a subject and then a stage. The illustration and teaching example change immediately—no downloads or external libraries.</p>
 <div class="visual-tabs">${V.labs.map(x=>`<button type="button" class="visual-tab ${x.id===lab.id?'active':''}" data-action="visual" data-visual="${x.id}"><span>${x.icon}</span>${escape(x.label)}</button>`).join('')}</div>
 <section class="visual-feature"><div class="eyebrow">${escape(lab.label.toUpperCase())}</div><h2>${escape(lab.title)}</h2><p>${escape(lab.description)}</p>${V.renderSvg(lab,state.visualStep)}
 <div class="visual-steps">${lab.nodes.map((x,i)=>`<button type="button" class="step-tab ${i===state.visualStep?'active':''}" data-action="visual-step" data-step="${i}"><b>0${i+1}</b>${escape(x.title)}</button>`).join('')}</div>
 <div class="visual-explain"><div class="visual-step-count">STAGE ${state.visualStep+1} OF 4</div><h3>${escape(node.title)} · ${escape(node.short)}</h3><blockquote>${escape(node.example)}</blockquote><p>${escape(node.tip)}</p><button class="button small" data-action="visual-next">Next step →</button></div></section>`;}
function prepareLabQuestion(){const source=saved.paper?.reference||'';const prompt=saved.paper?.prompt||'Analyze the text';const focus=saved.paper?.focus||'';
 const chosen=chosenPaperTask(),lesson=chosenPaperLesson();
 if(chosen&&lesson&&prompt===chosen.prompt&&source===lesson.source)return {...chosen,type:'essay',points:100,minimumWords:saved.paper.mode==='page'?A.profile(state.level).targetPage:chosen.minimumWords,referenceText:lesson.source,level:state.level,taskId:chosen.id};
 const focusConcepts=focus.split('|').map(x=>x.trim()).filter(Boolean).slice(0,7).map(x=>({label:x,terms:x.split(',').map(v=>v.trim()).filter(Boolean)}));
 const references=source.split(/[.!?]+(?:\s|$)/).map(x=>x.trim()).filter(x=>x.length>30).slice(0,3);
 return {id:'paper',type:'essay',prompt,points:100,level:state.level,minimumWords:saved.paper.mode==='page'?A.profile(state.level).targetPage:A.profile(state.level).targetParagraph,
 referenceText:source,expectedEvidence:references,concepts:focusConcepts,
 rubric:[{key:'task',weight:.18},{key:'reason',weight:.22},{key:'evidence',weight:.24},{key:'organization',weight:.16},{key:'style',weight:.12},{key:'integrity',weight:.08}]};
}
function paperView(){const p=saved.paper||fresh().paper;return `<div class="eyebrow">WRITING LAB / EXPLAINABLE FEEDBACK</div><h1 class="page-title">Paper correction studio <span class="v3-marker">v3.0</span></h1><p class="intro">Choose an assigned reading prompt or paste a draft. Check writing conventions, task coverage, evidence and structure. Offline estimates include a broad uncertainty range; a parent must verify accuracy and meaning.</p>
 ${paperExercisePicker()}
 <div class="paper-workspace"><section class="paper-editor"><div class="panel-title"><div><span class="eyebrow">YOUR PAPER</span><h2>Draft and revise</h2></div><button class="small-btn" data-action="clear-paper">Clear draft</button></div>
 <div class="paper-fields"><label>Writing prompt / assignment <textarea id="paper-prompt" rows="2" placeholder="What is the essay supposed to answer?">${escape(p.prompt)}</textarea></label>
 <label>Reference reading or source (optional) <textarea id="paper-reference" rows="4" placeholder="Paste the supplied passage here, if applicable. Evidence matching is approximate.">${escape(p.reference)}</textarea></label>
 <label>Key concepts to consider (optional; separate clusters with | and variants with commas) <input id="paper-focus" value="${escape(p.focus)}" placeholder="evidence,detail | because,therefore | limitation,uncertain"></label>
 <label>Response format <select id="paper-mode"><option value="paragraph" ${p.mode==='paragraph'?'selected':''}>Paragraph (short response)</option><option value="page" ${p.mode==='page'?'selected':''}>One-page response</option></select></label>
 <label>Your essay <textarea id="paper-text" rows="20" spellcheck="true" placeholder="Paste your paper here and select Analyze draft…">${escape(p.text)}</textarea></label>
 <div class="paper-bottom"><span id="paper-counter">${wordCount(p.text)} words · saved in browser</span><div><button type="button" class="button secondary" data-action="download-paper">Download TXT</button><button type="button" class="button primary" data-action="paper-grade">Analyze draft ↗</button></div></div></div></section>
 <section class="paper-side"><div class="paper-side-card"><span class="eyebrow">WHAT THE REVIEWER CAN CHECK</span><h3>Six writing dimensions</h3>
 ${['Task coverage','Reasoning signals','Textual evidence','Organization','Clarity and conventions','Repetition / copying indicators'].map((s,i)=>`<div class="rubric-preview"><span>${String(i+1).padStart(2,'0')}</span>${s}</div>`).join('')}
 <p>Writing quality is not reducible to keywords. Feedback is a revision aid; human judgment remains necessary.</p></div>
 <div class="paper-side-card"><span class="eyebrow">OPTIONAL LOCAL AI REVIEW</span><h3>Review with your own model</h3><p>This option works only if you start the included <code>local_review_server.py</code> and have Ollama running locally. No API key is embedded in this page.</p>
 <button type="button" class="button secondary" data-action="ai-review">Request local model critique</button><div id="ai-result">${localReviewHTML()}</div></div>
 </section></div>
 <div id="paper-result">${paperResultHTML()}</div><section class="v3-review-history"><h2>Parent-review calibration</h2>${paperReviewStatsHTML()}<p>Local comparisons summarize agreement with the scores a parent entered. They do not prove that the software grades accurately or fairly.</p></section>`;}
function paperProofreadHTML(){const fixes=G.proofread(saved.paper.text||'');if(!fixes.count)return '<div class="proofread-panel"><b>Mechanical proofreader:</b> No listed high-confidence edit patterns detected. This is not a declaration of grammatical correctness.</div>';
 return `<div class="proofread-panel"><div class="proofread-head"><strong>${fixes.count} proposed mechanical edits</strong><button type="button" class="button small secondary" data-action="apply-paper-fixes">Apply these mechanical edits to draft</button></div><p>These corrections are conservative spelling/spacing patterns. Check them before retaining changes.</p>
 <details><summary>Review individual changes</summary><div class="changes-list">${fixes.changes.map(c=>`<div><span>${escape(c.rule)}</span><del>${escape(c.before)}</del><b>→</b><ins>${escape(c.after)}</ins></div>`).join('')}</div></details></div>`;}
function paperResultHTML(){const r=state.paperResult;if(!r)return '';
 if(!r.report)return '';
 const hasReference=Boolean(r.report.scoreEligible&&saved.paper.reference.trim());
 return `<section class="paper-output"><div class="eyebrow">DRAFT REVIEW</div><h2>${hasReference?`Provisional rubric indicator: ${r.percent}%`:'Writing diagnostics (not scorable yet)'}</h2>
 ${hasReference?`<p class="v3-score-range">Broader estimated range: <strong>${r.report.estimatedRange.low}–${r.report.estimatedRange.high}%</strong> · Needs a parent’s judgment of the actual meaning.</p>`:''}
 <p>${hasReference?'The reference provides material for approximate comparison, but a human must still verify your claims.':'No source text was provided, so the app cannot evaluate evidence accuracy or give a justified overall score.'}</p>
 ${paperProofreadHTML()}
 ${reportHTML(r.report,null,null)}
 <div class="v3-parent-panel"><h3>Parent / teacher verification</h3><p>Read the writing and source; check whether the interpretation and specific details are correct. Record an independent score out of 100, or leave the grade blank.</p>
 <label>Reviewed score (0–100) <input type="number" id="paper-human-score" min="0" max="100" placeholder="Parent’s score"></label>
 <label>Feedback on meaning and reasoning <textarea id="paper-human-note" rows="3" placeholder="What was accurate? What should the student revise?"></textarea></label>
 <button class="button secondary" data-action="save-paper-human" type="button">Save independent parent review</button></div></section>`;
}
function paperReviewStatsHTML(){const rows=(saved.paperReviews||[]);const x=C.analyze(rows,state.level);if(!x.n)return '<p>There are no parent-reviewed papers for this level yet.</p>';
 return `<div class="v3-calibration-stats"><div><strong>${x.n}</strong><span>Reviewed papers</span></div><div><strong>${x.mae} pts</strong><span>Mean estimate error</span></div><div><strong>${x.within10}%</strong><span>Within ±10 points of the parent’s grade</span></div><div><strong>${x.bias>0?'+':''}${x.bias}</strong><span>Average software minus parent score</span></div></div><p>${escape(x.note)}</p>`;
}
function paperSignature(text){let hash=2166136261;for(const ch of String(text).slice(0,75000)){hash^=ch.charCodeAt(0);hash=Math.imul(hash,16777619);}return (hash>>>0).toString(16);}
function savePaperHuman(){const scoreEl=qs('#paper-human-score'),noteEl=qs('#paper-human-note');const str=scoreEl?.value?.trim();const score=Number(str);
 if(str===''||!Number.isFinite(score)||score<0||score>100){fireNotice('Enter an independent parent score between 0 and 100.');return;}
 const result=state.paperResult;if(!result?.report){fireNotice('Analyze the writing before adding a parent score.');return;}
 const notes=String(noteEl?.value||'').slice(0,2000),signature=paperSignature((saved.paper.text||'')+'\n'+(saved.paper.prompt||''));
 saved.paper.parentScore=Math.round(score);saved.paper.parentNote=notes;
 if(result.report.scoreEligible){
   const review={level:state.level,machine:result.percent,teacher:Math.round(score),taskId:saved.paper.taskId||'',mode:saved.paper.mode||'paragraph',date:new Date().toISOString(),note:notes,wordCount:result.report.metrics.wordCount,signature};
   const existing=saved.paperReviews.findIndex(r=>r.signature===signature&&r.level===state.level);
   if(existing>=0)saved.paperReviews[existing]=review;else saved.paperReviews.push(review);
   saved.paperReviews=saved.paperReviews.slice(-250);
 }
 persist();render();fireNotice(result.report.scoreEligible?'Independent parent review saved for local comparison.':'Independent parent score saved; no automated grade was counted without enough reference material.');
}
function localReviewHTML(){const x=state.localResult;if(!x)return '<p class="help-hint">Local AI evaluation is optional and disabled until you run the included reviewer server.</p>';
 if(x.error)return `<div class="paper-warning">${escape(x.error)}</div>`;
 return `<section class="llm-response"><h4>Local model feedback <span class="provisional">Provisional</span></h4><p>${escape(x.summary||'No summary returned.')}</p>
 ${Array.isArray(x.rubric)?x.rubric.map(item=>`<div class="ai-criterion"><b>${escape(item.dimension)} ${Number.isFinite(item.rating)?`· tentative ${item.rating}/4`:''}</b><p>${escape(item.feedback)}</p>${item.studentExcerpt?`<blockquote>Student: ${escape(item.studentExcerpt)}</blockquote>`:''}</div>`).join(''):''}
 ${Array.isArray(x.revisions)?`<h4>Suggested edits</h4><ol>${x.revisions.map(x=>`<li>${escape(x)}</li>`).join('')}</ol>`:''}
 <p class="help-hint">An LLM may make errors. Confirm every comment against the source and prompt. This assessment does not override teacher scoring.</p></section>`;
}
function progressView(){const s=stats();const perStrand=M.strands.map(x=>({label:x.name,attempts:Object.keys(saved.history).filter(k=>indexById.get(k)?.strand===x.id).length}));
 const rows=Object.entries(saved.history).sort((a,b)=>String(b[1].lastAt).localeCompare(String(a[1].lastAt))).slice(0,50);
 return `<div class="eyebrow">PRIVATE LEARNING ANALYTICS</div><h1 class="page-title">Your progress</h1><p class="intro">Scores and drafts are stored in this browser only. Objective answers are verified; written-response scores remain provisional until reviewed.</p>
 ${summaryCards()}<div class="progress-layout"><section class="progress-card"><h2>Curriculum coverage</h2><div class="big-number">${s.pct}%</div><div class="meter huge"><span style="width:${s.pct}%"></span></div><p>${s.attempts} of ${M.lessonCount} new studios attempted.</p>
 <h3>Practice by subject</h3>${perStrand.map(x=>`<div class="subject-meter"><span>${escape(x.label)}</span><div class="meter"><span style="width:${Math.min(100,x.attempts/(16*8)*100)}%"></span></div><b>${x.attempts}</b></div>`).join('')}</section>
 <section class="progress-card"><h2>Recent work</h2><div class="history-scroll">${rows.length?rows.map(([id,x])=>`<button class="history-item" data-action="lesson" data-lesson="${escape(id)}"><span>${escape(indexById.get(id)?.title||id)}<small>${escape(indexById.get(id)?.level||'')} · ${escape(x.lastAt?.slice(0,10)||'')}</small></span><b>${x.best}%</b></button>`).join(''):'<div class="empty">Your scored assignments will appear here after you submit a lesson.</div>'}</div>
 <div class="bottom-tools"><button class="button secondary" data-action="export">Export progress JSON</button><button class="button danger" data-action="reset">Reset stored progress</button></div></section></div>`;}
function guideView(){return `<div class="eyebrow">ASSESSMENT TRANSPARENCY</div><h1 class="page-title">How scoring works</h1><p class="intro">This platform separates deterministic answer checking from fallible writing analysis. Students can always inspect the reason for feedback and revise their answers.</p>
 <div class="guide-grid"><section class="guide-card"><span class="verify-chip">✓ VERIFIED</span><h2>Objective assessment</h2><p>Multiple choice, fill-in terminology and ordered sequences are checked against the authored key. Sentence edits accept listed alternatives. Similar-looking but different responses are not silently credited.</p><div class="guide-sample">TYPE AN ANSWER → CHECK → KEY + EXPLANATION</div></section>
 <section class="guide-card"><span class="provisional">○ PROVISIONAL</span><h2>Writing assessment</h2><p>Short responses and essays are screened against grade-specific rubrics, source-linked evidence anchors, task coverage, organization, sentence conventions, repetition and source overlap. Wide score ranges reflect uncertainty. A model review can provide a separate second opinion.</p><div class="guide-sample">DRAFT → RUBRIC INDICATORS → REVISION ADVICE</div></section>
 <section class="guide-card"><span class="verify-chip">✎ HUMAN REVIEW</span><h2>Teacher assessment</h2><p>A parent or teacher can record an independent paper grade and compare estimates to human reviews. Machine scores never replace the human score. Nuanced argument quality, voice, factual accuracy, authorial intent, fairness and originality require expert review.</p><div class="guide-sample">REVIEW → COMMENT → SAVE OVERRIDE</div></section>
 <section class="guide-card"><span class="provisional">◇ OPTIONAL MODEL</span><h2>Local AI critique</h2><p>The optional loopback-only review server can query Ollama for richer semantic feedback. Results are not guaranteed correct, should be verified, and are separate from objective keys and teacher decisions. No external AI model is required to use the course.</p><div class="guide-sample">OLLAMA ON YOUR MACHINE → CRITIQUE</div></section></div>
 <section class="guide-wide"><h2>Keyboard, accessibility and privacy</h2><div class="guide-columns"><p><strong>Enter</strong> checks a focused single-line answer. <strong>Ctrl+Enter</strong> grades the current lesson. Use Tab to navigate controls. Listen uses the browser’s available text-to-speech voices.</p><p>All 1,536 diagrams are local SVG files. Course levels load on demand, including from extracted files without a web server. Back up progress before clearing browser data.</p><p>Data is not sent anywhere by default. Choosing local-model review sends only the pasted prompt, source, and draft to the server running on your machine; it does not involve a hosted cloud service unless you explicitly change the server implementation.</p></div></section>`;}
function render(){setAppearance();host.innerHTML=`<div class="studio-shell">${sidebar()}<div class="main-pane">${toolbar()}<main id="main" tabindex="-1" class="page-content">${state.storageWarning?'<div class="storage-alert">Storage is unavailable. Use Export to preserve your responses.</div>':''}${state.view==='home'?home():state.view==='lesson'?lessonView():state.view==='visual'?visualView():state.view==='paper'?paperView():state.view==='progress'?progressView():guideView()}</main><footer class="app-footer">ATLAS ENGLISH ACADEMY 3.0 · ORIGINAL EDUCATIONAL CONTENT · NO ACCOUNT REQUIRED · EVALUATION IS EDUCATIONAL, NOT ACCREDITED</footer></div></div><div id="toast" class="toast" role="status"></div>`;}
function stopSpeaking(){try{speechSynthesis.cancel();}catch(e){}}
function readLesson(){const l=curLesson();if(!l)return;if(!('speechSynthesis' in window)){fireNotice('Speech synthesis is not supported in this browser.');return;}
 stopSpeaking();const utter=new SpeechSynthesisUtterance(l.reading.paragraphs.join(' '));utter.lang='en-US';utter.rate=['PK','K','1','2'].includes(l.level)?.85:1;window.speechSynthesis.speak(utter);}
function saveAnswer(id,value){if(!curLesson())return;
 saved.answers[state.lessonId]=saved.answers[state.lessonId]||{};saved.answers[state.lessonId][id]=value;
 if(state.feedback[state.lessonId]?.[id]){delete state.feedback[state.lessonId][id];const box=qs(`#feedback-${id}`);if(box)box.innerHTML='';}
 persist();const n=qs(`[data-word-counter="${id}"]`);if(n)n.textContent=`${wordCount(value)} words entered`;
}
function checkOne(id){const l=curLesson(),q=l?.questions.find(x=>x.id===id);if(!q)return;
 const result=G.grade(q,answerDraft()[id]);state.feedback[l.id]=state.feedback[l.id]||{};state.feedback[l.id][id]=result;
 const box=qs(`#feedback-${id}`);if(box)box.innerHTML=feedback(q,result);
}
function gradeAll(){const l=curLesson();if(!l)return;const r=G.gradeLesson(l,answerDraft());
 state.lastResults[l.id]=r;state.feedback[l.id]=Object.fromEntries(r.items.map(x=>[x.id,x]));
 const old=saved.history[l.id];saved.history[l.id]={best:Math.max(old?.best||0,r.percent),objectivePercent:r.objectivePercent,attempts:(old?.attempts||0)+1,lastAt:r.gradedAt};
 persist();render();qs('#score-panel')?.scrollIntoView({behavior:'smooth',block:'center'});
}
async function openLesson(id){const summary=indexById.get(id);if(!summary)return;state.level=summary.level;state.lessonId=id;state.view='lesson';state.mobile=false;stopSpeaking();
 try{await loadLevel(summary.level);render();window.scrollTo({top:0,behavior:'instant'});try{location.hash=`studio-${encodeURIComponent(id)}`;}catch(e){}}
 catch(e){host.innerHTML=`<div class="error-large">${escape(e.message)} <a href="classic.html">Open the original course</a>.</div>`;}
}
function nextLesson(){const i=M.lessonIndex.findIndex(x=>x.id===state.lessonId);if(i>=0)openLesson(M.lessonIndex[(i+1)%M.lessonIndex.length].id);}
function setView(v){if(!['home','lesson','visual','paper','progress','guide'].includes(v))return;
 if(v==='lesson'){openLesson(state.lessonId);return;}state.view=v;state.mobile=false;render();window.scrollTo({top:0,behavior:'instant'});if(v==='paper'){Promise.all([loadLevel(state.level),loadWritingTasks(state.level)]).then(()=>{if(state.view==='paper')render();}).catch(e=>fireNotice(e.message));}}
function download(name,text,mime='text/plain'){const blob=new Blob([text],{type:mime}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1400);}
function exportBackup(){const clean={kind:'ATLAS_STUDIO_V2_BACKUP',saved:{...saved}};download('ATLAS_English_Academy_v3_Progress.json',JSON.stringify(clean,null,2),'application/json');}
async function importBackup(file){if(!file||file.size>16*1024*1024){fireNotice('Choose a backup file smaller than 16 MB.');return;}
 try{const raw=JSON.parse(await file.text());if(raw.kind!=='ATLAS_STUDIO_V2_BACKUP'||raw.saved?.schema!==2)throw Error('Unrecognized backup format');
  const v=raw.saved,ids=new Set(M.lessonIndex.map(x=>x.id));let imported=0;
  for(const [id,data] of Object.entries(v.answers||{}))if(ids.has(id)&&data&&typeof data==='object'){
   const qids=new Set(Array.from({length:15},(_,i)=>`q${String(i+1).padStart(2,'0')}`));const out={};
   for(const [qid,a] of Object.entries(data))if(qids.has(qid)){
     if(typeof a==='string')out[qid]=a.slice(0,30000);
     else if(Array.isArray(a)&&a.length<=4)out[qid]=a.map(x=>String(x).slice(0,3));
   }saved.answers[id]=out;imported++;
  }
  for(const [id,x] of Object.entries(v.history||{}))if(ids.has(id)&&x&&Number.isFinite(x.best)){
    saved.history[id]={best:Math.round(Math.min(100,Math.max(0,x.best))),objectivePercent:Number.isFinite(x.objectivePercent)?Math.round(Math.min(100,Math.max(0,x.objectivePercent))):null,
     attempts:Math.min(10000,Math.max(1,Number(x.attempts)||1)),lastAt:String(x.lastAt||'').slice(0,40)};
  }
  for(const [id,n] of Object.entries(v.manual||{}))if(/^((PK|K|C1|C2|\d{1,2})-[a-z]+-\d\d)-q\d\d$/.test(id)&&Number.isFinite(n)&&n>=0&&n<=100)saved.manual[id]=n;
  if(Array.isArray(v.paperReviews))saved.paperReviews=v.paperReviews.filter(C.validRow).slice(-250).map(r=>({level:String(r.level).slice(0,3),machine:r.machine,teacher:r.teacher,mode:String(r.mode||'paragraph').slice(0,15),date:String(r.date||'').slice(0,40),taskId:String(r.taskId||'').slice(0,80),signature:String(r.signature||'').slice(0,16),note:String(r.note||'').slice(0,2000),wordCount:Math.max(0,Number(r.wordCount)||0)}));
  if(v.paper&&typeof v.paper==='object')for(const k of ['text','prompt','reference','focus','taskId','lessonId','mode','parentScore','parentNote'])if(typeof v.paper[k]==='string')saved.paper[k]=v.paper[k].slice(0,50000);
  if(v.paper&&Number.isFinite(v.paper.parentScore)&&v.paper.parentScore>=0&&v.paper.parentScore<=100)saved.paper.parentScore=Math.round(v.paper.parentScore);
  persist();render();fireNotice(`Imported answers from ${imported} lessons.`);
 }catch(e){fireNotice('Import failed: '+e.message);}}
function paperEvaluate(){const text=(saved.paper.text||'').trim();if(!text){fireNotice('Enter or paste your paper first.');return;}
 const q=prepareLabQuestion();state.paperResult=G.grade(q,text);render();qs('#paper-result')?.scrollIntoView({behavior:'smooth',block:'start'});}
async function localAI(){if(!saved.paper.text?.trim()){fireNotice('Write or paste a paper to review.');return;}
 const btn=qs('[data-action="ai-review"]');if(btn){btn.disabled=true;btn.textContent='Contacting local reviewer…';}
 try{const ctrl=new AbortController(),timeout=setTimeout(()=>ctrl.abort(),40000);
   let r;try{r=await fetch('http://127.0.0.1:8798/review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({level:shortLabel(state.level),prompt:saved.paper.prompt||'',source:saved.paper.reference||'',paper:saved.paper.text||''}),signal:ctrl.signal});}
   finally{clearTimeout(timeout);}if(!r.ok)throw Error('Local reviewer returned HTTP '+r.status);
   const out=await r.json();if(out.error)throw Error(String(out.error).slice(0,250));state.localResult=out;
 }catch(e){state.localResult={error:`Local AI review unavailable: ${e.message}. Start the included local_review_server.py and a compatible Ollama model. The offline rules-based reviewer remains fully functional.`};}
 const target=qs('#ai-result');if(target)target.innerHTML=localReviewHTML();if(btn){btn.disabled=false;btn.textContent='Request local model critique';}
}
function handReview(id){const input=qs(`[data-manual-input="${id}"]`);if(!input)return;
 const n=Number(input.value);if(input.value.trim()===''||!Number.isFinite(n)||n<0||n>100){fireNotice('Enter a teacher-reviewed score from 0 to 100.');return;}
 saved.manual[id]=Math.round(n);persist();const l=curLesson();const q=l?.questions.find(x=>`${state.lessonId}-${x.id}`===id);
 if(q){const holder=qs(`#feedback-${q.id}`);if(holder)holder.innerHTML=feedback(q,state.feedback[l.id]?.[q.id]);}
 fireNotice(`Human-reviewed score saved separately: ${Math.round(n)}%.`);
}
function onInput(e){const t=e.target;
 if(t.id==='filter-search'){state.search=t.value;const out=qs('#filtered-lessons');if(out)out.innerHTML=lessonGrid();return;}
 if(t.matches('[data-question]')&&t.type!=='radio'){saveAnswer(t.dataset.question,t.value);return;}
 const map={'paper-text':'text','paper-prompt':'prompt','paper-reference':'reference','paper-focus':'focus'};
 if(map[t.id]){saved.paper[map[t.id]]=t.value.slice(0,75000);if(t.id!=='paper-text')saved.paper.taskId='';persist();const c=qs('#paper-counter');if(c)c.textContent=`${wordCount(saved.paper.text)} words · saved in browser`;state.paperResult=null;state.localResult=null;const old=qs('#paper-result');if(old)old.innerHTML='';}
}
function onChange(e){const t=e.target;
 if(t.id==='paper-level'){state.level=t.value;delete saved.paper.taskId;saved.paper.lessonId='';state.paperResult=null;Promise.all([loadLevel(state.level),loadWritingTasks(state.level)]).then(()=>render()).catch(e=>fireNotice(e.message));return;}
 if(t.id==='paper-lesson'){saved.paper.lessonId=t.value;saved.paper.taskId='';persist();render();return;}
 if(t.id==='paper-task-choice'){saved.paper.taskId=t.value;persist();render();return;}
 if(t.id==='paper-mode'){saved.paper.mode=t.value==='page'?'page':'paragraph';persist();state.paperResult=null;render();return;}
 if(t.id==='filter-level'){state.level=t.value;state.strand='all';state.showAll=false;state.search='';loadLevel(state.level).then(render).catch(e=>fireNotice(e.message));return;}
 if(t.id==='filter-strand'){state.strand=t.value;state.showAll=false;const out=qs('#filtered-lessons');if(out)out.innerHTML=lessonGrid();return;}
 if(t.matches('input[data-question][type="radio"]')){saveAnswer(t.dataset.question,t.value);t.closest('.option-list')?.querySelectorAll('.option').forEach(n=>n.classList.toggle('selected',n.querySelector('input')?.checked));return;}
 if(t.matches('select[data-order]')){const id=t.dataset.order,p=Number(t.dataset.pos),arr=answerDraft()[id]||['','','',''];const newAnswer=Array.isArray(arr)?arr.slice():['','','',''];newAnswer[p]=t.value;saveAnswer(id,newAnswer);return;}
 if(t.id==='backup-file')importBackup(t.files?.[0]);
}
document.addEventListener('input',onInput);document.addEventListener('change',onChange);
document.addEventListener('click',e=>{const el=e.target.closest('[data-action]');if(!el)return;const cmd=el.dataset.action;
 if(cmd==='view')setView(el.dataset.view);
 else if(cmd==='level'){state.strand='all';state.showAll=false;state.search='';state.level=el.dataset.level;state.view='home';loadLevel(state.level).then(render).catch(e=>fireNotice(e.message));}
 else if(cmd==='lesson')openLesson(el.dataset.lesson);
 else if(cmd==='menu'){state.mobile=!state.mobile;qs('.atlas-sidebar')?.classList.toggle('sidebar-open',state.mobile);}
 else if(cmd==='show-more'){state.showAll=!state.showAll;qs('#filtered-lessons').innerHTML=lessonGrid();}
 else if(cmd==='check')checkOne(el.dataset.q);
 else if(cmd==='fix-question'){const id=el.dataset.q;const before=String(answerDraft()[id]||'');const f=G.proofread(before);if(!f.changed){fireNotice('No listed mechanical fixes were found. Review your sentences manually.');return;}if(confirm(`Apply ${f.count} mechanical spelling/spacing fixes? Please review the revised wording afterward.`)){saveAnswer(id,f.revised);render();const editor=qs(`[data-question="${id}"]`);if(editor)editor.focus();fireNotice(`${f.count} edits applied. Recheck and resubmit for a new score.`);}}
 else if(cmd==='grade')gradeAll();
 else if(cmd==='next')nextLesson();
 else if(cmd==='clear'){if(confirm('Clear unsent answers in this studio? Previous scores are preserved.')){delete saved.answers[state.lessonId];delete state.feedback[state.lessonId];persist();render();}}
 else if(cmd==='paper-grade')paperEvaluate();
 else if(cmd==='choose-paper-task')choosePaperTask();
 else if(cmd==='save-paper-human')savePaperHuman();
 else if(cmd==='apply-paper-fixes'){const f=G.proofread(saved.paper.text||'');if(!f.changed)return;if(confirm(`Apply ${f.count} proposed mechanical edits? This changes your saved draft.`)){saved.paper.text=f.revised;state.paperResult=null;state.localResult=null;persist();render();fireNotice(`${f.count} edits applied. Read your paper and analyze it again.`);}}
 else if(cmd==='clear-paper'){if(confirm('Clear the paper draft and sources?')){saved.paper=fresh().paper;state.paperResult=null;state.localResult=null;persist();render();}}
 else if(cmd==='download-paper')download('ATLAS_My_Essay.txt',saved.paper.text||'');
 else if(cmd==='ai-review')localAI();
 else if(cmd==='manual')handReview(el.dataset.manual);
 else if(cmd==='visual'){state.visualId=el.dataset.visual;state.visualStep=0;render();}
 else if(cmd==='visual-step'){state.visualStep=Math.max(0,Math.min(3,Number(el.dataset.step)));render();}
 else if(cmd==='visual-next'){state.visualStep=(state.visualStep+1)%4;render();}
 else if(cmd==='export')exportBackup();
 else if(cmd==='import')qs('#backup-file')?.click();
 else if(cmd==='print')window.print();
 else if(cmd==='read')readLesson();
 else if(cmd==='stop')stopSpeaking();
 else if(cmd==='theme'){saved.theme=saved.theme==='dark'?'light':'dark';persist();render();}
 else if(cmd==='font'){saved.font=saved.font>=1.35?.9:Math.round((saved.font+.09)*100)/100;persist();setAppearance();fireNotice('Reading font size changed.');}
 else if(cmd==='reset'){if(confirm('Erase all Studio grades, saved essay drafts and manual reviews in this browser? Export a backup first.')){Object.assign(saved,fresh());state.lastResults={};state.feedback={};persist();render();}}
});
document.addEventListener('keydown',e=>{
 if((e.ctrlKey||e.metaKey)&&e.key==='Enter'&&state.view==='lesson'){e.preventDefault();gradeAll();return;}
 if(e.key==='Enter'&&e.target.matches('input[data-question][type="text"]')){e.preventDefault();checkOne(e.target.dataset.question);}
 if(e.key==='Escape'&&state.mobile){state.mobile=false;qs('.atlas-sidebar')?.classList.remove('sidebar-open');}
});
const deep=decodeURIComponent(location.hash.replace(/^#studio-/,'').replace(/^#/,''));if(deep==='pathway-paper'){state.view='paper';Promise.all([loadLevel(state.level),loadWritingTasks(state.level)]).then(render).catch(e=>fireNotice(e.message));render();}else if(indexById.has(deep)){state.lessonId=deep;openLesson(deep);}else{loadLevel(state.level).then(()=>render()).catch(e=>host.textContent=e.message);render();}
window.addEventListener('beforeunload',stopSpeaking);
})();
