/** Cartesian graph studio. Canvas only; no external dependencies. */
import {parse,realAt,fmt} from './math-engine.js';
const COLORS=['#54e0f0','#a69bff','#78e4b3','#f5c57c'];
export class GraphStudio{
 constructor(canvas,{status,legend,table}){
  this.canvas=canvas;this.ctx=canvas.getContext('2d');this.status=status;this.legend=legend;this.table=table;
  this.expressions=[];this.scale=55;this.centerX=0;this.centerY=0;this.drag=null;
  this.onSize=()=>this.draw();window.addEventListener('resize',this.onSize);
  canvas.addEventListener('pointerdown',e=>{this.drag={x:e.clientX,y:e.clientY,cx:this.centerX,cy:this.centerY};canvas.setPointerCapture(e.pointerId);canvas.style.cursor='grabbing';});
  canvas.addEventListener('pointermove',e=>{if(!this.drag)return;const r=canvas.getBoundingClientRect();this.centerX=this.drag.cx-(e.clientX-this.drag.x)*this.canvasCssW/r.width/this.scale;this.centerY=this.drag.cy+(e.clientY-this.drag.y)*this.canvasCssH/r.height/this.scale;this.draw();});
  const stop=()=>{this.drag=null;canvas.style.cursor='crosshair';};canvas.addEventListener('pointerup',stop);canvas.addEventListener('pointercancel',stop);
  canvas.addEventListener('wheel',e=>{e.preventDefault();this.zoom(e.deltaY<0?1.18:1/1.18);},{passive:false});
 }
 zoom(factor){this.scale=Math.min(1200,Math.max(8,this.scale*factor));this.draw();}
 reset(){this.centerX=0;this.centerY=0;this.scale=55;this.draw();}
 plot(text){const lines=String(text).split(/\n+/).map(s=>s.trim()).filter(Boolean);if(!lines.length){this.status.textContent='Enter at least one function.';return false;}
  if(lines.length>4){this.status.textContent='Maximum four functions per graph.';return false;}
  const expr=[];try{for(const input of lines){let normalized=input.replace(/^[a-z]\(x\)\s*=\s*/i,'').replace(/^y\s*=\s*/i,'');expr.push({input,ast:parse(normalized)});}this.expressions=expr;}catch(err){this.status.textContent=`Graph error: ${err.message}`;return false;}
  this.status.textContent=`${expr.length} function${expr.length===1?'':'s'} plotted • drag to pan • wheel to zoom (radians)`;
  this.legend.replaceChildren(...expr.map((item,i)=>{const e=document.createElement('span');e.className='legend-item';const color=document.createElement('span');color.className='legend-swatch';color.style.background=COLORS[i];const label=document.createElement('span');label.textContent=item.input;e.append(color,label);return e;}));
  this.tableValues();this.draw();return true;
 }
 tableValues(){const samples=[-3,-2,-1,0,1,2,3],thead=this.table.querySelector('thead'),tbody=this.table.querySelector('tbody');thead.replaceChildren();tbody.replaceChildren();let r=document.createElement('tr');for(const name of ['x',...this.expressions.map(x=>x.input)]){let c=document.createElement('th');c.textContent=name;r.append(c);}thead.append(r);
 for(const x of samples){let tr=document.createElement('tr');for(const [j,e] of [null,...this.expressions].entries()){let td=document.createElement('td');if(j===0)td.textContent=String(x);else{try{const v=realAt(e.ast,x,'RAD');td.textContent=Number.isFinite(v)?fmt(v,7):'undefined';}catch{td.textContent='undefined';}}tr.append(td);}tbody.append(tr);}}
 draw(){const rect=this.canvas.getBoundingClientRect();if(rect.width<20)return;this.canvasCssW=rect.width;this.canvasCssH=Math.max(280,Math.min(555,rect.width*.63));
  const dpr=Math.min(2,window.devicePixelRatio||1),W=this.canvasCssW,H=this.canvasCssH;
  this.canvas.style.height=`${H}px`;const dw=Math.round(W*dpr),dh=Math.round(H*dpr);if(this.canvas.width!==dw||this.canvas.height!==dh){this.canvas.width=dw;this.canvas.height=dh;}
  const c=this.ctx;c.setTransform(dpr,0,0,dpr,0,0);c.fillStyle='#091b2d';c.fillRect(0,0,W,H);
  const xpx=x=>W/2+(x-this.centerX)*this.scale,ypx=y=>H/2-(y-this.centerY)*this.scale;
  const minX=this.centerX-W/(2*this.scale),maxX=this.centerX+W/(2*this.scale),minY=this.centerY-H/(2*this.scale),maxY=this.centerY+H/(2*this.scale);
  let tick=Math.pow(10,Math.floor(Math.log10(85/this.scale)));if(tick*this.scale<45)tick*=2;if(tick*this.scale>200)tick/=2;
  c.lineWidth=1;c.strokeStyle='#284159';c.fillStyle='#7192a9';c.font='11px ui-monospace, Consolas, monospace';
  for(let x=Math.ceil(minX/tick)*tick,k=0;x<=maxX&&k<300;x+=tick,k++){const xp=xpx(x);c.beginPath();c.moveTo(xp,0);c.lineTo(xp,H);c.stroke();if(Math.abs(x)>tick/1000)c.fillText(fmt(x,5),xp+3,Math.min(H-7,Math.max(13,ypx(0)+13)));}
  for(let y=Math.ceil(minY/tick)*tick,k=0;y<=maxY&&k<300;y+=tick,k++){const yp=ypx(y);c.beginPath();c.moveTo(0,yp);c.lineTo(W,yp);c.stroke();if(Math.abs(y)>tick/1000)c.fillText(fmt(y,5),Math.min(W-54,Math.max(6,xpx(0)+6)),yp-5);}
  c.strokeStyle='#658ba3';c.lineWidth=1.7;
  if(xpx(0)>=0&&xpx(0)<=W){c.beginPath();c.moveTo(xpx(0),0);c.lineTo(xpx(0),H);c.stroke();}
  if(ypx(0)>=0&&ypx(0)<=H){c.beginPath();c.moveTo(0,ypx(0));c.lineTo(W,ypx(0));c.stroke();}
  this.expressions.forEach((expr,j)=>{c.strokeStyle=COLORS[j];c.lineWidth=2.4;c.lineCap='round';c.lineJoin='round';let drawing=false,lastY=0,lastRealY=null;
   c.beginPath();const step=1.8;for(let xp=0;xp<=W;xp+=step){const x=minX+xp/this.scale;let y;try{y=realAt(expr.ast,x,'RAD');}catch{y=NaN;}
     const py=ypx(y),valid=Number.isFinite(py)&&Number.isFinite(y)&&Math.abs(py)<H*20;
     const crossesJump=drawing&&(Math.abs(py-lastY)>H*.6||lastRealY!==null&&Math.sign(y)!==Math.sign(lastRealY)&&Math.abs(y)>maxY-minY&&Math.abs(lastRealY)>maxY-minY);
     if(!valid||crossesJump){drawing=false;lastRealY=null;continue;}
     if(!drawing){c.moveTo(xp,py);drawing=true;}else c.lineTo(xp,py);
     lastY=py;lastRealY=y;
   }c.stroke();});
 }
}
