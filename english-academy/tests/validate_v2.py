"""Full offline data validation: v2 curriculum, answer keys, assets, edition preservation."""
import json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'source';D=S/'studio-data';ART=S/'illustrations'
m=json.loads((D/'manifest.json').read_text())
assert m['levelCount']==16, m
assert m['lessonCount']==1536
assert m['assignmentCount']==23040
assert m['combinedAssignmentCount']==37248 and m['newWritingAssignmentCount']==12288
assert len(m['lessonIndex'])==1536
lesson_ids=set();counts={};bad=[];qtypes={};models=[]
for lev in m['levels']:
 d=json.loads((D/f"level_{lev['id'].lower()}.json").read_text())
 assert d['level']==lev['id'] and len(d['lessons'])==96
 for l in d['lessons']:
  assert l['id'] not in lesson_ids,l['id']; lesson_ids.add(l['id'])
  assert len(l['questions'])==15,(l['id'],len(l['questions']))
  assert len(l['mentor'])==8
  assert len(l['glossary'])>=4
  assert all(g['meaning'].strip() and 'subject-specific' not in g['meaning'].lower() for g in l['glossary'])
  assert len(l['reading']['paragraphs'])>=2
  read=' '.join(l['reading']['paragraphs']).lower()
  assert 'we still do not know everything' in read or 'there was still a boundary' in read or 'learned that' in read or 'the passage does not' in read,(l['id'],'missing qualifier')
  assert l['title'] and l['objective'] and l['writingPlan']['outline']
  assert (S/l['art']).exists(),l['art'];counts[l['strand']]=counts.get(l['strand'],0)+1
  if len(models)<5:models.append(l)
  seen=set()
  for q in l['questions']:
   assert q['id'] not in seen and q['points']>0 and q['prompt'],(l['id'],q['id']);seen.add(q['id'])
   qtypes[q['type']]=qtypes.get(q['type'],0)+1
   if q['type']=='mcq':
    assert len(q['options'])==4 and len({x['text'] for x in q['options']})==4,(l['id'],q['id'])
    assert q['answer'] in {x['id'] for x in q['options']}
   if q['type'] in ('fill','edit'):
    assert q['answer'] and 'alternatives' in q
   if q['type']=='order':
    assert len(q['steps'])==4 and sorted(q['answer'])==list(range(4))
   if q['type'] in ('short','essay'):
    assert q['minimumWords']>0 and q['sample'] and q['concepts'] and q['expectedEvidence']
   if q['type']=='essay':
    assert sum(x['weight'] for x in q['rubric'])==1.0
    assert len(q['rubric'])==6
  assert len(seen)==15
assert set(lesson_ids)=={x['id'] for x in m['lessonIndex']}
assert set(counts)=={x['id'] for x in m['strands']} and all(v==128 for v in counts.values())
assert (S/'classic.html').exists() and (S/'data.js').exists() and (S/'grader.js').exists()
files=list(ART.glob('*.svg'));assert len(files)==1536,len(files)
for i,p in enumerate(files):
 try:
  root=ET.parse(p).getroot()
  assert root.tag.endswith('svg') and root.attrib.get('viewBox')=='0 0 1200 570'
 except Exception as e:bad.append((p.name,str(e)))
assert not bad,bad[:10]
print('PASS:',len(lesson_ids),'new lessons, 23,040 new tasks, 1,536 well-formed SVGs, 12 subjects, 16 levels')
print('Question type distribution:',qtypes)
print('Original v1 source files available in source/ (classic.html, data.js, grader.js, curriculum.json)')
