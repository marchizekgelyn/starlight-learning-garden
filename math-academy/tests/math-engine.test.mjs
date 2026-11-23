import test from 'node:test';
import assert from 'node:assert/strict';
import {calculate,Complex,parse,evaluateAst,fmt,descriptiveStats,matrixOp,matrixDet,matrixRref,solveQuadratic} from '../js/math-engine.js';
import {derivative,antiderivative,definiteIntegral,numericLimit,numericalDerivative,rootFind,summation,taylor} from '../js/calculus.js';
import {CURRICULUM,ALL_LESSONS} from '../js/curriculum.js';
import {FORMULAS,convertUnit,generateProblem,checkAnswer} from '../js/reference.js';
function near(actual,expected,eps=1e-7){assert.ok(Math.abs(actual-expected)<=eps*Math.max(1,Math.abs(expected)),`${actual} ≈ ${expected}`);}
test('curriculum completeness, identity and self-contained examples',()=>{
 assert.equal(CURRICULUM.length,14);assert.ok(ALL_LESSONS.length>=140,`lessons=${ALL_LESSONS.length}`);
 assert.equal(new Set(ALL_LESSONS.map(x=>x.id)).size,ALL_LESSONS.length);
 for(const l of ALL_LESSONS){for(const k of ['title','idea','example','question','answer','hint'])assert.ok(l[k],`${l.grade}/${l.title}:${k}`);assert.ok(l.steps.length>=2);}
 assert.ok(FORMULAS.length>=85);
});
test('arithmetic precedence, factorial, percentages and implicit multiplication',()=>{
 assert.equal(calculate('3+4*5'),23);assert.equal(calculate('(3+4)*5'),35);assert.equal(calculate('2^3^2'),512);assert.equal(calculate('-2^2'),-4);assert.equal(calculate('(-2)^2'),4);assert.equal(calculate('5!'),120);assert.equal(calculate('25%'),0.25);near(calculate('2pi'),2*Math.PI);assert.equal(calculate('2(3+4)'),14);assert.equal(calculate('(2+3)(4+1)'),25);assert.equal(calculate('18 mod 7'),4);near(calculate('1/1e-14'),1e14);
});
test('functions and angles',()=>{near(calculate('sin(pi/6)'),0.5);near(calculate('sin(30)',{angleMode:'DEG'}),0.5);near(calculate('asin(0.5)',{angleMode:'DEG'}),30);near(calculate('cos(pi)'),-1);near(calculate('log(32,2)'),5);near(calculate('ln(exp(4))'),4);near(calculate('nCr(10,3)'),120);near(calculate('nPr(6,2)'),30);near(calculate('gcd(54,24)'),6);near(calculate('lcm(6,8)'),24);near(calculate('avg(2,4,6)'),4);near(calculate('root(27,3)'),3);near(calculate('sqrt(25)'),5);});
test('complex evaluation',()=>{const r=calculate('sqrt(-16)');assert.ok(r instanceof Complex);near(r.re,0);near(r.im,4);near(calculate('i^2'),-1);near(calculate('exp(i*pi)'),-1);near(calculate('exp(i*pi/2)').im,1);});
test('malformed expression rejected without JS execution',()=>{for(const s of ['window.alert(1)','eval(1)','4+','2**3','1/0','sine(2)','2+foo','x+3','3..4'])assert.throws(()=>calculate(s),undefined,s);});
test('symbolic calculus',()=>{const d=derivative('x^3 + 2*x',2);near(d.value,14);near(calculate(d.expression,{vars:{x:3}}),29);near(derivative('sin(x)',0).value,1);near(derivative('ln(x)',Math.E).value,1/Math.E);near(derivative('(x^2+1)/x',2).value,.75);assert.match(antiderivative('3*x^2 + 4*x - 7').expression,/C$/);assert.throws(()=>derivative('sin(x)',1,'DEG'));});
test('numerical calculus',()=>{near(definiteIntegral('x^2',0,3),9);near(definiteIntegral('sin(x)',0,Math.PI),2);near(definiteIntegral('2*x',0,4),16);near(numericalDerivative('sin(x)',0),1);near(numericLimit('(x^2-4)/(x-2)',2).value,4,0.001);assert.equal(numericLimit('1/x',0).value,null);assert.equal(numericLimit('1/x^2',0).value,Infinity);near(summation('n^2',1,10),385);near(summation('n',1,4,'product'),24);assert.deepEqual(rootFind('x^2-4',-5,5).map(x=>Math.round(x)),[-2,2]);near(taylor('exp(x)',0,3).terms.at(-1).coef,1/6);});
test('matrices and descriptive statistics',()=>{assert.equal(matrixDet([[1,2],[3,4]]),-2);assert.deepEqual(matrixOp('1,2;3,4','2,0;1,2','multiply'),[[4,4],[10,8]]);assert.deepEqual(matrixOp('1,2;3,4','2,0;1,2','add'),[[3,2],[4,6]]);const inv=matrixOp('1,2;3,4',null,'inverse');near(inv[0][0],-2);near(inv[1][1],-.5);const s=descriptiveStats('2,4,4,4,5,5,7,9');near(s.mean,5);near(s.median,4.5);near(s.populationSD,2);assert.deepEqual(s.modes,[4]);const q=solveQuadratic(1,-5,6);assert.deepEqual(q.roots,[3,2]);});
test('units and grading',()=>{near(convertUnit(100,'length','cm','m'),1);near(convertUnit(32,'temperature','°F','°C'),0);near(convertUnit(100,'temperature','°C','K'),373.15);assert.equal(checkAnswer('1/2','0.5'),true);assert.equal(checkAnswer('2/3','0.7'),false);for(let level=0;level<14;level++){for(let i=0;i<20;i++){const p=generateProblem(level);assert.ok(p.prompt&&p.steps.length);assert.equal(checkAnswer(p.answer,p.answer),true);}}});
