/* ATLAS English Academy — standalone application, no external dependencies */
(function(){
  'use strict';
  const C=window.ATLAS_CONTENT,G=window.ATLAS_GRADER;
  const $=s=>document.querySelector(s);
  const escape=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  if(!C||!G){document.getElementById('app').innerHTML='<div class="boot">Curriculum failed to load. Make sure index.html, data.js, grader.js, and app.js are in the same folder.</div>';return;}
  const idSet=new Set(C.lessons.map(l=>l.id));
  const levelsById=Object.fromEntries(C.levels.map(l=>[l.id,l]));
  const strandsById=Object.fromEntries(C.strands.map(s=>[s.id,s]));
  const lessonsById=Object.fromEntries(C.lessons.map(l=>[l.id,l]));
  const storageKey='atlas-english-academy-v1';
  const fresh=()=>({schema:1,drafts:{},attempts:{},theme:'dark',size:1});
  function load(){try{const x=JSON.parse(localStorage.getItem(storageKey)||'null');if(x&&x.schema===1&&typeof x.drafts==='object'&&typeof x.attempts==='object')return {...fresh(),...x};}catch(e){}return fresh();}
  const saved=load();
  const state={view:'learn',lessonId:'pk-sounds',level:'PK',strand:'all',search:'',feedback:{},saved,sidebarOpen:false,storageProblem:false};
  const formatGrade=l=>levelsById[l]?.name||l;
  function save(){try{localStorage.setItem(storageKey,JSON.stringify(state.saved));state.storageProblem=false;}catch(e){state.storageProblem=true;}}
  function answers(){return state.saved.drafts[state.lessonId]||{};}
  function attempt(lid){return state.saved.attempts[lid]||null;}
  function lesson(){return lessonsById[state.lessonId];}
  function stats(){
    const all=Object.values(state.saved.attempts).filter(x=>x&&x.best!==undefined);
    const scored=all.map(x=>x.best);
    return {completed:all.length,answered:all.length*10,avg:scored.length?Math.round(scored.reduce((a,b)=>a+b,0)/scored.length):0,
      mastered:scored.filter(x=>x>=80).length,progress:Math.round(all.length/C.lessons.length*100)};
  }
  function lessonStatus(lid){const a=attempt(lid);return a?`<span class="done" aria-label="Completed">✓ ${a.best}% best</span>`:'Not started';}
  function filteredLessons(){
    return C.lessons.filter(l=>(state.level==='all'||l.level===state.level)&&(state.strand==='all'||l.strand===state.strand)
      &&(!state.search||[l.title,l.readingTitle,l.objective,l.level,strandsById[l.strand].name].join(' ').toLowerCase().includes(state.search.toLowerCase())));
  }
  function setTheme(){document.body.classList.toggle('light',state.saved.theme==='light');document.body.style.setProperty('--reader-size',`${(1.13*state.saved.size).toFixed(2)}rem`);}
  function sidebarHTML(){return `<aside class="sidebar ${state.sidebarOpen?'open':''}" id="sidebar" aria-label="Lesson navigation">
    <div class="brand"><div class="brand-top"><div class="brand-icon" aria-hidden="true">Aa</div><div><h1>ATLAS English Academy</h1><small>Preschool → College</small></div></div></div>
    <div class="side-controls">
      <label for="gradeSelect" class="field-label">Learning level</label><select class="field" id="gradeSelect"><option value="all" ${state.level==='all'?'selected':''}>All 16 learning levels</option>${C.levels.map(l=>`<option value="${escape(l.id)}" ${state.level===l.id?'selected':''}>${escape(l.name)}</option>`).join('')}</select>
      <div class="filter-mini"><label for="strandSelect" class="field-label">English subject</label><select class="field" id="strandSelect"><option value="all">All 12 strands</option>${C.strands.map(s=>`<option value="${s.id}" ${state.strand===s.id?'selected':''}>${escape(s.name)}</option>`).join('')}</select></div>
      <div class="filter-mini"><label for="lessonSearch" class="field-label">Find lessons</label><div class="search-wrap"><span class="search-glyph" aria-hidden="true">⌕</span><input class="field" id="lessonSearch" placeholder="Search concepts, topics…" value="${escape(state.search)}"></div></div>
    </div><div id="sidebarLessonResults">${sidebarListHTML()}</div>
    <div class="sidebar-bottom">192 lessons · 1,920 exercises · Offline-ready<br>Responses stored on this device unless exported.</div></aside>`;}
  function sidebarListHTML(){
    const filtered=filteredLessons();return `<div class="lesson-counter">${filtered.length} lesson${filtered.length!==1?'s':''} available</div><div class="lesson-list" aria-label="Filtered lesson list">${filtered.length?filtered.map(l=>`<button class="lesson-link ${l.id===state.lessonId?'active':''}" data-action="lesson" data-id="${l.id}" ${l.id===state.lessonId?'aria-current="page"':''}>
     <span class="lesson-number">${String(l.index).padStart(2,'0')}</span><span><strong>${escape(l.title)}</strong><small>${escape(formatGrade(l.level))} · ${escape(strandsById[l.strand].name)} · ${lessonStatus(l.id)}</small></span></button>`).join(''):'<div class="empty">No matching lessons. Try another level or search term.</div>'}</div>`;
  }
  function headerHTML(){return `<header class="topbar"><button class="button mobile-menu" data-action="mobile" aria-label="Open lesson menu">☰ Lessons</button>
     <nav class="tabs" aria-label="Main sections">${[['learn','Learn'],['progress','My progress'],['curriculum','Curriculum'],['guide','How scoring works']].map(([v,t])=>`<button class="tab ${state.view===v?'active':''}" data-action="view" data-id="${v}" ${state.view===v?'aria-current="page"':''}>${t}</button>`).join('')}</nav>
     <div class="top-actions"><button class="button subtle" data-action="font" title="Adjust reading text size">A±</button><button class="button subtle" data-action="theme" title="Toggle light/dark theme">${state.saved.theme==='light'?'☾ Dark':'☀ Light'}</button><button class="button" data-action="export" title="Download your progress as JSON">⇩ Export</button><a class="button subtle" href="index.html" title="Open the expanded version 2.0 learning studio">↗ Studio 2.0</a><button class="button subtle" data-action="import" title="Import previously exported progress">⇧ Import</button><input type="file" accept="application/json,.json" id="importPicker" style="display:none" aria-label="Import saved progress"></div></header>`;}
  function statsHTML(){const s=stats();return `<div class="summary-grid" aria-label="Learning statistics"><div class="stat"><div class="value">${s.completed}<span class="muted"> / 192</span></div><label>Lessons attempted</label></div><div class="stat"><div class="value">${s.mastered}</div><label>Scores of 80% or higher</label></div><div class="stat"><div class="value">${s.avg}%</div><label>Average best score</label></div><div class="stat"><div class="value">${s.progress}%</div><label>Course explored</label></div></div>`;}
  const typeLabel={mcq:'Select one',fill:'Type the word',short:'Short response',order:'Put in order',essay:'Extended writing'};
  function controlHTML(q,a){
    if(q.type==='mcq')return `<div class="choices">${q.options.map(o=>`<label class="choice"><input type="radio" name="response-${q.id}" value="${escape(o.id)}" data-q="${q.id}" ${a===o.id?'checked':''}><span>${escape(o.text)}</span></label>`).join('')}</div>`;
    if(q.type==='fill')return `<input class="field" data-q="${q.id}" type="text" value="${escape(a||'')}" autocomplete="off" spellcheck="true" placeholder="Type your answer and press Enter to check">`;
    if(q.type==='short')return `<textarea class="field" data-q="${q.id}" placeholder="Write an explanation using details from the reading…" rows="4">${escape(a||'')}</textarea><div class="subhint">Suggested length: ${q.minimumWords} words. Feedback is an approximate keyword-based estimate.</div>`;
    if(q.type==='essay')return `<textarea class="field essay" data-q="${q.id}" placeholder="Develop your response here. Include a claim, evidence, reasoning, and limitations where appropriate." rows="9">${escape(a||'')}</textarea><div class="subhint">Target: ${q.minimumWords} words · <span class="word-counter" id="words-${q.id}">${G.tokens(a||'').length} words drafted</span></div>`;
    if(q.type==='order')return `<div class="order-list">${[0,1,2].map(pos=>`<div class="order-row"><b>${pos+1}.</b><select class="field" data-order="${q.id}" data-pos="${pos}" aria-label="Step ${pos+1}"><option value="">Choose an event…</option>${[2,0,1].map(k=>`<option value="${k}" ${Array.isArray(a)&&String(a[pos])===String(k)?'selected':''}>${escape(q.steps[k])}</option>`).join('')}</select></div>`).join('')}</div><div class="subhint">Select each event once, from first to last.</div>`;
    return '';
  }
  function feedbackHTML(q,result){if(!result)return '';
    const good=result.score===result.max;
    return `<strong>${result.score}/${result.max} points · ${escape(result.message)}</strong>${result.confidence==='provisional'?'<small>Provisional result — teacher or self-review recommended.</small>':''}
      <ul>${(result.details||[]).map(x=>`<li>${escape(x)}</li>`).join('')}</ul><small>${escape(q.explanation||'')}</small>`;
  }
  function quizHTML(l){const a=answers();const fb=state.feedback[l.id]||{};
    return l.questions.map((q,index)=>{const r=fb[q.id];return `<article class="question-card" id="card-${q.id}"><div class="question-top"><span class="question-number">Assignment ${index+1} of 10</span><span class="question-type">${typeLabel[q.type]} · ${q.points} pts</span></div>
      <h4>${escape(q.prompt)}</h4><div class="answer-zone">${controlHTML(q,a[q.id])}</div><div class="question-foot"><span class="word-counter">${q.type==='essay'?'Writing rubric applies':q.type==='short'?'Partial-credit rubric applies':q.type==='fill'?'Enter ↵ to check':'Practice and review'}</span><button class="button" data-action="check" data-q="${q.id}">Check answer</button></div>
      <div class="feedback ${r?'visible':''} ${r&&r.score===r.max?'good':r?'needs':''}" id="feedback-${q.id}" role="status">${r?feedbackHTML(q,r):''}</div></article>`;}).join('');
  }
  function resultHTML(l){const a=attempt(l.id);if(!a)return '';
    const r=a.lastResult;return `<section class="results" id="lessonResults" aria-label="Latest lesson grade"><h3>Your most recent submission</h3><div class="score">${r.percent}% <span style="font-size:1rem;color:var(--muted)">(${r.score}/${r.max} points)</span></div>
      <p><strong>${r.answered}/10</strong> assignments answered · Objective questions: <strong>${r.objectivePercent}%</strong> · Personal best: <strong>${a.best}%</strong> · Attempts: <strong>${a.count}</strong></p>
      <div class="progress-track" aria-label="Lesson grade ${r.percent}%"><span style="width:${r.percent}%"></span></div>
      <p>${r.provisionalCount} written responses used heuristic scoring. This overall percentage is an instructional estimate, not a validated exam grade.</p></section>`;}
  function readerHTML(l){return `<section class="panel" id="reading"><div class="panel-head"><h3>Original reading · ${escape(l.readingTitle)}</h3><div><button class="button" data-action="read" aria-label="Read passage aloud">🔊 Listen</button> <button class="button" data-action="stop" aria-label="Stop narration">■ Stop</button></div></div>
     <div class="panel-body"><p class="reader">${escape(l.passage)}</p><div class="glossary"><h4>Vocabulary in context</h4>${l.glossary.map(t=>`<div class="term-card"><b>${escape(t.term)}</b> <span>— ${escape(t.definition)}</span></div>`).join('')}</div></div></section>`;}
  function learnHTML(){const l=lesson();const st=strandsById[l.strand],rec=attempt(l.id);
    return `<div class="hero"><div class="eyebrow">${escape(formatGrade(l.level))} / ${escape(st.name)}</div><h2>${escape(l.title)}</h2><p>${escape(l.objective)}</p><div class="chips"><span class="chip">${escape(st.icon)} ${escape(st.name)}</span><span class="chip">◷ ${l.estimatedMinutes} minute lesson</span><span class="chip">10 assignments · 100 points</span>${rec?`<span class="chip">✓ Best ${rec.best}%</span>`:''}</div></div>
      ${statsHTML()}<div class="lesson-grid"><div>
      <section class="panel"><div class="panel-head"><h3>Learn the skill</h3><button class="button" data-action="print">▤ Print worksheet</button></div><div class="panel-body"><p class="instruction">${escape(l.instruction)}</p><h4>How to complete this lesson</h4><ol class="lesson-steps">${l.steps.map(x=>`<li>${escape(x)}</li>`).join('')}</ol></div></section>
      ${readerHTML(l)}<section class="panel"><div class="panel-head"><h3>Mastery checklist</h3></div><div class="panel-body"><div class="muted">The final grade counts 4 multiple-choice, 2 fill-in-the-blank, 2 short responses, 1 sequence, and 1 extended written response. Answers save automatically in this browser.</div><div class="notice">Short responses and essays receive only an <strong>approximate automated score</strong> based on terms, length, and structure. They require human review for a reliable evaluation of meaning, quality, and accuracy.</div></div></section></div>
      <div class="quiz-col"><h3 class="section-title" id="practice">Practice & assignments</h3>${resultHTML(l)}${quizHTML(l)}
      <div class="submit-panel"><div><strong>Ready for your score?</strong><div class="muted">You may leave answers blank, revise, and submit again. Press Ctrl+Enter to submit.</div></div><div style="display:flex;gap:8px;flex-wrap:wrap"><button class="button" data-action="clear">Clear draft</button><button class="button primary" data-action="submit">✓ Submit all & score</button><button class="button" data-action="next">Next lesson →</button></div></div></div></div>`;
  }
  function progressHTML(){const s=stats();const rows=Object.entries(state.saved.attempts).filter(([id,x])=>idSet.has(id)&&x&&x.lastResult).sort((a,b)=>String(b[1].at).localeCompare(String(a[1].at)));
    const bar=(label,ids)=>{const vals=ids.map(id=>attempt(id)).filter(Boolean);const avg=vals.length?Math.round(vals.reduce((x,y)=>x+y.best,0)/vals.length):0;return `<div class="line-item"><b>${escape(label)}</b><div class="progress-track" title="${avg}% average best grade"><span style="width:${avg}%"></span></div><small>${vals.length}/${ids.length}</small></div>`;};
    return `<div class="hero"><div class="eyebrow">Your learning record</div><h2>Progress dashboard</h2><p>Track performance, review completed lessons, and revisit any topic. Your scores remain in this browser until exported or cleared.</p></div>${statsHTML()}
      <div class="dashboard-grid"><section class="dash-card"><h3>By learning level</h3>${C.levels.map(l=>bar(l.name,C.lessons.filter(x=>x.level===l.id).map(x=>x.id))).join('')}</section>
      <section class="dash-card"><h3>By subject strand</h3>${C.strands.map(t=>bar(t.name.split('&')[0].trim(),C.lessons.filter(x=>x.strand===t.id).map(x=>x.id))).join('')}</section></div>
      <section class="guide-section" style="max-width:none;margin-top:20px"><h3>Recent submissions</h3>${rows.length?`<div class="table-wrap"><table class="scores-table"><thead><tr><th>Lesson</th><th>Level</th><th>Last grade</th><th>Best</th><th>Attempts</th><th>Last submitted</th></tr></thead><tbody>${rows.slice(0,60).map(([id,a])=>`<tr><td><button data-action="lesson" data-id="${id}">${escape(lessonsById[id].title)}</button></td><td>${escape(formatGrade(lessonsById[id].level))}</td><td>${a.lastResult.percent}%</td><td>${a.best}%</td><td>${a.count}</td><td>${escape(new Date(a.at).toLocaleDateString())}</td></tr>`).join('')}</tbody></table></div>`:'<p class="muted">No submissions yet. Open any lesson, type your responses, and press “Submit all & score.”</p>'}</section>
      <div class="submit-panel"><div><strong>Manage your local learning record</strong><div class="muted">Export a backup before resetting. Imports merge only after validation.</div></div><div style="display:flex;gap:8px"><button class="button" data-action="export">Export JSON</button><button class="button danger" data-action="reset">Reset all scores</button></div></div>`;}
  function curriculumHTML(){return `<div class="hero"><div class="eyebrow">Complete course map</div><h2>16 levels · 12 subjects · 192 lessons</h2><p>A structured progression from sounds and decoding to argument, research synthesis, literary criticism, and advanced academic writing. Choose any level or subject to jump into the curriculum.</p></div>
    <h3 class="section-title">Learning levels</h3><div class="level-rows">${C.levels.map(l=>`<button class="level-tile" data-action="level" data-id="${l.id}"><strong>${escape(l.name)}</strong><small>${escape(l.stage)} · 12 lessons · ${C.lessons.filter(x=>x.level===l.id&&attempt(x.id)).length} attempted</small></button>`).join('')}</div>
    <h3 class="section-title" style="margin-top:30px">The 12 subject strands</h3><div class="curriculum-grid">${C.strands.map(t=>`<section class="curr-card"><h3>${escape(t.icon)} ${escape(t.name)}</h3><p>${escape(t.description)}</p><button data-action="strand" data-id="${t.id}">Explore 16 lessons</button></section>`).join('')}</div>`;}
  function guideHTML(){return `<div class="hero"><div class="eyebrow">Using the platform</div><h2>How to answer, score, and improve</h2><p>ATLAS provides offline reading instruction, automatic checking for objective items, explainable provisional feedback for written responses, and private local progress tracking.</p></div>
    <section class="guide-section"><h3>How to complete a lesson</h3><ol><li>Select a grade and a topic in the lesson menu.</li><li>Read the instruction and original passage. Choose “Listen” for browser text-to-speech where supported.</li><li>Select a multiple-choice response or type into the response fields. For the sequence exercise, put the three events in order.</li><li>Select “Check answer” to see a score and an explanation. In single-line fill-in answers, press Enter to check.</li><li>Select “Submit all & score” to calculate the overall lesson score. Ctrl+Enter also submits.</li><li>Review explanations, revise your answers, and resubmit. Your highest percentage is retained.</li></ol></section>
    <section class="guide-section"><h3>What the scoring engine can and cannot do</h3><p><strong>Objective:</strong> Four multiple-choice answers, two fill-ins, and one ordering question receive deterministic marking. Spelling answers allow known alternatives, with limited typo partial credit. Ordering awards partial credit by correct position when each step is used once.</p><p><strong>Provisional:</strong> Two short answers and one extended response are evaluated by explicitly listed checks such as reference keywords, suggested length, transitions, and punctuation. This is a heuristic <strong>not</strong> a language model, reliable semantic comparison, plagiarism detector, or teacher replacement. Creative but correct wording can receive an unfairly low score; irrelevant text containing the target words can receive undeserved credit.</p><p><strong>Review:</strong> Compare your work with the sample and explanation, ask a teacher or knowledgeable reader to review writing quality, and use the score as formative feedback rather than a formal credential.</p></section>
    <section class="guide-section"><h3>Reading and grade-level support</h3><p>Preschool activities are designed for shared reading, with adult assistance for typed or dictated responses. Older levels progress through vocabulary, sentence structures, evidence, writing, rhetoric, source evaluation, and academic analysis. Placement is flexible: learners may start in any grade and revisit earlier lessons.</p><p>Spoken presentation skill objectives are practiced through typed planning/reflection and optional read-aloud. This version does not record, transcribe, or assess actual live speech. It also does not contain copyrighted commercial textbooks or claim formal standards certification.</p></section>
    <section class="guide-section"><h3>Privacy and offline operation</h3><p>All lesson content and scoring rules are packaged locally. Responses and grades are saved in browser localStorage, and no student submissions are sent to a server. Clearing browser data may erase scores. Export JSON periodically to make a backup. The app can run by double-clicking <code>index.html</code> after extracting the complete ZIP.</p></section>
    <section class="guide-section"><h3>Curriculum design references</h3><p>The progression is informed by publicly accessible literacy and writing guidance, not presented as a verbatim reproduction or an official endorsement.</p><ul>${C.sources.map(s=>`<li><a href="${escape(s.url)}" rel="noopener noreferrer" target="_blank">${escape(s.title)}</a></li>`).join('')}</ul></section>`;}
  function render(){setTheme();$('#app').innerHTML=`<div class="app-shell">${sidebarHTML()}<main class="app-main">${headerHTML()}<div class="body-content">${state.storageProblem?'<p class="notice">Your browser blocked local storage. Export your answers before leaving; they might not persist.</p>':''}${state.view==='learn'?learnHTML():state.view==='progress'?progressHTML():state.view==='curriculum'?curriculumHTML():guideHTML()}</div></main></div>`;}
  function openLesson(id){if(!idSet.has(id))return;state.lessonId=id;state.level=lessonsById[id].level;state.strand='all';state.view='learn';state.sidebarOpen=false;state.search='';try{history.replaceState(null,'','#'+encodeURIComponent(id));}catch(e){}speechCancel();render();window.scrollTo(0,0);}
  function gradeOne(qid){const q=lesson().questions.find(x=>x.id===qid);if(!q)return;const result=G.grade(q,answers()[qid]);
    if(!state.feedback[state.lessonId])state.feedback[state.lessonId]={};state.feedback[state.lessonId][qid]=result;
    const el=$(`#feedback-${qid}`);if(el){el.innerHTML=feedbackHTML(q,result);el.className=`feedback visible ${result.score===result.max?'good':'needs'}`;}
  }
  function gradeAll(){const l=lesson();const a=answers();const r=G.gradeLesson(l,a);state.feedback[l.id]=Object.fromEntries(r.items.map(x=>[x.id,x]));
    const old=attempt(l.id);state.saved.attempts[l.id]={count:(old?.count||0)+1,best:Math.max(old?.best||0,r.percent),lastResult:r,at:r.gradedAt};
    save();render();const result=document.getElementById('lessonResults');if(result)result.scrollIntoView({behavior:'smooth',block:'start'});
  }
  function saveResponse(qid,value){if(!state.saved.drafts[state.lessonId])state.saved.drafts[state.lessonId]={};state.saved.drafts[state.lessonId][qid]=value;
    if(state.feedback[state.lessonId]&&state.feedback[state.lessonId][qid]){delete state.feedback[state.lessonId][qid];const feedback=$(`#feedback-${qid}`);if(feedback){feedback.className='feedback';feedback.innerHTML='';}}
    save();const count=$(`#words-${qid}`);if(count)count.textContent=G.tokens(value).length+' words drafted';
  }
  function speechCancel(){if('speechSynthesis' in window){try{window.speechSynthesis.cancel();}catch(e){}}}
  function speak(){if(!('speechSynthesis' in window)){alert('Speech synthesis is not available in this browser.');return;}
    speechCancel();const u=new SpeechSynthesisUtterance(lesson().passage);u.lang='en-US';u.rate=['PK','K','1','2'].includes(lesson().level)?0.84:0.96;window.speechSynthesis.speak(u);
  }
  function download(filename,contents){const blob=new Blob([contents],{type:'application/json;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);}
  function exportProgress(){const file={kind:'ATLAS_English_Academy_Progress',version:1,exportedAt:new Date().toISOString(),data:state.saved};download('ATLAS_English_Academy_Progress.json',JSON.stringify(file,null,2));}
  async function importProgress(file){if(!file||file.size>10_000_000){alert('Choose a JSON file smaller than 10 MB.');return;}try{
    const data=JSON.parse(await file.text());if(data.kind!=='ATLAS_English_Academy_Progress'||data.version!==1||!data.data||typeof data.data!=='object')throw new Error('Unrecognized ATLAS backup format');
    const imp=data.data;if(!imp.drafts||!imp.attempts||typeof imp.drafts!=='object'||typeof imp.attempts!=='object')throw new Error('Invalid progress structure');
    let count=0;for(const [id,a] of Object.entries(imp.drafts)){if(!idSet.has(id)||!a||typeof a!=='object')continue;const allowed=new Set(lessonsById[id].questions.map(q=>q.id));
      const clean={};for(const [qid,x] of Object.entries(a)){if(!allowed.has(qid))continue;if(typeof x==='string')clean[qid]=x.slice(0,50000);else if(Array.isArray(x)&&x.length===3)clean[qid]=x.map(v=>String(v).slice(0,3));}
      state.saved.drafts[id]=clean;count++;
    }
    for(const [id,x] of Object.entries(imp.attempts)){if(!idSet.has(id)||!x||typeof x!=='object'||!x.lastResult)continue;if(!Number.isFinite(x.best)||!Number.isFinite(x.count)||!Number.isFinite(x.lastResult.percent))continue;
      const v=x.lastResult;const bounded=(n,max=100)=>Math.max(0,Math.min(max,Number.isFinite(Number(n))?Number(n):0));
      const safeResult={score:bounded(v.score),max:100,percent:bounded(v.percent),objectivePercent:bounded(v.objectivePercent),provisionalCount:bounded(v.provisionalCount,3),answered:bounded(v.answered,10),gradedAt:String(v.gradedAt||'').slice(0,40),items:[]};
      state.saved.attempts[id]={best:bounded(x.best),count:Math.max(1,Math.min(10000,Math.round(x.count))),lastResult:safeResult,at:String(x.at||'').slice(0,40)};
    }
    save();render();alert(`Imported available responses from ${count} lessons. Existing scores were updated for matching lesson IDs.`);
  }catch(e){alert('Import failed: '+e.message);}}
  document.addEventListener('input',e=>{
    const t=e.target;
    if(t.id==='lessonSearch'){state.search=t.value;const el=$('#sidebarLessonResults');if(el)el.innerHTML=sidebarListHTML();return;}
    if(t.matches('[data-q]')&&t.type!=='radio')saveResponse(t.dataset.q,t.value);
  });
  document.addEventListener('change',e=>{
    const t=e.target;
    if(t.id==='gradeSelect'){state.level=t.value;state.strand='all';state.search='';state.view='learn';const first=filteredLessons()[0];if(first)state.lessonId=first.id;render();return;}
    if(t.id==='strandSelect'){state.strand=t.value;state.search='';state.view='learn';const first=filteredLessons()[0];if(first)state.lessonId=first.id;render();return;}
    if(t.matches('[data-q]')&&t.type==='radio')saveResponse(t.dataset.q,t.value);
    if(t.matches('[data-order]')){const id=t.dataset.order,pos=Number(t.dataset.pos);const a=answers()[id]||['','',''];const next=Array.isArray(a)?a.slice():['','',''];next[pos]=t.value;saveResponse(id,next);}
    if(t.id==='importPicker')importProgress(t.files?.[0]);
  });
  document.addEventListener('click',e=>{
    const target=e.target.closest('[data-action]');if(!target)return;const action=target.dataset.action,id=target.dataset.id;
    if(action==='lesson')openLesson(id);
    else if(action==='view'){state.view=id;state.sidebarOpen=false;render();window.scrollTo(0,0);}
    else if(action==='level'){state.level=id;state.strand='all';openLesson(C.lessons.find(l=>l.level===id)?.id);}
    else if(action==='strand'){state.strand=id;state.level='all';const first=C.lessons.find(l=>l.strand===id);if(first){state.lessonId=first.id;state.view='learn';state.sidebarOpen=false;render();window.scrollTo(0,0);}}
    else if(action==='check')gradeOne(target.dataset.q);
    else if(action==='submit')gradeAll();
    else if(action==='next'){const idx=C.lessons.findIndex(x=>x.id===state.lessonId);openLesson(C.lessons[(idx+1)%C.lessons.length].id);}
    else if(action==='clear'){if(confirm('Clear the draft answers for this lesson? Saved grade history will remain.')){delete state.saved.drafts[state.lessonId];delete state.feedback[state.lessonId];save();render();}}
    else if(action==='reset'){if(confirm('Permanently reset all saved grades and draft responses from this browser? Export a backup first if needed.')){state.saved.drafts={};state.saved.attempts={};state.feedback={};save();render();}}
    else if(action==='export')exportProgress();
    else if(action==='import')$('#importPicker')?.click();
    else if(action==='read')speak();
    else if(action==='stop')speechCancel();
    else if(action==='print')window.print();
    else if(action==='theme'){state.saved.theme=state.saved.theme==='dark'?'light':'dark';save();render();}
    else if(action==='font'){state.saved.size=state.saved.size>=1.4?.9:Math.round((state.saved.size+.1)*10)/10;save();setTheme();}
    else if(action==='mobile'){state.sidebarOpen=!state.sidebarOpen;$('#sidebar')?.classList.toggle('open',state.sidebarOpen);}
  });
  document.addEventListener('keydown',e=>{
    if((e.ctrlKey||e.metaKey)&&e.key==='Enter'&&state.view==='learn'){e.preventDefault();gradeAll();return;}
    if(e.key==='Enter'&&e.target.matches('input[data-q][type="text"]')){e.preventDefault();gradeOne(e.target.dataset.q);}
    if(e.key==='Escape'&&state.sidebarOpen){state.sidebarOpen=false;$('#sidebar')?.classList.remove('open');}
  });
  const hash=decodeURIComponent(location.hash.slice(1));if(idSet.has(hash)){state.lessonId=hash;state.level=lessonsById[hash].level;}
  setTheme();render();
  window.addEventListener('beforeunload',speechCancel);
})();
