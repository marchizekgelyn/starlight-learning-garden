/**
 * ATLAS Writing Engine 2.0 | Deterministic, explainable formative assessment.
 *
 * It cannot establish factual accuracy, genuine comprehension, authorship or
 * provide a reliable summative essay mark. A human must review consequential scores.
 * No network, telemetry, AI calls or user identifiers are included.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) root.ATLAS_WRITING_ENGINE = api;
})(typeof window === 'undefined' ? null : window, function () {
  'use strict';
  const stop = new Set('a an the of and or to for from with as is are was were be being been am in on at by so it its this that these those they them their there than then when where who what why how while but do does did can may might must into onto out about against through under over some all each every not no one two three four his her she he you your i we our me my us have has had will would could should very more most much many just also said says made make goes went what which where way'.split(' '));
  const reasonConnect = ['because', 'therefore','as a result','this suggests','this shows','consequently','since','for this reason','indicates','implies','illustrates','means that','supports','rather than','suggests that','due to'];
  const qualification = ['however','although','despite','whereas','may','might','could','cannot','uncertain','limited','not prove','not necessarily','on the other hand','nevertheless','perhaps','one limitation','alternative','in contrast'];
  const transitions = ['first','next','finally','second','in addition','furthermore','however','therefore','for example','in conclusion','as a result','in contrast','similarly','meanwhile','consequently','although','for instance'];
  const clamp=(v,min=0,max=1)=>Math.min(max,Math.max(min,v));
  const round=v=>Math.round(v*10)/10;
  function normalize(raw){return String(raw??'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[’‘]/g,"'").replace(/[–—]/g,'-').replace(/[^a-z0-9'\s-]/g,' ').replace(/\s+/g,' ').trim();}
  function words(raw){return String(raw??'').match(/[\p{L}\p{N}]+(?:['’-][\p{L}\p{N}]+)*/gu)||[];}
  function stableTerms(raw){return words(normalize(raw)).map(w=>w.replace(/'s$/,'')).filter(Boolean);}
  function stems(raw){return stableTerms(raw).map(w=>{
    if(w.length>6&&/ies$/.test(w))return w.slice(0,-3)+'y';
    if(w.length>5&&/(ing|ers|ed)$/.test(w))return w.replace(/(ing|ers|ed)$/,'');
    if(w.length>4&&/s$/.test(w)&&!/ss$/.test(w))return w.slice(0,-1);
    return w;
  });}
  function units(text){return (String(text??'').match(/[^.!?\n]+(?:[.!?]+|$)/g)||[]).map(x=>x.trim()).filter(Boolean);}
  function paragraphs(text){return String(text??'').split(/\n\s*\n/).map(x=>x.trim()).filter(Boolean);}
  function hasPhrase(text,phrase){const a=' '+normalize(text)+' ',b=' '+normalize(phrase)+' ';return b.trim().length>2&&a.includes(b);}
  function lexicalSet(text){return new Set(stems(text).filter(w=>w.length>2&&!stop.has(w)));}
  function coverage(a,b){const aa=lexicalSet(a),bb=lexicalSet(b);if(!bb.size)return 0;let hits=0;for(const k of bb)if(aa.has(k))hits++;return hits/bb.size;}
  function groupsMet(answer,concepts){return (concepts||[]).map(x=>{
    const terms=x.terms||[];
    const matched=terms.filter(w=>hasPhrase(answer,w));
    return {label:x.label||'Reference concept',matched:matched.slice(0,4),found:matched.length>0};
  });}
  function repeatedNgrams(text,n=3){const t=stems(text),seen=new Map();for(let i=0;i+n<=t.length;i++){const key=t.slice(i,i+n).join(' ');seen.set(key,(seen.get(key)||0)+1);}let repeat=0;for(const v of seen.values())repeat+=Math.max(0,v-1);return {ratio:t.length>=n?repeat/(t.length-n+1):0, worst:Math.max(0,...seen.values())};}
  function copiedWords(student,source){const a=stems(student),b=stems(source);if(a.length<10||b.length<10)return {share:0,longest:0};
    const lengths=new Map();let copied=0,longest=0;const win=8;const keys=new Set();for(let i=0;i+win<=b.length;i++)keys.add(b.slice(i,i+win).join(' '));
    for(let i=0;i+win<=a.length;i++) if(keys.has(a.slice(i,i+win).join(' '))) {copied+=1;longest=Math.max(longest,win)};
    return {share:clamp(copied/Math.max(1,a.length-win+1)),longest};
  }
  function sentenceNotes(text){
    const ss=units(text);const out=[];let veryLong=0,fragments=0,noEnding=0,lowercase=0,overPunctuation=0;
    for(let i=0;i<ss.length;i++){
      const s=ss[i],w=words(s),wc=w.length;
      if(wc>36){veryLong++;out.push({severity:'advice',issue:'Long sentence',excerpt:s.slice(0,145),suggestion:'Consider splitting this sentence near a logical boundary to make the reasoning easier to follow.'});}
      if(wc>0&&wc<=2&&ss.length>1){fragments++;out.push({severity:'advice',issue:'Very short sentence',excerpt:s.slice(0,145),suggestion:'Check whether this fragment conveys a complete thought; fragments can also be intentional.'});}
      if(s&&!/[.!?][”’"']?$/.test(s)){noEnding++;out.push({severity:'advice',issue:'Possible missing ending punctuation',excerpt:s.slice(0,145),suggestion:'If this is a complete sentence, add an appropriate ending mark.'});}
      if(/^[a-z]/.test(s)){lowercase++;out.push({severity:'advice',issue:'Sentence may need capitalization',excerpt:s.slice(0,145),suggestion:'Standard written English normally capitalizes the first word of a sentence.'});}
      if(/[!?.,]{3,}/.test(s)){overPunctuation++;out.push({severity:'advice',issue:'Repeated punctuation',excerpt:s.slice(0,145),suggestion:'Use one ending mark unless a specific stylistic context calls for something else.'});}
    }
    const repeatWord=/(?:^|\s)([A-Za-z]{3,})\s+\1\b/gi;for(const m of text.matchAll(repeatWord)){
       out.push({severity:'advice',issue:'Repeated adjacent word',excerpt:m[0].trim(),suggestion:'Check whether this word was accidentally repeated.'});
    }
    if(/\bi\b/.test(text))out.push({severity:'advice',issue:'Lowercase first-person pronoun',excerpt:'i',suggestion:'In standard written English, write the standalone pronoun “I” with a capital.'});
    return {sentences:ss.length,long:veryLong,fragments,noEnding,lowercase,overPunctuation,notes:out.slice(0,10)};
  }
  function riskSignals(text,q){
    const wc=words(text).length;
    const repetition=repeatedNgrams(text),copyPassage=copiedWords(text,q?.referenceText||'');
    const copySample=copiedWords(text,q?.sample||'');
    const distinct=new Set(stems(text)).size;
    const diversity=wc?distinct/wc:0;
    const noise=wc>10&&diversity<.22;
    const promptcopy=copiedWords(text,q?.prompt||'');
    const flags=[];
    if(repetition.ratio>.45||noise)flags.push({name:'Highly repetitive language',message:'Much of the response repeats words or phrases. Add original explanation rather than repeating vocabulary.',severity:'high'});
    if(copyPassage.share>.40)flags.push({name:'Passage copied extensively',message:'Long sequences resemble the supplied passage. Try paraphrasing and explaining evidence.',severity:'high'});
    if(copySample.share>.38)flags.push({name:'Model response copied extensively',message:'The response appears to reuse substantial parts of the sample. Write your own explanation.',severity:'high'});
    if(promptcopy.share>.48)flags.push({name:'Prompt repeated',message:'Repeating the question does not answer it. Add your own claim and evidence.',severity:'high'});
    if(wc<3)flags.push({name:'Too little content',message:'Provide a response substantial enough to assess.',severity:'high'});
    return {flags,repetition:repetition.ratio,copyPassage:copyPassage.share,copySample:copySample.share,diversity};
  }
  function evidenceChecks(text,expected){
    const facts=(expected||[]).map(phrase=>{
      const closeness=coverage(text,phrase);const direct=hasPhrase(text,phrase);
      return {excerpt:phrase,closeness:round(closeness),direct,recognizable:direct||closeness>=.52};
    });
    const hits=facts.filter(f=>f.recognizable);
    return {hits:hits.length,total:facts.length,items:facts,strength:facts.length?hits.reduce((a,f)=>a+Math.max(.75,f.closeness),0)/facts.length:0};
  }
  function evaluation(text,q,extended){
    const target=Math.max(5,Number(q?.minimumWords)||25),w=words(text),wc=w.length,p=paragraphs(text),ss=sentenceNotes(text),risk=riskSignals(text,q),
          concept=groupsMet(text,q?.concepts||[]),covered=concept.filter(x=>x.found).length,
          ideas=concept.length?covered/concept.length:.25;
    const evid=evidenceChecks(text,q?.expectedEvidence||[]);
    const reason=reasonConnect.filter(k=>hasPhrase(text,k));
    const limits=qualification.filter(k=>hasPhrase(text,k));
    const transitionsFound=transitions.filter(k=>hasPhrase(text,k));
    const quotes=(text.match(/[“"][^”"]{8,200}[”"]/g)||[]).length;
    const length=clamp(wc/target),hasParagraphs=extended?clamp(p.length/(target>100?3:target>45?2:1)):1;
    const lowWordCount=wc<target*.30;
    const criteria=[];
    function criterion(key,label,weight,raw,why,toImprove){criteria.push({key,label,weight,ratio:round(clamp(raw)),earned:round(weight*clamp(raw)*100)/100,why,toImprove});}
    criterion('task','Task completion and reference concepts',.18,clamp(ideas*.65+length*.35),
       `${covered}/${concept.length} reference concept clusters recognized; ${wc}/${target} target words.`,
       concept.filter(x=>!x.found).length?`Develop: ${concept.filter(x=>!x.found).map(x=>x.label).join(', ')}.`:'Check whether you answered every part of the prompt in your own words.');
    criterion('reason','Explanation and reasoning',.22,clamp((reason.length? .62: .06)+(limits.length? .22:.02)+(.16*Math.min(ss.sentences/3,1))),
       `${reason.length} reasoning connectors and ${limits.length} qualifying expressions observed.`,
       reason.length?'Expand the explanation: show exactly how the cited detail leads to your conclusion.':'Use a causal explanation such as “because …” and show how a detail supports your conclusion.');
    criterion('evidence','Recognizable textual evidence',.24,clamp((evid.total?evid.strength:0)*.85+(quotes? .15:0)),
       `${evid.hits}/${evid.total} textual evidence anchors recognizable${quotes?`; ${quotes} quoted passages detected`:''}.`,
       evid.hits? 'Analyze the evidence you selected; explaining a quotation matters more than quoting at length.':'Refer to a specific detail actually present in the supplied reading and explain what it supports.');
    criterion('organization','Organization and cohesion',.16,clamp(.30*hasParagraphs+.35*(transitionsFound.length?1:.15)+.35*(ss.sentences>=2?1:ss.sentences*.35)),
       `${p.length} paragraph(s), ${ss.sentences} sentence(s), ${transitionsFound.length} transition types.`,
       p.length<2&&extended&&target>80?'Separate the main claim, evidence, and interpretation into logical paragraphs.':'Use a clear opening claim and transitions that match the relationships between ideas.');
    const conventional=clamp(1-(ss.noEnding/Math.max(1,ss.sentences))*.27-(ss.lowercase/Math.max(1,ss.sentences))*.15-(ss.long/Math.max(1,ss.sentences))*.28-Math.min(.25,ss.notes.length*.022));
    criterion('style','Readability and conventions',.12,clamp(conventional*(length>=.2?1:.4)),
       `${ss.long} potentially overlong sentence(s), ${ss.noEnding} possible boundary issue(s), ${ss.lowercase} possible capitalization issue(s).`,
       ss.notes[0]?.suggestion||'Read the response aloud, check sentence boundaries, and choose specific verbs and nouns.');
    criterion('integrity','Independent explanation and calibrated claims',.08,
       clamp(1- (risk.repetition>.30?.50:0)-(risk.copyPassage>.20?.5:0)-(risk.copySample>.18?.6:0)-(risk.flags.some(x=>x.name==='Prompt repeated')?.6:0)),
       `Repeated-language share ${Math.round(risk.repetition*100)}%; source-overlap signal ${Math.round(risk.copyPassage*100)}%.`,
       'Paraphrase in your own words, attribute quotations, and distinguish what you know from what you infer.');
    let fraction=criteria.reduce((sum,x)=>sum+x.weight*x.ratio,0);
    const caps=[];
    if(lowWordCount){fraction=Math.min(fraction,.44);caps.push('Very short relative to the assignment; provisional score capped.');}
    if(wc<4){fraction=Math.min(fraction,.18);caps.push('Insufficient writing; provisional score capped.');}
    if(risk.flags.some(x=>x.severity==='high'&&x.name!=='Too little content')){
       fraction=Math.min(fraction,.34);caps.push('Repeated or copied text signal; provisional score capped.');
    }
    if(ideas===0&&evid.hits===0){fraction=Math.min(fraction,.38);caps.push('No recognizable prompt concepts or passage evidence; provisional score capped.');}
    if(extended&&target>=60&&evid.hits===0){fraction=Math.min(fraction,.64);caps.push('No recognizable passage evidence; provisional score capped.');}
    const fixes=[...risk.flags.map(x=>x.message),...ss.notes.map(x=>x.suggestion),...criteria.filter(x=>x.ratio<.70).map(x=>x.toImprove)];
    return {fraction:clamp(fraction),criteria,fixes:[...new Set(fixes)].slice(0,9),metrics:{wordCount:wc,targetWords:target,paragraphCount:p.length,sentenceCount:ss.sentences,conceptHits:covered,conceptTotal:concept.length,evidenceHits:evid.hits,evidenceTotal:evid.total,reasonConnectors:reason.length,qualifiers:limits.length},
           concepts:concept,evidence:evid,annotations:ss.notes,risks:risk.flags,caps,confidence:'provisional',reviewRequired:true};
  }
  function editMatch(a,expected,alternatives=[]){
    const all=[expected,...alternatives];const strip=s=>String(s??'').trim().replace(/\s+/g,' ');
    if(all.some(x=>strip(x)===strip(a)))return {fraction:1,message:'Correct. This is an accepted revision.'};
    const sim=all.some(x=>normalize(x)===normalize(a));
    if(sim)return {fraction:.6,message:'The wording matches, but check capitalization and sentence punctuation.'};
    return {fraction:0,message:'Compare your revision with the reference correction; check word order and punctuation.'};
  }
  /** Conservative proofreader. Never silently edits the student's original.
   *  User explicitly selects Apply fixes to write this revised version to the editor.
   *  Changes are mechanical suggestions, NOT a comprehensive grammar checker.
   */
  function proofread(raw){
    const advanced=(typeof window!=='undefined'?window.ATLAS_PROOFREAD_V3:globalThis.ATLAS_PROOFREAD_V3);
    if(advanced && typeof advanced.proofread==='function')return advanced.proofread(raw);
    let revised=String(raw??''),changes=[];
    function change(rule,pattern,replace){
      revised=revised.replace(pattern,(...args)=>{
        const original=args[0];const replacement=typeof replace==='function'?replace(...args):replace;
        if(replacement!==original)changes.push({rule,before:original,after:replacement});
        return replacement;
      });
    }
    const spell={alot:'a lot',adress:'address',definately:'definitely',recieve:'receive',recieved:'received',seperate:'separate',seperately:'separately',becuase:'because',thier:'their',teh:'the',occurence:'occurrence',wich:'which',writting:'writing'};
    change('Common misspelling',/\b(alot|adress|definately|recieve|recieved|seperate|seperately|becuase|thier|teh|occurence|wich|writting)\b/gi,
      s=>{const corrected=spell[s.toLowerCase()];return /^[A-Z]/.test(s)?corrected[0].toUpperCase()+corrected.slice(1):corrected;});
    const contracted={dont:"don't",cant:"can't",wont:"won't",doesnt:"doesn't",didnt:"didn't",isnt:"isn't",arent:"aren't",wasnt:"wasn't",werent:"weren't",shouldnt:"shouldn't",couldnt:"couldn't",wouldnt:"wouldn't"};
    change('Contraction apostrophe',/\b(dont|cant|wont|doesnt|didnt|isnt|arent|wasnt|werent|shouldnt|couldnt|wouldnt)\b/gi,
      s=>{const corrected=contracted[s.toLowerCase()];return /^[A-Z]/.test(s)?corrected[0].toUpperCase()+corrected.slice(1):corrected;});
    change('First-person pronoun capitalization',/\bi\b/g,'I');
    change('Space before punctuation',/\s+([,;:.!?])/g,(all,mark)=>mark);
    change('Accidental repeated function word',/\b(the|and|a|of|to|for|in|is)\s+\1\b/gi,(_all,word)=>word);
    change('Extra consecutive spaces',/ {2,}/g,' ');
    return {revised,changed:revised!==String(raw??''),changes:changes.slice(0,150),count:changes.length,
      note:'Only selected high-confidence spelling and spacing patterns are proposed. Review the revised wording before accepting; meanings and source claims are not verified.'};
  }
  function grade(q,value){
    const max=Number(q?.points)||10;
    if(value===undefined||value===null||(typeof value==='string'&&!value.trim())||(Array.isArray(value)&&(!value.length||value.some(x=>x===''||x===undefined))))
      return {score:0,max,percent:0,kind:'unanswered',confidence:'none',message:'No response entered.',details:['Enter or select an answer to receive feedback.'],reviewRequired:false};
    const result={score:0,max,percent:0,confidence:'verified',kind:'objective',message:'',details:[],reviewRequired:false};
    let fraction=0;
    if(q.type==='mcq'){
      const ok=String(value)===String(q.answer);fraction=ok?1:0;
      result.message=ok?'Correct — the choice matches the passage.':'Review the text and the answer explanation.';
      result.details=[q.reason||'',...(ok?[]:[`Correct answer: ${(q.options||[]).find(o=>o.id===q.answer)?.text||q.answer}`])];
    }else if(q.type==='fill'){
      const a=normalize(value),all=[q.answer,...(q.alternatives||[])].map(normalize);
      fraction=all.includes(a)?1:0;
      result.message=fraction?'Correct.':'Not quite — compare the exact term or short phrase.';
      result.details=[q.reason||'',...(fraction?[]:[`Expected: ${q.answer}`])];
    }else if(q.type==='edit'){
      const r=editMatch(value,q.answer,q.alternatives);fraction=r.fraction;result.message=r.message;result.details=[q.reason||'',`Reference revision: ${q.answer}`];
    }else if(q.type==='order'){
      const entries=Array.isArray(value)?value.map(x=>Number(x)):[];
      const len=q.answer.length;
      fraction=entries.length===len&&new Set(entries).size===len&&entries.every(Number.isInteger)?entries.reduce((n,v,i)=>n+(v===q.answer[i]?1:0),0)/len:0;
      result.message=fraction===1?'Correct sequence.':'Revisit the order in which the information occurs.';
      result.details=[q.reason||'',`Expected: ${q.answer.map(n=>q.steps[n]).join(' → ')}`];
    }else if(q.type==='short'||q.type==='essay'){
      const advanced=(typeof window!=='undefined'?window.ATLAS_ASSESSMENT_V3:globalThis.ATLAS_ASSESSMENT_V3);
      const report=advanced&&typeof advanced.assess==='function'?advanced.assess(String(value),q):evaluation(String(value),q,q.type==='essay');
      fraction=report.fraction;
      result.confidence='provisional';result.kind='writing';result.reviewRequired=true;
      result.message=report.estimatedRange?`Preliminary rubric indicator (${report.estimatedRange.low}–${report.estimatedRange.high}% plausible range). A parent or teacher must check meaning and source accuracy.`:'Provisional formative score. A teacher must review meaning, factual correctness, style and originality.';
      result.details=[q.reason||'',`Model response (one possible approach): ${q.sample||'not supplied'}`];
      result.report=report;
    }else throw Error('Unknown exercise type: '+q.type);
    result.score=round(max*clamp(fraction));result.percent=round(result.score/max*100);
    result.details=result.details.filter(Boolean);return result;
  }
  function gradeLesson(lesson,answers){
    const items=(lesson.questions||[]).map(q=>({id:q.id,type:q.type,skill:q.skill,...grade(q,answers?.[q.id])}));
    const sum=items.reduce((n,r)=>n+r.score,0),max=items.reduce((n,r)=>n+r.max,0);
    const objective=items.filter(x=>x.kind==='objective');const objectiveMax=objective.reduce((n,r)=>n+r.max,0),objectiveEarned=objective.reduce((n,r)=>n+r.score,0);
    return {score:round(sum),max,percent:max?Math.round(100*sum/max):0,
            objectiveScore:round(objectiveEarned),objectiveMax,objectivePercent:objectiveMax?Math.round(100*objectiveEarned/objectiveMax):null,
            writingCount:items.filter(x=>x.kind==='writing').length,answered:items.filter(x=>x.kind!=='unanswered').length,
            items,gradedAt:new Date().toISOString(),reviewRequired:items.some(x=>x.reviewRequired)};
  }
  return {grade,gradeLesson,evaluation,editMatch,normalize,words,hasPhrase,groupsMet,evidenceChecks,sentenceNotes,riskSignals,coverage,proofread};
});
