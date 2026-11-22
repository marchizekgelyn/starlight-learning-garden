/* Pure, inspectable scoring rules. Objective scores are exact; writing scores provisional. */
(function(root,factory){
  const lib=factory();
  if(typeof module!=='undefined' && module.exports) module.exports=lib;
  if(root) root.ATLAS_GRADER=lib;
})(typeof window!=='undefined'?window:null,function(){
  'use strict';
  const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
  const normalize=x=>String(x??'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[\u2019']/g,'').replace(/[^a-z0-9\s-]/g,' ').replace(/\s+/g,' ').trim();
  const tokens=x=>String(x??'').match(/[A-Za-z]+(?:['’\-][A-Za-z]+)*/g)||[];
  const levenshtein=(a,b)=>{
    const x=normalize(a),y=normalize(b);let row=Array.from({length:y.length+1},(_,i)=>i);
    for(let i=1;i<=x.length;i++){const next=[i];for(let j=1;j<=y.length;j++)next[j]=Math.min(next[j-1]+1,row[j]+1,row[j-1]+(x[i-1]===y[j-1]?0:1));row=next;}
    return row[y.length];
  };
  const keywordsPresent=(value,keywords)=>{
    const words=new Set(tokens(normalize(value)).map(x=>normalize(x)));
    return (keywords||[]).map(k=>({word:k,found:words.has(normalize(k))}));
  };
  const answerProvided=(q,a)=>q.type==='order'?Array.isArray(a)&&a.every(x=>x!==''&&x!==undefined&&x!==null):String(a??'').trim().length>0;
  function grade(q,a){
    if(!answerProvided(q,a)) return {score:0,max:q.points||10,confidence:'none',message:'Not answered. Add a response to earn credit.',details:[]};
    let fraction=0,message='',details=[];let confidence='objective';
    if(q.type==='mcq'){
      fraction=String(a)===q.answer?1:0;
      const correct=q.options.find(o=>o.id===q.answer);
      message=fraction===1?'Correct.':'Not quite. Review the passage and try again.';
      details=[`Answer: ${correct?correct.text:'not available'}`];
    }else if(q.type==='fill'){
      const n=normalize(a),expected=[q.answer,...(q.alternatives||[])].map(normalize);
      fraction=expected.includes(n)?1:expected.some(x=>x.length>=6&&n.length>=5&&levenshtein(n,x)<=1)?0.7:0;
      message=fraction===1?'Correct.':fraction>0?'Close spelling; partial credit.':'Check the term used in the passage.';
      details=[`Expected: ${q.answer}`];
    }else if(q.type==='order'){
      const given=Array.isArray(a)?a.map(x=>Number(x)):[];
      const seen=new Set(given);
      fraction=seen.size===q.answer.length?given.reduce((sum,v,i)=>sum+(v===q.answer[i]?1:0),0)/q.answer.length:0;
      message=fraction===1?'The steps are in the correct order.':'Revisit the sequence in the reading.';
      details=[`Order: ${q.answer.map(i=>q.steps[i]).join(' → ')}`];
    }else if(q.type==='short'){
      confidence='provisional';
      const wc=tokens(a).length;
      const keys=keywordsPresent(a,q.keywords),hits=keys.filter(x=>x.found).length;
      const coverage=keys.length?hits/keys.length:0;
      const length=clamp(wc/Math.max(1,q.minimumWords||8));
      const sentence=/[.!?]\s*$/.test(String(a).trim())?1:0;
      fraction=clamp(coverage*.75+length*.2+sentence*.05);
      message='Provisional keyword-and-structure score; meaning must be reviewed by a reader.';
      details=[`${hits}/${keys.length} reference concepts recognized`,`${wc}/${q.minimumWords||8} suggested words`,...keys.filter(x=>!x.found).map(x=>`Review term: ${x.word}`),`Sample response: ${q.sample}`];
    }else if(q.type==='essay'){
      confidence='provisional';
      const words=tokens(a),wc=words.length,paragraphs=String(a).trim().split(/\n\s*\n/).filter(Boolean).length;
      const keys=keywordsPresent(a,q.keywords),hits=keys.filter(x=>x.found).length;
      const coverage=keys.length?hits/keys.length:0;
      const growth=clamp(wc/Math.max(1,q.minimumWords));
      const sentences=String(a).split(/[.!?]+(?:\s|$)/).map(x=>x.trim()).filter(Boolean);
      const sentenceEnds=(String(a).match(/[.!?](?=\s|$)/g)||[]).length;
      const mechanics=clamp(sentenceEnds/Math.max(1,Math.ceil(wc/24)));
      const transition=/(\b(because|however|therefore|for example|for instance|although|first|next|finally|nevertheless|in contrast|in addition|as a result|this shows|according to)\b)/i.test(a)?1:0;
      const structure=q.minimumWords<30?clamp(.7*growth+.3*transition):clamp(.5*Math.min(paragraphs/2,1)+.5*transition);
      fraction=clamp(.35*coverage+.3*growth+.2*structure+.15*mechanics);
      message='Provisional writing score only; this software cannot reliably judge originality, factual accuracy, or sophisticated reasoning.';
      details=[`Reference concepts: ${hits}/${keys.length} recognized`,`Length: ${wc}/${q.minimumWords} target words`,`Organization indicator: ${Math.round(structure*100)}%`,`Sentence-ending indicator: ${Math.round(mechanics*100)}%`,
               'Rubric: '+(q.rubric||[]).join('; '),'Review the sample after submitting; it is one possible response, not the only valid answer.'];
    }else throw new Error('Unknown question type: '+q.type);
    return {score:Math.round(clamp(fraction)*(q.points||10)*10)/10,max:q.points||10,confidence,message,details};
  }
  function gradeLesson(lesson,answers){
    const items=lesson.questions.map(q=>({id:q.id,type:q.type,...grade(q,answers?.[q.id])}));
    const earned=items.reduce((s,x)=>s+x.score,0),max=items.reduce((s,x)=>s+x.max,0);
    const objective=items.filter(x=>x.confidence==='objective');
    const objPoints=objective.reduce((s,x)=>s+x.score,0),objMax=objective.reduce((s,x)=>s+x.max,0);
    const provisional=items.filter(x=>x.confidence==='provisional');
    return {score:Math.round(earned*10)/10,max,percent:Math.round(earned/max*100),objectivePercent:objMax?Math.round(objPoints/objMax*100):null,
            provisionalCount:provisional.length,answered:lesson.questions.filter(q=>answerProvided(q,answers?.[q.id])).length,
            items,gradedAt:new Date().toISOString()};
  }
  return {grade,gradeLesson,normalize,tokens,levenshtein,answerProvided};
});
