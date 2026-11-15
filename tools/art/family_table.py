import math

PERIOD = 2.0  # seconds; every motion loops cleanly inside this

def _s(t, cycles=1, phase=0.0):
    return math.sin(2 * math.pi * (t * cycles + phase))

def A(mode, t, kind, px=0, py=0, phase=0.0):
    """Animation attribute: CSS class in 'css' mode, explicit transform for a GIF frame."""
    if mode == 'css':
        delay = f' style="animation-delay: {-phase * PERIOD:.2f}s"' if phase else ''
        return f' class="{kind}"{delay}'
    if kind == 'bob':
        return f' transform="translate(0,{-4 - 4 * _s(t, 1, phase):.2f})"'
    if kind == 'thumb':
        return f' transform="rotate({2 + 20 * _s(t, 2, phase):.2f} {px} {py})"'
    if kind == 'wave':
        return f' transform="rotate({-4 + 30 * _s(t, 2, phase):.2f} {px} {py})"'
    if kind == 'tilt':
        return f' transform="rotate({11 * _s(t, 1, phase):.2f} {px} {py})"'
    if kind == 'steam':
        u = (t + phase) % 1.0
        op = min(1, u / 0.4) * (1 - u) * 1.4
        return f' transform="translate(0,{6 - 26 * u:.2f})" opacity="{max(0, min(1, op)):.2f}"'
    if kind == 'leaf':
        u = (t + phase) % 1.0
        op = min(1, u / 0.1) * min(1, (1 - u) / 0.15)
        return f' transform="translate({28 * u + 6 * math.sin(6.283 * u * 2):.2f},{215 * u:.2f}) rotate({360 * u:.1f})" opacity="{op:.2f}"'
    return ''

DARK = '#2A1A14'

def happy(sc=1.0, col=DARK):
    return (f'<path d="M{-11*sc:.1f},{2*sc:.1f} q{4*sc:.1f},{-5*sc:.1f} {8*sc:.1f},0 '
            f'M{3*sc:.1f},{2*sc:.1f} q{4*sc:.1f},{-5*sc:.1f} {8*sc:.1f},0" fill="none" stroke="{col}" '
            f'stroke-width="2.4" stroke-linecap="round"/>')

def grin(w=9, y=10, col='#7A2A1E'):
    return (f'<path d="M{-w},{y} Q0,{y+11} {w},{y} Z" fill="#FFFFFF" stroke="{col}" stroke-width="2" '
            f'stroke-linejoin="round"/>')

def cheeks(dx=16, col='#E58A6E'):
    return (f'<circle cx="{-dx}" cy="9" r="4" fill="{col}" opacity="0.5"/>'
            f'<circle cx="{dx}" cy="9" r="4" fill="{col}" opacity="0.5"/>')

def shades(cat=False):
    if cat:
        lens = ('<path d="M-25,-6 Q-14,-11 -4,-6 Q-5,4 -14,5 Q-23,4 -25,-6 Z"/>'
                '<path d="M4,-6 Q14,-11 25,-6 Q23,4 14,5 Q5,4 4,-6 Z"/>')
        return (f'<g fill="#1B1B22" stroke="#5E8F86" stroke-width="2">{lens}</g>'
                '<path d="M-4,-5 Q0,-8 4,-5" fill="none" stroke="#5E8F86" stroke-width="2"/>')
    return ('<g fill="#15151A"><rect x="-24" y="-8" width="20" height="13" rx="5"/>'
            '<rect x="4" y="-8" width="20" height="13" rx="5"/></g>'
            '<path d="M-4,-4 L4,-4" stroke="#15151A" stroke-width="2.5"/>'
            '<path d="M-20,-5 L-15,-5 M8,-5 L13,-5" stroke="#FFFFFF" stroke-width="1.5" opacity="0.5" stroke-linecap="round"/>')

def thumb(x, y, skin, mode, t, phase, sleeve):
    pivot = A(mode, t, 'thumb', x, y + 10, phase)
    return (f'<g{pivot}>'
            f'<rect x="{x-7}" y="{y+6}" width="14" height="14" rx="4" fill="{sleeve}"/>'
            f'<rect x="{x-8}" y="{y-6}" width="16" height="14" rx="6" fill="{skin}"/>'
            f'<rect x="{x-3}" y="{y-16}" width="7" height="13" rx="3.5" fill="{skin}"/>'
            f'<path d="M{x-6},{y-1} H{x+6} M{x-6},{y+3} H{x+6}" stroke="#00000022" stroke-width="1"/>'
            f'</g>')

def curls(cx_list, col, r=9):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{col}"/>' for x, y, rr in cx_list)

def svg(mode='css', t=0.0, width=640, height=178, holiday=True, bg1='#F6DDB0', bg2='#F2CC8C', table='#3E6B48', rim='#C98A12'):
    back = ''
    tones = ['#D9A07A', '#C98E6A', '#E2B48F', '#CF9873', '#DDAA84', '#C4875F', '#E0B08B', '#D49C76', '#C99068']
    xs = [64, 142, 226, 312, 448, 532, 618, 700, 380]
    for i, x in enumerate(xs):
        y = 56 if i != 8 else 38
        tc = tones[i]
        back += (f'<g transform="translate({x},{y})"><g{A(mode, t, "bob", phase=i * 0.11)}>'
                 f'<path d="M-30,62 Q-30,26 0,26 Q30,26 30,62 Z" fill="{tc}"/><circle cx="0" cy="0" r="18" fill="{tc}"/></g></g>')

    gsk = '#D3A27F'
    DRUM = ('''<g'''+A(mode, t, 'wave', 36, 15, 0.2)+'''>
<ellipse cx="36" cy="-14" rx="9" ry="12" fill="#9C5222"/>
<ellipse cx="33" cy="-18" rx="3" ry="5" fill="#C27A3E"/>
<rect x="34" y="-3" width="4.5" height="12" fill="#FFF7EA"/>
<circle cx="33.5" cy="10" r="3" fill="#FFF7EA"/><circle cx="39" cy="10" r="3" fill="#FFF7EA"/>
<circle cx="36" cy="15" r="6" fill="'''+gsk+'''"/>
''') if holiday else ''
    # ---------- Gabriel (curly brown hair, patterned sweater, drumstick) ----------
    gsk = '#D3A27F'
    gabriel = f'''<g transform="translate(100,124)"><g{A(mode, t, 'bob', phase=0.5)}>
<rect x="-24" y="16" width="48" height="32" rx="15" fill="#EFE6D6"/>
<path d="M-20,26 l5,-5 5,5 5,-5 5,5 5,-5 5,5 5,-5 5,5" fill="none" stroke="#7A4E2D" stroke-width="2.5"/>
<path d="M-20,35 l5,-5 5,5 5,-5 5,5 5,-5 5,5 5,-5 5,5" fill="none" stroke="#B5652B" stroke-width="2"/>
{curls([(-15,-12,8),(-6,-18,8),(5,-18,8),(14,-12,8),(18,-3,6),(-18,-3,6),(0,-22,6)], '#6B4A32')}
<circle cx="0" cy="0" r="19" fill="{gsk}"/>
{curls([(-12,-14,6),(-3,-17,6),(7,-16,6),(14,-10,5)], '#6B4A32')}
{happy(0.75)}<ellipse cx="0" cy="9" rx="4.5" ry="3.8" fill="#7A2A1E"/>{cheeks(13)}
{DRUM}</g></g></g>'''

    # ---------- Shajan (bald, gray beard, sunglasses, olive bomber over gray henley) ----------
    ssk = '#A06A47'
    shajan = f'''<g transform="translate(184,100)"><g{A(mode, t, 'bob', phase=0.1)}>
<path d="M-38,72 Q-38,30 0,30 Q38,30 38,72 Z" fill="#7B8466"/>
<path d="M-13,30 L0,60 L13,30 Z" fill="#BDBDB8"/>
<path d="M0,36 V54" stroke="#8E8E8A" stroke-width="1.5"/>
<circle cx="0" cy="40" r="1.6" fill="#8E8E8A"/><circle cx="0" cy="47" r="1.6" fill="#8E8E8A"/>
<g{A(mode, t, 'tilt', 0, 28, 0.1)}>
<circle cx="-29" cy="2" r="6" fill="{ssk}"/><circle cx="29" cy="2" r="6" fill="{ssk}"/>
<circle cx="0" cy="0" r="29" fill="{ssk}"/>
<path d="M-14,-22 Q-6,-27 2,-25" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.35" stroke-linecap="round"/>
<path d="M-27,4 Q-27,36 0,38 Q27,36 27,4 Q22,12 14,10 Q0,8 -14,10 Q-22,12 -27,4 Z" fill="#D8D3CB"/>
<path d="M-12,10 Q0,4 12,10 Q6,14 0,12 Q-6,14 -12,10 Z" fill="#9A938A"/>
<path d="M-8,18 Q0,25 8,18" fill="none" stroke="#5A3020" stroke-width="2.4" stroke-linecap="round"/>
{shades()}
</g></g></g>'''

    # ---------- Daughter in mustard corduroy jacket (long wavy dark hair) ----------
    m_sk = '#9A6343'
    mustard = f'''<g transform="translate(278,104)"><g{A(mode, t, 'bob', phase=0.3)}>
<path d="M-30,-6 Q-34,-34 0,-34 Q34,-34 30,-6 Q36,22 34,58 Q22,64 14,52 L-14,52 Q-22,64 -34,58 Q-36,22 -30,-6 Z" fill="#17100C"/>
<path d="M-34,68 Q-34,28 0,28 Q34,28 34,68 Z" fill="#C8922E"/>
<path d="M-11,28 L0,44 L11,28 Z" fill="#1E1E24"/>
<path d="M-24,40 V66 M-17,36 V66 M17,36 V66 M24,40 V66" stroke="#A9781F" stroke-width="1.5"/>
<circle cx="0" cy="0" r="25" fill="{m_sk}"/>
<path d="M-26,0 Q-26,-30 0,-28 Q24,-28 26,-2 Q14,-18 -4,-16 Q-18,-14 -26,0 Z" fill="#17100C"/>
<path d="M-27,4 Q-31,18 -26,32 M27,4 Q31,18 26,32" fill="none" stroke="#17100C" stroke-width="6" stroke-linecap="round"/>
{happy(0.9)}{grin(8, 9)}{cheeks(15)}
</g></g>'''
    mustard += thumb(250, 136, m_sk, mode, t, 0.0, '#C8922E')

    # ---------- Abby (big curly light-brown/blonde hair, cat-eye sunglasses, black sweater) ----------
    a_sk = '#F0CDB2'
    ah = '#C2935A'; ah2 = '#DDB47A'
    abby_back = [(-30,-20,12),(-36,-2,12),(-36,16,12),(-32,32,11),(-22,42,10),(30,-20,12),(36,-2,12),(36,16,12),(32,32,11),(22,42,10),(-18,-32,12),(0,-36,12),(18,-32,12)]
    abby = f'''<g transform="translate(482,100)"><g{A(mode, t, 'bob', phase=0.6)}>
{curls(abby_back, ah)}
{curls([(-34,8,5),(34,8,5),(-28,30,5),(28,30,5),(-10,-36,5),(12,-34,5)], ah2)}
<path d="M-38,72 Q-38,30 0,30 Q38,30 38,72 Z" fill="#1F2230"/>
<path d="M-6,30 L0,52 L6,30" fill="none" stroke="#C9B48A" stroke-width="1.2"/>
<path d="M0,52 l4,4 -4,4 -4,-4 Z" fill="#2A2A2A" stroke="#C9B48A" stroke-width="1"/>
<path d="M18,32 L30,70" stroke="#A8642F" stroke-width="3"/>
<g{A(mode, t, 'tilt', 0, 28, 0.6)}>
<circle cx="0" cy="0" r="27" fill="{a_sk}"/>
{curls([(-22,-16,9),(-10,-24,9),(4,-25,9),(17,-20,9),(25,-8,7),(-25,-6,7)], ah)}
{curls([(-14,-22,4),(10,-24,4),(22,-14,4)], ah2)}
<path d="M-11,11 Q0,26 11,11 Z" fill="#FFFFFF" stroke="#9A3B3B" stroke-width="2" stroke-linejoin="round"/>
<path d="M-6,17 Q0,21 6,17" fill="#E58A80" opacity="0.7"/>
{cheeks(18, '#E58A80')}
{shades(cat=True)}
</g></g></g>'''
    abby += thumb(456, 132, a_sk, mode, t, 0.25, '#1F2230')

    # ---------- Daughter in black puffer (very curly long dark hair, hoops, light-blue collar) ----------
    p_sk = '#A9714E'
    pb = [(-26,-24,11),(-34,-8,11),(-36,10,11),(-36,28,11),(-30,44,10),(-22,56,9),(26,-24,11),(34,-8,11),(36,10,11),(36,28,11),(30,44,10),(22,56,9),(-12,-34,11),(6,-36,11),(20,-32,10)]
    puffer = f'''<g transform="translate(580,104)"><g{A(mode, t, 'bob', phase=0.8)}>
{curls(pb, '#16100C')}
<path d="M-34,68 Q-34,28 0,28 Q34,28 34,68 Z" fill="#1C1C22"/>
<path d="M-32,44 H32 M-34,56 H34" stroke="#3A3A44" stroke-width="2"/>
<path d="M-12,28 L0,42 L12,28 Z" fill="#A9C3E6"/>
<circle cx="0" cy="0" r="25" fill="{p_sk}"/>
{curls([(-20,-16,8),(-8,-24,8),(6,-24,8),(18,-18,8),(24,-6,6),(-24,-6,6)], '#16100C')}
<circle cx="-25" cy="12" r="4" fill="none" stroke="#E2B84A" stroke-width="2"/>
<circle cx="25" cy="12" r="4" fill="none" stroke="#E2B84A" stroke-width="2"/>
{happy(0.9)}<path d="M-6,10 q6,6 12,0" fill="none" stroke="#7A2A1E" stroke-width="2.2" stroke-linecap="round"/>{cheeks(15)}
</g></g>'''
    puffer += thumb(612, 136, p_sk, mode, t, 0.5, '#A9C3E6')

    # ---------- Turkey ----------
    steam = ''.join(
        f'<g{A(mode, t, "steam", phase=ph)}><path d="M{dx},100 q-5,-8 0,-16 q5,-8 0,-16" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/></g>'
        for dx, ph in [(-12, 0.0), (0, 0.33), (12, 0.66)])
    turkey = f'''<g transform="translate(380,0)">{steam}
<ellipse cx="0" cy="160" rx="64" ry="10" fill="#FFFFFF"/>
<path d="M-44,158 A44,40 0 0 1 44,158 Z" fill="#B5652B"/>
<path d="M-26,136 A30,22 0 0 1 10,120" fill="none" stroke="#D98E4F" stroke-width="6" stroke-linecap="round"/>
<circle cx="-42" cy="148" r="11" fill="#9C5222"/><circle cx="42" cy="148" r="11" fill="#9C5222"/>
<rect x="-58" y="140" width="10" height="5" rx="2.5" fill="#FFF7EA" transform="rotate(-30 -53 142)"/>
<rect x="48" y="140" width="10" height="5" rx="2.5" fill="#FFF7EA" transform="rotate(30 53 142)"/>
</g>'''

    rocky = f'''<g transform="translate(30,140)"><g{A(mode, t, 'tilt', 0, 18, 0.45)}>
<path d="M-17,-8 L-13,-28 L-2,-15 Z M17,-8 L13,-28 L2,-15 Z" fill="#7C7C80"/>
<circle cx="0" cy="0" r="19" fill="#8A8A8F"/>
{happy(0.75, '#1d1d1d')}<path d="M-3,6 L3,6 L0,9 Z" fill="#E9A0A8"/>
<path d="M-9,8 L-22,6 M9,8 L22,6" stroke="#4a4a4a" stroke-width="1"/>
</g></g>'''

    ash = f'''<g transform="translate(706,126)"><g{A(mode, t, 'tilt', 0, 30, 0.15)}><g transform="scale(0.74)"><g>
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
</g></g></g></g>'''

    HEART = (f'<g transform="translate(380,118)"><g{A(mode, t, "bob", phase=0.25)}>'
             f'<path d="M0,30 C-46,2 -40,-34 -14,-34 C-4,-34 0,-26 0,-20 C0,-26 4,-34 14,-34 C40,-34 46,2 0,30 Z" fill="{rim}"/>'
             f'<path d="M-24,-18 Q-20,-26 -12,-26" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.6"/></g></g>')
    leaf_specs = [(60,'#E8891C',0.0),(170,'#C0392B',0.55),(250,'#F2B632',0.25),(345,'#D35400',0.8),(430,'#C0392B',0.1),(520,'#F2B632',0.65),(625,'#E8891C',0.35),(735,'#D35400',0.9),(110,'#F2B632',0.4),(560,'#E8891C',0.15)]
    leaves = ''.join(f'<g transform="translate({x},-12)"><g{A(mode, t, "leaf", phase=ph)}><path d="M0,-9 Q8,-4 0,9 Q-8,-4 0,-9 Z" fill="{c}"/><path d="M0,-7 V8" stroke="#00000033" stroke-width="1"/></g></g>' for x, c, ph in leaf_specs)
    labels = [(30, 'ROCKY'), (100, 'GABRIEL'), (184, 'SHAJAN'), (278, 'EMMA'), (482, 'ABBY'), (580, 'EVALYN'), (708, 'ASH')]
    lab = ''.join(f'<text x="{x}" y="192">{n}</text>' for x, n in labels)

    aria = ('Animated cartoon of the family around the Thanksgiving table: Rocky the cat, Gabriel waving a drumstick, '
            'Shajan, Emma, a steaming roast turkey, Abby, Evalyn and Ash the black shepherd in a sweater, giving thumbs-ups, with the extended family behind them')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{aria}" viewBox="0 0 760 212" width="{width}" height="{height}" style="width: {width}px; height: {height}px; display: block">
<circle cx="380" cy="150" r="140" fill="{bg1}"/>
<circle cx="380" cy="150" r="104" fill="{bg2}"/>
{back}{leaves if holiday else ""}{rocky}{gabriel}{shajan}{mustard}{turkey if holiday else HEART}{abby}{puffer}{ash}
<rect x="0" y="160" width="760" height="52" rx="8" fill="{table}"/>
<rect x="0" y="160" width="760" height="5" fill="{rim}"/>
<g font-family="DM Sans, DejaVu Sans, sans-serif" font-size="12" font-weight="700" letter-spacing="1.5" fill="#FFF7EA" text-anchor="middle">{lab}</g>
</svg>'''

CSS = '''@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes thumb{0%,100%{transform:rotate(-18deg)}50%{transform:rotate(22deg)}}
@keyframes wave{0%,100%{transform:rotate(-34deg)}50%{transform:rotate(26deg)}}
@keyframes tilt{0%,100%{transform:rotate(-11deg)}50%{transform:rotate(11deg)}}
@keyframes steam{0%{transform:translateY(4px);opacity:0}40%{opacity:.9}100%{transform:translateY(-20px);opacity:0}}
@keyframes fall{0%{transform:translate(0,0) rotate(0deg);opacity:0}10%{opacity:1}85%{opacity:1}100%{transform:translate(28px,215px) rotate(360deg);opacity:0}}
.bob{animation:bob 2s ease-in-out infinite}
.thumb{transform-box:fill-box;transform-origin:50% 100%;animation:thumb 1s ease-in-out infinite}
.wave{transform-box:fill-box;transform-origin:30% 100%;animation:wave 1s ease-in-out infinite}
.tilt{transform-box:fill-box;transform-origin:50% 90%;animation:tilt 2s ease-in-out infinite}
.steam{animation:steam 2s linear infinite}
.leaf{transform-box:fill-box;transform-origin:center;animation:fall 2s linear infinite}
@media (prefers-reduced-motion: reduce){.bob,.thumb,.wave,.tilt,.steam,.leaf{animation:none}}'''
