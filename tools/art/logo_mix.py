import math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
f=TTFont('/home/claude/fonts/node_modules/@fontsource/jost/files/jost-latin-700-normal.woff2')
gs=f.getGlyphSet(); cmap=f.getBestCmap()
S=0.2; BASE=300; TOP=BASE-700*S
GREEN='#1E6B47'; AU='#D4AF37'; INK='#2A1A14'
ADV={}; PATH={}; X0={}
x=40
for ch in 'THOMAS':
    g=gs[cmap[ord(ch)]]; p=SVGPathPen(gs); g.draw(p); PATH[ch]=p.getCommands(); ADV[ch]=g.width
    X0[ch]=x; x+=g.width*S+6
W=x+60
def gx(ch,ux): return X0[ch]+ux*S
def gy(uy): return BASE-uy*S
def glyphs(fill,dx=0,dy=0):
    return ''.join(f'<path d="{PATH[c]}" transform="translate({X0[c]+dx:.1f},{BASE+dy}) scale({S},{-S})" fill="{fill}"/>' for c in 'THOMAS')

PERIOD=2.0
def A(mode,t,kind,px=0,py=0,ph=0.0,amp=1.0):
    if mode=='css':
        d=f' style="animation-delay:{-ph*PERIOD:.2f}s"' if ph else ''
        return f' class="{kind}"{d}'
    s=math.sin(2*math.pi*(t+ph))
    if kind=='bob': return f' transform="translate(0,{-2-3*s*amp:.2f})"'
    if kind=='swing': return f' transform="rotate({18*s:.1f} {px} {py})"'
    if kind=='wag': return f' transform="rotate({16*math.sin(4*math.pi*(t+ph)):.1f} {px} {py})"'
    if kind=='swish': return f' transform="rotate({12*s:.1f} {px} {py})"'
    if kind=='tilt': return f' transform="rotate({7*s:.1f} {px} {py})"'
    if kind=='bounce':
        u=(t+ph)%0.5/0.5; return f' transform="translate(0,{-22*math.sin(math.pi*u):.1f})"'
    if kind=='blink':
        u=(t+ph)%0.5/0.5; return f' opacity="{1 if u<0.5 else 0.25}"'
    if kind=='crumb':
        u=(t+ph)%1; return f' transform="translate(0,{u*26:.1f})" opacity="{max(0,1-u):.2f}"'
    if kind=='hover':
        return f' transform="translate({3*math.sin(2*math.pi*(t+ph)):.1f},{-4*math.sin(4*math.pi*(t+ph)):.1f})"'
    if kind=='peek':
        u=(t+ph)%1; y=0
        if u<0.25: y=14*math.sin(math.pi*u/0.25)
        return f' transform="translate(0,{y:.1f})"'
    return ''
CSS='''@keyframes bob{0%,100%{transform:translateY(-2px)}50%{transform:translateY(-5px)}}
@keyframes swing{0%,100%{transform:rotate(-18deg)}50%{transform:rotate(18deg)}}
@keyframes wag{0%,100%{transform:rotate(-16deg)}50%{transform:rotate(16deg)}}
@keyframes swish{0%,100%{transform:rotate(-12deg)}50%{transform:rotate(12deg)}}
@keyframes tilt{0%,100%{transform:rotate(-7deg)}50%{transform:rotate(7deg)}}
@keyframes peek{0%{transform:translateY(0)}12%{transform:translateY(14px)}25%{transform:translateY(0)}100%{transform:translateY(0)}}
.bob{animation:bob 2s ease-in-out infinite}
.swing{transform-box:fill-box;transform-origin:50% 0;animation:swing 2s ease-in-out infinite}
.wag{transform-box:fill-box;transform-origin:0% 100%;animation:wag 1s ease-in-out infinite}
.swish{transform-box:fill-box;transform-origin:50% 0;animation:swish 2s ease-in-out infinite}
.tilt{transform-box:fill-box;transform-origin:50% 100%;animation:tilt 2s ease-in-out infinite}
.peek{animation:peek 2s ease-in-out infinite}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-22px)}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.25}}
@keyframes crumb{0%{transform:translateY(0);opacity:1}100%{transform:translateY(26px);opacity:0}}
@keyframes hover{0%,100%{transform:translate(0,0)}25%{transform:translate(3px,-4px)}50%{transform:translate(0,0)}75%{transform:translate(-3px,-4px)}}
.bounce{animation:bounce 1s ease-in-out infinite}
.blink{animation:blink 1s steps(1) infinite}
.crumb{animation:crumb 2s linear infinite}
.hover{animation:hover 2s ease-in-out infinite}
@media (prefers-reduced-motion: reduce){.bob,.swing,.wag,.swish,.tilt,.peek,.bounce,.blink,.crumb,.hover{animation:none}}'''

def happy(s=1,c=INK,w=2.6): return f'<path d="M{-11*s:.1f},{2*s:.1f} q{4*s:.1f},{-5*s:.1f} {8*s:.1f},0 M{3*s:.1f},{2*s:.1f} q{4*s:.1f},{-5*s:.1f} {8*s:.1f},0" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
def curls(l,c): return ''.join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="{c}"/>' for a,b,r in l)
def cheeks(d=16,c='#E58A6E'): return f'<circle cx="{-d}" cy="9" r="4.5" fill="{c}" opacity="0.5"/><circle cx="{d}" cy="9" r="4.5" fill="{c}" opacity="0.5"/>'
shades='<g fill="#15151A"><rect x="-24" y="-8" width="20" height="13" rx="5"/><rect x="4" y="-8" width="20" height="13" rx="5"/></g><path d="M-4,-4 L4,-4" stroke="#15151A" stroke-width="2.5"/><path d="M-20,-5 L-15,-5 M8,-5 L13,-5" stroke="#FFF" stroke-width="1.5" opacity="0.5" stroke-linecap="round"/>'
cat_shades='<g fill="#1B1B22" stroke="#5E8F86" stroke-width="2"><path d="M-25,-6 Q-14,-11 -4,-6 Q-5,4 -14,5 Q-23,4 -25,-6 Z"/><path d="M4,-6 Q14,-11 25,-6 Q23,4 14,5 Q5,4 4,-6 Z"/></g><path d="M-4,-5 Q0,-8 4,-5" fill="none" stroke="#5E8F86" stroke-width="2"/>'
SHAJAN=f'''<circle cx="-29" cy="2" r="6" fill="#A06A47"/><circle cx="29" cy="2" r="6" fill="#A06A47"/><circle r="29" fill="#A06A47"/>
<path d="M-14,-22 Q-6,-27 2,-25" fill="none" stroke="#FFF" stroke-width="3" opacity="0.35" stroke-linecap="round"/>
<path d="M-27,4 Q-27,36 0,38 Q27,36 27,4 Q22,12 14,10 Q0,8 -14,10 Q-22,12 -27,4 Z" fill="#D8D3CB"/>
<path d="M-12,10 Q0,4 12,10 Q6,14 0,12 Q-6,14 -12,10 Z" fill="#9A938A"/>
<path d="M-8,18 Q0,25 8,18" fill="none" stroke="#5A3020" stroke-width="2.4" stroke-linecap="round"/>{shades}<path d="M-21,-1 H-7 M7,-1 H21" stroke="#38E1F2" stroke-width="1.6" stroke-linecap="round" opacity="0.9"/><rect x="9" y="-6" width="6" height="3" rx="1" fill="#38E1F2" opacity="0.8"/>'''
ABBY=f'''{curls([(-30,-20,12),(-36,-2,12),(-36,16,12),(-32,32,11),(30,-20,12),(36,-2,12),(36,16,12),(32,32,11),(-18,-32,12),(0,-36,12),(18,-32,12)],'#C2935A')}
{curls([(-34,8,5),(34,8,5),(-10,-36,5),(12,-34,5)],'#DDB47A')}<circle r="27" fill="#F0CDB2"/>
{curls([(-22,-16,9),(-10,-24,9),(4,-25,9),(17,-20,9),(25,-8,7),(-25,-6,7)],'#C2935A')}
<path d="M-11,11 Q0,26 11,11 Z" fill="#FFF" stroke="#9A3B3B" stroke-width="2"/>{cheeks(18,'#E58A80')}{cat_shades}<path d="M-30,-18 Q0,-44 30,-18 Q0,-32 -30,-18 Z" fill="#C8423A"/>{''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="#FAF7F2"/>' for x,y in [(-20,-25),(-8,-31),(4,-32),(16,-28),(24,-22),(-2,-26),(12,-23)])}<path d="M18,-32 L30,-44 L32,-30 Z M18,-32 L36,-30 L28,-22 Z" fill="#C8423A"/><circle cx="18" cy="-32" r="3.5" fill="#A83530"/><circle cx="28" cy="-38" r="1.6" fill="#FAF7F2"/>'''
EVALYN=f'''{curls([(-26,-24,11),(-34,-8,11),(-36,10,11),(-34,28,10),(26,-24,11),(34,-8,11),(36,10,11),(34,28,10),(-12,-34,11),(6,-36,11),(20,-32,10)],'#16100C')}
<circle r="25" fill="#A9714E"/>{curls([(-20,-16,8),(-8,-24,8),(6,-24,8),(18,-18,8),(24,-6,6),(-24,-6,6)],'#16100C')}
<circle cx="-25" cy="12" r="4" fill="none" stroke="#E2B84A" stroke-width="2"/><circle cx="25" cy="12" r="4" fill="none" stroke="#E2B84A" stroke-width="2"/>
{happy(0.9)}<path d="M-6,10 q6,6 12,0" fill="none" stroke="#7A2A1E" stroke-width="2.2" stroke-linecap="round"/>{cheeks(15)}'''
GABRIEL=f'''{curls([(-15,-12,8),(-6,-18,8),(5,-18,8),(14,-12,8),(18,-3,6),(-18,-3,6),(0,-22,6)],'#6B4A32')}<circle r="19" fill="#D3A27F"/>
{curls([(-12,-14,6),(-3,-17,6),(7,-16,6),(14,-10,5)],'#6B4A32')}{happy(0.75)}<ellipse cx="0" cy="9" rx="4.5" ry="3.8" fill="#7A2A1E"/>{cheeks(13)}'''
EMMA_HEAD=f'''<path d="M-17,-4 Q-20,-22 0,-22 Q20,-22 17,-4 L19,26 H-19 Z" fill="#17100C"/><circle r="14.5" fill="#9A6343"/>
<path d="M-15,0 Q-15,-17 0,-16 Q14,-16 15,-1 Q8,-10 -2,-9 Q-10,-8 -15,0 Z" fill="#17100C"/>
{happy(0.55,INK,2)}<path d="M-5,5 Q0,12 5,5 Z" fill="#FFF" stroke="#7A2A1E" stroke-width="1.4"/><path d="M-15,0 Q-16,-19 0,-20 Q16,-19 15,0" fill="none" stroke="#141414" stroke-width="4.6"/><path d="M-15,0 Q-16,-19 0,-20 Q16,-19 15,0" fill="none" stroke="#D4AF37" stroke-width="2.8"/><path d="M-13,-9 Q0,-1 13,-9" fill="none" stroke="#141414" stroke-width="4"/><path d="M-13,-9 Q0,-1 13,-9" fill="none" stroke="#D4AF37" stroke-width="2.2"/><path d="M-14,9 Q0,19 14,9" fill="none" stroke="#141414" stroke-width="2.6"/><path d="M-14,9 Q0,19 14,9" fill="none" stroke="#D4AF37" stroke-width="1.4"/><ellipse cx="0" cy="15.5" rx="5" ry="3" fill="#D4AF37" stroke="#141414" stroke-width="1.2"/><ellipse cx="-17" cy="4" rx="7" ry="9" fill="#D4AF37" stroke="#141414" stroke-width="1.8"/><ellipse cx="-17" cy="4" rx="3.6" ry="5.2" fill="#141414"/><circle cx="-18.4" cy="1.7999999999999998" r="0.9" fill="#D4AF37"/><circle cx="-15.6" cy="1.7999999999999998" r="0.9" fill="#D4AF37"/><circle cx="-18.4" cy="4.6" r="0.9" fill="#D4AF37"/><circle cx="-15.6" cy="4.6" r="0.9" fill="#D4AF37"/><circle cx="-17" cy="7" r="0.9" fill="#D4AF37"/><ellipse cx="17" cy="4" rx="7" ry="9" fill="#D4AF37" stroke="#141414" stroke-width="1.8"/><ellipse cx="17" cy="4" rx="3.6" ry="5.2" fill="#141414"/><circle cx="15.6" cy="1.7999999999999998" r="0.9" fill="#D4AF37"/><circle cx="18.4" cy="1.7999999999999998" r="0.9" fill="#D4AF37"/><circle cx="15.6" cy="4.6" r="0.9" fill="#D4AF37"/><circle cx="18.4" cy="4.6" r="0.9" fill="#D4AF37"/><circle cx="17" cy="7" r="0.9" fill="#D4AF37"/>'''
def ASH(mode,t):
    return f'''<g{A(mode,t,'tilt',0,40,0.3)}>
<path d="M-42,62 Q-46,20 -22,12 H22 Q46,20 42,62 Z" fill="#F3E9D2"/>
<path d="M-44,34 H44 V42 H-44 Z M-45,50 H45 V56 H-45 Z" fill="#1E6B47"/>
<path d="M-44,44 H44 V48 H-44 Z" fill="#D4AF37"/>
<path d="M-30,20 l-4,8 M-20,18 l-2,9 M20,18 l2,9 M30,20 l4,8" stroke="#D8CDB4" stroke-width="2" stroke-linecap="round"/>
<path d="M-24,10 Q0,26 24,10 L22,20 Q0,34 -22,20 Z" fill="#D4AF37"/>
<path d="M-18,14 v8 M-10,17 v9 M-2,18 v9 M6,18 v9 M14,16 v8" stroke="#B8962A" stroke-width="1.6"/>
<path d="M-27,-14 Q-36,-34 -28,-44 Q-14,-36 -8,-26 Z" fill="#141414"/><path d="M-28,-44 Q-40,-42 -42,-30 Q-38,-26 -33,-33 Z" fill="#141414"/><path d="M-30,-40 Q-37,-38 -39,-32" fill="none" stroke="#2C2C2C" stroke-width="1.6"/>
<path d="M27,-14 Q36,-34 28,-44 Q14,-36 8,-26 Z" fill="#141414"/><path d="M28,-44 Q40,-42 42,-30 Q38,-26 33,-33 Z" fill="#141414"/><path d="M30,-40 Q37,-38 39,-32" fill="none" stroke="#2C2C2C" stroke-width="1.6"/>
<ellipse cx="0" cy="-8" rx="27" ry="25" fill="#171717"/>
<path d="M-15,-2 Q-13,24 -9,32 Q0,38 9,32 Q13,24 15,-2 Z" fill="#1E1E1E"/>
<path d="M-6,-20 Q0,-24 6,-20" fill="none" stroke="#2E2E2E" stroke-width="2" stroke-linecap="round"/>
<circle cx="-11" cy="-8" r="4.2" fill="#6B3B1E"/><circle cx="11" cy="-8" r="4.2" fill="#6B3B1E"/>
<circle cx="-11" cy="-8" r="2" fill="#0A0A0A"/><circle cx="11" cy="-8" r="2" fill="#0A0A0A"/>
<circle cx="-9.8" cy="-9.4" r="1.2" fill="#FFF"/><circle cx="12.2" cy="-9.4" r="1.2" fill="#FFF"/>
<path d="M-15,-14 Q-11,-17 -7,-14 M7,-14 Q11,-17 15,-14" fill="none" stroke="#3A3A3A" stroke-width="1.6" stroke-linecap="round"/>
<ellipse cx="0" cy="27" rx="9.5" ry="7" fill="#050505"/><ellipse cx="-3" cy="24.5" rx="3.2" ry="1.6" fill="#FFF" opacity="0.35"/>
<path d="M-17,34 Q0,54 17,34 Q0,42 -17,34 Z" fill="#0A0A0A"/>
<path d="M-7,41 Q0,52 7,41 Q0,44 -7,41 Z" fill="#E9707E"/>
<path d="M-12,37 l2,3 2,-3 M10,37 l2,3 2,-3" fill="#F5F0E6"/>
<path d="M0,34 V38" stroke="#2A2A2A" stroke-width="1.4"/>
</g>'''
def heart(x,y,sc,rot,c):
    return f'<path d="M0,6 C-9,0 -8,-7 -3,-7 C-1,-7 0,-5 0,-4 C0,-5 1,-7 3,-7 C8,-7 9,0 0,6 Z" fill="{c}" transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({sc})"/>'
def kpot(cx,top,w,h):
    x0=cx-w/2
    band=''.join(f'<path d="M{xx},{top+h*0.38} l3,3 -3,3 -3,-3 Z" fill="#141414"/>' for xx in range(int(x0+8),int(x0+w-6),9))
    return (f'<path d="M{x0},{top} H{x0+w} L{x0+w-8},{top+h} H{x0+8} Z" fill="#141414"/>'
            f'<rect x="{x0+3}" y="{top+h*0.38-6}" width="{w-6}" height="2" fill="#D4AF37"/><rect x="{x0+3}" y="{top+h*0.38-2}" width="{w-6}" height="10" fill="#D4AF37"/><rect x="{x0+4}" y="{top+h*0.38+10}" width="{w-8}" height="2" fill="#D4AF37"/>{band}'
            f'<rect x="{x0-4}" y="{top-6}" width="{w+8}" height="9" rx="3" fill="#141414"/>')
def build(mode='css',t=0.0,width=900):
    back=''; front=''
    # --- Shajan behind the T, arms draped over the crossbar
    tx=gx('T',(196+365)/2)
    back+=f'<g{A(mode,t,"bob",ph=0.0)}><g transform="translate({tx:.1f},{TOP-26}) scale(1.1)">{SHAJAN}</g></g>'
    dx_,dy_=tx+46,TOP-86
    front+=f'''<g{A(mode,t,"hover",ph=0.1)}><g transform="translate({dx_:.1f},{dy_})"><path d="M-16,-6 L16,6 M-16,6 L16,-6" stroke="#3A3A3A" stroke-width="2.5"/>
<ellipse cx="-17" cy="-7" rx="9" ry="2.2" fill="#9AA0A6" opacity="0.8"/><ellipse cx="17" cy="-7" rx="9" ry="2.2" fill="#9AA0A6" opacity="0.8"/><ellipse cx="-17" cy="5" rx="9" ry="2.2" fill="#9AA0A6" opacity="0.8"/><ellipse cx="17" cy="5" rx="9" ry="2.2" fill="#9AA0A6" opacity="0.8"/>
<rect x="-9" y="-5" width="18" height="10" rx="4" fill="#2B2F36"/><circle cx="0" cy="0" r="2.6" fill="#38E1F2"{A(mode,t,"blink",ph=0.0)}/><circle cx="0" cy="7" r="2.4" fill="#141414"/></g></g>'''
    for s in (-1,1):
        ax=tx+s*30
        front+=f'<g{A(mode,t,"bob",ph=0.0)}><rect x="{ax-9}" y="{TOP-8}" width="18" height="30" rx="8" fill="#7B8466"/><circle cx="{ax}" cy="{TOP+26}" r="8" fill="#A06A47"/></g>'
    # --- Rocky sitting on top of the H's right post, tail hanging in front
    rx=gx('O',410)
    front+=f'''<g{A(mode,t,'swish',rx+14,gy(716)+4,0.2)}><path d="M{rx+14:.1f},{gy(716)+4:.1f} q14,4 18,22 q2,10 10,10" fill="none" stroke="#7C7C80" stroke-width="6" stroke-linecap="round"/></g>
<g transform="translate({rx:.1f},{gy(716)+2:.1f})"><path d="M-16,0 Q-18,-26 0,-28 Q18,-26 16,0 Z" fill="#8A8A8F"/>
<rect x="-15" y="-24.5" width="30" height="6" rx="3" fill="#141414"/><path d="M-11.6,-19 L-9,-12.5 L-6.4,-19 Z" fill="#C9CDD2" stroke="#8E949B" stroke-width="0.6"/><path d="M-5.6,-19 L-3,-12.5 L-0.3999999999999999,-19 Z" fill="#C9CDD2" stroke="#8E949B" stroke-width="0.6"/><path d="M0.3999999999999999,-19 L3,-12.5 L5.6,-19 Z" fill="#C9CDD2" stroke="#8E949B" stroke-width="0.6"/><path d="M6.4,-19 L9,-12.5 L11.6,-19 Z" fill="#C9CDD2" stroke="#8E949B" stroke-width="0.6"/><circle cx="-12" cy="-21.5" r="1.1" fill="#E6E9EC"/><circle cx="-6" cy="-21.5" r="1.1" fill="#E6E9EC"/><circle cx="0" cy="-21.5" r="1.1" fill="#E6E9EC"/><circle cx="6" cy="-21.5" r="1.1" fill="#E6E9EC"/><circle cx="12" cy="-21.5" r="1.1" fill="#E6E9EC"/><circle cx="0" cy="-12" r="2.4" fill="#D4AF37"/><g transform="translate(0,-36)"><g{A(mode,t,'tilt',0,12,0.5)}><path d="M-15,-6 L-12,-24 L-2,-12 Z M15,-6 L12,-24 L2,-12 Z" fill="#7C7C80"/><path d="M-11,-9 L-10,-18 L-5,-12 Z M11,-9 L10,-18 L5,-12 Z" fill="#E9A0A8"/>
<circle r="16" fill="#8A8A8F"/>{happy(0.65,'#1d1d1d',2)}<path d="M-2.5,5 L2.5,5 L0,7.5 Z" fill="#E9A0A8"/><path d="M-7,6 L-20,4 M7,6 L20,4" stroke="#4a4a4a" stroke-width="1"/></g></g>
<ellipse cx="-8" cy="0" rx="6" ry="3.5" fill="#9A9AA0"/><ellipse cx="8" cy="0" rx="6" ry="3.5" fill="#9A9AA0"/></g>'''
    # --- Emma standing behind the H, jacket showing through its top, hands on both posts
    hx=gx('H',(243+544)/2)
    back+=f'''<g{A(mode,t,'bob',ph=0.25)}><path d="M{hx-34},{TOP+60} Q{hx-34},{TOP+4} {hx},{TOP+2} Q{hx+34},{TOP+4} {hx+34},{TOP+60} Z" fill="#C8922E"/>
<path d="M{hx-12},{TOP+3} L{hx},{TOP+22} L{hx+12},{TOP+3} Z" fill="#1E1E24"/>
<g transform="translate({hx:.1f},{TOP-26}) scale(1.75)">{EMMA_HEAD}</g></g>'''
    for sgn in (-1,1):
        ex=hx+sgn*47
        front+=f'<g{A(mode,t,"bob",ph=0.25)}>'+''.join(f'<rect x="{ex+i*7-10:.1f}" y="{TOP-10}" width="6.5" height="16" rx="3.2" fill="#9A6343" stroke="#00000030" stroke-width="1"/>' for i in range(3))+'</g>'
    # --- Gabriel peeking through the O's counter
    ox=gx('O',(213+608)/2); oy=gy((139+561)/2)
    back+=f'<g{A(mode,t,"peek",ph=0.6)}><g transform="translate({ox:.1f},{oy+6:.1f}) scale(1.35)">{GABRIEL}</g></g>'
    front+=''.join(f'<g{A(mode,t,"peek",ph=0.6)}><g transform="translate({ox+s*24:.1f},{gy(139)+2:.1f})"><circle r="7" fill="#D3A27F"/><path d="M-4,-3 v6 M0,-4 v7 M4,-3 v6" stroke="#00000025" stroke-width="1"/></g></g>' for s in (-1,1))
    ck_x,ck_y=ox+20,oy+26
    cookie=f'<circle r="13" fill="#C68B4E"/><circle r="13" fill="none" stroke="#A86E38" stroke-width="1.5"/><circle cx="-5" cy="-4" r="2.2" fill="#4A2A14"/><circle cx="4" cy="-6" r="2" fill="#4A2A14"/><circle cx="-2" cy="5" r="2.3" fill="#4A2A14"/><circle cx="6" cy="3" r="1.8" fill="#4A2A14"/><circle cx="-11" cy="-9" r="6" fill="#FAF7F2"/><circle cx="-6" cy="-12" r="4" fill="#FAF7F2"/>'
    front+=f'<g{A(mode,t,"peek",ph=0.6)}><g transform="translate({ck_x:.1f},{ck_y:.1f}) rotate(-15)">{cookie}</g><circle cx="{ck_x+10:.1f}" cy="{ck_y+10:.1f}" r="6" fill="#D3A27F"/></g>'
    front+=''.join(f'<g{A(mode,t,"crumb",ph=p)}><circle cx="{ck_x+dx:.1f}" cy="{ck_y+14:.1f}" r="1.8" fill="#A86E38"/></g>' for dx,p in [(-6,0),(2,0.35),(8,0.7)])
    # --- Abby nestled in the M's V
    mx=gx('M',445.5)
    back+=f'<g{A(mode,t,"tilt",mx,TOP+40,0.75)}><g transform="translate({mx:.1f},{TOP+10}) scale(1.08)">{ABBY}</g></g>'
    # --- Evalyn behind the A setting a bouncing volleyball, hands holding its legs, one thumbs-up
    ax=gx('A',368)
    back+=f'<g{A(mode,t,"bob",ph=0.4)}><g transform="translate({ax:.1f},{TOP-28}) scale(1.08)">{EVALYN}</g></g>'
    hands=''
    for sx in (-1,1):
        hx_=ax+sx*20; hy_=TOP-74
        hands+=f'<path d="M{ax+sx*30:.1f},{TOP-30} Q{ax+sx*34:.1f},{TOP-54} {hx_:.1f},{hy_+8}" fill="none" stroke="#1C1C22" stroke-width="9" stroke-linecap="round"/>'
        hands+=f'<g transform="translate({hx_:.1f},{hy_}) rotate({sx*-25})"><rect x="-7" y="-6" width="14" height="14" rx="5" fill="#A9714E"/>'+''.join(f'<rect x="{fx-1.6}" y="-13" width="3.4" height="9" rx="1.7" fill="#A9714E"/>' for fx in (-4.5,-1.2,2.1,5.2))+'</g>'
    front+=f'<g{A(mode,t,"bob",ph=0.4)}>{hands}</g>'
    vb=(f'<circle r="21" fill="#FFFFFF" stroke="#141414" stroke-width="2"/>'
        f'<path d="M-6,-20 Q-2,-4 -20,6 M-20,6 Q0,2 12,17 M12,17 Q4,0 18,-11 M18,-11 Q2,-6 -6,-20" fill="none" stroke="#141414" stroke-width="1.6"/>'
        f'<path d="M-6,-20 Q-2,-4 -20,6 Q-22,-12 -6,-20 Z" fill="#D4AF37"/>'
        f'<path d="M12,17 Q4,0 18,-11 Q22,6 12,17 Z" fill="#1E6B47"/>'
        f'<path d="M-20,6 Q0,2 12,17 Q-6,22 -20,6 Z" fill="#D4AF37"/>'
        f'<circle r="21" fill="none" stroke="#141414" stroke-width="2"/>')
    front+=f'<g{A(mode,t,"bounce",ph=0)}><g transform="translate({ax:.1f},{TOP-112})">{vb}</g></g>'
    # --- Ash: black German shepherd peeking over the S, paws in front, tail wagging out the other side
    sx=gx('S',330)
    tx0,ty0=gx('S',560),gy(260)
    back+=f'<g{A(mode,t,"wag",tx0,ty0,0)}><path d="M{tx0:.1f},{ty0:.1f} q34,-6 44,-34 q4,-10 -4,-8 q-8,18 -40,26 Z" fill="#151515"/></g>'
    back+=f'<g{A(mode,t,"bob",ph=0.15)}><g transform="translate({sx:.1f},{TOP-52}) scale(1.08)">{ASH(mode,t)}</g></g>'
    front+=f'<g{A(mode,t,"bob",ph=0.15)}>'+''.join(f'<ellipse cx="{sx+s*20:.1f}" cy="{TOP+4}" rx="11" ry="7" fill="#151515"/><path d="M{sx+s*20-5:.1f},{TOP+6} v3 M{sx+s*20:.1f},{TOP+7} v3 M{sx+s*20+5:.1f},{TOP+6} v3" stroke="#555" stroke-width="1.2"/>' for s in (-1,1))+'</g>'
    # --- houseplants woven through the letters
    G1,G2,G3,GOLD='#1E6B47','#2F8A5C','#4FA877','#D4AF37'
    def mleaf(x,y,sc,rot,c):
        leaf='M0,-46 C25,-46 50,-28 52,-3 C54,22 38,38 18,40 C9,40 3,35 0,26 C-3,35 -9,40 -18,40 C-38,38 -54,22 -52,-3 C-50,-28 -25,-46 0,-46 Z'
        cut='<path d="M52,-8 L32,-6 M-52,-8 L-32,-6 M44,22 L28,12 M-44,22 L-28,12 M34,-38 L22,-24 M-34,-38 L-22,-24" stroke="#FAF7F2" stroke-width="7" stroke-linecap="round"/>'
        return f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({sc})"><path d="{leaf}" fill="{c}"/>{cut}<path d="M0,-42 V26" stroke="{GOLD}" stroke-width="3"/></g>'
    # 1) pothos climbing around the T's stem, weaving in front and behind
    tcx=gx('T',280.5); pts=[]
    for i in range(0,61):
        u=i/60; yy=BASE-2-u*(BASE-2-(TOP+36)); ph=u*math.pi*5
        pts.append((tcx+21*math.sin(ph),yy,math.cos(ph)))
    def seg(p,q): return f'<path d="M{p[0]:.1f},{p[1]:.1f} L{q[0]:.1f},{q[1]:.1f}" stroke="{G1}" stroke-width="2.6" stroke-linecap="round"/>'
    back+=''.join(seg(pts[i],pts[i+1]) for i in range(60) if pts[i][2]<=0)
    front+=''.join(seg(pts[i],pts[i+1]) for i in range(60) if pts[i][2]>0)
    for k,i in enumerate(range(3,60,5)):
        x_,y_,c_=pts[i]
        leaf=heart(x_+(9 if k%2 else -9),y_,1.35,90 if k%2 else -90,GOLD if k==4 else (G2 if k%2 else G1))
        if c_>0: front+=leaf
        else: back+=leaf
    # 2) snake plant in a tiny kasavu pot inside the H, under the crossbar
    hcx=gx('H',393.5); hb=gy(293)
    sl=''.join(f'<path d="M{hcx+b0},{BASE-20} C{hcx+b0+l-3},{BASE-34} {hcx+b0+l},{hb+12} {hcx+b0+l*1.4},{hb+4+dh} C{hcx+b0+l+5},{hb+14} {hcx+b0+6},{BASE-34} {hcx+b0+7},{BASE-20} Z" fill="{c}" stroke="{GOLD}" stroke-width="1.6" stroke-linejoin="round"/>' for b0,l,dh,c in [(-14,-6,10,G2),(-4,0,0,G1),(6,5,8,G2)])
    pot=(f'<path d="M{hcx-17},{BASE-22} H{hcx+17} L{hcx+13},{BASE} H{hcx-13} Z" fill="#141414"/>'
         f'<rect x="{hcx-15}" y="{BASE-15}" width="30" height="6" fill="{GOLD}"/>'+''.join(f'<path d="M{hcx+d},{BASE-14} l2,2 -2,2 -2,-2 Z" fill="#141414"/>' for d in (-10,-4,2,8))+
         f'<rect x="{hcx-19}" y="{BASE-25}" width="38" height="5" rx="2" fill="#141414"/>')
    front+=f'<g{A(mode,t,"tilt",hcx,BASE-20,0.4)}>{sl}</g>{pot}'
    # 3) calathea (prayer plant) leaves fanning out from behind the O
    ocx=gx('O',410.5); obase=BASE+2
    def cal(rot,ln,c,stripe):
        return (f'<g transform="translate({ocx:.1f},{obase}) rotate({rot})"><path d="M0,0 V-{ln*0.35:.0f}" stroke="#7A3A4A" stroke-width="2.4"/>'
                f'<path d="M0,-{ln*0.3:.0f} C14,-{ln*0.45:.0f} 14,-{ln*0.9:.0f} 0,-{ln:.0f} C-14,-{ln*0.9:.0f} -14,-{ln*0.45:.0f} 0,-{ln*0.3:.0f} Z" fill="{c}"/>'
                + ''.join(f'<path d="M0,-{ln*f:.0f} l{8*sgn},-6" stroke="{stripe}" stroke-width="2" stroke-linecap="round"/>' for f in (0.45,0.58,0.71,0.84) for sgn in (-1,1))
                + f'<path d="M0,-{ln*0.32:.0f} V-{ln*0.97:.0f}" stroke="#E8A3B4" stroke-width="1.2"/></g>')
    front+=f'<g{A(mode,t,"tilt",ocx,obase,0.35)}>'+cal(-78,74,'#2E7D52','#B5E0B0')+cal(-52,80,'#3A8C5E','#CDEBC4')+cal(52,80,'#3A8C5E','#CDEBC4')+cal(78,74,'#2E7D52','#B5E0B0')+'</g>'
    # 4) monstera growing up between the M and the A, leaf peeking out above
    mx_=X0['A']-2
    back+=f'<g{A(mode,t,"tilt",mx_,BASE,0.7)}><path d="M{mx_},{BASE} Q{mx_-6},{BASE-80} {mx_+2},{TOP+30}" fill="none" stroke="{G1}" stroke-width="4"/>{mleaf(mx_+2,TOP+10,0.58,-14,G2)}</g>'
    # 5) string of pearls trailing off the S's lower curve
    sx0,sy0=gx('S',110),gy(150)
    strands=''
    for k,(dx,ln) in enumerate([(-6,40),(0,30),(6,36)]):
        pts=[(sx0+dx+3*math.sin(i*0.9+k),sy0+i*ln/8) for i in range(9)]
        strands+=f'<path d="M'+' L'.join(f'{p:.1f},{q:.1f}' for p,q in pts)+'" fill="none" stroke="#3E6B48" stroke-width="1.2"/>'
        strands+=''.join(f'<circle cx="{p:.1f}" cy="{q:.1f}" r="3.2" fill="#6FB07A" stroke="#3E8A50" stroke-width="0.8"/>' for p,q in pts[1::1])
    front+=f'<g{A(mode,t,"swish",sx0,sy0,0.5)}>{strands}</g>'
    # drone carries a tiny succulent
    front=front.replace('<circle cx="0" cy="7" r="2.4" fill="#141414"/></g></g>',
        '<circle cx="0" cy="7" r="2.4" fill="#141414"/><path d="M0,9 V22" stroke="#555" stroke-width="1"/><path d="M-8,22 H8 L6,34 H-6 Z" fill="#D4AF37"/>'
        +''.join(f'<ellipse cx="{dx}" cy="{dy}" rx="3.2" ry="6" fill="#4FA877" transform="rotate({r} {dx} {dy})"/>' for dx,dy,r in [(-4,18,-35),(4,18,35),(0,16,0),(-7,20,-70),(7,20,70)])
        +'</g></g>',1)
    h=330*width/W
    return f'''<svg role="img" aria-label="THOMAS in bold green letters with the family woven in, each with a personal touch, with houseplants woven through the letters (pothos climbing the T, a snake plant inside the H, calathea leaves fanning out from behind the O, a monstera between the M and A, string of pearls trailing off the S, and a tiny succulent carried by the drone): Shajan leaning over the T Emma in gold wrestling headgear behind the H with her hands on its posts, Rocky the cat in a spiked biker collar sitting on top of the O, Gabriel peeking through the O with a chocolate chip cookie, Abby in a vintage polka-dot headscarf nestled in the M, Evalyn behind the A setting a bouncing volleyball, and Ash the black shepherd in a cozy sweater peeking over the S" viewBox="0 0 {W:.0f} 330" width="{width}" height="{h:.0f}" style="display: block">
{back}
{glyphs(AU,7,7)}{glyphs(GREEN)}
{front}
</svg>'''
