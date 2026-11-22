/* ATLAS Essay Assessment Engine 3.0 — independently inspectable formative scoring.
   Copyright 2026 ATLAS English Academy. No network calls, no third-party dependencies.
   IMPORTANT: lexical evidence and language conventions cannot verify understanding.
   Outputs are provisional, explainable and explicitly require human review.
 */
(function(root,factory){const obj=factory();if(typeof module!=='undefined'&&module.exports)module.exports=obj;if(root)root.ATLAS_ASSESSMENT_V3=obj;})(typeof window!=='undefined'?window:null,function(){
'use strict';
const clamp=(n,a=0,b=1)=>Math.min(b,Math.max(a,Number.isFinite(n)?n:a));
const round=(n,d=1)=>Math.round(n*10**d)/10**d;
const stop=new Set(`a an the and or nor but so to of from by for in on at under over between through with within without into onto after before until as than then there here this that those these i me you we us they them she he it her him their our your my his its is are was were am be been being have has had do does did can could should would will may might must one two three some many most much very quite really just also only even when where what which who whose how why because therefore however while either neither any all each every own same more less few several both such any about like`.split(' '));
const synonyms={
 'important':['significant','meaningful','essential','key','central'],'shows':['demonstrates','reveals','indicates','illustrates','suggests'],'result':['outcome','effect','consequence'],'reason':['cause','explanation','rationale'],
 'learn':['understand','discover','realize'],'idea':['concept','thought','point'],'character':['person','protagonist'],'main':['central','primary','principal'],'change':['shift','develop','transform'],'problem':['challenge','difficulty','issue'],
 'help':['support','assist','aid'],'compare':['contrast','relate','evaluate'],'difference':['distinction','contrast'],'evidence':['detail','example','proof','observation'],'claim':['argument','thesis','position'],
 'uncertain':['unknown','unproven','unverified'],'similar':['alike','same','related'],'because':['since','as'],'first':['initially','beginning'],'end':['conclusion','final'],
 'happy':['glad','pleased','joyful'],'sad':['unhappy','upset'],'went':['traveled','moved'],'looked':['saw','observed'],'said':['stated','told','explained'],
 'observe':['notice','see','record'],'describe':['explain','depict','outline'],'belief':['opinion','perspective','view'],'effect':['result','impact','outcome'],
 'fact':['observation','information'],'action':['step','behavior','response'],'limit':['restriction','boundary','uncertainty'], 'response':['reaction','answer','action']
};
const invSyn={};for(const [k,v] of Object.entries(synonyms)){invSyn[k]=k;for(const x of v)if(!invSyn[x])invSyn[x]=k;}
const contractions={"can't":"cannot","won't":"will not","didn't":"did not","doesn't":"does not","isn't":"is not","aren't":"are not","wasn't":"was not","weren't":"were not","shouldn't":"should not","wouldn't":"would not","couldn't":"could not"};
const negative=new Set(['not','no','never','nothing','neither','nor','cannot','without','hardly','rarely']);
const splitWords=t=>String(t??'').match(/[\p{L}\p{N}]+(?:[’'\-][\p{L}\p{N}]+)*/gu)||[];
function plain(t){return String(t??'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[‘’]/g,"'").replace(/[—–]/g,'-');}
function stem(w){let v=plain(w).replace(/'s$/,'');if(v.length>7&&v.endsWith('ization'))v=v.slice(0,-7)+'ize';else if(v.length>6&&v.endsWith('ies'))v=v.slice(0,-3)+'y';else if(v.length>6&&v.endsWith('ing'))v=v.slice(0,-3);else if(v.length>5&&v.endsWith('ed'))v=v.slice(0,-2);else if(v.length>5&&v.endsWith('es'))v=v.slice(0,-2);else if(v.length>4&&v.endsWith('s')&&!v.endsWith('ss'))v=v.slice(0,-1);return invSyn[v]||v;}
function meaningful(t){return splitWords(t).map(stem).filter(x=>x.length>=3&&!stop.has(x));}
function tokenPositions(text){const result=[],re=/[\p{L}\p{N}]+(?:[’'\-][\p{L}\p{N}]+)*/gu;let m;while((m=re.exec(String(text)))!==null)result.push({raw:m[0],value:stem(m[0]),start:m.index,end:m.index+m[0].length});return result;}
function tokenize(text){return tokenPositions(text).map(t=>t.value);}
function segmentSentences(text){
 const raw=String(text??'');const result=[];const abbreviations=new Set(['mr','mrs','ms','dr','prof','sr','jr','etc','vs','e.g','i.e','st','no','fig','inc','jan','feb','mar','apr','jun','jul','aug','sep','sept','oct','nov','dec']);
 let start=0;for(let i=0;i<raw.length;i++){
  const char=raw[i];if(!'.?!'.includes(char)&&char!=='\n')continue;
  if(char==='\n' && raw[i+1]!=='\n' && i!==raw.length-1)continue;
  if(char==='.'&&/\d/.test(raw[i-1]||'')&&/\d/.test(raw[i+1]||''))continue;
  const pre=raw.slice(start,i+1),last=(pre.match(/([A-Za-z.]+)\.$/)||[])[1];
  if(char==='.'&&last&&abbreviations.has(last.toLowerCase().replace(/\.$/,'')))continue;
  const next=raw.slice(i+1);if(char!=='\n'&&next[0]&&!/\s|[\"'”’]/.test(next[0]))continue;
  const piece=pre.trim();if(piece)result.push({text:piece,start:start+pre.indexOf(piece),end:i+1});start=i+1;
 }
 if(start<raw.length){const remaining=raw.slice(start).trim();if(remaining)result.push({text:remaining,start:start+raw.slice(start).indexOf(remaining),end:raw.length});}
 return result;
}
function paragraphSegments(text){const parts=[],re=/[^\n]+(?:\n(?!\n)[^\n]+)*/g;let m;while((m=re.exec(String(text??'')))!==null)if(m[0].trim())parts.push({text:m[0].trim(),start:m.index,end:m.index+m[0].length});return parts;}
function ratio(a,b){return b?clamp(a/b):0;}
function similarity(a,b){const as=new Set(meaningful(a)),bs=new Set(meaningful(b));if(!bs.size)return 0;let hits=0;for(const t of bs)if(as.has(t))hits++;return hits/bs.size;}
function evidenceSpans(text,anchor){const words=meaningful(anchor);if(!words.length)return {strength:0,matched:[],excerpt:'',position:-1};const s=segmentSentences(text);let best={strength:0,matched:[],excerpt:'',position:-1};for(const sent of s){const set=new Set(meaningful(sent.text));const matched=[...new Set(words)].filter(t=>set.has(t));const strength=ratio(matched.length,new Set(words).size);if(strength>best.strength){best={strength,matched,excerpt:sent.text.slice(0,240),position:sent.start};}}return best;}
function phrase(text,term){const v=plain(text).replace(/[^a-z0-9'\s-]/g,' ').replace(/\s+/g,' ').trim();const w=plain(term).replace(/[^a-z0-9'\s-]/g,' ').replace(/\s+/g,' ').trim();return w.length>1&&(' '+v+' ').includes(' '+w+' ');}
function lexicalRedundancy(text){const w=meaningful(text);if(w.length<12)return 0;const count=new Map();for(let i=0;i<w.length-3;i++){const k=w.slice(i,i+4).join(' ');count.set(k,(count.get(k)||0)+1);}const repeated=[...count.values()].reduce((n,v)=>n+Math.max(0,v-1),0);return clamp(repeated/Math.max(1,w.length-3));}
function sourceOverlap(text,source){const a=tokenize(text),b=tokenize(source);if(!source||a.length<10||b.length<10)return {share:0,matches:[],longest:0};const n=9,sourceSets=new Set();for(let i=0;i+n<=b.length;i++)sourceSets.add(b.slice(i,i+n).join(' '));const matched=new Set(),starts=[];for(let i=0;i+n<=a.length;i++){if(sourceSets.has(a.slice(i,i+n).join(' '))){starts.push(i);for(let j=i;j<i+n;j++)matched.add(j);}}return {share:ratio(matched.size,a.length),matches:starts.slice(0,12),longest:starts.length?n:0};}
function contradictions(text,anchors){const claims=[];const sentences=segmentSentences(text);for(const anchor of (anchors||[]).slice(0,12)){
 const expected=String(anchor?.text||anchor||'');const aTerms=meaningful(expected);if(aTerms.length<2)continue;
 const aHasNot=tokenize(expected).some(w=>negative.has(w));for(const sentence of sentences){const found=evidenceSpans(sentence.text,expected);if(found.strength<.67)continue;const hasNot=tokenize(sentence.text).some(w=>negative.has(w));
 if(hasNot!==aHasNot){claims.push({type:'possible_negation_mismatch',severity:'check',excerpt:sentence.text.slice(0,170),anchor:expected.slice(0,170),message:'This sentence may reverse a fact from the reading. Verify the intended meaning; negation detection is only a warning.'});break;}
 }}return claims.slice(0,5);}
function mechanics(text,level){const sentences=segmentSentences(text),notes=[];let missing=0,lowercase=0,long=0,fragments=0,repeat=0,comma=0;
 const maxLength=level<=2?28:level<=6?38:48;
 for(const s of sentences){const w=splitWords(s.text);if(!/[.!?][\"'”’)]?$/.test(s.text)){missing++;notes.push({issue:'Check sentence ending',excerpt:s.text.slice(0,145),suggestion:'Add a period, question mark, or exclamation mark if this is a complete sentence.',severity:'check'});}
 if(/^[a-z]/.test(s.text)&&!/^\b(?:iPhone|eBay)\b/.test(s.text)){lowercase++;notes.push({issue:'Possible lowercase sentence beginning',excerpt:s.text.slice(0,130),suggestion:'Review whether the first letter should be capitalized.',severity:'check'});}
 if(w.length>maxLength){long++;notes.push({issue:'Long sentence',excerpt:s.text.slice(0,145),suggestion:'Read this sentence aloud; consider dividing it if the ideas are hard to follow.',severity:'advice'});}
 if(w.length<=2&&sentences.length>1){fragments++;notes.push({issue:'Very short sentence',excerpt:s.text.slice(0,120),suggestion:'Check whether this short sentence is intentional or missing a subject or verb.',severity:'advice'});}
 }
 const dup=/\b([A-Za-z]{2,})\s+\1\b/gi;let m;while((m=dup.exec(text))!==null){repeat++;notes.push({issue:'Repeated word',excerpt:m[0],suggestion:'Check whether the repeated word is accidental.',severity:'check'});}
 if(/\s[,.;!?]/.test(text))notes.push({issue:'Space before punctuation',excerpt:'Extra space',suggestion:'Remove spaces immediately before commas, periods, and other punctuation.',severity:'check'});
 if(/(?:^|\s)i(?:\s|[.,!?;]|$)/.test(text))notes.push({issue:'First-person pronoun',excerpt:'i',suggestion:'Use the capitalized pronoun “I” in standard English.',severity:'check'});
 if(/,{2,}|\.{4,}|!{3,}|\?{3,}/.test(text))notes.push({issue:'Unusual punctuation cluster',excerpt:'Repeated punctuation',suggestion:'Check whether punctuation is intentional.',severity:'advice'});
 const density=sentences.length?clamp(1-(missing*.17+lowercase*.10+repeat*.14+long*.08+fragments*.02+comma*.10)/sentences.length):.1;
 return {sentences:sentences.length,missing,lowercase,long,fragments,repeat,notes:notes.slice(0,20),density};}
const discourse={cause:['because','as a result','therefore','consequently','since','due to','so that'],evidence:['for example','for instance','according to','the text says','the passage says','one detail','the author says','in the story','the reading'],contrast:['although','however','in contrast','on the other hand','whereas','instead','nevertheless'],sequence:['first','then','next','later','finally','afterward','before','at the end'],conclusion:['therefore','in conclusion','overall','this suggests','as a result']};
function signalSummary(text){const signals={};for(const [name,arr] of Object.entries(discourse))signals[name]=arr.filter(k=>phrase(text,k));return signals;}
function gradeNumber(id){if(id==='PK')return -1;if(id==='K')return 0;if(id==='C1')return 13;if(id==='C2')return 14;const n=Number(id);return Number.isFinite(n)?clamp(n,0,14):5;}
const presets={emergent:{task:.37,evidence:.12,reason:.09,organization:.12,conventions:.23,independence:.07},elementary:{task:.26,evidence:.20,reason:.15,organization:.15,conventions:.16,independence:.08},middle:{task:.24,evidence:.23,reason:.21,organization:.14,conventions:.10,independence:.08},secondary:{task:.20,evidence:.25,reason:.25,organization:.16,conventions:.07,independence:.07}};
function profile(level){const n=gradeNumber(level);const band=n<=1?'emergent':n<=5?'elementary':n<=8?'middle':'secondary';return {level:level||'unspecified',band,grade:n,weights:{...presets[band]},targetParagraph:n<=0?8:n<=2?25:n<=5?60:n<=8?100:n<=12?140:180,targetPage:n<=2?90:n<=5?160:n<=8?220:n<=12?300:400};}
function taskType(q){if(q?.taskType)return q.taskType;const p=plain(q?.prompt||'');if(/summari[sz]|retell/.test(p))return 'summary';if(/compar|contrast/.test(p))return 'compare';if(/argue|persuad|defend|position|opinion/.test(p))return 'argument';if(/chronolog|sequence|order of event/.test(p))return 'sequence';if(/reflect|your life|your opinion/.test(p))return 'reflection';return 'explanation';}
function conceptCoverage(text,groups){const result=[];for(const item of (groups||[]).slice(0,12)){
 const variants=(item.terms||[]).filter(Boolean);let best={strength:0,excerpt:'',matched:[]};for(const v of variants){const near=evidenceSpans(text,v);const direct=phrase(text,v);const strength=direct?1:near.strength*.72;if(strength>best.strength)best={...near,strength};}
 const score=clamp(best.strength);result.push({label:item.label||'Task idea',found:score>=.42,strength:round(score,2),excerpt:best.excerpt,matched:best.matched});
 }return result;}
function evidenceCoverage(text,anchors){const items=[];for(const item of (anchors||[]).slice(0,14)){
 const anchor=String(item?.text||item);if(!anchor.trim())continue;
 const near=evidenceSpans(text,anchor);items.push({anchor,excerpt:near.excerpt,match:round(near.strength,2),recognizable:near.strength>=.52});
 }return {items,total:items.length,hits:items.filter(x=>x.recognizable).length,coverage:items.length?items.reduce((n,x)=>n+x.match,0)/items.length:0};}
function feedbackPriorities(criteria){return criteria.filter(c=>c.ratio<.75).sort((a,b)=>(a.ratio-b.ratio)*.6+(b.weight-a.weight)).slice(0,5).map(x=>x.toImprove);}
function countQuotes(text){return (String(text).match(/[“"][^”"]{4,450}[”"]/g)||[]).length;}
function assess(text,q={},opts={}){
 const writing=String(text??'');const wc=splitWords(writing).length;const p=profile(q.level||opts.level||'5');const type=taskType(q),target=Math.max(5,Number(q.minimumWords)||((q.mode||opts.mode)==='page'?p.targetPage:p.targetParagraph));const wordsRatio=ratio(wc,target);
 const source=String(q.referenceText||'');const concepts=conceptCoverage(writing,q.concepts||[]);const evidence=evidenceCoverage(writing,q.expectedEvidence||[]);const syntax=mechanics(writing,p.grade),paragraphs=paragraphSegments(writing),signals=signalSummary(writing),sourceMatch=sourceOverlap(writing,source),sampleMatch=sourceOverlap(writing,q.sample||''),promptMatch=sourceOverlap(writing,q.prompt||'');
 const contradictionsFound=contradictions(writing,q.expectedEvidence||[]),repeat=lexicalRedundancy(writing);
 const taskAnchorCount=concepts.length;const matchedConcepts=concepts.filter(x=>x.found).length;
 const conceptStrength=taskAnchorCount?concepts.reduce((n,x)=>n+x.strength,0)/taskAnchorCount:0;
 const measuredEvidence=evidence.total?evidence.coverage:0;
 const actualPrompt=Boolean(String(q.prompt||'').trim().length>=12);
 const supported=actualPrompt&&source.trim().length>=20&&((q.expectedEvidence||[]).length>0||(q.concepts||[]).length>0);
 const reason=signals.cause.length+signals.conclusion.length,needReason=type!=='sequence'&&type!=='summary'&&p.grade>=3;
 const expectedSentences=p.grade<=0?1:p.grade<=2?2:p.grade<=5?3:4;
 const organizationRatio=clamp(.50*ratio(syntax.sentences,expectedSentences)+.25*(paragraphs.length?1:0)+.25*(type==='sequence'?clamp(signals.sequence.length/2):clamp((signals.cause.length+signals.contrast.length+signals.sequence.length)/2)),0,1);
 const clarityRatio=syntax.density;
 const reasonRatio=needReason?clamp(.55*ratio(reason,2)+.20*(signals.evidence.length>0?1:0)+.25*ratio(syntax.sentences,3)):
   clamp(.50*ratio(syntax.sentences,2)+.50*(type==='sequence'?Math.min(1,signals.sequence.length):.9));
 const expectedCoverage=(evidence.total?measuredEvidence:conceptStrength);
 const evidenceRatio=clamp(expectedCoverage*(sourceMatch.share>.50?.78:1));
 const taskRatio=clamp(.70*(taskAnchorCount?conceptStrength:evidenceRatio)+.30*clamp(wc/Math.max(5,target*.7)));
 const independenceRatio=clamp(1-(repeat>.25?.45:repeat*.5)-(sourceMatch.share>.35?.35:0)-(sampleMatch.share>.32?.5:0)-(promptMatch.share>.5?.5:0));
 const criteria=[];
 const add=(key,label,raw,why,toImprove)=>{const weight=p.weights[key];criteria.push({key,label,ratio:round(clamp(raw),3),weight,earned:round(weight*clamp(raw),3),why,toImprove});};
 add('task','Responding to the actual assignment',taskRatio,`${matchedConcepts}/${taskAnchorCount} expected ideas recognizable; ${wc} of approximately ${target} suggested words.`,`Reread the prompt and add a specific answer to each requested part. ${concepts.filter(c=>!c.found).slice(0,2).map(c=>'Consider '+c.label).join('. ')}`);
 add('evidence','Reading evidence and details',evidenceRatio,`${evidence.hits}/${evidence.total} provided evidence anchors recognizable. Matching terms are NOT proof the conclusion is correct.`,`Choose a detail from the supplied reading, cite or paraphrase it accurately, and explain why it matters.`);
 add('reason','Reasoning and explanation',reasonRatio,`Found ${reason} possible causal/concluding expressions; analysis of meaning needs a reader.`,`Explain why your example supports your claim; a connector alone is not evidence.`);
 add('organization','Sequence and organization',organizationRatio,`${syntax.sentences} sentence(s), ${paragraphs.length} paragraph(s).`,`State your main idea early, develop it in a logical order, and close with a thought tied to the prompt.`);
 add('conventions','Sentence clarity and conventions',clarityRatio,`${syntax.notes.length} possible sentence-level checks; dialect and purposeful style are not errors.`,`Review the highlighted sentences for punctuation and clarity, and keep any wording that is intentional.`);
 add('independence','Independent thinking and source use',independenceRatio,`Repeated-sequence signal ${Math.round(repeat*100)}%; direct passage reuse ${Math.round(sourceMatch.share*100)}%. Quotation and references can be legitimate.`,`Explain source material in your own words and attribute direct quotations. This tool does not determine authorship.`);
 let fraction=criteria.reduce((n,x)=>n+x.ratio*x.weight,0);const caps=[];const risks=[];
 if(wc<3){fraction=Math.min(fraction,.12);caps.push('Insufficient response to evaluate.');}
 else if(wc<target*.30){fraction=Math.min(fraction,.43);caps.push('Substantially under the suggested response length; a teacher can adjust the target.');}
 else if(wc<target*.55){fraction=Math.min(fraction,.67);caps.push('The response may need more development; the target is guidance, not a hard rule.');}
 if(repeat>.50){fraction=Math.min(fraction,.38);risks.push({name:'Substantial repetition',message:'Many phrase sequences repeat. Check that each sentence adds a new idea.',severity:'high'});}
 if(sourceMatch.share>.68||sampleMatch.share>.68){fraction=Math.min(fraction,.52);risks.push({name:'Extensive exact phrase overlap',message:'Long passages resemble a source or model answer. Quoting may be appropriate; review attribution instead of treating this as plagiarism proof.',severity:'check'});}
 if(contradictionsFound.length){fraction=Math.min(fraction,.70);risks.push({name:'Possible change of meaning',message:'A potential negation conflict was detected. A teacher must verify whether it is an actual contradiction.',severity:'check'});}
 if(supported&&taskAnchorCount&&matchedConcepts===0&&evidence.hits===0){fraction=Math.min(fraction,.43);caps.push('No recognizable anchor details: valid paraphrases might be missed.');}
 if(!supported){caps.push('No instructor-provided concepts or evidence criteria. A numeric assessment should not be used.');}
 if(!actualPrompt){caps.push('A specific writing prompt is needed to estimate task completion.');}
 const uncertainty=clamp(.17+(taskAnchorCount===0?.12:0)+(evidence.total===0?.11:0)+(p.grade>=7?.07:0)+(wc<target*.6?.10:0)+(contradictionsFound.length?.10:0)+(sourceMatch.share>.4?.08:0),.14,.42);
 const low=Math.max(0,Math.floor((fraction-uncertainty)*100));const high=Math.min(100,Math.ceil((fraction+uncertainty)*100));
 const semanticUnknown=['Whether the answer is factually correct','Whether a claim logically follows from the evidence','Whether an interpretation is valid even with different vocabulary','Whether the paper shows original understanding'];
 return {fraction:round(clamp(fraction),4),scoreEligible:supported&&wc>=3,estimatedRange:{low,high},uncertainty:'high',confidence:'provisional',reviewRequired:true,profile:p,taskType:type,
  criteria,fixes:[...new Set([...feedbackPriorities(criteria),...syntax.notes.map(n=>n.suggestion),...risks.map(r=>r.message)])].slice(0,11),
  metrics:{wordCount:wc,targetWords:target,paragraphCount:paragraphs.length,sentenceCount:syntax.sentences,conceptHits:matchedConcepts,conceptTotal:concepts.length,evidenceHits:evidence.hits,evidenceTotal:evidence.total,reasonConnectors:reason,qualifiers:signals.contrast.length,quotes:countQuotes(writing)},
  concepts,evidence:{hits:evidence.hits,total:evidence.total,strength:measuredEvidence,items:evidence.items},annotations:syntax.notes,risks,caps,contradictions:contradictionsFound,overlap:sourceMatch,signals,semanticUnknown,
  caution:'A broad formative estimate, not a validated paper grade. Parent or teacher review is required; a local AI review is an optional second opinion.'};
}
function analysisOnly(text,q={}){return assess(text,{...q,concepts:q.concepts||[],expectedEvidence:q.expectedEvidence||[]});}
function gradeBand(percent){if(percent>=90)return'A';if(percent>=80)return'B';if(percent>=70)return'C';if(percent>=60)return'D';return'Needs revision';}
return {version:'3.0.0',assess,analysisOnly,gradeBand,profile,taskType,plain,stem,meaningful,tokenize,tokenPositions,splitWords,segmentSentences,paragraphSegments,evidenceSpans,similarity,conceptCoverage,evidenceCoverage,mechanics,signalSummary,sourceOverlap,contradictions,lexicalRedundancy,phrase,clamp};
});
