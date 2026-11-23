import {EXTRA_FORMULAS} from './finance-formulas.js';
/** Formula reference, data transforms and independently checkable exercises. */
import {calculate,MathError} from './math-engine.js';
export const FORMULAS=[
 ['Arithmetic','Additive identity','a + 0 = a','0+8'],['Arithmetic','Commutative addition','a + b = b + a','4+7'],['Arithmetic','Commutative multiplication','ab = ba','3*9'],
 ['Arithmetic','Distributive property','a(b+c) = ab + ac','3*(4+5)'],['Arithmetic','Order of operations','Grouping → Powers → × and ÷ → + and −','3+4*5'],
 ['Arithmetic','Percentage','p% of N = (p/100)N','18%*250'],['Arithmetic','Percent change','100(new−old)/old','100*(110-100)/100'],
 ['Fractions','Equivalent fractions','a/b = (ak)/(bk), k≠0','2/3'],['Fractions','Add fractions','a/b + c/d = (ad+bc)/(bd)','1/3+1/4'],
 ['Fractions','Multiply fractions','(a/b)(c/d) = ac/bd','2/3*3/4'],['Fractions','Divide fractions','(a/b)÷(c/d)=ad/bc','(2/3)/(4/5)'],
 ['Number theory','Greatest common divisor','gcd(a,b)','gcd(54,24)'],['Number theory','Least common multiple','lcm(a,b)','lcm(6,8)'],
 ['Number theory','Factorial','n! = 1 × 2 × ··· × n','6!'],['Number theory','Combination','C(n,r)=n!/[r!(n−r)!]','nCr(8,3)'],
 ['Number theory','Permutation','P(n,r)=n!/(n−r)!','nPr(6,2)'],['Number theory','Powers','a^m × a^n = a^(m+n)','2^3*2^4'],
 ['Number theory','Negative exponents','a^(−n)=1/a^n','2^-3'],['Number theory','Radical rule','sqrt(a²)=|a|','sqrt(49)'],
 ['Algebra','Slope','m = (y₂−y₁)/(x₂−x₁)','(8-2)/(3-1)'],['Algebra','Slope-intercept','y = mx + b','2*4+3'],
 ['Algebra','Quadratic formula','x = (−b ± sqrt(b²−4ac))/(2a)','(-(-5)+sqrt(25-24))/2'],
 ['Algebra','Difference of squares','a²−b²=(a−b)(a+b)','(7-3)*(7+3)'],['Algebra','Square of sum','(a+b)²=a²+2ab+b²','(3+4)^2'],
 ['Algebra','Distance','d = sqrt((x₂−x₁)²+(y₂−y₁)²)','sqrt((4-1)^2+(6-2)^2)'],
 ['Algebra','Midpoint','((x₁+x₂)/2,(y₁+y₂)/2)','(3+9)/2'],
 ['Geometry','Rectangle perimeter','P=2(l+w)','2*(7+5)'],['Geometry','Rectangle area','A=lw','7*5'],
 ['Geometry','Triangle area','A=bh/2','12*8/2'],['Geometry','Triangle angle sum','A+B+C=180°','180-45-70'],
 ['Geometry','Pythagorean theorem','a²+b²=c²','sqrt(5^2+12^2)'],
 ['Geometry','Circle circumference','C=2πr','2*pi*5'],['Geometry','Circle area','A=πr²','pi*5^2'],
 ['Geometry','Sector area','A=(θ/360)πr² (degrees)','(90/360)*pi*4^2'],
 ['Geometry','Trapezoid area','A=(b₁+b₂)h/2','(6+10)*4/2'],
 ['Geometry','Cylinder volume','V=πr²h','pi*3^2*7'],['Geometry','Sphere volume','V=4πr³/3','4*pi*3^3/3'],
 ['Geometry','Cone volume','V=πr²h/3','pi*3^2*6/3'],['Geometry','Box volume','V=lwh','4*5*6'],
 ['Trigonometry','Sine','sin θ = opposite/hypotenuse','sin(pi/6)'],['Trigonometry','Cosine','cos θ = adjacent/hypotenuse','cos(pi/3)'],
 ['Trigonometry','Tangent','tan θ = sin θ/cos θ','tan(pi/4)'],
 ['Trigonometry','Pythagorean identity','sin²θ+cos²θ=1','sin(0.7)^2+cos(0.7)^2'],
 ['Trigonometry','Double-angle sine','sin(2θ)=2sinθ cosθ','2*sin(pi/6)*cos(pi/6)'],
 ['Trigonometry','Double-angle cosine','cos(2θ)=cos²θ−sin²θ','cos(pi/6)^2-sin(pi/6)^2'],
 ['Trigonometry','Degrees to radians','radians=degrees·π/180','rad(90)'],
 ['Trigonometry','Radians to degrees','degrees=radians·180/π','deg(pi/2)'],
 ['Trigonometry','Law of sines','a/sin A=b/sin B=c/sin C','5/sin(pi/6)'],
 ['Trigonometry','Law of cosines','c²=a²+b²−2ab cos C','sqrt(3^2+4^2-2*3*4*cos(pi/3))'],
 ['Functions','Exponential','f(x)=a·b^x','3*2^4'],['Functions','Natural exponential','e^x=exp(x)','exp(2)'],
 ['Functions','Log inverse','log_b(b^x)=x','log(2^5,2)'],['Functions','Log product','ln(ab)=ln a+ln b','ln(4*7)'],
 ['Functions','Log quotient','ln(a/b)=ln a−ln b','ln(16/4)'],
 ['Statistics','Mean','x̄=Σx/n','avg(3,4,5,8)'],['Statistics','Sample variance','s²=Σ(x−x̄)²/(n−1)','variance(3,4,5,8)'],
 ['Statistics','Sample standard deviation','s=sqrt[s²]','stdev(3,4,5,8)'],
 ['Statistics','Normal z-score','z=(x−μ)/σ','(80-70)/5'],
 ['Probability','Complement','P(not A)=1−P(A)','1-0.25'],
 ['Probability','Independent events','P(A∩B)=P(A)P(B)','0.5*0.2'],
 ['Probability','Conditional probability','P(A|B)=P(A∩B)/P(B)','0.1/0.4'],
 ['Probability','Binomial probability','P(X=k)=C(n,k)p^k(1−p)^(n−k)','nCr(5,2)*0.5^2*0.5^3'],
 ['Sequences','Arithmetic nth term','aₙ=a₁+(n−1)d','4+(10-1)*3'],
 ['Sequences','Arithmetic sum','Sₙ=n(a₁+aₙ)/2','10*(3+21)/2'],
 ['Sequences','Geometric nth term','aₙ=a₁r^(n−1)','3*2^5'],
 ['Sequences','Geometric partial sum','Sₙ=a₁(1−r^n)/(1−r)','(1-0.5^10)/(1-0.5)'],
 ['Sequences','Infinite geometric sum','S=a/(1−r), |r|<1','3/(1-0.5)'],
 ['Vectors','2D magnitude','||v||=sqrt(x²+y²)','hypot(6,8)'],
 ['Vectors','2D dot product','a·b=a₁b₁+a₂b₂','2*4+3*5'],
 ['Vectors','Polar to x','x=r cos θ','5*cos(pi/3)'],
 ['Vectors','Polar to y','y=r sin θ','5*sin(pi/3)'],
 ['Calculus I','Limit of polynomial','lim x→a f(x)=f(a), for polynomials','2^3+1'],
 ['Calculus I','Derivative definition','f′(x)=lim h→0 [f(x+h)−f(x)]/h',null],
 ['Calculus I','Constant rule','d(c)/dx=0',null],
 ['Calculus I','Power rule','d(xⁿ)/dx=n x^(n−1)',null],
 ['Calculus I','Product rule','(uv)′=u′v+uv′',null],
 ['Calculus I','Quotient rule','(u/v)′=(u′v−uv′)/v²',null],
 ['Calculus I','Chain rule','(f∘g)′=(f′∘g)g′',null],
 ['Calculus I','Trigonometric derivative','d(sin x)/dx=cos x',null],
 ['Calculus I','Exponential derivative','d(e^x)/dx=e^x',null],
 ['Calculus I','Log derivative','d(ln|x|)/dx=1/x (x≠0)',null],
 ['Calculus I','Power antiderivative','∫xⁿdx=x^(n+1)/(n+1)+C (n≠−1)',null],
 ['Calculus I','Fundamental theorem','∫ₐᵇf(x)dx=F(b)−F(a)',null],
 ['Calculus II','u-substitution','∫f(g(x))g′(x)dx=∫f(u)du',null],
 ['Calculus II','Integration by parts','∫u dv=uv−∫v du',null],
 ['Calculus II','Trig half-angle','sin²x=(1−cos2x)/2','(1-cos(2*pi/3))/2'],
 ['Calculus II','Improper integral','∫ₐ∞f(x)dx=lim b→∞∫ₐᵇf(x)dx',null],
 ['Calculus II','Ratio test','L=lim|aₙ₊₁/aₙ|; L<1 implies absolute convergence',null],
 ['Calculus II','Taylor series','Σ[f⁽ⁿ⁾(a)/n!](x−a)ⁿ',null],
 ['Calculus II','Euler identity','e^(iπ)+1=0','cos(pi)+1'],
 ['Calculus II','Parametric slope','dy/dx=(dy/dt)/(dx/dt)',null],
 ['Calculus II','Polar area','A=1/2∫[r(θ)]² dθ',null],
 ['Calculus II','Arc length','L=∫ₐᵇsqrt(1+[f′(x)]²)dx',null],
 ['Calculus II','Disk volume','V=π∫ₐᵇ[f(x)]²dx',null]
].map(([category,name,formula,tryExpression],i)=>({id:i,category,name,formula,tryExpression}));
FORMULAS.push(...EXTRA_FORMULAS.map(([category,name,formula,tryExpression],i)=>({id:FORMULAS.length+i,category,name,formula,tryExpression})));
export const FORMULA_CATEGORIES=[...new Set(FORMULAS.map(f=>f.category))];
const rnd=(a,b)=>Math.floor(Math.random()*(b-a+1))+a;
const problem=(prompt,answer,steps,hint)=>({prompt,answer:String(answer),steps,hint:hint||steps[0],level:'practice'});
export function generateProblem(gradeIndex){
 const pool=Math.max(0,Math.min(13,Number(gradeIndex)||0));const g=pool;
 if(g===0){const a=rnd(1,19),b=rnd(1,19);return problem(`${a} + ${b} = ?`,a+b,[`Start with ${a}.`,`Count forward ${b} more: ${a+b}.`],'Use a number line or make ten.');}
 if(g===1){const a=rnd(30,300),b=rnd(20,250),neg=rnd(0,1);return neg?problem(`${a+b} − ${a} = ?`,b,[`Subtract the hundreds/tens/ones.`,`Check: ${b}+${a}=${a+b}.`]):problem(`${a} + ${b} = ?`,a+b,[`Align the place values.`,`Add ones, tens, then hundreds: ${a+b}.`]);}
 if(g===2){const a=rnd(2,12),b=rnd(2,12);return rnd(0,1)?problem(`${a} × ${b} = ?`,a*b,[`${a} groups of ${b} mean repeated addition.`,`Total is ${a*b}.`]):problem(`${a*b} ÷ ${a} = ?`,b,[`Find the number that multiplies ${a} to give ${a*b}.`,`Answer ${b}.`]);}
 if(g===3){const a=rnd(12,90),b=rnd(3,12);return problem(`${a} × ${b} = ?`,a*b,[`Break ${b} into tens and ones.`,`Multiply and add to obtain ${a*b}.`]);}
 if(g===4){const a=rnd(1,9),b=rnd(1,9);return problem(`${a}/10 + ${b}/10 = ?`,(a+b)/10,[`Both fractions have denominator 10.`,`Add numerators: (${a}+${b})/10 = ${(a+b)/10}.`]);}
 if(g===5){const p=rnd(1,9)*5,n=rnd(2,20)*10;return problem(`What is ${p}% of ${n}?`,p*n/100,[`Convert ${p}% to ${p/100}.`,`Multiply by ${n} to get ${p*n/100}.`]);}
 if(g===6){const x=rnd(-10,12),a=rnd(2,9),b=rnd(-10,15);return problem(`Solve ${a}x ${b<0?'−':'+'} ${Math.abs(b)} = ${a*x+b}. Enter x.`,x,[`Subtract ${b} from both sides.`,`Divide by ${a}: x=${x}.`]);}
 if(g===7){const x1=rnd(-5,3),y1=rnd(-6,4),run=rnd(1,6),slope=rnd(-5,5);return problem(`Slope between (${x1}, ${y1}) and (${x1+run}, ${y1+slope*run})?`,slope,[`Rise=${slope*run}.`,`Run=${run}.`,`m=${slope*run}/${run}=${slope}.`]);}
 if(g===8){const x=rnd(-5,5),m=rnd(-7,7)||2,b=rnd(-9,9);return problem(`If f(x)=${m}x+(${b}), find f(${x}).`,m*x+b,[`Replace x with ${x}.`,`Compute ${m}·${x}+(${b})=${m*x+b}.`]);}
 if(g===9){const a=rnd(3,14),b=rnd(3,12);return problem(`Area of a right triangle with legs ${a} and ${b}?`,a*b/2,[`Area=base·height/2.`,`A=${a}×${b}/2=${a*b/2}.`]);}
 if(g===10){const n=rnd(2,7),x=rnd(2,4);return problem(`Evaluate x^${n} at x=${x}.`,x**n,[`Substitute x=${x}.`,`Compute ${x}^${n}=${x**n}.`]);}
 if(g===11){const n=rnd(2,6),a=rnd(2,6);return problem(`Magnitude of vector (${n},${a})?`,Math.hypot(n,a),[`Use sqrt(${n}²+${a}²).`,`Result sqrt(${n*n+a*a}) ≈ ${Math.hypot(n,a).toFixed(5)}.`]);}
 if(g===12){const n=rnd(2,6),x=rnd(1,4);return problem(`If f(x)=x^${n}, find f′(${x}).`,n*x**(n-1),[`Apply the power rule: f′(x)=${n}x^${n-1}.`,`Substitute ${x} to get ${n*x**(n-1)}.`]);}
 const n=rnd(1,5),b=rnd(1,4);return problem(`Evaluate ∫ from 0 to ${b} of x^${n} dx.`,b**(n+1)/(n+1),[`Antiderivative is x^${n+1}/${n+1}.`,`At upper bound: ${b**(n+1)}/${n+1}.`]);
}
export function checkAnswer(user,expected){
 try{const got=calculate(user,{angleMode:'RAD'}),wanted=calculate(String(expected),{angleMode:'RAD'});
 if(typeof got!=='number'||typeof wanted!=='number')return false;
 return Math.abs(got-wanted)<=Math.max(1e-7,1e-5*Math.abs(wanted));
 }catch{return String(user).trim().toLowerCase()===String(expected).trim().toLowerCase();}
}
export const CONVERSIONS={
 length:{base:'m',units:{mm:0.001,cm:0.01,m:1,km:1000,in:0.0254,ft:0.3048,yd:0.9144,mi:1609.344}},
 mass:{base:'kg',units:{mg:1e-6,g:0.001,kg:1,oz:0.028349523125,lb:0.45359237}},
 time:{base:'s',units:{ms:0.001,s:1,min:60,hr:3600,day:86400,week:604800}},
 area:{base:'m²',units:{'cm²':1e-4,'m²':1,'km²':1e6,'ft²':0.09290304,acre:4046.8564224}},
 volume:{base:'L',units:{mL:0.001,L:1,'m³':1000,'fl oz (US)':0.0295735295625,'gal (US)':3.785411784}},
 speed:{base:'m/s',units:{'m/s':1,'km/h':1/3.6,mph:0.44704,knot:0.514444444}},
 temperature:{base:'°C',units:{'°C':1,'°F':1,K:1}}
};
export function convertUnit(value,kind,from,to){const n=Number(value),group=CONVERSIONS[kind];if(!Number.isFinite(n)||!group||!Object.hasOwn(group.units,from)||!Object.hasOwn(group.units,to))throw new MathError('Select valid units and a numeric value');
 if(kind==='temperature'){const c=from==='°C'?n:from==='°F'?(n-32)*5/9:n-273.15;return to==='°C'?c:to==='°F'?c*9/5+32:c+273.15;}
 return n*group.units[from]/group.units[to];}
