from pathlib import Path
import base64,re,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent.parent
cache={}
def module_url(filename):
 if filename in cache:return cache[filename]
 text=(ROOT/'js'/filename).read_text()
 text=re.sub(r"from\s+(['\"])(\./[^'\"]+)\1",lambda m:"from '"+module_url(m.group(2)[2:])+"'",text)
 text=re.sub(r"import\((['\"])(\./[^'\"]+)\1\)",lambda m:"import('"+module_url(m.group(2)[2:])+"')",text)
 cache[filename]='data:text/javascript;base64,'+base64.b64encode(text.encode()).decode()
 return cache[filename]
html=(ROOT/'index.html').read_text()
html=html.replace('<link rel="stylesheet" href="css/app.css" />','<style>'+(ROOT/'css/app.css').read_text()+'</style>')
visuals=(ROOT/'data/visual-library.json').read_text()
# We do not alter the shipped app: mock only a local file fetch for about:blank browser testing.
mock='<script>window.fetch=async ()=>({ok:true,json:async()=>('+visuals+')});</script>'
html=html.replace('<script type="module" src="js/app.js"></script>',mock+'<script type="module" src="'+module_url('app.js')+'"></script>')
methodGroups={'algebra':['quadratic','root','percent','change'],'calculus':['derivative','numericalDerivative','integral','antiderivative','limit','taylor','summation'],'linear':['matrix','linear','eigen'],'statistics':['stats','regression'],'probability':['binomial','poisson','normal','quantile','confidence'],'utilities':['fraction','bases','integer','date']}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-web-security'])
 page=b.new_page(viewport={'width':1440,'height':900})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)[:500]))
 page.set_content(html,wait_until='domcontentloaded',timeout=20000)
 page.wait_for_function("document.querySelectorAll('.calc-key').length===42",timeout=10000)
 assert page.locator('.topbar .menu-btn').is_hidden(),'Menu should be hidden on wide desktop'
 completed=[]
 for view,keys in methodGroups.items():
  page.locator(f'.nav-link[data-view="{view}"]').click()
  for key in keys:
   page.locator(f'#tool-options-{view} [data-method="{key}"]').click()
   page.locator(f'#tool-layout-{view} .tool-form .primary-btn').click()
   page.wait_for_timeout(30)
   err=page.locator(f'#tool-result-{view} .error-message')
   if err.count():raise RuntimeError(f'{view}/{key}: {err.inner_text()}')
   completed.append(key)
 print('Guided mathematics browser forms passing:',len(completed))
 page.locator('.nav-link[data-view="finance"]').click()
 fin=[]
 buttons=page.locator('#finance-list .finance-option')
 count=buttons.count()
 for i in range(count):
  page.locator('#finance-list .finance-option').nth(i).click()
  title=page.locator('#finance-title').inner_text()
  page.locator('#finance-form .primary-btn').click();page.wait_for_timeout(18)
  err=page.locator('#finance-result .error-message')
  if err.count():raise RuntimeError('finance '+title+': '+err.inner_text())
  fin.append(title)
 print('Guided finance browser forms passing:',len(fin))
 page.locator('.nav-link[data-view="visuals"]').click()
 page.wait_for_timeout(260)
 print('Atlas initial cards',page.locator('#atlas-gallery .atlas-card').count())
 assert page.locator('#atlas-gallery .atlas-card').count()==18
 page.locator('#atlas-gallery .atlas-card').first.click()
 assert page.locator('#atlas-dialog').evaluate('(el)=>el.open')
 page.locator('#dialog-close').click()
 page.locator('#atlas-query').fill('derivative')
 print('Atlas filtered label',repr(page.locator('#atlas-count').inner_text()));assert 'diagram' in page.locator('#atlas-count').inner_text().lower()
 page.screenshot(path=str(ROOT/'docs/atlas-preview.png'),full_page=False)
 print('Atlas browser: PASS')
 page.keyboard.press('Control+k')
 assert page.locator('#command-dialog').evaluate('(el)=>el.open')
 page.locator('#command-query').fill('loan')
 assert page.locator('#command-results .command-entry').count()>=1
 page.locator('#command-close').click()
 print('Command search: PASS')
 mobile=b.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 mobile_errors=[];mobile.on('pageerror',lambda e:mobile_errors.append(str(e)))
 mobile.set_content(html,wait_until='domcontentloaded',timeout=20000)
 mobile.wait_for_function("document.querySelectorAll('.calc-key').length===42",timeout=10000)
 assert mobile.locator('.topbar .menu-btn').is_visible()
 mobile.locator('#menu-toggle').click()
 assert mobile.locator('#sidebar').evaluate('(el)=>el.classList.contains("open")')
 mobile.locator('.nav-link[data-view="finance"]').click()
 assert mobile.locator('#view-finance').evaluate('(el)=>el.classList.contains("active")')
 mobile.evaluate('window.scrollTo(0,0)')
 mobile.wait_for_timeout(350)
 mobile.screenshot(path=str(ROOT/'docs/mobile-preview.png'),full_page=False)
 print('Mobile navigation: PASS')
 print('JavaScript page errors:',errors[:3], 'mobile errors:',mobile_errors[:3])
 assert not errors and not mobile_errors
 b.close()
