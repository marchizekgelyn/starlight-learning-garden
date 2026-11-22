#!/usr/bin/env node
/* ATLAS v3 validation utility: compares software results to externally provided human rubric ratings.
 * It does NOT create human labels, modify marks, send student writing over a network, or prove validity.
 * Usage: node tools/human_review_benchmark.js path/to/private_human_reviews.json
 * Input: { cases: [{ id, level, writing, assignment:{prompt,referenceText,expectedEvidence,concepts,minimumWords,taskType}, humanRatings:[70,75] }] }
 * Keep children's responses private: this utility only prints aggregate metrics, no drafts.
 */
'use strict';
const fs=require('node:fs'),A=require('../source/assessment_v3/engine');
const file=process.argv[2];if(!file){console.error('Usage: node tools/human_review_benchmark.js HUMAN_RATED_PAPERS.json');process.exit(2);}
let raw;try{raw=JSON.parse(fs.readFileSync(file,'utf8'));}catch(e){console.error('Unable to read JSON input:',e.message);process.exit(2);}
if(!Array.isArray(raw.cases)){console.error('Expected an object with cases array.');process.exit(2);}
const rows=[],bad=[];
for(const item of raw.cases.slice(0,10000)){
 const teachers=(item.humanRatings||[]).filter(x=>Number.isFinite(x)&&x>=0&&x<=100);
 if(!teachers.length||typeof item.writing!=='string'||typeof item.assignment!=='object')continue;
 if(!item.assignment.prompt||!item.assignment.referenceText){bad.push(String(item.id||'missing-id'));continue;}
 const teacher=teachers.reduce((a,b)=>a+b,0)/teachers.length;
 const result=A.assess(item.writing,{...item.assignment,level:item.level});if(!result.scoreEligible){bad.push(String(item.id||'missing-id'));continue;}
 rows.push({level:String(item.level||'unknown'),software:result.fraction*100,teacher,teachers,range:result.estimatedRange});
}
function avg(xs){return xs.length?xs.reduce((x,y)=>x+y,0)/xs.length:null;}
function report(sample){const residual=sample.map(x=>x.software-x.teacher),abs=residual.map(Math.abs);
 const coverage=sample.filter(x=>x.teacher>=x.range.low&&x.teacher<=x.range.high).length;
 return {samples:sample.length,meanAbsoluteError:avg(abs)===null?null:+avg(abs).toFixed(2),meanBias:avg(residual)===null?null:+avg(residual).toFixed(2),within10Percent:sample.length?+(100*abs.filter(x=>x<=10).length/sample.length).toFixed(2):null,
   humanScoreInsideEstimatedRangePercent:sample.length?+(100*coverage/sample.length).toFixed(2):null,
   twoRaterAgreementMAE:avg(sample.filter(x=>x.teachers.length>=2).map(x=>Math.abs(x.teachers[0]-x.teachers[1])))===null?null:+avg(sample.filter(x=>x.teachers.length>=2).map(x=>Math.abs(x.teachers[0]-x.teachers[1]))).toFixed(2)};
}
const grades=[...new Set(rows.map(r=>r.level))].sort();
const output={caseCountProvided:raw.cases.length,scorable:rows.length,excludedIds:bad.slice(0,20),aggregate:report(rows),byGrade:Object.fromEntries(grades.map(g=>[g,report(rows.filter(x=>x.level===g))])),
 disclaimer:'These statistics show agreement with the selected human scorers on this specific dataset. They do not establish accuracy, fairness, authorship, semantic validity, or external generalizability. Review human-rater agreement and grade-level sample sizes.'};
console.log(JSON.stringify(output,null,2));
if(rows.length<20)console.error('WARNING: fewer than 20 human-rated writing samples. Treat all statistics as exploratory.');
