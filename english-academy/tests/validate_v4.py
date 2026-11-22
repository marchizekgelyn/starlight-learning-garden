#!/usr/bin/env python3
"""Static integrity and semantic-key checks for v4 constructed reading corpus."""
from pathlib import Path
import json, re, collections, sys
base=Path(__file__).resolve().parents[1]
meta=json.loads((base/'source/pathway-v4/manifest.json').read_text(encoding='utf-8'))
files=list((base/'source/pathway-v4/content').glob('level_*.js'))
assert len(files)==16,len(files)
size=sum(p.stat().st_size for p in files)
assert size>=20*1024**2,f'Educational content below 20 MiB: {size}'
counts=collections.Counter(); ids=set();stem_titles=set()
for f in files:
 text=f.read_text(encoding='utf-8')
 label=text.split(']=',1)[1].rstrip(';\n')
 d=json.loads(label)
 level=d['level'];grade=d['order'];assert len(d['lessons'])==64
 for i,l in enumerate(d['lessons']):
  assert l['id'] not in ids;lids=ids.add(l['id']);assert l['sequence']==i
  stem_titles.add(l['title'])
  assert len(l['texts'])==3 and all(t['paragraphs'] for t in l['texts'])
  assert len(l['vocabulary'])>=4 and l['lessonGoal']
  assert len(l['questions'])==13
  assert len(l['annotations'])==6
  objective=[q for q in l['questions'] if q['type']=='mcq']
  written=[q for q in l['questions'] if q['type']=='writing']
  assert len(objective)==10 and len(written)==3
  corpus=' '.join(p.lower() for t in l['texts'] for p in t['paragraphs'])
  for q in objective:
   assert len(q['options'])==4,(l['id'],q['id'])
   assert len(set(q['options']))==4,(l['id'],q['id'])
   assert 0<=q['correct']<4
   assert q['explanation'] and q['points']==10
   if q['kind']=='explicit':
    assert q['options'][q['correct']].lower() in corpus,(l['id'],q['kind'])
   if q['kind']=='second-source':
    assert q['options'][q['correct']].lower() in corpus,(l['id'],q['kind'])
   if q['kind']=='measurement':
    assert q['options'][q['correct']].lower() in corpus,(l['id'],q['kind'])
   if q['kind']=='limitations':
    assert q['options'][q['correct']].lower() in corpus,(l['id'],q['kind'])
  for q in written:
   assert q['rubric'] and q['model'] and q['question']
  counts['lessons']+=1;counts['objective']+=10;counts['writing']+=3;counts['readings']+=3;counts['microLessons']+=len(l['instruction'])
assert len(stem_titles)==64
assert counts['lessons']==1024 and counts['objective']==10240 and counts['writing']==3072
assert counts['microLessons']==meta['counts']['microLessons']
assert meta['counts']['words']>1000000
print('PASS corpus',dict(counts),'content_bytes',size,'content_MiB',round(size/1024**2,2),'topic_stems',len(stem_titles),'reading_words',meta['counts']['words'])
