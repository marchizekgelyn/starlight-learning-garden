/** Symbolic differentiation and polynomial integration plus numerical Calculus I–II tools.
 * Author: Marc Lavoie | 2026-11-20
 */
import {parse,evaluateAst,realAt,MathError,fmt,formatValue} from './math-engine.js';
const N=v=>({type:'num',value:v}),V=name=>({type:'var',name}),B=(op,left,right)=>({type:'binary',op,left,right}),U=(op,arg)=>({type:'unary',op,arg}),F=(name,...args)=>({type:'call',name,args});
function hasVar(a,x='x'){if(a.type==='var')return a.name===x;if(a.type==='unary'||a.type==='postfix')return hasVar(a.arg,x);if(a.type==='binary')return hasVar(a.left,x)||hasVar(a.right,x);if(a.type==='call')return a.args.some(v=>hasVar(v,x));return false;}
function constant(a){if(hasVar(a))return null;try{const v=evaluateAst(a);return typeof v==='number'&&Number.isFinite(v)?v:null;}catch{return null;}}
export function derive(a,x='x'){
 switch(a.type){
 case 'num':return N(0);
 case 'var':return N(a.name===x?1:0);
 case 'unary':return U(a.op,derive(a.arg,x));
 case 'binary':{
  const u=a.left,v=a.right,du=derive(u,x),dv=derive(v,x);
  if(a.op==='+')return B('+',du,dv);if(a.op==='-')return B('-',du,dv);
  if(a.op==='*')return B('+',B('*',du,v),B('*',u,dv));
  if(a.op==='/')return B('/',B('-',B('*',du,v),B('*',u,dv)),B('^',v,N(2)));
  if(a.op==='^'){
   const c=constant(v);if(c!==null)return B('*',B('*',N(c),B('^',u,N(c-1))),du);
   return B('*',B('^',u,v),B('+',B('*',dv,F('ln',u)),B('*',v,B('/',du,u))));
  }throw new MathError(`Derivative of ${a.op} is not supported symbolically`);
 }
 case 'call':{
   if(a.args.length!==1)throw new MathError('Symbolic differentiation supports single-argument functions');
   const u=a.args[0],du=derive(u,x);
   const funcs={sin:()=>F('cos',u),cos:()=>U('-',F('sin',u)),tan:()=>B('/',N(1),B('^',F('cos',u),N(2))),
     exp:()=>F('exp',u),ln:()=>B('/',N(1),u),log10:()=>B('/',N(1),B('*',u,F('ln',N(10)))),
     sqrt:()=>B('/',N(1),B('*',N(2),F('sqrt',u))),asin:()=>B('/',N(1),F('sqrt',B('-',N(1),B('^',u,N(2))))),
     acos:()=>U('-',B('/',N(1),F('sqrt',B('-',N(1),B('^',u,N(2)))))),atan:()=>B('/',N(1),B('+',N(1),B('^',u,N(2))))};
   if(!funcs[a.name])throw new MathError(`Derivative of ${a.name} not implemented`);
   return B('*',funcs[a.name](),du);
 }
 default:throw new MathError('Symbolic derivative unavailable for this expression');
 }
}
export function simplify(a){
 if(a.type==='num'||a.type==='var')return a;
 if(a.type==='unary'){
  const arg=simplify(a.arg);if(a.op==='+')return arg;if(arg.type==='num')return N(-arg.value);if(arg.type==='unary'&&arg.op==='-')return arg.arg;return U(a.op,arg);
 }
 if(a.type==='binary'){
  const l=simplify(a.left),r=simplify(a.right),cv=constant(B(a.op,l,r));if(cv!==null)return N(cv);
  if(a.op==='+'){if(l.type==='num'&&l.value===0)return r;if(r.type==='num'&&r.value===0)return l;}
  if(a.op==='-'){if(r.type==='num'&&r.value===0)return l;if(l.type==='num'&&l.value===0)return simplify(U('-',r));}
  if(a.op==='*'){if(l.type==='num'&&l.value===0||r.type==='num'&&r.value===0)return N(0);if(l.type==='num'&&l.value===1)return r;if(r.type==='num'&&r.value===1)return l;}
  if(a.op==='/'){if(l.type==='num'&&l.value===0)return N(0);if(r.type==='num'&&r.value===1)return l;}
  if(a.op==='^'){if(r.type==='num'&&r.value===0)return N(1);if(r.type==='num'&&r.value===1)return l;if(l.type==='num'&&l.value===1)return N(1);}
  return B(a.op,l,r);
 }
 if(a.type==='call')return {...a,args:a.args.map(simplify)};
 return a;
}
function treeString(a,parent=0){
 if(a.type==='num')return fmt(a.value);
 if(a.type==='var')return a.name;
 if(a.type==='unary')return a.op+(a.arg.type==='binary'?`(${treeString(a.arg)})`:treeString(a.arg));
 if(a.type==='call')return `${a.name}(${a.args.map(e=>treeString(e)).join(', ')})`;
 if(a.type==='postfix')return `${treeString(a.arg,50)}${a.op}`;
 if(a.type==='binary'){
   const rank={'^':40,'*':25,'/':25,'+':10,'-':10}[a.op];
   const left=treeString(a.left,rank),right=treeString(a.right,rank+((a.op==='-'||a.op==='/')?1:0));
   const s=`${left} ${a.op} ${right}`;return rank<parent?`(${s})`:s;
 }return '?';
}
export function derivative(expression,at=null,mode='RAD'){
 if(mode!=='RAD')throw new MathError('Symbolic calculus uses radians. Switch to RAD mode.');
 const ast=parse(expression),result=simplify(derive(ast));return {expression:treeString(result),value:at===null?null:realAt(result,at,'RAD'),ast:result};
}
function polyMul(a,b){const r=Array(a.length+b.length-1).fill(0);for(let i=0;i<a.length;i++)for(let j=0;j<b.length;j++)r[i+j]+=a[i]*b[j];if(r.length>17)throw new MathError('Polynomial degree is too high for exact integration');return r;}
function polyAdd(a,b,sign=1){const r=Array(Math.max(a.length,b.length)).fill(0);for(let i=0;i<a.length;i++)r[i]+=a[i];for(let i=0;i<b.length;i++)r[i]+=sign*b[i];return r;}
export function polynomialCoefficients(ast){
 const c=constant(ast);if(c!==null)return [c];
 if(ast.type==='var'&&ast.name==='x')return [0,1];
 if(ast.type==='unary'){const v=polynomialCoefficients(ast.arg);return ast.op==='-'?v.map(n=>-n):v;}
 if(ast.type==='binary'){
 const a=polynomialCoefficients(ast.left),b=polynomialCoefficients(ast.right);
 if(ast.op==='+')return polyAdd(a,b);if(ast.op==='-')return polyAdd(a,b,-1);
 if(ast.op==='*')return polyMul(a,b);
 if(ast.op==='/'){if(b.length!==1||b[0]===0)throw new MathError('Polynomial division must be by a nonzero constant');return a.map(v=>v/b[0]);}
 if(ast.op==='^'){if(b.length!==1||!Number.isInteger(b[0])||b[0]<0||b[0]>16)throw new MathError('Polynomial exponent must be a whole number from 0 to 16');let out=[1];for(let i=0;i<b[0];i++)out=polyMul(out,a);return out;}
 }
 throw new MathError('Exact antiderivative supports polynomials in x. Use the definite integral for other functions.');
}
export function antiderivative(expression){const a=polynomialCoefficients(parse(expression));const parts=[];
 a.forEach((v,i)=>{if(Math.abs(v)<1e-12)return;const coeff=v/(i+1),abs=Math.abs(coeff),mono=i+1===1?'x':`x^${i+1}`;
 const term=Math.abs(abs-1)<1e-12?mono:`${fmt(abs)}*${mono}`;
 parts.push({sgn:coeff<0?'-':'+',term});});
 let out=parts.length?parts.map((p,i)=>`${i?(p.sgn==='-'?' - ':' + '):(p.sgn==='-'?'-':'')}${p.term}`).join(''):'0';
 return {expression:out+' + C',coefficients:a};
}
function fAt(ast,x,mode){try{const v=realAt(ast,x,mode);return Number.isFinite(v)?v:NaN;}catch{return NaN;}}
export function numericalDerivative(expression,x,mode='RAD'){
 const ast=parse(expression),h=Math.max(1e-5,Math.abs(x)*1e-5);const f=(z)=>fAt(ast,z,mode);
 const v=(-f(x+2*h)+8*f(x+h)-8*f(x-h)+f(x-2*h))/(12*h);
 if(!Number.isFinite(v))throw new MathError('Derivative cannot be evaluated at this point');return v;
}
export function numericLimit(expression,point,direction='both',mode='RAD'){
 const ast=parse(expression),f=(v)=>fAt(ast,v,mode);let direct=f(point);
 if(Number.isFinite(direct))return {value:direct,left:direct,right:direct,behavior:'Direct substitution'};
 function from(sign){let prev=null;const samples=[];for(let i=2;i<=9;i++){const h=Math.pow(10,-i)*Math.max(1,Math.abs(point));const y=f(point+sign*h);if(Number.isFinite(y))samples.push(y);}if(samples.length<3)return NaN;
 const last=samples.slice(-3);if(last.every(x=>Math.abs(x)>1e5)&&last.every(x=>Math.sign(x)===Math.sign(last[0])))return Math.sign(last[0])*Infinity;
 if(last.length>=3&&Math.abs(last[2]-last[1])<Math.max(1e-4,Math.abs(last[2])*1e-4))return last[2];
 return last.at(-1);
 }
 const left=from(-1),right=from(1);if(direction==='left')return {value:left,left,right,behavior:'Left-hand numerical estimate'};if(direction==='right')return {value:right,left,right,behavior:'Right-hand numerical estimate'};
 if(!Number.isFinite(left)||!Number.isFinite(right)){const same=left===right;return {value:same?left:null,left,right,behavior:same?'Both sides approach the same infinity (estimated)':'One-sided behavior differs; two-sided limit does not exist'};}
 const tol=1e-3*Math.max(1,Math.abs(left),Math.abs(right));return {value:Math.abs(left-right)<=tol?((left+right)/2):null,left,right,behavior:Math.abs(left-right)<=tol?'Two-sided numerical estimate':'One-sided limits differ; the two-sided limit does not exist'};
}
export function definiteIntegral(expression,a,b,mode='RAD'){
 if(!Number.isFinite(a)||!Number.isFinite(b))throw new MathError('Bounds must be finite');if(a===b)return 0;
 const ast=parse(expression);let left=a,right=b,sign=1;if(b<a){left=b;right=a;sign=-1;}
 const f=x=>fAt(ast,x,mode);const steps=48;let prev=null;
 for(let i=0;i<=steps;i++){const x=left+(right-left)*i/steps,y=f(x);if(!Number.isFinite(y))throw new MathError('Integral crosses an undefined point: use separate intervals or check for divergence');if(prev!==null&&Math.abs(y)>1e7&&Math.abs(prev)>1e7&&Math.sign(y)!==Math.sign(prev))throw new MathError('Possible discontinuity in integration interval');prev=y;}
 const simpson=(a,b,fa,fm,fb)=>((b-a)/6)*(fa+4*fm+fb);
 let calls=0;
 function adapt(a,b,fa,fm,fb,whole,depth){if(++calls>350000)throw new MathError('Integration complexity exceeded');const m=(a+b)/2,l=(a+m)/2,r=(m+b)/2,fl=f(l),fr=f(r);
  if(!Number.isFinite(fl)||!Number.isFinite(fr))throw new MathError('Integral includes a singularity');
  const one=simpson(a,m,fa,fl,fm),two=simpson(m,b,fm,fr,fb);
  if(depth<=0)return one+two;if(Math.abs(one+two-whole)<1e-9*(1+Math.abs(one+two)))return one+two+(one+two-whole)/15;
  return adapt(a,m,fa,fl,fm,one,depth-1)+adapt(m,b,fm,fr,fb,two,depth-1);
 }
 const fm=f((left+right)/2),fa=f(left),fb=f(right);
 if(![fa,fm,fb].every(Number.isFinite))throw new MathError('Integral endpoints or midpoint undefined');
 return sign*adapt(left,right,fa,fm,fb,simpson(left,right,fa,fm,fb),19);
}
export function summation(expression,lo,hi,operation='sum',mode='RAD'){
 if(!Number.isSafeInteger(lo)||!Number.isSafeInteger(hi)||hi<lo||hi-lo>10000)throw new MathError('Use whole-number bounds with at most 10,001 terms');const ast=parse(expression);let result=operation==='product'?1:0;
 for(let k=lo;k<=hi;k++){const v=evaluateAst(ast,{n:k,k,x:k},mode);if(typeof v!=='number')throw new MathError('Series terms must be real');result=operation==='product'?result*v:result+v;if(!Number.isFinite(result))throw new MathError('Series exceeds numerical range');}return result;
}
export function rootFind(expression,lo,hi,mode='RAD'){
 if(!(Number.isFinite(lo)&&Number.isFinite(hi)&&lo<hi))throw new MathError('Choose finite search bounds with min < max');const ast=parse(expression),f=x=>fAt(ast,x,mode),results=[];
 let px=lo,py=f(px);const samples=600;
 for(let i=1;i<=samples;i++){
 const x=lo+(hi-lo)*i/samples,y=f(x);
 if(Number.isFinite(y)&&Math.abs(y)<1e-9&&!results.some(r=>Math.abs(r-x)<1e-4))results.push(x);
 if(Number.isFinite(py)&&Number.isFinite(y)&&py*y<0){let l=px,r=x,fl=py;for(let k=0;k<70;k++){const m=(l+r)/2,fm=f(m);if(!Number.isFinite(fm))break;if(fl*fm<=0)r=m;else{l=m;fl=fm;}}const root=(l+r)/2,delta=1e-5;if(Math.abs(f(root))<1e-5&&!results.some(t=>Math.abs(t-root)<1e-4))results.push(root);}
 px=x;py=y;
 }return results.sort((a,b)=>a-b);
}
export function taylor(expression,center=0,degree=5){
 if(!Number.isInteger(degree)||degree<0||degree>8)throw new MathError('Taylor degree must be 0–8');
 let a=parse(expression),terms=[],fac=1;
 for(let n=0;n<=degree;n++){
  let d;try{d=realAt(a,center,'RAD');}catch{throw new MathError('Cannot evaluate Taylor coefficients at the center');}
  if(n>0)fac*=n;
  const coef=d/fac;if(Math.abs(coef)>1e-10)terms.push({power:n,coef});
  if(n<degree)a=simplify(derive(a));
 }
 const out=terms.map((t,i)=>`${i?(t.coef<0?' - ':' + '):(t.coef<0?'-':'')}${fmt(Math.abs(t.coef),8)}${t.power?`*(x${center?(center<0?` + ${fmt(-center)}`:` - ${fmt(center)}`):''})${t.power===1?'':`^${t.power}`}`:''}`).join('')||'0';
 return {expression:out,terms};
}
