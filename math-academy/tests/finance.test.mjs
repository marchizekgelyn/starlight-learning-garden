import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,statSync} from 'node:fs';
import {simpleInterest,compoundInterest,continuousInterest,effectiveAnnualRate,paymentAmount,amortizeLoan,futureValueSavings,savingsGoal,inflation,investmentReturn,debtPayoff,npv,irr,investmentGrowthSeries,FINANCE_METHODS,runFinanceMethod} from '../js/finance.js';
import {calculate} from '../js/math-engine.js';
import {CURRICULUM,ALL_LESSONS} from '../js/curriculum.js';
import {FORMULAS} from '../js/reference.js';
const close=(a,b,tol=1e-8)=>assert.ok(Math.abs(a-b)<=tol*Math.max(1,Math.abs(a),Math.abs(b)),`got ${a}, expected ${b}`);
test('simple and compound interest calculations are mathematically consistent',()=>{
 const si=simpleInterest({principal:10000,apr:5,years:3});close(si.interest,1500);close(si.endingBalance,11500);
 const cp=compoundInterest({principal:10000,apr:5,years:10,periodsPerYear:12});close(cp.endingBalance,10000*Math.pow(1+0.05/12,120),1e-10);close(cp.interest,cp.endingBalance-10000);close(cp.apy,Math.pow(1+0.05/12,12)-1);
 const continuous=continuousInterest({principal:10000,apr:5,years:10});close(continuous.endingBalance,10000*Math.exp(.5));assert.ok(continuous.endingBalance>cp.endingBalance);
 const ear=effectiveAnnualRate({apr:6,periodsPerYear:12});close(ear.ear,Math.pow(1+.06/12,12)-1);
 close(compoundInterest({principal:1000,apr:0,years:5}).endingBalance,1000);
 close(compoundInterest({principal:1000,apr:10,years:0}).endingBalance,1000);
});
test('stable amortization and early payoff with extra principal',()=>{
 const loan=amortizeLoan({principal:240000,apr:6.5,years:30});
 close(loan.scheduledPayment,1516.963256383,1e-9); // independently calculated 30-year fixed-rate payment
 assert.equal(loan.periods,360);close(loan.rows[0].interest,1300);close(loan.rows[0].principalPaid,loan.scheduledPayment-1300);
 assert.ok(loan.rows.every(r=>r.endingBalance>=0));close(loan.rows.at(-1).endingBalance,0);close(loan.rows.reduce((s,r)=>s+r.principalPaid,0),240000);
 const early=amortizeLoan({principal:240000,apr:6.5,years:30,extraPayment:150});assert.ok(early.periods<loan.periods);assert.ok(early.interest<loan.interest);
 const zero=amortizeLoan({principal:1200,apr:0,years:1});assert.equal(zero.periods,12);close(zero.scheduledPayment,100);close(zero.interest,0);
 assert.throws(()=>amortizeLoan({principal:5000,apr:3,years:0}),/greater than zero/);
 close(paymentAmount(1000,0,10),100);
});
test('savings future value verified against repeated monthly update',()=>{
 const settings={initial:3000,monthlyContribution:250,apr:4.2,years:10};const fv=futureValueSavings(settings);
 let independent=settings.initial;for(let month=0;month<120;month++)independent=independent*(1+settings.apr/100/12)+settings.monthlyContribution;
 close(fv.endingBalance,independent,1e-10);close(fv.totalContributed,33000);
 const growth=investmentGrowthSeries(settings);close(growth.endingBalance,independent);close(growth.rows.at(-1).balance,independent);
 const goal=savingsGoal({goal:fv.endingBalance,initial:3000,apr:4.2,years:10});close(goal.monthlyDeposit,250,1e-9);
 close(savingsGoal({goal:500,initial:500,apr:0,years:1}).monthlyDeposit,0);
});
test('inflation, CAGR, debt repayment and discounted cashflows',()=>{
 const i=inflation({amount:1000,inflationRate:3,years:10});close(i.futurePrice,1000*Math.pow(1.03,10));close(i.purchasingPower,1000/Math.pow(1.03,10));
 close(investmentReturn({startValue:1000,endValue:1210,years:2}).cagr,0.1);
 const debt=debtPayoff({principal:1000,apr:0,monthlyPayment:100});assert.equal(debt.months,10);close(debt.totalPaid,1000);assert.throws(()=>debtPayoff({principal:1000,apr:24,monthlyPayment:20}),/must exceed/);
 close(npv({discountRate:10,cashflows:[-100,110]}).npv,0);close(irr({cashflows:[-100,110]}).irr,0.1,1e-7);
 assert.throws(()=>irr({cashflows:[100,200]}),/positive and one negative/);
});
test('input validation catches invalid debt, terms and percent rates',()=>{
 for(const fn of [
 ()=>compoundInterest({principal:-5,apr:5,years:10}),
 ()=>compoundInterest({principal:10,apr:5,years:10,periodsPerYear:0}),
 ()=>compoundInterest({principal:10,apr:5,years:10,periodsPerYear:12.5}),
 ()=>simpleInterest({principal:1000,apr:Infinity,years:5}),
 ()=>amortizeLoan({principal:1000,apr:5,years:1.01}),
 ()=>futureValueSavings({initial:500,monthlyContribution:100,apr:5,years:1.01}),
 ()=>effectiveAnnualRate({apr:5,periodsPerYear:-12}),
 ()=>savingsGoal({goal:1000,initial:0,apr:0,years:0}),
 ()=>npv({discountRate:10,cashflows:'bad values'})])assert.throws(fn);
});
test('all 12 financial calculators have a method, description and validated fields',()=>{
 assert.equal(Object.keys(FINANCE_METHODS).length,12);
 for(const [name,meta] of Object.entries(FINANCE_METHODS)){
  assert.ok(meta.name&&meta.description&&meta.fields.length>=1,name);
  const sample=Object.fromEntries(meta.fields.map(([key,label,unit,value])=>[key,key==='cashflows'?value:Number(value)]));
  const result=runFinanceMethod(name,sample);assert.ok(result.formula&&result.explanation,name);
 }
});
test('financial calculations also work in the safe scientific expression parser',()=>{
 close(calculate('simpleinterest(10000,5,3)'),1500);
 close(calculate('compoundinterest(10000,5,10,12)'),10000*Math.pow(1+.05/12,120));
 close(calculate('continuousinterest(10000,5,10)'),10000*Math.exp(.5));
 close(calculate('apy(6,12)'),100*(Math.pow(1+.06/12,12)-1));
 close(calculate('loanpmt(240000,6.5,30)'),amortizeLoan({principal:240000,apr:6.5,years:30}).scheduledPayment);
 close(calculate('savingsfv(3000,250,4.2,10)'),futureValueSavings({initial:3000,monthlyContribution:250,apr:4.2,years:10}).endingBalance);
 close(calculate('financenpv(10,-100,110)'),0);close(calculate('financeirr(-100,110)'),10);
 assert.throws(()=>calculate('compoundinterest(10000,5,2,0)'),/frequency/);
});
test('visual encyclopedia has a lesson-matched, readable image for every illustrated new lesson',()=>{
 const visuals=JSON.parse(readFileSync(new URL('../data/visuals.json',import.meta.url),'utf8'));
 const illustrated=ALL_LESSONS.filter(x=>x.visualKey);
 assert.equal(visuals.length,716);assert.equal(illustrated.length,716);assert.equal(ALL_LESSONS.length,861);
 const allIds=new Set(ALL_LESSONS.map(x=>x.id));assert.equal(new Set(visuals.map(x=>x.id)).size,716);
 for(const diagram of visuals){assert.ok(allIds.has(diagram.lessonId));assert.ok(diagram.caption&&diagram.title&&diagram.family);assert.ok(statSync(new URL('../'+diagram.image,import.meta.url)).size>10000,diagram.id);}
 assert.ok(FORMULAS.length>=140);
 for(let grade=0;grade<14;grade++)assert.ok(CURRICULUM[grade].lessons.length>=40);
});
