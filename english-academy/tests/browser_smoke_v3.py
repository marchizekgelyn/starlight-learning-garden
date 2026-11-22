#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).resolve().parents[1]/'source'
script_files=['studio-data/manifest.js','assessment_v3/engine.js','assessment_v3/proofreading.js','assessment_v3/calibration.js','writing_engine.js','visuals.js','studio.js']
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 page=browser.new_page(viewport={'width':1360,'height':900})
 page.on('pageerror', lambda exc: errors.append(str(exc)))
 # Restricted test environment forbids local navigation; inject source into a browser DOM.
 css=(base/'studio.css').read_text()+'\n'+(base/'assessment_v3'/'assessment.css').read_text()
 page.set_content('<!doctype html><html><head><title>ATLAS English 3.0</title><style>'+css+'</style></head><body><div id="studio"></div></body></html>')
 # Simulate the file:// script loader using the exact generated file contents.
 sources={f: (base/f).read_text() for f in ['studio-data/level_pk.js','studio-data/level_4.js','assessment_v3/tasks/level_pk.js','assessment_v3/tasks/level_4.js']}
 page.evaluate('''sources => { window.__sourceFiles = sources; const native = document.head.appendChild.bind(document.head);
 document.head.appendChild = function(el) { if (el.tagName === 'SCRIPT' && el.src) {
 const name=Object.keys(window.__sourceFiles).find(k => el.src.endsWith(k));
 if (name) { (0,eval)(window.__sourceFiles[name]); queueMicrotask(()=>el.onload&&el.onload()); return el; }
 } return native(el); }; }''',sources)
 for f in script_files:page.add_script_tag(content=(base/f).read_text())
 page.wait_for_timeout(900)
 print('TITLE',page.title())
 print('HOME',page.locator('body').inner_text()[:270])
 page.locator('.atlas-sidebar [data-action="view"][data-view="paper"]').click()
 page.wait_for_function("!!window.ATLAS_WRITING_TASKS && !!window.ATLAS_WRITING_TASKS.PK",timeout=20000)
 page.wait_for_timeout(200)
 assert page.locator('#paper-level').count()==1
 assert page.locator('#paper-lesson option').count()==96
 assert page.locator('#paper-task-choice option').count()==8
 page.locator('[data-action="choose-paper-task"]').click()
 assert page.locator('#paper-reference').input_value()
 assert 'Retell' in page.locator('#paper-prompt').input_value()
 page.locator('#paper-text').fill('Nia was in class with picture cards. The bell and boat both begin with the same b sound. She tapped the sound twice because she wanted the class to hear the matching first sound. Her classmates then found two matching words. I can tell that she noticed sounds in words, but that does not mean all letters always sound the same.')
 page.locator('[data-action="paper-grade"]').click()
 assert 'rubric' in page.locator('#paper-result').inner_text().lower()
 score=page.locator('#paper-result h2').first.inner_text()
 print('SCORE',score)
 page.locator('#paper-human-score').fill('83')
 page.locator('#paper-human-note').fill('Good explanation. Check punctuation and keep evidence tied to text.')
 page.locator('[data-action="save-paper-human"]').click()
 assert 'Reviewed papers' in page.locator('.v3-calibration-stats').inner_text()
 print('PARENT',page.locator('.v3-calibration-stats').inner_text())
 page.locator('#paper-level').select_option('4')
 page.wait_for_function("!!window.ATLAS_WRITING_TASKS['4']",timeout=20000)
 assert page.locator('#paper-lesson option').count()==96
 page.locator('#paper-task-choice').select_option(index=3)
 page.locator('[data-action="choose-paper-task"]').click()
 assert page.locator('#paper-mode').input_value()=='page'
 print('MODE',page.locator('#paper-mode').input_value())
 out=Path(__file__).resolve().parents[1]/'docs'/'V3_BROWSER_SCREENSHOT.png'
 page.screenshot(path=str(out),full_page=False)
 print('SCREENSHOT',out)
 print('PAGE ERRORS',errors[:5]);assert not errors,errors
 browser.close()
