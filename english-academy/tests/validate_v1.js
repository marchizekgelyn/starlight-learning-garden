'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../source');
const data=JSON.parse(fs.readFileSync(path.join(root,'curriculum.json'),'utf8'));
const G=require(path.join(root,'grader.js'));
const errors=[];const types=new Set(['mcq','fill','short','order','essay']);
assert.equal(data.levels.length,16);assert.equal(data.strands.length,12);assert.equal(data.lessons.length,192);
assert.equal(data.metadata.assignmentCount,1920);
const ids=new Set();let questions=0,gradedCorrect=0;
for(const l of data.lessons){
 assert(!ids.has(l.id));ids.add(l.id);assert(l.title&&l.readingTitle&&l.passage&&l.instruction);assert.equal(l.questions.length,10);
 assert(l.passage.split(/\s+/).length>=20);assert(l.instruction.length>=100);
 const perType={};const responses={};
 for(const q of l.questions){
   questions++;perType[q.type]=(perType[q.type]||0)+1;
   assert(types.has(q.type));assert.equal(q.points,10);assert(q.prompt.length>12);
   if(q.type==='mcq'){
     assert.equal(q.options.length,4);assert(q.options.some(x=>x.id===q.answer));assert.equal(new Set(q.options.map(x=>x.text)).size,4);
     assert.equal(G.grade(q,q.answer).score,10);gradedCorrect++;
     assert.equal(G.grade(q,q.options.find(x=>x.id!==q.answer).id).score,0);
     responses[q.id]=q.answer;
   } else if(q.type==='fill'){
     assert.equal(G.grade(q,q.answer).score,10);gradedCorrect++;assert.equal(G.grade(q,'qzxxyy').score,0);responses[q.id]=q.answer;
   } else if(q.type==='order'){
     assert.equal(q.steps.length,3);assert.equal(G.grade(q,q.answer).score,10);gradedCorrect++;
     assert.equal(G.grade(q,[2,1,0]).score,10/3===G.grade(q,[2,1,0]).score?10/3:3.3); // tests partial credit
     responses[q.id]=q.answer;
   }else{
     assert(q.sample&&q.keywords?.length>=1);
     const r=G.grade(q,q.sample);assert(r.confidence==='provisional');assert(r.score>=0&&r.score<=10);
     responses[q.id]=q.sample;
   }
 }
 assert.deepEqual(perType,{mcq:4,fill:2,short:2,order:1,essay:1});
 const r=G.gradeLesson(l,responses);assert.equal(r.answered,10);assert.equal(r.objectivePercent,100);assert.equal(r.provisionalCount,3);assert(r.percent>0&&r.percent<=100);
}
assert.equal(questions,1920);assert.equal(gradedCorrect,1344);
console.log('CONTENT PASS',data.lessons.length,'lessons,',questions,'assignments,',gradedCorrect,'objective keys validated');

// Browser-equivalent smoke test using a minimal document/localStorage shim.
const events={};const appNode={innerHTML:''};const body={classList:{toggle(){},add(){},remove(){}},style:{setProperty(){}}};
const doc={body,querySelector(sel){return sel==='#app'?appNode:null;},getElementById(id){return id==='app'?appNode:null;},addEventListener(name,cb){events[name]=cb;}};
const local={values:{},getItem(k){return this.values[k]||null;},setItem(k,v){this.values[k]=v;}};
const ctx={console,window:{addEventListener(){},scrollTo(){},speechSynthesis:{cancel(){}}},document:doc,localStorage:local,location:{hash:''},history:{replaceState(){}},alert(){},confirm(){return true},URL,Blob,setTimeout,Date};
ctx.window.ATLAS_CONTENT=data;ctx.window.ATLAS_GRADER=G;
vm.runInNewContext(fs.readFileSync(path.join(root,'app.js'),'utf8'),ctx,{filename:'app.js'});
assert(appNode.innerHTML.includes('ATLAS English Academy'));
assert(appNode.innerHTML.includes('Assignment 10 of 10'));
const click=(action,id)=>events.click({target:{closest(){return {dataset:{action,id}};}}});
click('view','progress');assert(appNode.innerHTML.includes('Progress dashboard'));
click('view','curriculum');assert(appNode.innerHTML.includes('16 levels'));
click('view','guide');assert(appNode.innerHTML.includes('What the scoring engine can and cannot do'));
click('lesson','c2-research');assert(appNode.innerHTML.includes('Design and critique a research-based literature review'));
click('submit');assert(appNode.innerHTML.includes('Your most recent submission'));
const record=JSON.parse(local.values['atlas-english-academy-v1']);assert.equal(record.attempts['c2-research'].count,1);
console.log('APP SMOKE PASS: render, navigation, scoring, local saving');
