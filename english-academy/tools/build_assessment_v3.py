#!/usr/bin/env python3
"""Generate source-linked, developmental writing practice *code* from existing ATLAS readings.

8 genuinely distinct instructional tasks for every one of the 1,536 lessons. Each task
includes its own prompt, lesson-specific evidence anchors, an actionable checklist,
transparent rubric expectations and common failure modes. These are generated derived
activities, not human-validated standardized test items or teacher-annotated gold data.
"""
from __future__ import annotations
import json, pathlib, re, hashlib, csv
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=ROOT/'source'
OUT=SRC/'assessment_v3'/'tasks';OUT.mkdir(exist_ok=True,parents=True)
levels=['pk','k',*map(str,range(1,13)),'c1','c2']
verbs=['retell','identify','trace','explain','qualify','apply','compare','revise']
labels=['Retelling and main idea','Evidence detective','Sequence and outcomes','Explain the reason','What the text cannot prove','Use a vocabulary word','Compare two ideas','Revise and clarify']
criteria={
'PK':'Use your own words. Adults may read questions aloud. A spoken or dictated response is appropriate.',
'K':'Make your idea clear with a picture label, a dictated answer, or one complete sentence.',
'1':'Answer the question in your own sentence and name one detail from the story.',
'2':'State a complete thought, then use one piece of story information to support it.',
'3':'Use a topic sentence, a specific example from the passage, and a closing thought.',
'4':'Explain how a detail in the text connects to the point you are making.',
'5':'Introduce the idea, cite a relevant detail, explain it, and maintain a logical order.',
'6':'Develop the central idea and support it with an accurate paraphrase or quotation.',
'7':'Support a defensible claim, explain the relationship between evidence and reasoning, and acknowledge limitations.',
'8':'Develop a claim with specific evidence and distinguish what the text says from your interpretation.',
'9':'Maintain a clear analytical focus and integrate evidence with commentary instead of merely inserting quotations.',
'10':'Develop a nuanced claim with appropriate qualifiers, textual evidence, and analysis of counterreadings.',
'11':'Sustain a coherent argument that separates observations, warrants, and limitations.',
'12':'Use precise academic language, deliberate structure, relevant evidence, and defensible qualifications.',
'C1':'Construct a defensible thesis; differentiate observation, inference and counterclaim, and consider evidentiary limits.',
'C2':'Demonstrate advanced rhetorical judgment, traceable evidence, nuanced counterinterpretation and disciplined attribution.'}

def target(l,mode):
 x={'PK':(6,12),'K':(9,25),'1':(16,50),'2':(25,75),'3':(40,100),'4':(55,130),'5':(70,170),'6':(85,200),'7':(105,230),'8':(120,270),'9':(145,310),'10':(160,340),'11':(175,380),'12':(190,420),'C1':(220,500),'C2':(240,600)}
 return x[l][int(mode=='page')]

def concise(t,limit=160):
 t=re.sub(r'\s+',' ',t or '').strip()
 return t[:limit].rsplit(' ',1)[0]+'…' if len(t)>limit else t

def sentence_chunks(s):
 return [x.strip() for x in re.split(r'(?<=[.!?])\s+',s) if len(x.split())>=5]

def activities(lesson):
 lid=lesson['id'];level=lesson['level'];title=lesson['caseTitle'];stage=lesson['stage'];strand=lesson['strandName'];
 source='\n\n'.join(lesson['reading']['paragraphs'])
 notice=re.sub('^Core evidence:\\s*','',lesson['reading'].get('notice',''),flags=re.I)
 limit=lesson['reading'].get('limitation','')
 glossary=(lesson['glossary'] or [])
 word=glossary[0]['word'] if glossary else 'main idea'
 definition=glossary[0]['meaning'] if glossary else 'the passage detail that matters most'
 candidate=sentence_chunks(source)
 action=next((x for x in candidate if any(v in x.lower() for v in ['respond','tapp','decid','chose','sorted','asked','tried','observed','noted','practiced','learned','used'])),candidate[min(1,len(candidate)-1)] if candidate else notice)
 end=candidate[-1] if candidate else notice
 primary=concise(notice,240)
 action=concise(action,230)
 end=concise(end,230)
 excerpt=concise(source,160)
 weak='A plausible-sounding claim with no support from the passage is not enough. Explain what words or events justify it.'
 early=level in ('PK','K','1','2')
 specs=[
  ('summary',f'Retell “{title}” in your own words. Tell the main idea and one thing that happened.' if early else f'Summarize the central idea of “{title}” without copying sentences. Include the main observation and its significance.',
   [primary],['Say what happened without copying the whole passage.','Choose the detail that most helps the reader understand the main point.','Use an ending that matches the story rather than an invented fact.'],
   ['The retelling repeats the question but never identifies a story detail.','The summary adds a major event that is not in the reading.']),
  ('evidence',f'What did you notice in “{title}”? Point to the words that helped you know.' if early else f'Identify a clear observation in “{title}.” Paraphrase or quote the strongest supporting detail and explain why it supports your claim.',
   [primary],['Make a specific claim about what the text actually says.','Point to a concrete detail from the reading.','Explain the connection between that detail and your answer.'],
   ['The response states a belief but does not mention the reported observation.','A quotation is included but its meaning is never explained.']),
  ('sequence',f'What happened first and what came next in “{title}”?' if early else f'Trace the sequence in “{title}” from initial observation to the response and outcome. Show how each step follows from the previous one.',
   [primary,action],['Use time order, not a random list of disconnected details.','Separate what was observed from what a character did next.','Avoid confusing the reported outcome with an inferred cause.'],
   ['Events are reported in reverse order without explanation.','An action is described as though it were the initial observation.']),
  ('explanation',f'Why did that detail matter in “{title}”? Use a clue from the reading.' if early else f'Explain why the key detail in “{title}” matters for understanding the outcome. Support your explanation with evidence rather than simply saying it was important.',
   [primary,action],['Give a reason tied to actual story information.','Explain an example in your own words.','Distinguish what the account establishes from your additional inference.'],
   ['The explanation uses because but gives no actual reason.','The writing states an unsupported causal relationship as a proven fact.']),
  ('limits',f'What do we still not know from “{title}”?' if early else f'Identify an uncertainty or limitation in “{title}.” Explain one claim the text supports and one stronger claim it does not establish.',
   [primary,limit],['Name something the text directly tells us.','Identify what the story leaves uncertain.','Use words such as may or cannot prove when a conclusion goes beyond the passage.'],
   ['The writer claims certainty about a fact the passage leaves unknown.','The writer treats an example as proof of a universal rule.']),
  ('vocabulary',f'Use the word “{word}” when telling what “{title}” is about.' if early else f'Explain the meaning of “{word}” in the context of “{title}.” Use a concrete example from the passage to demonstrate its meaning.',
   [primary],['Explain the word through an accurate example, not by listing unrelated vocabulary.','Identify how the word helps explain this particular story.','Use original wording, and review the glossary if you need support.'],
   ['A dictionary-like definition is provided with no connection to the text.','The example does not illustrate the named word.']),
  ('compare',f'What is the difference between what happened and what we think happened in “{title}”?' if early else f'Compare observation and interpretation in “{title}.” Explain how the recorded detail differs from a possible conclusion that someone might draw from it.',
   [primary,limit],['Name both things being compared.','Give one similarity or meaningful difference.','Identify which statement is directly reported and which is a conclusion.'],
   ['The two ideas are listed without a comparison.','An inference is incorrectly presented as a direct quotation.']),
  ('revision',f'Write a clearer answer to: What is the most important clue in “{title}”?' if early else f'Draft a clear paragraph making one defensible claim about “{title}.” Strengthen it by including an accurate detail, an explanation, and a qualification when needed.',
   [primary,action,limit],['Start with a clear answer, not only background information.','Use a relevant detail from the source and explain it.','Review clarity, organization, and the limits of the evidence.'],
   ['The response names several details but has no central point.','The writer repeats a model sentence instead of clarifying the claim.'])
 ]
 out=[]
 for i,(typ,prompt,anchors,checks,pitfalls) in enumerate(specs):
  mode='page' if (i in (3,6,7) and level not in ('PK','K','1','2','3')) else 'paragraph'
  minw=target(level,mode)
  coreTerms=[{ 'label':'Observation from the passage', 'terms':[notice,primary]},
             {'label':'Action or outcome', 'terms':[action]},
             {'label':'Scope or limitation', 'terms':[limit]}]
  if typ in ('summary','evidence','vocabulary'):coreTerms=coreTerms[:1]+([{'label':'Key vocabulary in context','terms':[word,definition]}] if typ=='vocabulary' else [])
  elif typ=='sequence':coreTerms=coreTerms[:2]
  elif typ=='explanation':coreTerms=coreTerms[:2]
  elif typ=='limits':coreTerms=[coreTerms[0],coreTerms[2]]
  elif typ=='compare':coreTerms=[coreTerms[0],coreTerms[2]]
  anchors=[x for x in anchors if x.strip()]
  spec={
   'id':f'{lid}-W{i+1:02d}','lessonId':lid,'level':level,'strand':lesson['strand'], 'kind':typ,
   'title':labels[i], 'mode':mode,'minimumWords':minw,'prompt':prompt, 'taskType':typ,
   'concepts':coreTerms,'expectedEvidence':list(dict.fromkeys(anchors)),
   'checklist':checks,
   'typicalPitfalls':pitfalls,
   'successCriteria':criteria[level],
   'scoringPolicy':'Formative only. Anchor recognition is a clue, not a proof of factual correctness. A parent or teacher must review interpretations.',
   'sourceLabel':f'Original instructional passage: {title} ({strand}).',
   'parentReview':['Does the response actually answer the writing prompt?','Is every referenced detail accurate in the passage?','Does the explanation make sense even if it uses different vocabulary?', 'Is the response appropriate to this child’s current writing development?'],
   'teachingHint':f'The passage says: “{primary}”. Ask the child to tell you what this shows before writing.',
   'rubricNarrative':f'To succeed at {labels[i].lower()}, demonstrate the following grade-level expectation: {criteria[level]}',
   'sourceExcerpt':excerpt,
   'clarifyQuestion':f'Which sentence in “{title}” makes you think that? Explain in your own words.',
   'revisionPrompt':f'What could you add to make your {labels[i].lower()} answer more specific to “{title}”?',
  }
  out.append(spec)
 return {'id':lid,'title':title,'strand':lesson['strand'],'source':source,'tasks':out}

all_tasks=0;all_bytes=0;writing_index=[]
for name in levels:
 data=json.loads((SRC/'studio-data'/f'level_{name}.json').read_text())
 records=[activities(l) for l in data['lessons']]
 count=sum(len(l['tasks']) for l in records);all_tasks+=count
 for item in records:
  for t in item['tasks']:
   writing_index.append({'assignment_id':t['id'],'level':t['level'],'lesson_id':t['lessonId'],'strand':t['strand'],'format':t['mode'],'task_type':t['taskType'],'minimum_words':t['minimumWords'],'title':t['title'],'prompt':t['prompt']})
 object={'level':data['level'],'version':'3.0.0','lessons':records}
 out=OUT/f'level_{name}.js'
 # Actual browser-loadable JavaScript, no fetch needed under file://.
 txt=f'/* ATLAS v3 original passage-linked writing assessment specifications — {data["level"]}. */\nwindow.ATLAS_WRITING_TASKS=window.ATLAS_WRITING_TASKS||{{}};\nwindow.ATLAS_WRITING_TASKS[{json.dumps(data["level"])}]={json.dumps(object,ensure_ascii=False,separators=(",",":"))};\n'
 out.write_text(txt,encoding='utf-8')
 all_bytes+=out.stat().st_size
 print(out.name,count,f'{out.stat().st_size:,} bytes')
with (ROOT/'docs'/'V3_WRITING_ASSIGNMENT_INDEX.csv').open('w',newline='',encoding='utf-8') as f:
 writer=csv.DictWriter(f,fieldnames=list(writing_index[0]));writer.writeheader();writer.writerows(writing_index)
summary={'version':'3.0.0','newWritingTasks':all_tasks,'gradeLevels':len(levels),'sourceBytes':all_bytes,'sourceMiB':round(all_bytes/2**20,3),'method':'8 prompt-specific new writing tasks per existing v2 lesson; authored task types composed from original lesson cases and evidence'}
(ROOT/'docs'/'V3_TASK_COUNTS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(summary)
