/* Run: node tests/validate_v3.js
 * Structural and synthetic regression tests. Synthetic probes are NOT human-rated calibration data.
 */
'use strict';
const assert=require('node:assert/strict');const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const A=require('../source/assessment_v3/engine.js');const P=require('../source/assessment_v3/proofreading.js');const C=require('../source/assessment_v3/calibration.js');
const root=path.join(__dirname,'..','source');const grades=['pk','k',...Array.from({length:12},(_,i)=>String(i+1)),'c1','c2'];let taskCount=0,lessonCount=0,totalBytes=0,sampleRecords=[],ids=new Set(),cases=0;
for(const g of grades){const fname=path.join(root,'assessment_v3','tasks',`level_${g}.js`);const script=fs.readFileSync(fname,'utf8');totalBytes+=Buffer.byteLength(script);
 const context=vm.createContext({window:{}});vm.runInContext(script,context,{timeout:10000});const data=context.window.ATLAS_WRITING_TASKS[g.toUpperCase()]||context.window.ATLAS_WRITING_TASKS[g];assert(data,`No code for ${g}`);assert.equal(data.lessons.length,96);
 const lessonIds=new Set();for(const lesson of data.lessons){lessonCount++;assert(lesson.source.length>65);assert(!lessonIds.has(lesson.id));lessonIds.add(lesson.id);assert.equal(lesson.tasks.length,8);
 for(const task of lesson.tasks){taskCount++;assert(!ids.has(task.id),task.id);ids.add(task.id);assert(task.prompt.length>28);assert(task.checklist.length>=3);assert(task.parentReview.length>=3);assert(task.minimumWords>=5);assert(task.expectedEvidence.every(x=>typeof x==='string'&&x.length>=4));assert(task.concepts.length>=1);assert(task.sourceLabel&&task.successCriteria&&task.typicalPitfalls.length===2);}
 if(sampleRecords.length<25||lessonCount%24===0)sampleRecords.push(lesson);
 }
}
assert.equal(taskCount,12288);assert.equal(lessonCount,1536);assert(totalBytes>10*1024*1024,`New task source is only ${totalBytes} bytes`);
const sample=sampleRecords[0],task=sample.tasks[1],options={...task,referenceText:sample.source,type:'essay'};
const positive=`The most important observation is that ${task.expectedEvidence[0]}. This matters because it is a detail actually described in the reading. It helps explain the main point. I would check what happened next before drawing a larger conclusion.`;
const irrelevant='The dinosaurs fly across the moon. My family likes chocolate ice cream. The weather is sunny and orange. Every animal drives a new spaceship. None of this discusses the assigned story.';
const repeated=(`${task.expectedEvidence[0]} `).repeat(24);
const correct=A.assess(positive,options),wrong=A.assess(irrelevant,options),stuffed=A.assess(repeated,options);
assert(correct.fraction>wrong.fraction,`Relevant ${correct.fraction} not higher than irrelevant ${wrong.fraction}`);
assert(stuffed.fraction<.60,`Keyword stuffing scored too highly: ${stuffed.fraction}`);
assert(correct.scoreEligible);assert(!A.assess('The sky is blue.',{prompt:'Tell me about your experience',minimumWords:10}).scoreEligible);
assert(A.assess('',options).fraction<=.12);
assert(A.assess(positive,{...options,referenceText:''}).scoreEligible===false);
assert(A.assess(positive,{...options,expectedEvidence:[],concepts:[]}).scoreEligible===false);
assert(A.profile('PK').band==='emergent'&&A.profile('C2').band==='secondary');
assert(A.segmentSentences('Dr. Lee has 3.14 pies. She eats one!').length===2);
assert(A.mechanics('hello there. i am here',3).lowercase>=1);
assert(A.lexicalRedundancy(('bell boat red yellow ').repeat(40))>.3);
assert(A.sourceOverlap(sample.source,sample.source).share>.9);
assert(A.sourceOverlap('This is a short sentence.','').share===0);
const edited=P.proofread('i recieved teh letter and dont have time. The the word is is repeated.');
assert(edited.revised.includes('I received the letter'));assert(edited.revised.includes("don't"));assert(!edited.revised.includes('the the'));
assert.equal(P.proofread('The right to write is important. Their words may differ.').count,0);
assert.deepEqual(C.analyze([]).n,0);assert(C.analyze([{level:'3',teacher:80,machine:90},{level:'3',teacher:90,machine:80}],'3').mae===10);
for(const lesson of sampleRecords.slice(0,40))for(const t of lesson.tasks){const q={...t,referenceText:lesson.source};const text=`${t.expectedEvidence[0]}. The source offers this detail, and a reader must explain how it supports their claim. The writer should distinguish actual observations from an inference.`;const x=A.assess(text,q);cases++;assert(Number.isFinite(x.fraction)&&x.fraction>=0&&x.fraction<=1);assert(x.estimatedRange.low<=x.estimatedRange.high);assert.equal(x.criteria.length,6);assert(Math.abs(x.criteria.reduce((n,c)=>n+c.weight,0)-1)<.00001);assert.equal(x.reviewRequired,true);}
console.log(JSON.stringify({passed:true,lessons:lessonCount,newWritingAssignments:taskCount,generatedJavaScriptBytes:totalBytes,syntheticScoringProbes:cases,relevantEstimate:correct.fraction,irrelevantEstimate:wrong.fraction,stuffedEstimate:stuffed.fraction,notes:'These are software consistency tests, not validated human-grading accuracy.'},null,2));
