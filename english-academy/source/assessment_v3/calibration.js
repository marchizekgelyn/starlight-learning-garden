/* ATLAS Writing v3: compare teacher scores to provisional indicators on THIS device.
 * No cloud, external identifiers, automatic overwriting, or claims of standardization.
 * Error statistics are summaries of provided reviews, NOT evidence of universal accuracy.
 */
(function(root,factory){const api=factory();if(typeof module!=='undefined'&&module.exports)module.exports=api;if(root)root.ATLAS_CALIBRATION_V3=api;})(typeof window!=='undefined'?window:null,function(){'use strict';
 function finite(n){return typeof n==='number'&&Number.isFinite(n);}
 function validRow(r){return r&&finite(r.machine)&&finite(r.teacher)&&r.machine>=0&&r.machine<=100&&r.teacher>=0&&r.teacher<=100&&typeof r.level==='string';}
 function analyze(rows,level){const valid=(Array.isArray(rows)?rows:[]).filter(validRow).filter(r=>!level||r.level===level);
  if(!valid.length)return {n:0,mae:null,bias:null,medianError:null,within10:null,level:level||'all',ready:false,note:'No parent-reviewed comparison scores are available.'};
  const e=valid.map(r=>r.machine-r.teacher);const abs=e.map(Math.abs).sort((a,b)=>a-b);const sum=x=>x.reduce((a,b)=>a+b,0);
  const middle=abs.length%2?abs[(abs.length-1)/2]:(abs[abs.length/2]+abs[abs.length/2-1])/2;
  const mae=sum(abs)/abs.length,bias=sum(e)/e.length,within10=abs.filter(x=>x<=10).length/abs.length;
  return {n:valid.length,mae:Math.round(mae*10)/10,bias:Math.round(bias*10)/10,medianError:Math.round(middle*10)/10,within10:Math.round(within10*100),level:level||'all',ready:valid.length>=5,note:valid.length<5?'Too few reviewed examples for even a local trend.':'This only measures agreement with the entered parent scores, not academic validity or fairness.'};
 }
 function summary(rows,level){const all=analyze(rows,level);return {...all,warning:'The parent may use a different rubric from the software. Never silently modify grades or draw conclusions about a student from these comparisons.'};}
 return {version:'3.0.0',analyze,summary,validRow};
});
