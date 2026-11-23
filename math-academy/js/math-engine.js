import {simpleInterest,compoundInterest,continuousInterest,effectiveAnnualRate,amortizeLoan,futureValueSavings,npv as financialNPV,irr as financialIRR} from './finance.js';
/** ATLAS Math Academy | Safe mathematical AST parser and numerical engine.
 * No eval(), Function(), remote execution or third-party runtime dependencies.
 * Author: Marc Lavoie | 2026-11-20
 */
const EPS=1e-12;
export class MathError extends Error {constructor(message){super(message);this.name='MathError';}}
export class Complex {
  constructor(re=0,im=0){this.re=re;this.im=im;}
  static from(v){return v instanceof Complex?v:new Complex(v,0);}
  add(v){const c=Complex.from(v);return new Complex(this.re+c.re,this.im+c.im);}
  neg(){return new Complex(-this.re,-this.im);}
  sub(v){return this.add(Complex.from(v).neg());}
  mul(v){const c=Complex.from(v);return new Complex(this.re*c.re-this.im*c.im,this.re*c.im+this.im*c.re);}
  div(v){const c=Complex.from(v),d=c.re*c.re+c.im*c.im;if(d===0)throw new MathError('Division by zero');return new Complex((this.re*c.re+this.im*c.im)/d,(this.im*c.re-this.re*c.im)/d);}
  abs(){return Math.hypot(this.re,this.im);}
  log(){return new Complex(Math.log(this.abs()),Math.atan2(this.im,this.re));}
  exp(){const a=Math.exp(this.re);return new Complex(a*Math.cos(this.im),a*Math.sin(this.im));}
  pow(v){const c=Complex.from(v);if(this.abs()===0){if(c.re>0&&Math.abs(c.im)<EPS)return new Complex(0);throw new MathError('Undefined zero power');}return this.log().mul(c).exp();}
  sqrt(){return this.pow(0.5);}
  toString(){if(Math.abs(this.im)<1e-10)return fmt(this.re);if(Math.abs(this.re)<1e-10)return `${fmt(this.im)}i`;return `${fmt(this.re)} ${this.im<0?'−':'+'} ${fmt(Math.abs(this.im))}i`;}
}
export const CONSTANTS=Object.freeze({pi:Math.PI,'π':Math.PI,e:Math.E,tau:Math.PI*2,'τ':Math.PI*2,phi:(1+Math.sqrt(5))/2,'φ':(1+Math.sqrt(5))/2,i:new Complex(0,1)});
export const FUNCTION_NAMES=new Set('sin cos tan asin acos atan atan2 sinh cosh tanh asinh acosh atanh sec csc cot sqrt cbrt root abs ln log log10 log2 exp floor ceil round trunc sign min max sum avg mean median std stdev variance hypot ncr npr gcd lcm fact factorial deg rad simpleinterest compoundinterest continuousinterest apy loanpmt savingsfv financenpv financeirr'.split(' '));
export function fmt(x,digits=12){if(!Number.isFinite(x))return x===Infinity?'∞':x===-Infinity?'−∞':'undefined';if(Math.abs(x)<EPS)x=0;return Number.parseFloat(x.toPrecision(digits)).toString();}
export function formatValue(v,digits=12){if(v instanceof Complex)return v.toString();if(typeof v==='number')return fmt(v,digits);return String(v);}
export function tokenize(input){
  if(String(input).length>4096)throw new MathError('Expression is too long; split the calculation into smaller steps');
  const src=String(input).replaceAll('×','*').replaceAll('÷','/').replaceAll('−','-').replaceAll('π','pi').replaceAll('τ','tau').replaceAll('φ','phi').replaceAll('√','sqrt').replaceAll('²','^2').replaceAll('³','^3').replaceAll('∞','Infinity');
  const out=[];let pos=0;
  while(pos<src.length){let c=src[pos];if(/\s/.test(c)){pos++;continue;}
    if(/[0-9.]/.test(c)){
      let m=src.slice(pos).match(/^(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?/);
      if(!m)throw new MathError(`Invalid number at character ${pos+1}`);
      const n=Number(m[0]);if(!Number.isFinite(n))throw new MathError('Number exceeds supported range');
      out.push({type:'num',value:n,raw:m[0]});pos+=m[0].length;continue;
    }
    if(/[A-Za-z_]/.test(c)){
      const m=src.slice(pos).match(/^[A-Za-z_][A-Za-z_0-9]*/)[0].toLowerCase();
      out.push({type:m==='mod'?'op':'id',value:m});pos+=m.length;continue;
    }
    if('+-*/^!%(),'.includes(c)){out.push({type:'(),'.includes(c)?c:'op',value:c});pos++;continue;}
    throw new MathError(`Unrecognized character “${c}” at position ${pos+1}`);
  }
  const inserted=[];
  for(let j=0;j<out.length;j++){
    const prior=out[j-1],cur=out[j];
    if(prior&&['num','id',')'].includes(prior.type)&&['num','id','('].includes(cur.type)){
      const fcall=prior.type==='id'&&cur.type==='('&&FUNCTION_NAMES.has(prior.value);
      const consecutiveNums=prior.type==='num'&&cur.type==='num';
      if(!fcall&&!consecutiveNums)inserted.push({type:'op',value:'*',implicit:true});
    }
    if(prior&&prior.type==='op'&&['!','%'].includes(prior.value)&&['num','id','('].includes(cur.type))inserted.push({type:'op',value:'*',implicit:true});
    inserted.push(cur);
  }
  inserted.push({type:'eof',value:''});return inserted;
}
export function parse(expression){
  let tokens=tokenize(expression),index=0;
  function peek(){return tokens[index];}
  function next(){return tokens[index++];}
  function need(type){const t=next();if(t.type!==type)throw new MathError(`Expected “${type}”, found “${t.value||'end'}”`);return t;}
  function expressionAt(min=0){
    let t=next(),lhs;
    if(t.type==='num')lhs={type:'num',value:t.value};
    else if(t.type==='id'){
      if(peek().type==='('&&FUNCTION_NAMES.has(t.value)){
        next();const args=[];if(peek().type!==')'){do{args.push(expressionAt(0));if(peek().type!==',')break;next();}while(true);}need(')');lhs={type:'call',name:t.value,args};
      }else lhs={type:'var',name:t.value};
    } else if(t.type==='('){lhs=expressionAt(0);need(')');}
    else if(t.type==='op'&&['+','-'].includes(t.value))lhs={type:'unary',op:t.value,arg:expressionAt(35)};
    else throw new MathError(`Expected number, function or parenthesis; found “${t.value||'end'}”`);
    while(true){const p=peek();if(p.type!=='op')break;
      if(['!','%'].includes(p.value)){if(50<min)break;next();lhs={type:'postfix',op:p.value,arg:lhs};continue;}
      const prec=p.value==='^'?40:['*','/','mod'].includes(p.value)?25:['+','-'].includes(p.value)?10:-1;
      if(prec<min||prec<0)break;
      next();const rhs=expressionAt(prec+(p.value==='^'?0:1));lhs={type:'binary',op:p.value,left:lhs,right:rhs};
    }
    return lhs;
  }
  if(tokens.length===1)throw new MathError('Enter an expression first');
  const ast=expressionAt();if(peek().type!=='eof')throw new MathError(`Unexpected “${peek().value}”`);return ast;
}
function real(x,why='This operation'){if(x instanceof Complex){if(Math.abs(x.im)>EPS)throw new MathError(`${why} requires a real number`);return x.re;}return x;}
function toComplex(z){return z instanceof Complex?z:new Complex(z,0);}
function collapse(c){return c instanceof Complex&&Math.abs(c.im)<EPS?c.re:c;}
function add(a,b){return a instanceof Complex||b instanceof Complex?collapse(toComplex(a).add(b)):a+b;}
function sub(a,b){return a instanceof Complex||b instanceof Complex?collapse(toComplex(a).sub(b)):a-b;}
function mul(a,b){return a instanceof Complex||b instanceof Complex?collapse(toComplex(a).mul(b)):a*b;}
function div(a,b){if(toComplex(b).abs()===0)throw new MathError('Division by zero');return a instanceof Complex||b instanceof Complex?collapse(toComplex(a).div(b)):a/b;}
function power(a,b){if(a instanceof Complex||b instanceof Complex||a<0&&Math.abs(b%1)>EPS)return collapse(toComplex(a).pow(b));return a**b;}
function factorial(n){n=real(n,'Factorial');if(!Number.isInteger(n)||n<0||n>170)throw new MathError('Factorial supports whole numbers from 0 to 170');let v=1;for(let k=2;k<=n;k++)v*=k;return v;}
function integer(n){n=real(n,'Combinatorics');if(!Number.isSafeInteger(n)||n<0)throw new MathError('Expected a nonnegative whole number');return n;}
function gcd2(a,b){a=Math.abs(Math.round(a));b=Math.abs(Math.round(b));while(b)[a,b]=[b,a%b];return a;}
function fn(name,args,mode){
  const complexOk=['sqrt','abs','ln','exp'].includes(name);const all=args.map(v=>complexOk&&v instanceof Complex?v:real(v,name));const z=all[0],z2=all[1],rad=mode==='DEG'?Math.PI/180:1;
  const exactly=(n)=>{if(args.length!==n)throw new MathError(`${name}() expects ${n} argument${n===1?'':'s'}`);};
  const one=()=>{exactly(1);return z;};
  const two=()=>{exactly(2);return [z,z2];};
  switch(name){
  case 'simpleinterest':{exactly(3);return simpleInterest({principal:all[0],apr:all[1],years:all[2]}).interest;}
  case 'compoundinterest':{if(args.length!==3&&args.length!==4)throw new MathError('compoundinterest(principal, APR_percent, years, periodsPerYear=12)');return compoundInterest({principal:all[0],apr:all[1],years:all[2],periodsPerYear:all[3]??12}).endingBalance;}
  case 'continuousinterest':{exactly(3);return continuousInterest({principal:all[0],apr:all[1],years:all[2]}).endingBalance;}
  case 'apy':{exactly(2);return effectiveAnnualRate({apr:all[0],periodsPerYear:all[1]}).ear*100;}
  case 'loanpmt':{if(args.length!==3&&args.length!==4)throw new MathError('loanpmt(principal, APR_percent, years, paymentsPerYear=12)');return amortizeLoan({principal:all[0],apr:all[1],years:all[2],paymentsPerYear:all[3]??12}).scheduledPayment;}
  case 'savingsfv':{exactly(4);return futureValueSavings({initial:all[0],monthlyContribution:all[1],apr:all[2],years:all[3]}).endingBalance;}
  case 'financenpv':{if(args.length<2)throw new MathError('financenpv(discountRatePercent, cashflowAt0, cashflowAt1, ...)');return financialNPV({discountRate:all[0],cashflows:all.slice(1)}).npv;}
  case 'financeirr':{if(args.length<2)throw new MathError('financeirr(cashflowAt0, cashflowAt1, ...)');return financialIRR({cashflows:all}).irr*100;}
  case 'sin':return Math.sin(one()*rad);case 'cos':return Math.cos(one()*rad);case 'tan':return Math.tan(one()*rad);
  case 'sec':return div(1,Math.cos(one()*rad));case 'csc':return div(1,Math.sin(one()*rad));case 'cot':return div(1,Math.tan(one()*rad));
  case 'asin':return Math.asin(one())/rad;case 'acos':return Math.acos(one())/rad;case 'atan':return Math.atan(one())/rad;
  case 'atan2':{const [a,b]=two();return Math.atan2(a,b)/rad;}
  case 'sinh':return Math.sinh(one());case 'cosh':return Math.cosh(one());case 'tanh':return Math.tanh(one());
  case 'asinh':return Math.asinh(one());case 'acosh':return Math.acosh(one());case 'atanh':return Math.atanh(one());
  case 'sqrt':{exactly(1);return args[0] instanceof Complex||z<0?collapse(toComplex(args[0]).sqrt()):Math.sqrt(z);}
  case 'cbrt':return Math.cbrt(one());
  case 'root':{const [a,b]=two();if(b===0)throw new MathError('Root index cannot be zero');if(a<0&&Number.isInteger(b)&&Math.abs(b%2)===1)return -Math.pow(-a,1/b);return power(a,1/b);}
  case 'abs':{exactly(1);return args[0] instanceof Complex?args[0].abs():Math.abs(z);}
  case 'ln':{exactly(1);return z<0||args[0] instanceof Complex?collapse(toComplex(args[0]).log()):Math.log(z);}
  case 'log10':return Math.log10(one());case 'log2':return Math.log2(one());
  case 'log':{if(args.length===1)return Math.log10(z);if(args.length===2)return Math.log(z)/Math.log(z2);throw new MathError('log(number) or log(number,base)');}
  case 'exp':{exactly(1);return args[0] instanceof Complex?collapse(args[0].exp()):Math.exp(z);}
  case 'floor':return Math.floor(one());case 'ceil':return Math.ceil(one());case 'round':return Math.round(one());case 'trunc':return Math.trunc(one());case 'sign':return Math.sign(one());
  case 'deg':return one()*180/Math.PI;case 'rad':return one()*Math.PI/180;
  case 'min':return Math.min(...all);case 'max':return Math.max(...all);case 'sum':return all.reduce((a,b)=>a+b,0);
  case 'avg':case 'mean':if(!args.length)throw new MathError('Provide at least one number');return all.reduce((a,b)=>a+b,0)/all.length;
  case 'median':{if(!args.length)throw new MathError('Provide numbers');const v=all.slice().sort((a,b)=>a-b),k=v.length>>1;return v.length%2?v[k]:(v[k-1]+v[k])/2;}
  case 'std':case 'stdev':case 'variance':{if(args.length<2)throw new MathError('Provide two or more numbers');const mean=all.reduce((a,b)=>a+b,0)/all.length;const v=all.reduce((s,n)=>s+(n-mean)**2,0)/(all.length-1);return name==='variance'?v:Math.sqrt(v);}
  case 'hypot':return Math.hypot(...all);
  case 'fact':case 'factorial':return factorial(one());
  case 'ncr':{const [n,r]=two().map(integer);if(r>n)throw new MathError('r cannot exceed n');let k=Math.min(r,n-r),v=1;for(let j=1;j<=k;j++)v=v*(n-k+j)/j;return Math.round(v);}
  case 'npr':{const [n,r]=two().map(integer);if(r>n)throw new MathError('r cannot exceed n');let v=1;for(let j=0;j<r;j++)v*=n-j;return v;}
  case 'gcd':return all.map(integer).reduce(gcd2);case 'lcm':return all.map(integer).reduce((a,b)=>a*b/gcd2(a,b));
  default:throw new MathError(`Unsupported function “${name}”`);
  }
}
export function evaluateAst(ast,vars={},angleMode='RAD'){
  let v;
  switch(ast.type){
    case 'num':v=ast.value;break;
    case 'var':{
      if(Object.prototype.hasOwnProperty.call(vars,ast.name))v=vars[ast.name];
      else if(Object.prototype.hasOwnProperty.call(CONSTANTS,ast.name))v=CONSTANTS[ast.name];
      else throw new MathError(`Unknown variable “${ast.name}”. Supply its value or use x in Graph/Advanced.`);
      break;
    }
    case 'unary':v=evaluateAst(ast.arg,vars,angleMode);v=ast.op==='-'?mul(-1,v):v;break;
    case 'postfix':v=evaluateAst(ast.arg,vars,angleMode);v=ast.op==='!'?factorial(v):div(v,100);break;
    case 'binary':{
      const a=evaluateAst(ast.left,vars,angleMode),b=evaluateAst(ast.right,vars,angleMode);
      switch(ast.op){case '+':v=add(a,b);break;case '-':v=sub(a,b);break;case '*':v=mul(a,b);break;case '/':v=div(a,b);break;case '^':v=power(a,b);break;case 'mod':v=real(a)%real(b);break;default:throw new MathError('Unrecognized operator');}break;
    }
    case 'call':v=fn(ast.name,ast.args.map(a=>evaluateAst(a,vars,angleMode)),angleMode);break;
    default:throw new MathError('Invalid expression tree');
  }
  if(typeof v==='number'&&Number.isNaN(v))throw new MathError('Undefined result: check function domain');
  if(v instanceof Complex&&(!Number.isFinite(v.re)||!Number.isFinite(v.im)))throw new MathError('Complex result is not finite');
  return v;
}
export function calculate(input,options={}){const ast=parse(input);return evaluateAst(ast,options.vars??{},options.angleMode??'RAD');}
export function realAt(ast,x,mode='RAD'){const v=evaluateAst(ast,{x},mode);return real(v,'Graphing');}
export function parseData(input){const v=String(input).split(/[\s,;]+/).filter(Boolean).map(Number);if(!v.length||v.some(n=>!Number.isFinite(n)))throw new MathError('Enter numeric data separated by commas, spaces, or semicolons');return v;}
export function descriptiveStats(data){const a=Array.isArray(data)?data:parseData(data),v=[...a].sort((a,b)=>a-b),n=v.length,mean=a.reduce((s,x)=>s+x,0)/n;
 const median=s=>{const m=s.length>>1;return s.length%2?s[m]:(s[m-1]+s[m])/2;};
 const freq=new Map();a.forEach(x=>freq.set(x,(freq.get(x)||0)+1));const peak=Math.max(...freq.values()),modes=peak>1?[...freq].filter(([,c])=>c===peak).map(([x])=>x):[];
 return {count:n,sum:a.reduce((s,x)=>s+x,0),mean,median:median(v),modes,min:v[0],max:v[n-1],range:v[n-1]-v[0],q1:n>=2?median(v.slice(0,Math.floor(n/2))):v[0],q3:n>=2?median(v.slice(Math.ceil(n/2))):v[0],populationSD:Math.sqrt(a.reduce((s,x)=>s+(x-mean)**2,0)/n),sampleSD:n>1?Math.sqrt(a.reduce((s,x)=>s+(x-mean)**2,0)/(n-1)):null};
}
export function matrixParse(str){let rows=String(str).trim().split(/[;\n]+/).map(line=>line.trim().split(/[\s,]+/).filter(Boolean).map(Number));if(!rows.length||!rows[0].length||rows.some(r=>r.length!==rows[0].length||r.some(n=>!Number.isFinite(n))))throw new MathError('Matrix rows must have equal lengths of numeric entries. Separate rows with semicolons.');if(rows.length>8||rows[0].length>8)throw new MathError('Matrices are limited to 8 × 8 for this browser edition');return rows;}
export function matrixDet(A){if(A.length!==A[0].length)throw new MathError('Determinant requires a square matrix');const n=A.length,M=A.map(r=>r.slice());let d=1;for(let k=0;k<n;k++){let pivot=k;for(let i=k+1;i<n;i++)if(Math.abs(M[i][k])>Math.abs(M[pivot][k]))pivot=i;if(Math.abs(M[pivot][k])<EPS)return 0;if(pivot!==k){[M[pivot],M[k]]=[M[k],M[pivot]];d*=-1;}const p=M[k][k];d*=p;for(let i=k+1;i<n;i++){const scale=M[i][k]/p;for(let j=k+1;j<n;j++)M[i][j]-=scale*M[k][j];}}return d;}
export function matrixRref(A){const M=A.map(r=>r.slice()),rows=M.length,cols=M[0].length;let lead=0;for(let r=0;r<rows;r++){if(lead>=cols)break;let i=r;while(Math.abs(M[i][lead])<EPS){i++;if(i===rows){i=r;lead++;if(lead===cols)return M;}}[M[r],M[i]]=[M[i],M[r]];const p=M[r][lead];M[r]=M[r].map(v=>v/p);for(let j=0;j<rows;j++)if(j!==r){const f=M[j][lead];M[j]=M[j].map((v,k)=>v-f*M[r][k]);}lead++;}return M.map(r=>r.map(x=>Math.abs(x)<EPS?0:x));}
export function matrixOp(a,b,op){const A=Array.isArray(a)?a:matrixParse(a),B=b?(Array.isArray(b)?b:matrixParse(b)):null,r=A.length,c=A[0].length;
 switch(op){
 case 'det':return matrixDet(A);
 case 'transpose':return Array.from({length:c},(_,j)=>A.map(row=>row[j]));
 case 'rref':return matrixRref(A);
 case 'inverse':{if(r!==c)throw new MathError('Inverse requires square matrix');const aug=A.map((row,i)=>[...row,...Array.from({length:r},(_,j)=>+(i===j))]);const out=matrixRref(aug);if(out.some((row,i)=>Math.abs(row[i]-1)>1e-8))throw new MathError('Matrix is singular; no inverse exists');return out.map(row=>row.slice(r));}
 case 'add':case 'subtract':{if(!B||B.length!==r||B[0].length!==c)throw new MathError('Matrix dimensions must match');return A.map((row,i)=>row.map((v,j)=>op==='add'?v+B[i][j]:v-B[i][j]));}
 case 'multiply':{if(!B||c!==B.length)throw new MathError('A columns must equal B rows');return A.map(row=>Array.from({length:B[0].length},(_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)));}
 default:throw new MathError('Unknown matrix operation');
 }}
export function matrixText(M){return Array.isArray(M)?M.map(row=>row.map(v=>fmt(v,9)).join('   ')).join('\n'):formatValue(M);}
export function solveQuadratic(a,b,c){[a,b,c]=[a,b,c].map(Number);if([a,b,c].some(v=>!Number.isFinite(v)))throw new MathError('Coefficients must be finite numbers');if(Math.abs(a)<EPS){if(Math.abs(b)<EPS)throw new MathError(Math.abs(c)<EPS?'All numbers are solutions':'No solution');return {discriminant:null,roots:[-c/b]};}const d=b*b-4*a*c;if(d>=0){const r=Math.sqrt(d);return {discriminant:d,roots:[(-b+r)/(2*a),(-b-r)/(2*a)]};}const r=Math.sqrt(-d);return {discriminant:d,roots:[new Complex(-b/(2*a),r/(2*Math.abs(a))),new Complex(-b/(2*a),-r/(2*Math.abs(a)))]};}
