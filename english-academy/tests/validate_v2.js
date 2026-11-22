/* ATLAS V2 grading and browser-shell smoke tests — no packages needed. */
'use strict';
const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('assert');
const SRC=path.resolve(__dirname,'../source');
const G=require('../source/writing_engine.js');
const levels=JSON.parse(fs.readFileSync(path.join(SRC,'studio-data/manifest.json'),'utf8'));
assert.strictEqual(levels.lessonCount,1536);
let total=0;
for(const lev of levels.levels){
 const pack=JSON.parse(fs.readFileSync(path.join(SRC,`studio-data/level_${lev.id.toLowerCase()}.json`),'utf8'));
 for(const lesson of pack.lessons){
  const all={};for(const q of lesson.questions){
   // All objective reference answers must receive full credit.
   if(q.type==='mcq'||q.type==='fill'||q.type==='edit'||q.type==='order'){
    const mark=G.grade(q,q.answer);assert.strictEqual(mark.score,q.points,`${lesson.id}:${q.id} key failed`);
    assert.strictEqual(mark.kind,'objective');
    all[q.id]=q.answer;
    if(q.type==='mcq'){
      const other=q.options.find(x=>x.id!==q.answer);
      assert.strictEqual(G.grade(q,other.id).score,0,`${lesson.id}:${q.id} distractor credited`);
    }
   }else{
    const answer=G.grade(q,q.sample);
    assert.strictEqual(answer.kind,'writing');assert(answer.reviewRequired);
    assert(answer.report?.criteria.length===6,`${lesson.id}:${q.id} six analytic metrics`);
    assert(answer.score>=0&&answer.score<=q.points);
   }
   assert.strictEqual(G.grade(q,'').score,0);
   total++;
  }
  const scored=G.gradeLesson(lesson,all);
  assert(scored.objectivePercent===100 && scored.writingCount===0);
 }
}
assert.strictEqual(total,23040);
const exemplar={type:'essay',points:100,minimumWords:60,prompt:'Explain how the evidence supports the claim.',
   concepts:[{label:'evidence',terms:['evidence','detail']},{label:'connection',terms:['because','therefore']}],
   expectedEvidence:['the soil was wet and the prints pointed toward the gate'],
   referenceText:'The soil was wet and the prints pointed toward the gate. The student took a photograph.',
   sample:'The soil was wet and the prints pointed toward the gate. This is a clue, but we still do not know who made the prints.'};
const weak=G.grade(exemplar,'evidence because evidence because evidence because evidence because evidence because');
assert(weak.score<=34,'repeated keyword stuffing must not get a strong score');
const copy=G.grade(exemplar,(exemplar.referenceText+' ').repeat(8));
assert(copy.score<=34,'repeating the source material must be capped');
const strong=G.grade(exemplar,'The evidence offers a narrow basis for interpretation. The soil was wet and the prints pointed toward the gate. This detail matters because the direction of the marks can help reconstruct the movement. However, no identity is established from this limited information. I would compare the markings with a second observation and avoid a definitive conclusion without additional support and documented conditions.');
assert(strong.score>weak.score,`a thoughtful response should outperform stuffing (${strong.score}, ${weak.score})`);
const c=G.editMatch('The group tested the bridge.', 'The group tested the bridge.');assert(c.fraction===1);
assert(G.editMatch('the group tested the bridge','The group tested the bridge.').fraction<1);
console.log('PASS full grading matrix:',total,'items; objective keys, invalid distractors, essay report and guardrail tests');

// Tiny DOM shim: tests JS execution and navigation in environments where a real
// browser is prohibited by administrative network/file URL restrictions.
(async function(){
const events={},host={innerHTML:''},store={},ctx={console,Date,Math,JSON,Promise,setTimeout,clearTimeout,alert:()=>{},confirm:()=>true};
ctx.localStorage={getItem:k=>store[k]||null,setItem:(k,v)=>store[k]=v};
ctx.location={hash:''};ctx.window={addEventListener:()=>{},scrollTo:()=>{},location:ctx.location};
const doc={
 body:{dataset:{}},documentElement:{style:{setProperty:()=>{}}},
 getElementById:id=>id==='studio'?host:null,
 querySelector:()=>null,
 addEventListener:(type,handler)=>events[type]=handler,
 createElement:tag=>({tagName:tag.toUpperCase(),src:'',onload:null,onerror:null}),
 head:{appendChild:el=>{
  try{vm.runInContext(fs.readFileSync(path.join(SRC,el.src),'utf8'),context,{filename:el.src});queueMicrotask(()=>el.onload?.());}
  catch(e){queueMicrotask(()=>el.onerror?.());}
 }}
};ctx.document=doc;
ctx.speechSynthesis={cancel:()=>{}};ctx.window.speechSynthesis=ctx.speechSynthesis;
const context=vm.createContext(ctx);
for(const f of ['studio-data/manifest.js','assessment_v3/engine.js','assessment_v3/proofreading.js','assessment_v3/calibration.js','writing_engine.js','visuals.js','studio.js'])
 vm.runInContext(fs.readFileSync(path.join(SRC,f),'utf8'),context,{filename:f});
await new Promise(r=>setTimeout(r,90));
assert(host.innerHTML.includes('Choose a learning pathway')&&host.innerHTML.includes('lesson-tile'),'landing page not rendered');
function click(fields){const el={dataset:fields};events.click({target:{closest:()=>el}});}
click({action:'lesson',lesson:'PK-phonics-01'});await new Promise(r=>setTimeout(r,40));
assert(host.innerHTML.includes('question-q15')&&host.innerHTML.includes('The Bell and the Boat'),'lesson view not rendered');
click({action:'view',view:'visual'});assert(host.innerHTML.includes('Evidence chain'),'visual view not rendered');
click({action:'view',view:'paper'});assert(host.innerHTML.includes('paper-text'),'essay editor not rendered');
click({action:'view',view:'progress'});assert(host.innerHTML.includes('Curriculum coverage'),'analytics view not rendered');
click({action:'view',view:'guide'});assert(host.innerHTML.includes('Teacher assessment'),'guide view not rendered');
console.log('PASS simulated application execution: landing, lazy-loaded lesson, visual lab, paper lab, analytics and scoring guide');
})().catch(e=>{console.error(e);process.exitCode=1});
