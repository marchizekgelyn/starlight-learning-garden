#!/usr/bin/env python3
"""Produce 716 topic-specific mathematical illustrations as high-resolution PNGs.
All graphics are deterministic, calculated from the same lesson metadata used in the app.
"""
import math,random,json,pathlib,textwrap,sys,time
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from generate_syllabus import make
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'assets/visuals';OUT.mkdir(exist_ok=True,parents=True)
W,H=1260,780
font_file='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT={size:ImageFont.truetype(font_file,size) for size in range(14,39)}
BOLD={size:ImageFont.truetype(font_bold,size) for size in range(14,39)}
C={'navy':(11,27,49),'panel':(16,38,62),'grid':(45,69,91),'line':(57,219,236),'purple':(154,134,255),'gold':(255,185,106),'mint':(116,244,194),'white':(240,248,255),'muted':(162,185,207),'red':(250,118,130)}

def background():
  x=np.arange(W)[None,:];y=np.arange(H)[:,None]
  field=((x/W)*14+(y/H)*22).astype(np.uint8)
  a=np.empty((H,W,3),dtype=np.uint8)
  a[:,:,0]=np.clip(8+field//5,0,255);a[:,:,1]=np.clip(21+field//2,0,255);a[:,:,2]=np.clip(42+field,0,255)
  return Image.fromarray(a,'RGB')
BASE=background()

def rounded(d,box,fill,outline=None,r=16,width=2):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def txt(d,point,text,size=23,color='white',bold=False,anchor=None):d.text(point,str(text),font=(BOLD if bold else FONT)[size],fill=C.get(color,color),anchor=anchor)
def wrap_line(d,text,x,y,max_chars=44,max_lines=3,size=19,color='muted',dy=31):
    text=' '.join(str(text).split())
    lines=textwrap.wrap(text,max_chars,break_long_words=False,break_on_hyphens=False)
    for line in lines[:max_lines]:txt(d,(x,y),line,size,color);y+=dy
    return y

def draw_frame(d,i,grade,title,family,ex,steps,context):
    rounded(d,(27,26,W-27,H-27),(11,29,49),C['grid'],r=25)
    rounded(d,(52,51,W-52,111),(23,48,74),r=12)
    txt(d,(76,68),'ATLAS   /   MATHEMATICS   VISUAL LIBRARY',20,'mint',True)
    txt(d,(W-79,68),f'GRADE / TRACK {grade+1:02}',20,'muted',True,anchor='ra')
    name=title if len(title)<64 else title[:61]+'...'
    txt(d,(67,144),name,31,'white',True)
    txt(d,(67,197),f'TOPIC FAMILY  /  {family.upper().replace("_"," ")}',18,'purple',True)
    rounded(d,(54,241,802,698),C['panel'],C['grid'],r=18)
    rounded(d,(825,241,1205,698),(18,43,68),C['grid'],r=18)
    txt(d,(853,267),'GUIDED EXAMPLE',20,'mint',True)
    wrap_line(d,ex,853,319,37,4,20,'white',31)
    txt(d,(853,449),'METHOD',19,'gold',True)
    yy=487
    for n,step in enumerate(steps[:3]):
      yy=wrap_line(d,f'{n+1}. {step}',853,yy,40,2,18,'muted',25)+10
    d.line((66,713,W-68,713),fill=C['grid'],width=2)
    txt(d,(72,719),'INTERACTIVE CONCEPT ATLAS  •  GENERATED FROM VERIFIED MATH RULES',15,'muted')
    txt(d,(W-75,719),f'FIGURE {i+1:04}',15,'muted',anchor='ra')

def ax_grid(d,l,t,r,b,zero=True):
    ww=r-l;hh=b-t
    for j in range(9):
      x=l+j*ww/8;d.line((x,t,x,b),fill=C['grid'],width=1)
    for j in range(7):
      y=t+j*hh/6;d.line((l,y,r,y),fill=C['grid'],width=1)
    if zero:
      d.line((l,(t+b)/2,r,(t+b)/2),fill=C['muted'],width=2)
      d.line(((l+r)/2,t,(l+r)/2,b),fill=C['muted'],width=2)

def poly(d,pts,color='line',width=5):
    if len(pts)>1:d.line(pts,fill=C.get(color,color),width=width,joint='curve')

def graph(d,family,rng):
    l,t,r,b=102,279,765,638;ax_grid(d,l,t,r,b,True)
    xm=(l+r)/2;ym=(t+b)/2;scale_x=29;scale_y=29
    def cx(x):return xm+x*scale_x
    def cy(y):return ym-y*scale_y
    def plot(f,col='line',lo=-9,hi=9):
      path=[]
      for k in range(550):
        x=lo+(hi-lo)*k/549
        try:y=f(x)
        except (ValueError,ZeroDivisionError,OverflowError):y=float('nan')
        if math.isfinite(y) and -6.6<y<6.6:
          p=(cx(x),cy(y))
          if path and abs(path[-1][1]-p[1])>95:poly(d,path,col,4);path=[]
          path.append(p)
        else:poly(d,path,col,4);path=[]
      poly(d,path,col,4)
    k=rng.randint(1,5)
    if family in ('linear','functions'):
      plot(lambda x:.5*x+(k-3)/2);plot(lambda x:-.3*x+1,'purple');txt(d,(118,295),'y = mx + b',21,'gold',True)
    elif family in ('quadratic','polynomial','powers','radical','roots'):
      plot(lambda x:(x-(k-3))**2/5-2);plot(lambda x:(x+(k-3))**2/8-1,'purple');txt(d,(118,295),'PARABOLA / TRANSFORMATION',18,'gold',True)
    elif family in ('trig','polar'):
      plot(lambda x:3*math.sin(x+(k-3)*.2));plot(lambda x:3*math.cos(x),'purple');txt(d,(118,295),'SINUSOIDAL PERIODICITY',18,'gold',True)
    elif family in ('exp','finance'):
      plot(lambda x:3*(1.08**(x*2)-1));plot(lambda x:3*(1+.15*x),'purple');txt(d,(118,295),'LINEAR vs COMPOUND GROWTH',17,'gold',True)
    elif family=='log':
      plot(lambda x:2*math.log(x),lo=.01,hi=9);plot(lambda x:2*math.sqrt(x)-2,'purple',lo=0,hi=9);txt(d,(118,295),'LOGARITHMIC GROWTH',19,'gold',True)
    elif family in ('rational','limit'):
      plot(lambda x:2/(x-1),lo=-8,hi=9);d.line((cx(1),t,cx(1),b),fill=C['gold'],width=2);txt(d,(118,295),'LIMITS & ASYMPTOTES',19,'gold',True)
    elif family in ('derivative','applications_derivative'):
      plot(lambda x:(x*x)/6-2);X=2+(k-3)*.3;Y=X*X/6-2;M=X/3
      x1,x2=X-4,X+4;d.line((cx(x1),cy(Y+M*(x1-X)),cx(x2),cy(Y+M*(x2-X))),fill=C['gold'],width=3)
      d.ellipse((cx(X)-8,cy(Y)-8,cx(X)+8,cy(Y)+8),fill=C['white']);txt(d,(118,295),'TANGENT = INSTANTANEOUS SLOPE',17,'gold',True)
    elif family in ('integral','ftc'):
      plot(lambda x:(x*x)/8+1);a,bb=-2,3
      for x in np.arange(a,bb,.055):d.line((cx(x),cy(0),cx(x),cy(x*x/8+1)),fill=(30,100,118),width=2)
      plot(lambda x:(x*x)/8+1,'gold');txt(d,(118,295),'SIGNED ACCUMULATED AREA',18,'gold',True)
    elif family=='series':
      for n in range(1,9):
        y=3-5/n;x=n-.5;d.ellipse((cx(x)-5,cy(y)-5,cx(x)+5,cy(y)+5),fill=C['line'])
      d.line((l,cy(3),r,cy(3)),fill=C['gold'],width=2);txt(d,(118,295),'SEQUENCE APPROACHING A LIMIT',17,'gold',True)
    elif family in ('parametric','arc','vector'):
      pts=[(cx(3*math.cos(th)),cy(2*math.sin(th))) for th in [i*2*math.pi/360 for i in range(361)]]
      poly(d,pts,'line',5)
      for th in [0,math.pi/2,math.pi]:
        x,y=cx(3*math.cos(th)),cy(2*math.sin(th));d.ellipse((x-8,y-8,x+8,y+8),fill=C['gold'])
      txt(d,(118,295),'PARAMETRIC PATH / VECTORS',17,'gold',True)
    elif family=='differential':
      for v in range(-6,7):
       for u in range(-9,10):
        x,y=cx(u),cy(v);m=-.15*v+.35*u;theta=math.atan(m);dd=10
        d.line((x-dd*math.cos(theta),y+dd*math.sin(theta),x+dd*math.cos(theta),y-dd*math.sin(theta)),fill=C['line'],width=2)
      txt(d,(118,295),'SLOPE FIELD',19,'gold',True)
    else:
      plot(lambda x:2.3*math.sin(x));txt(d,(118,295),'REAL-VALUED FUNCTION',19,'gold',True)
    for i in range(-8,9,4):txt(d,(cx(i),ym+20),str(i),15,'muted',anchor='mm')

def numberline(d,rng,family):
    l,r=109,741;y=468;d.line((l,y,r,y),fill=C['muted'],width=4)
    for v in range(-5,12):
      x=l+(v+5)*(r-l)/16;d.line((x,y-11,x,y+11),fill=C['muted'],width=2)
      txt(d,(x,y+24),str(v),18,'muted',anchor='mt')
    a=rng.randint(-3,4);b=rng.randint(2,6)
    x1=l+(a+5)*(r-l)/16;x2=l+(a+b+5)*(r-l)/16
    d.line((x1,y-65,x2,y-65),fill=C['line'],width=5)
    d.polygon([(x2,y-65),(x2-20,y-76),(x2-20,y-54)],fill=C['line'])
    d.ellipse((x1-9,y-9,x1+9,y+9),fill=C['gold']);d.ellipse((x2-10,y-10,x2+10,y+10),fill=C['line'])
    txt(d,(110,309),'NUMBER LINE / POSITION & CHANGE',19,'gold',True)
    txt(d,(295,368),f'{a} + {b} = {a+b}',35,'white',True)
    txt(d,(141,614),'Each tick mark represents one unit.',21,'muted')

def grid_blocks(d,rng,family):
    a=rng.randint(3,8);b=rng.randint(3,7);size=42;left=130;top=346
    for yy in range(b):
      for xx in range(a):
        x=left+xx*(size+7);y=top+yy*(size+7)
        rounded(d,(x,y,x+size,y+size),C['line'] if (xx+yy)%3 else C['purple'],r=6)
    txt(d,(115,293),'ARRAY MODEL  /  MULTIPLICATION',20,'gold',True)
    txt(d,(512,375),f'{a} × {b}',35,'white',True)
    txt(d,(512,427),f'= {a*b}',35,'mint',True)
    txt(d,(130,652),f'{b} rows of {a} equal units',21,'muted')

def fraction_diagram(d,rng):
    a=rng.randint(1,5);n=rng.randint(a+1,9)
    cx,cy=428,472;rad=175
    colors=[C['line'] if i<a else (47,72,94) for i in range(n)]
    for j in range(n):
      p=[]
      for v in range(26):
        angle=-math.pi/2+2*math.pi*(j+v/25)/n;p.append((cx+rad*math.cos(angle),cy+rad*math.sin(angle)))
      d.polygon([(cx,cy)]+p,fill=colors[j],outline=C['navy'],width=4)
    txt(d,(112,291),'FRACTION CIRCLE / PART OF A WHOLE',18,'gold',True)
    txt(d,(427,469),f'{a}/{n}',31,'white',True,anchor='mm')
    txt(d,(186,681),f'{a} of {n} equal sectors are selected',20,'muted')

def histogram(d,rng):
    data=[rng.randint(2,13) for _ in range(8)];left=133;floor=626;maxv=max(data)
    ax_grid(d,119,334,750,639,False)
    for idx,v in enumerate(data):
      x=139+idx*76;y=floor-v/maxv*255
      rounded(d,(x,y,x+52,floor),C['line'] if idx%2 else C['purple'],r=5)
      txt(d,(x+26,y-24),str(v),18,'white',anchor='mt')
    txt(d,(128,297),'FREQUENCIES / MEASURES OF CENTER',19,'gold',True)
    txt(d,(147,668),f'Mean = {sum(data)/len(data):.2f}  •  Sample size {len(data)}',20,'muted')

def geometric(d,rng,family):
    if family=='angle':
      x,y=360,546;length=230;a=rng.randint(30,125)*math.pi/180
      d.line((x,y,x+length,y),fill=C['mint'],width=6)
      d.line((x,y,x+length*math.cos(a),y-length*math.sin(a)),fill=C['line'],width=6)
      d.arc((x-87,y-87,x+87,y+87),180+(-a*180/math.pi),360,fill=C['gold'],width=3)
      txt(d,(129,314),'ANGLES / TWO RAYS, ONE VERTEX',19,'gold',True)
      txt(d,(470,552),f'{int(a*180/math.pi)} degrees',24,'white',True)
    elif family=='pythag':
      pts=[(235,610),(619,610),(235,322)];d.polygon(pts,fill=(20,85,110),outline=C['line'],width=5)
      d.line((235,610,296,610,296,549,235,549),fill=C['gold'],width=3)
      txt(d,(416,634),'4',25,'white',True);txt(d,(193,456),'3',25,'white',True);txt(d,(449,439),'5',25,'mint',True)
      txt(d,(128,292),'RIGHT TRIANGLE / 3² + 4² = 5²',20,'gold',True)
    elif family=='volume':
      pts=[(250,400),(480,400),(580,330),(350,330)];d.polygon(pts,fill=(21,104,132),outline=C['line'],width=5)
      d.polygon([(250,400),(480,400),(480,613),(250,613)],fill=(24,78,110),outline=C['line'],width=5)
      d.polygon([(480,400),(580,330),(580,543),(480,613)],fill=(65,80,147),outline=C['purple'],width=5)
      txt(d,(155,292),'VOLUME / THREE-DIMENSIONAL PRISM',18,'gold',True)
      txt(d,(190,678),'Volume = length × width × height',20,'muted')
    else:
      x,y=245,361;w,h=365,249
      rounded(d,(x,y,x+w,y+h),(23,88,126),C['line'],r=7,width=5)
      for i in range(1,7):d.line((x+i*w/7,y,x+i*w/7,y+h),fill=C['grid'],width=2)
      for j in range(1,5):d.line((x,y+j*h/5,x+w,y+j*h/5),fill=C['grid'],width=2)
      txt(d,(130,292),'SHAPE / AREA & SPATIAL REASONING',19,'gold',True)
      txt(d,(330,636),'Area = width × height',20,'white',True)

def percentage(d,rng):
    val=rng.randrange(10,91,5);left=151;top=398
    for row in range(10):
      for col in range(10):
        idx=row*10+col;v=(C['line'] if idx<val else (51,71,91));x=left+col*45;y=top+row*24
        rounded(d,(x,y,x+39,y+19),v,r=3)
    txt(d,(110,294),'PERCENT GRID  /  100 EQUAL UNITS',20,'gold',True)
    txt(d,(620,463),f'{val}%',35,'mint',True)
    txt(d,(601,519),f'= {val}/100',22,'white')

def draw_visual(i,item,lesson):
    rng=random.Random(i*191+501)
    image=BASE.copy();d=ImageDraw.Draw(image)
    family=item['family']
    draw_frame(d,i,item['gradeIndex'],item['topic'],family,lesson['example'],lesson['steps'],item['caption'])
    graph_set={'linear','functions','quadratic','polynomial','powers','radical','roots','trig','polar','exp','finance','log','rational','limit','derivative','applications_derivative','integral','ftc','series','parametric','arc','vector','differential'}
    if family in graph_set:graph(d,family,rng)
    elif family in ('count','place','integer','add','subtract','time','measure'):numberline(d,rng,family)
    elif family in ('multiply','divide','ratio','matrix','algebra'):grid_blocks(d,rng,family)
    elif family in ('fraction',):fraction_diagram(d,rng)
    elif family in ('decimal','percent','money'):percentage(d,rng)
    elif family in ('stats','prob','sequence'):histogram(d,rng)
    else:geometric(d,rng,family)
    return image

def main():
    lessons,visuals,_=make();all_lessons=[l for sub in lessons for l in sub]
    begin=time.perf_counter()
    for i,(item,lesson) in enumerate(zip(visuals,all_lessons)):
        path=ROOT/item['image']
        img=draw_visual(i,item,lesson);img.save(path,format='PNG',compress_level=6)
        if i%80==0:print('Rendered',i+1,'of',len(visuals),'PNG size',path.stat().st_size,'elapsed',round(time.perf_counter()-begin,1),'s',flush=True)
    size=sum((ROOT/v['image']).stat().st_size for v in visuals)
    print('DONE',len(visuals),'visuals, total',round(size/1048576,2),'MiB','elapsed',round(time.perf_counter()-begin,1),'s')
if __name__=='__main__':main()
