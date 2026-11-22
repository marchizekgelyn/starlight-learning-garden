#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright
src=Path(__file__).resolve().parents[1]/'source'
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 page=browser.new_page(viewport={'width':1500,'height':950},accept_downloads=True)
 page.on('pageerror',lambda e:errors.append(str(e)))
 css=(src/'pathway-v4/pathway.css').read_text(encoding='utf-8')
 page.set_content('<html><head><style>'+css+'</style></head><body><div id="pathway"></div></body></html>')
 sources={f'pathway-v4/content/level_{x}.js':(src/f'pathway-v4/content/level_{x}.js').read_text(encoding='utf-8') for x in ['pk','4','c1','c2']}
 page.evaluate('''sources=>{window.__scripts=sources;const old=document.head.appendChild.bind(document.head);document.head.appendChild=function(el){if(el.tagName==='SCRIPT'&&el.src){const filename=Object.keys(sources).find(k=>el.src.endsWith(k));if(filename){(0,eval)(sources[filename]);queueMicrotask(()=>el.onload?.());return el;}}return old(el);};}''',sources)
 page.add_script_tag(content=(src/'pathway-v4/manifest.js').read_text(encoding='utf-8'))
 page.add_script_tag(content=(src/'pathway-v4/capstones.js').read_text(encoding='utf-8'))
 page.add_script_tag(content=(src/'pathway-v4/pathway.js').read_text(encoding='utf-8'))
 page.wait_for_function("!!window.ATLAS_PATHWAY_CONTENT?.PK")
 assert page.locator('.card').count()==64
 assert 'Read with understanding' in page.locator('h1').first.inner_text()
 print('INITIAL CARD COUNT',page.locator('.card').count())
 page.locator('.card').first.click()
 assert page.locator('.reader p').count()>=3
 page.get_by_role('tab',name='Skill workshop').click()
 assert page.locator('.training').count()==5
 page.get_by_role('tab',name='10-question checkpoint').click()
 assert page.locator('.question').count()==10
 # Read keyed correct options from source and mark all correct without relying on fixed option position
 correct=page.evaluate('''()=>window.ATLAS_PATHWAY_CONTENT.PK.lessons[0].questions.filter(q=>q.type==='mcq').map(q=>q.correct)''')
 for i,x in enumerate(correct,1):page.locator('.question').nth(i-1).locator('.option').nth(x).click()
 page.locator('[data-act="grade"]').click()
 assert '100%' in page.locator('.score').inner_text()
 assert page.locator('.answer-box').count()==10
 page.get_by_role('tab',name='Write & revise').click()
 assert page.locator('[data-draft]').count()==3
 page.locator('[data-draft]').first.fill('I saw an important clue in the story. We can read the words again before we answer.')
 page.get_by_role('tab',name='Mastery review').click()
 page.locator('#human-check').check();page.locator('#human-score').fill('85');page.locator('#human-notes').fill('The retelling used an accurate direct detail.')
 page.locator('[data-act="save-review"]').click()
 assert 'Yes' in page.locator('.stat').last.inner_text()
 page.locator('[data-act="dashboard"]').first.click()
 assert 'Progress is evidence' in page.locator('h1').first.inner_text()
 page.locator('[data-act="home"]').first.click()
 page.locator('#level-picker').select_option('C2')
 page.wait_for_function("!!window.ATLAS_PATHWAY_CONTENT?.C2")
 assert page.locator('.card').count()==64
 page.locator('.card').nth(4).click()
 assert page.locator('.reader p').count()>=18
 page.get_by_role('tab',name='10-question checkpoint').click()
 assert page.locator('.question').count()==10
 page.locator('[data-act="capstone"]').first.click()
 assert 'Independent reading challenges' in page.locator('h1').first.inner_text()
 assert page.locator('.question').count()==5
 for i in range(5):
  correct=page.evaluate('''i=>{const c=window.ATLAS_PATHWAY_CAPSTONES[0],q=c.questions[i],opts=[q[1],...q[2]],shift=(i+2)%4;return opts.slice(-shift).concat(opts.slice(0,-shift)).indexOf(q[1])}''',i)
  page.locator('.question').nth(i).locator('.option').nth(correct).click()
 page.locator('[data-act="grade-cap"]').click()
 assert 'First attempt 100%' in page.locator('.score').inner_text()
 page.locator('[data-act="retry-cap"]').click()
 # Retake fails but preserved first attempt
 page.locator('[data-act="grade-cap"]').click()
 assert 'First attempt 100%' in page.locator('.score').inner_text()
 out=Path(__file__).resolve().parents[1]/'docs'/'V4_BROWSER_SCREENSHOT.png'
 page.screenshot(path=str(out),full_page=False)
 print('C2 VIEW',page.locator('h1').first.inner_text(), 'screenshot',out)
 assert not errors,errors
 browser.close()
print('PASS browser: level loader, 10-item grading, writing save, human review, dashboard, advanced reading')
