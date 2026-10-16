import os, random, math

OUT = "/workspace/miranda-site/public/img"
os.makedirs(OUT, exist_ok=True)

INK   = "#1d1d1b"
PARCH = "#e2dedb"
BONE  = "#cdc6be"
CHAR  = "#69645f"
EMBER = "#c03f13"

def noise(x0,y0,w,h,seed,opacity=0.06):
    return f'''<filter id="grain{seed}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="2" seed="{seed}" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0"/>
    </filter>
    <rect x="{x0}" y="{y0}" width="{w}" height="{h}" filter="url(#grain{seed})" opacity="{opacity}"/>'''

def svg_wrap(w, h, body, seed):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
  <radialGradient id="vig{seed}" cx="50%" cy="42%" r="75%">
    <stop offset="55%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity="0.42"/>
  </radialGradient>
</defs>
{body}
<rect width="{w}" height="{h}" fill="url(#vig{seed})"/>
{noise(0,0,w,h,seed)}
</svg>'''

# ------------------------------------------------------------------
# Warm wood studio interior (featured-left + avroko variant)
# ------------------------------------------------------------------
def warm_interior(fname, seed, accent_shelf=False):
    w,h = 800,1000
    rng = random.Random(seed)
    planks = []
    for i in range(14):
        y = i*(h//14)
        tone = ["#3a2c1e","#41311f","#332618","#463522"][i%4]
        planks.append(f'<rect x="0" y="{y}" width="{w}" height="{h//14}" fill="{tone}" stroke="#241a10" stroke-width="2"/>')
    # window light shaft
    shaft = f'''<polygon points="120,0 380,0 640,{h} 300,{h}" fill="#e8c98a" opacity="0.14"/>
    <polygon points="180,0 320,0 520,{h} 380,{h}" fill="#f3dda8" opacity="0.12"/>'''
    # shelves with records / bottles
    shelf = ''
    if accent_shelf:
        shelf = f'''<rect x="470" y="300" width="300" height="14" fill="#241a10"/>
        <rect x="470" y="520" width="300" height="14" fill="#241a10"/>'''
        for k in range(9):
            x = 482 + k*32
            hh = rng.randint(120,190)
            col = [INK,"#2e2114","#4a3623",EMBER][k%4] if k!=3 else EMBER
            shelf += f'<rect x="{x}" y="{520-hh-14 if False else 300-hh+ (300-300)}" width="24" height="{hh}" fill="{col}" transform="translate(0 {-hh-14+300-300})"/>'
    # simpler record spines on two shelves
    spines = ''
    for base_y in (300, 520):
        x = 480
        while x < 760:
            bw = rng.randint(16,30)
            bh = rng.randint(120,160)
            col = rng.choice(["#241a10","#3a2c1e","#463522", INK])
            spines += f'<rect x="{x}" y="{base_y-bh}" width="{bw}" height="{bh}" fill="{col}" stroke="#1a130b" stroke-width="1.5"/>'
            x += bw + 4
    # framed poster on wall
    poster = f'''<g transform="rotate(-2 250 260)">
      <rect x="150" y="140" width="220" height="260" fill="{PARCH}" stroke="{INK}" stroke-width="6"/>
      <text x="260" y="270" font-family="Georgia,serif" font-size="86" font-weight="bold" fill="{INK}" text-anchor="middle">A&amp;</text>
      <text x="260" y="340" font-family="Georgia,serif" font-size="34" fill="{INK}" text-anchor="middle" letter-spacing="4">KO·SOUND</text>
      <circle cx="260" cy="200" r="18" fill="{EMBER}"/>
    </g>'''
    # desk silhouette bottom
    desk = f'''<rect x="0" y="820" width="{w}" height="180" fill="#241a10"/>
    <rect x="60" y="770" width="240" height="52" rx="6" fill="#312415" stroke="#1a130b" stroke-width="3"/>
    <ellipse cx="620" cy="800" rx="120" ry="22" fill="#1a130b"/>
    <rect x="560" y="700" width="120" height="102" fill="#3a2c1e" stroke="#1a130b" stroke-width="3"/>'''
    # lamp glow
    lamp = f'''<circle cx="620" cy="640" r="150" fill="#f3dda8" opacity="0.16"/>
    <circle cx="620" cy="640" r="70" fill="#f3dda8" opacity="0.2"/>
    <path d="M620 500 q -60 60 -20 120 l 40 0 q 40 -60 -20 -120 z" fill="{INK}"/>'''
    body = ''.join(planks) + shaft + spines + poster + desk + lamp + f'<rect x="470" y="300" width="300" height="12" fill="#241a10"/><rect x="470" y="520" width="300" height="12" fill="#241a10"/>'
    return svg_wrap(w,h,body,seed)

# ------------------------------------------------------------------
# Cool blue retail space (featured-right + noorder variant)
# ------------------------------------------------------------------
def cool_retail(fname, seed, warm=False):
    w,h = 800,1000
    rng = random.Random(seed)
    base = "#16232e" if not warm else "#20242a"
    wall = f'<rect width="{w}" height="{h}" fill="{base}"/>'
    tiles = ''
    for ty in range(0,h,100):
        tiles += f'<line x1="0" y1="{ty}" x2="{w}" y2="{ty}" stroke="#0d161d" stroke-width="3"/>'
    for tx in range(0,w,100):
        tiles += f'<line x1="{tx}" y1="0" x2="{tx}" y2="{h}" stroke="#0d161d" stroke-width="3"/>'
    # neon-ish sign (kept flat, ink/parchment)
    sign = f'''<g>
      <rect x="140" y="180" width="520" height="200" fill="{INK}" stroke="#0a0f14" stroke-width="6"/>
      <text x="400" y="300" font-family="Georgia,serif" font-size="96" fill="{PARCH}" text-anchor="middle" letter-spacing="-4">NOORDER</text>
      <text x="400" y="352" font-family="Georgia,serif" font-size="30" fill="{CHAR}" text-anchor="middle" letter-spacing="10">LICHT · FM</text>
    </g>'''
    # counter
    counter = f'''<rect x="0" y="760" width="{w}" height="240" fill="#0d161d"/>
    <rect x="0" y="740" width="{w}" height="34" fill="#22384a"/>'''
    # objects on counter
    objs = ''
    for k in range(5):
        x = 90 + k*140
        hh = rng.randint(70,150)
        col = rng.choice(["#22384a","#2e4a61","#1a2a37"])
        objs += f'<rect x="{x}" y="{740-hh}" width="80" height="{hh}" fill="{col}" stroke="#0a121a" stroke-width="3"/>'
    objs += f'<circle cx="650" cy="660" r="40" fill="{EMBER}"/>'  # one ember note
    # hanging bulbs
    bulbs = ''
    for k in range(4):
        x = 120 + k*190
        ln = rng.randint(90,180)
        bulbs += f'<line x1="{x}" y1="0" x2="{x}" y2="{ln}" stroke="#0a121a" stroke-width="4"/><circle cx="{x}" cy="{ln+16}" r="16" fill="{PARCH}" opacity="0.85"/><circle cx="{x}" cy="{ln+16}" r="42" fill="{PARCH}" opacity="0.08"/>'
    body = wall + tiles + sign + bulbs + counter + objs
    return svg_wrap(w,h,body,seed)

# ------------------------------------------------------------------
# Rim-lit portrait (digital painting style)
# ------------------------------------------------------------------
def portrait():
    w,h = 900,1200
    bg = f'''<rect width="{w}" height="{h}" fill="#241a12"/>
    <ellipse cx="450" cy="500" rx="420" ry="520" fill="#3a2a1a" opacity="0.7"/>
    <ellipse cx="450" cy="460" rx="300" ry="400" fill="#4a3623" opacity="0.6"/>'''
    # shoulders / coat
    coat = f'''<path d="M150 1200 Q170 900 300 830 L600 830 Q730 900 750 1200 Z" fill="{INK}"/>
    <path d="M300 830 L450 1000 L600 830 L520 830 L450 930 L380 830 Z" fill="#2b2b28"/>'''
    # neck
    neck = '<rect x="400" y="700" width="100" height="160" fill="#8a5a3b"/>'
    # head
    head = f'''<ellipse cx="450" cy="520" rx="170" ry="220" fill="#9a6a45"/>
    <ellipse cx="450" cy="520" rx="170" ry="220" fill="#7a4e30" opacity="0.55"/>'''
    # hair mass
    hair = f'''<path d="M280 470 Q280 260 450 260 Q620 260 620 470 Q600 360 450 350 Q320 360 280 470 Z" fill="{INK}"/>
    <path d="M285 480 Q300 560 292 640 L322 620 Q310 540 315 480 Z" fill="{INK}"/>
    <path d="M615 480 Q600 560 608 640 L578 620 Q590 540 585 480 Z" fill="{INK}"/>'''
    # face features minimal, painterly
    feats = f'''<path d="M380 500 q 25 -14 50 0" stroke="#3a2416" stroke-width="8" fill="none" stroke-linecap="round"/>
    <path d="M470 500 q 25 -14 50 0" stroke="#3a2416" stroke-width="8" fill="none" stroke-linecap="round"/>
    <circle cx="405" cy="520" r="9" fill="#1a0f08"/><circle cx="495" cy="520" r="9" fill="#1a0f08"/>
    <path d="M450 530 l -12 78 q 12 10 26 4" stroke="#5a3a22" stroke-width="7" fill="none" stroke-linecap="round"/>
    <path d="M410 640 q 40 26 84 0" stroke="#3a2416" stroke-width="9" fill="none" stroke-linecap="round"/>
    <path d="M360 440 q 40 -22 84 -14 M456 426 q 44 -8 84 14" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>'''
    # beard shadow
    beard = '<path d="M320 600 Q450 800 580 600 Q560 740 450 760 Q340 740 320 600 Z" fill="#2b2016" opacity="0.8"/>'
    # RIM LIGHT from right — crescent strokes
    rim = f'''<path d="M600 330 Q660 480 610 660 Q590 730 560 780" stroke="{PARCH}" stroke-width="14" fill="none" opacity="0.9" stroke-linecap="round"/>
    <path d="M612 350 Q668 480 620 650" stroke="#f3e9d6" stroke-width="6" fill="none" opacity="0.7" stroke-linecap="round"/>
    <path d="M596 300 Q640 340 636 400" stroke="{PARCH}" stroke-width="10" fill="none" opacity="0.6" stroke-linecap="round"/>
    <path d="M620 840 Q700 900 726 1060" stroke="{PARCH}" stroke-width="10" fill="none" opacity="0.5" stroke-linecap="round"/>
    <path d="M292 360 Q262 480 300 640" stroke="{EMBER}" stroke-width="7" fill="none" opacity="0.5" stroke-linecap="round"/>'''
    # collar highlights
    collar = f'''<path d="M310 840 L450 990 L590 840" stroke="{PARCH}" stroke-width="6" fill="none" opacity="0.5"/>'''
    body = bg + coat + neck + head + hair + beard + feats + rim + collar
    return svg_wrap(w,h,body,7)

# ------------------------------------------------------------------
# Herb/apothecary, print club press, foundry specimen (project thumbs)
# ------------------------------------------------------------------
def apothecary(seed):
    w,h=800,600
    rng=random.Random(seed)
    bg=f'<rect width="{w}" height="{h}" fill="#2c3524"/>'
    shelf=''.join([f'<rect x="0" y="{y}" width="{w}" height="12" fill="#1c2317"/>' for y in (200,420)])
    jars=''
    x=40
    while x<760:
        jw=rng.randint(60,90); jh=rng.randint(110,170)
        col=rng.choice(["#3f4d33","#556647","#22301c"])
        label=rng.random()<0.3
        jars+=f'<rect x="{x}" y="{200-jh}" width="{jw}" height="{jh}" rx="6" fill="{col}" stroke="#141a0f" stroke-width="3"/>'
        jars+=f'<rect x="{x+jw//2-14}" y="{200-jh-16}" width="28" height="16" fill="{INK}"/>'
        if label: jars+=f'<rect x="{x+8}" y="{200-jh+30}" width="{jw-16}" height="42" fill="{PARCH}" opacity="0.85"/>'
        x+=jw+18
    jars2=''
    x=60
    while x<720:
        jw=rng.randint(50,80); jh=rng.randint(90,140)
        col=rng.choice(["#556647","#3f4d33","#1c2317"])
        jars2+=f'<rect x="{x}" y="{420-jh}" width="{jw}" height="{jh}" rx="4" fill="{col}" stroke="#141a0f" stroke-width="3"/>'
        x+=jw+22
    sprig=f'<g stroke="{BONE}" stroke-width="5" fill="none" opacity="0.9"><path d="M660 470 q 40 -120 10 -220"/><path d="M668 400 q -50 -20 -70 -60 M668 400 q 50 -20 66 -58 M674 330 q -46 -16 -62 -52 M674 330 q 46 -16 60 -50"/></g>'
    emberdot=f'<circle cx="90" cy="470" r="26" fill="{EMBER}"/>'
    return svg_wrap(w,h,bg+shelf+jars+jars2+sprig+emberdot,seed)

def print_press(seed):
    w,h=800,600
    bg=f'<rect width="{w}" height="{h}" fill="{BONE}"/>'
    floor=f'<rect x="0" y="480" width="{w}" height="120" fill="#a89e91"/>'
    press=f'''<rect x="220" y="150" width="360" height="330" fill="{INK}"/>
    <rect x="250" y="90" width="300" height="70" rx="35" fill="{INK}"/>
    <circle cx="400" cy="125" r="52" fill="none" stroke="{INK}" stroke-width="18"/>
    <line x1="400" y1="60" x2="400" y2="190" stroke="{INK}" stroke-width="14"/>
    <line x1="335" y1="125" x2="465" y2="125" stroke="{INK}" stroke-width="14"/>
    <rect x="270" y="300" width="260" height="120" fill="#3a3833"/>
    <rect x="290" y="330" width="220" height="26" fill="{PARCH}"/>'''
    paper=f'<rect x="300" y="404" width="200" height="60" fill="{PARCH}" stroke="{INK}" stroke-width="3" transform="rotate(-3 400 434)"/>'
    sheets=''.join([f'<rect x="{40+i*46}" y="{60-rng_i if False else 40}" width="34" height="46" fill="{PARCH}" stroke="{INK}" stroke-width="2"/>' for i,rng_i in enumerate([0,1,0,1,0,1,0,1])])
    stack=f'<g transform="translate(560 380)">{"".join([f"<rect x=\'0\' y=\'{-i*10}\' width=\'150\' height=\'120\' fill=\'{PARCH if i%2==0 else BONE}\' stroke=\'{INK}\' stroke-width=\'3\'/>" for i in range(4)])}</g>'
    ember=f'<circle cx="120" cy="150" r="44" fill="{EMBER}"/><text x="120" y="162" font-family="Georgia,serif" font-size="40" fill="{PARCH}" text-anchor="middle">★</text>'
    return svg_wrap(w,h,bg+floor+press+paper+stack+ember,seed)

def foundry_specimen(seed):
    w,h=800,600
    bg=f'<rect width="{w}" height="{h}" fill="{PARCH}"/>'
    rules=''.join([f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{INK}" stroke-width="1.5" opacity="0.35"/>' for y in range(60,h,60)])
    glyphs=[("A",300),("R",240),("&amp;",200),("Q",260),("g",180)]
    row=''
    x=40
    for ch,size in glyphs:
        row+=f'<text x="{x}" y="{180+size*0.6}" font-family="Georgia,serif" font-size="{size}" fill="{INK}" font-style="italic">{ch}</text>'
        x+=int(size*0.9)+30
    big=f'<text x="400" y="470" font-family="Georgia,serif" font-size="230" font-weight="bold" fill="{INK}" text-anchor="middle" letter-spacing="-14">ZV·4</text>'
    ember=f'<rect x="620" y="60" width="120" height="120" fill="{EMBER}"/><text x="680" y="135" font-family="Georgia,serif" font-size="44" fill="{PARCH}" text-anchor="middle">NEW</text>'
    caption=f'<text x="40" y="560" font-family="Georgia,serif" font-size="22" fill="{CHAR}" letter-spacing="6">ZWARTVIER — VARIABLE SPECIMEN</text>'
    return svg_wrap(w,h,bg+rules+row+big+ember+caption,seed)

# ---- write files ----
open(f"{OUT}/featured-left.svg","w").write(warm_interior("featured-left",1))
open(f"{OUT}/proj-avroko.svg","w").write(warm_interior("proj-avroko",2))
open(f"{OUT}/featured-right.svg","w").write(cool_retail("featured-right",3))
open(f"{OUT}/proj-noorder.svg","w").write(cool_retail("proj-noorder",4))
open(f"{OUT}/portrait.svg","w").write(portrait())
open(f"{OUT}/proj-kruid.svg","w").write(apothecary(5))
open(f"{OUT}/proj-vecht.svg","w").write(print_press(6))
open(f"{OUT}/proj-zwart.svg","w").write(foundry_specimen(8))
open(f"{OUT}/proj-houten.svg","w").write(warm_interior("proj-houten",9))
print("done:", sorted(os.listdir(OUT)))
