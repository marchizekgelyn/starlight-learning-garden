/** ATLAS graph visualization: interactive Cartesian, polar, parametric and 3D surface plotting.
 * JavaScript Canvas 2D renderer; mathematically sampled approximations, no WebGL or network.
 */
import {parse,evaluateAst} from './math-engine.js';
const COLORS=['#68e9dc','#b29fff','#ffbd77','#5dcbff'];
const clamp=(v,a,b)=>Math.max(a,Math.min(v,b));
const nice=n=>{if(!Number.isFinite(n))return 'undefined';if(Math.abs(n)<1e-10)n=0;return Number(n.toPrecision(5)).toString();};
export class GraphVisualizer{
 constructor(canvas,{status,hover,legend}){this.canvas=canvas;this.ctx=canvas.getContext('2d');this.status=status;this.hover=hover;this.legend=legend;this.mode='cartesian';this.scale=48;this.cx=0;this.cy=0;this.yaw=.55;this.pitch=.48;this.parsed=[];this.secondary=null;this.drag=null;this.lastPointer=null;
 canvas.addEventListener('pointerdown',e=>{this.drag={x:e.clientX,y:e.clientY,cx:this.cx,cy:this.cy,yaw:this.yaw,pitch:this.pitch};canvas.setPointerCapture(e.pointerId);});
 canvas.addEventListener('pointermove',e=>{const r=canvas.getBoundingClientRect();const px=(e.clientX-r.left),py=(e.clientY-r.top);this.lastPointer={px,py};this.hover.textContent=this.mode==='surface'?'Drag to rotate surface':`Cursor ≈ (${nice((px-r.width/2)/this.scale+this.cx)}, ${nice((r.height/2-py)/this.scale+this.cy)})`;if(!this.drag)return;if(this.mode==='surface'){this.yaw=this.drag.yaw+(e.clientX-this.drag.x)*.008;this.pitch=clamp(this.drag.pitch+(e.clientY-this.drag.y)*.006,-1.3,1.3);}else{this.cx=this.drag.cx-(e.clientX-this.drag.x)/this.scale;this.cy=this.drag.cy+(e.clientY-this.drag.y)/this.scale;}this.draw();});
 const drop=()=>this.drag=null;canvas.addEventListener('pointerup',drop);canvas.addEventListener('pointercancel',drop);
 canvas.addEventListener('wheel',e=>{e.preventDefault();this.zoom(e.deltaY<0?1.2:1/1.2);},{passive:false});
 window.addEventListener('resize',()=>this.draw());
 }
 zoom(f){this.scale=clamp(this.scale*f,9,380);this.draw();}
 reset(){this.cx=0;this.cy=0;this.scale=48;this.yaw=.55;this.pitch=.48;this.draw();}
 plot(mode,expression,secondary=''){this.mode=mode;this.parsed=[];this.secondary=null;
 let values=String(expression).split('\n').map(s=>s.trim()).filter(Boolean);if(values.length===0)throw new Error('Enter a function');if((mode==='cartesian'&&values.length>4)||(mode!=='cartesian'&&values.length>1))throw new Error('Cartesian supports up to four functions; other modes use one expression');
 for(const item of values){const x=item.replace(/^y\s*=\s*/i,'').replace(/^f\(x\)\s*=\s*/i,'');this.parsed.push({label:item,ast:parse(x)});}if(mode==='parametric'){if(!String(secondary).trim())throw new Error('Enter a parametric y(t) function');this.secondary=parse(secondary);}
 this.legend.replaceChildren(...this.parsed.map((p,i)=>{const el=document.createElement('span'),dot=document.createElement('i');dot.className='legend-dot';dot.style.background=COLORS[i];el.append(dot,document.createTextNode(p.label));return el;}));
 this.status.textContent=`${mode} · ${this.parsed.length} curve${this.parsed.length>1?'s':''} · drag to ${mode==='surface'?'rotate':'pan'} · scroll to zoom`;
 this.reset();
 }
 value(ast,x,y=0,t=0){try{let n=evaluateAst(ast,{x,y,t,theta:t},'RAD');return typeof n==='number'&&Number.isFinite(n)?n:NaN;}catch{return NaN;}}
 draw(){const canvas=this.canvas,r=canvas.getBoundingClientRect(),W=Math.max(10,r.width||800),H=Math.max(10,r.height||450),dpr=clamp(window.devicePixelRatio||1,1,2);if(canvas.width!==Math.floor(W*dpr)||canvas.height!==Math.floor(H*dpr)){canvas.width=Math.floor(W*dpr);canvas.height=Math.floor(H*dpr);}const ctx=this.ctx;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);ctx.fillStyle='#081a2c';ctx.fillRect(0,0,W,H);
 if(this.mode==='surface'){this.drawSurface(ctx,W,H);return;}this.drawGrid(ctx,W,H);
 if(!this.parsed.length)return;
 const xp=x=>W/2+(x-this.cx)*this.scale,yp=y=>H/2-(y-this.cy)*this.scale,minX=this.cx-W/(2*this.scale);
 if(this.mode==='cartesian'){for(let k=0;k<this.parsed.length;k++){let current=false,lastY=0;const ast=this.parsed[k].ast;ctx.beginPath();ctx.strokeStyle=COLORS[k];ctx.lineWidth=2.5;ctx.lineJoin='round';for(let px=0;px<=W;px+=1.5){const x=minX+px/this.scale,y=this.value(ast,x),screen=yp(y),valid=Number.isFinite(y)&&Math.abs(screen)<H*16;if(!valid||current&&Math.abs(screen-lastY)>H*.75){current=false;continue;}if(current)ctx.lineTo(px,screen);else{ctx.moveTo(px,screen);current=true;}lastY=screen;}ctx.stroke();}}
 else if(this.mode==='polar'){const ast=this.parsed[0].ast;ctx.beginPath();ctx.strokeStyle=COLORS[0];ctx.lineWidth=2.5;let live=false,lastX=0,lastY=0;for(let i=0;i<=2500;i++){const t=2*Math.PI*i/2500,r=this.value(ast,0,0,t),x=r*Math.cos(t),y=r*Math.sin(t),a=xp(x),b=yp(y);if(!Number.isFinite(r)||Math.abs(a)>W*15||Math.abs(b)>H*15||live&&Math.hypot(a-lastX,b-lastY)>H){live=false;continue;}if(!live){ctx.moveTo(a,b);live=true;}else ctx.lineTo(a,b);lastX=a;lastY=b;}ctx.stroke();}
 else if(this.mode==='parametric'){const ast=this.parsed[0].ast;ctx.beginPath();ctx.strokeStyle=COLORS[0];ctx.lineWidth=2.5;let live=false,lastX=0,lastY=0;for(let i=0;i<=2500;i++){const t=2*Math.PI*i/2500,x=this.value(ast,0,0,t),y=this.value(this.secondary,0,0,t),a=xp(x),b=yp(y);if(!Number.isFinite(x)||!Number.isFinite(y)||Math.abs(a)>W*15||Math.abs(b)>H*15||live&&Math.hypot(a-lastX,b-lastY)>H){live=false;continue;}if(!live){ctx.moveTo(a,b);live=true;}else ctx.lineTo(a,b);lastX=a;lastY=b;}ctx.stroke();}
 }
 drawGrid(c,W,H){const s=this.scale,xp=x=>W/2+(x-this.cx)*s,yp=y=>H/2-(y-this.cy)*s;let tick=Math.pow(10,Math.floor(Math.log10(90/s)));if(tick*s<52)tick*=2;if(tick*s>190)tick/=2;c.font='11px ui-monospace,Consolas,monospace';c.lineWidth=1;const lx=this.cx-W/(2*s),rx=this.cx+W/(2*s),by=this.cy-H/(2*s),ty=this.cy+H/(2*s);
 c.strokeStyle='#203b54';c.fillStyle='#7490a9';for(let x=Math.ceil(lx/tick)*tick,i=0;x<=rx&&i<300;x+=tick,i++){const X=xp(x);c.beginPath();c.moveTo(X,0);c.lineTo(X,H);c.stroke();if(Math.abs(x)>tick/100)c.fillText(nice(x),X+3,clamp(yp(0)+15,15,H-7));}for(let y=Math.ceil(by/tick)*tick,i=0;y<=ty&&i<300;y+=tick,i++){const Y=yp(y);c.beginPath();c.moveTo(0,Y);c.lineTo(W,Y);c.stroke();if(Math.abs(y)>tick/100)c.fillText(nice(y),clamp(xp(0)+8,6,W-54),Y-5);}
 c.strokeStyle='#7192ab';c.lineWidth=1.6;c.beginPath();if(xp(0)>=0&&xp(0)<=W){c.moveTo(xp(0),0);c.lineTo(xp(0),H);}if(yp(0)>=0&&yp(0)<=H){c.moveTo(0,yp(0));c.lineTo(W,yp(0));}c.stroke();}
 drawSurface(c,W,H){const ast=this.parsed[0]?.ast;if(!ast){c.fillStyle='#b5c8db';c.fillText('Enter z = f(x,y)',24,28);return;}const yaw=this.yaw,pitch=this.pitch,scale=this.scale*1.05,cos=Math.cos(yaw),sin=Math.sin(yaw),tilt=Math.sin(pitch),h=5;const project=(x,y,z)=>{const a=x*cos-y*sin,b=x*sin+y*cos;return [W/2+a*scale*.7,H/2+b*scale*.46*tilt-z*scale*.55]};
 c.lineWidth=1.3;c.strokeStyle='#375c72';for(let i=-h;i<=h;i+=1){for(const ax of [0,1]){let prev=null;c.beginPath();for(let j=-h;j<=h;j+=.2){let xyz=ax?[j,i,0]:[i,j,0],p=project(...xyz);if(prev)c.lineTo(...p);else c.moveTo(...p);prev=p;}c.stroke();}}
 const curves=[],steps=36;for(let row=0;row<=steps;row++){const y=(row/steps*2-1)*5,points=[];for(let col=0;col<=steps;col++){const x=(col/steps*2-1)*5,z=this.value(ast,x,y);points.push({x,y,z,p:Number.isFinite(z)?project(x,y,clamp(z,-12,12)):null});}curves.push(points);}
 const order=Array.from({length:curves.length},(_,i)=>i).sort((a,b)=>{const y1=curves[a][0].y,y2=curves[b][0].y;return (y2-y1)*Math.cos(yaw);});for(const j of order){const points=curves[j];c.beginPath();let prev=null;for(let i=0;i<points.length;i++){const p=points[i].p;if(!p){prev=null;continue;}if(prev)c.lineTo(...p);else c.moveTo(...p);prev=p;}c.strokeStyle=`hsla(${160+160*j/steps},90%,${55+12*j/steps}%,.82)`;c.lineWidth=1.35;c.stroke();}for(let col=0;col<=steps;col+=3){c.beginPath();let prev=null;for(let row=0;row<=steps;row++){const p=curves[row][col].p;if(!p){prev=null;continue;}if(prev)c.lineTo(...p);else c.moveTo(...p);prev=p;}c.strokeStyle='#c8b1ff88';c.lineWidth=1;c.stroke();}
 c.fillStyle='#aec6dc';c.font='12px ui-monospace,monospace';c.fillText('z = '+this.parsed[0].label,16,24);c.fillText('Drag to rotate • Wheel to zoom',16,H-17);
 }
 exportPng(){const a=document.createElement('a');a.download=`atlas-${this.mode}-graph.png`;a.href=this.canvas.toDataURL('image/png');a.click();}
}
