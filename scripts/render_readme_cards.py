import json, os, collections, datetime as dt, urllib.request

# ---- CONFIG ----
USER   = os.environ.get("GH_USER", "sujalgangarde")
NAME   = "Sujal Gangarde"
LINE   = "Software Engineer. I turn ideas into shipped products."
ACCENT = "#1f4fff"
TILES  = [("BUILD", ACCENT), ("BRAND", "#e5432d"), ("LEARN", "#f2b705")]
# ----------------
STATIC = os.environ.get("STATIC") == "1"
INK, PAPER, MUTED = "#1a1a1a", "#faf7f0", "#8a8578"
FONT = "Georgia,'Times New Roman',serif"
SANS = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"

PORTRAIT = """
                      ---  --------------
                 -=+=- =*#+- -=- -  --------
               - =**== --=+++#*+=   -----    --
              ++-- -=+=--== =+#*+----====-
           --=++*##*%@%*#+++=#@@#+#*+--++=-=+-
          -+%++*#@@@@@@%%@@@##%@@@%**#%%@@*=-+=-   -
         -++**+#%%@@@@@@@@@@@@@@@@@@@@@@@@#*===- -== -
       = =+*%%%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@%*+++===
      = =*+*#%@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@%#####*--+=
     -==##**%%%%*----=---=+#%@@@%%%##@%%@@@@@%%%%%%#*%*--
      =#*%@@@@*-                      --+**##@@@@@@@%#=-
      =*%@@@@*                              -=#@@###+-
       =%@@@#                                 =%%#+--
       +%%@%=                                  #@@@*--
       +##@%=                                  *@@@@#=
        +@@#-                                  =@@@%*
         %=+##+--=++###+===-     ---==+===--    #@@*
         -+ +@ -+++%%%#****@@%%@@####@##*+===*%*=#@-
          -  * -=- +*=-++=-@   %*=*#*=#%%=*#+=@- *-
         =   +            *-   -#     --     -*  -
         -    -          =-     ==           =   =
                      -          -=         -    -
                    -               ==-
                        -**===+*#+    -
           -      -=+=-=+****=****+=--==-
           -=+=   #@@%=          -==*@@@+-- ---
           --+*-  +*-=             *%#%%= -+*=
            =+==+--                   ++ =+*+-
            -*+++==                   +=+#**+-
             +###*+=                 =***%#*-
              -%@%%*=               =*##@@+
                +@@@#+=- =-=+--- --+#%@@*  -
             =    +%@@@@%@@@@@@@%%@@@%+    %-
                     =*%@@@@@@@@@@#+-     -@=
                        -=+****+=
"""

# ---------- data ----------
def fetch():
    q = ('{user(login:"%s"){contributionsCollection{contributionCalendar{'
         'weeks{contributionDays{date contributionCount}}}}}}' % USER)
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q}).encode(),
        headers={"Authorization": "bearer " + os.environ["GH_TOKEN"]})
    d = json.load(urllib.request.urlopen(req))
    cal = d["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [[(x["date"], x["contributionCount"]) for x in w["contributionDays"]] for w in cal]

weeks = fetch()
os.makedirs("data", exist_ok=True)
json.dump(weeks, open("data/contributions.json", "w"))
days = [x for w in weeks for x in w]
total = sum(c for _, c in days)
active = sum(1 for _, c in days if c)
best_day = max(days, key=lambda x: x[1])
streak = 0
for i, (_, c) in enumerate(reversed(days)):
    if c: streak += 1
    elif i > 0: break
mo = collections.OrderedDict()
for d, c in days: mo[d[:7]] = mo.get(d[:7], 0) + c
months = list(mo.items())[-12:]

# ---------- shared svg ----------
CSS = """
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pop{from{opacity:0;transform:scale(.3)}to{opacity:1;transform:scale(1)}}
@keyframes swing{0%{opacity:0;transform:translateY(40px) rotate(-6deg)}
 70%{opacity:1;transform:translateY(-6px) rotate(1deg)}100%{opacity:1;transform:none}}
@keyframes pulse{0%{r:6;opacity:.8}100%{r:26;opacity:0}}
.rise{opacity:0;animation:rise .7s ease forwards}
.fade{opacity:0;animation:fade .3s ease forwards}
.grow{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .8s ease forwards}
.pop{transform-box:fill-box;transform-origin:center;opacity:0;animation:pop .35s ease forwards}
.swing{transform-box:fill-box;transform-origin:bottom left;opacity:0;animation:swing .9s ease forwards}
.ring{animation:pulse 2.4s ease-out infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important;transform:none!important}}
""" + ("*{animation:none!important;opacity:1!important;transform:none!important}" if STATIC else "")

def svg(w, h, body, name):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
         f'<style>{CSS}</style><rect width="{w}" height="{h}" rx="18" fill="{PAPER}" '
         f'stroke="#e2ddd0"/>{body}</svg>')
    os.makedirs("cards", exist_ok=True)
    open(f"cards/{name}.svg", "w", encoding="utf-8").write(s)

def dl(t): return f'style="animation-delay:{t:.2f}s"'

# ---------- hero ----------
rows = PORTRAIT.strip("\n").split("\n")
art = ""
for i, r in enumerate(rows):
    art += (f'<text class="fade" {dl(0.6 + i*0.04)} x="680" y="{22 + i*6.2:.1f}" '
            f'font-family="monospace" font-size="5.4" fill="{INK}" '
            f'xml:space="preserve">{r}</text>')
svg(900, 240, f'''
<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" x2="300" y1="0" y2="0">
<stop offset="0" stop-color="{INK}"/><stop offset=".5" stop-color="{ACCENT}"/>
<stop offset="1" stop-color="{INK}"/>
<animateTransform attributeName="gradientTransform" type="translate"
 values="-300 0;700 0;700 0" keyTimes="0;.4;1" dur="6s" begin="1.5s" repeatCount="indefinite"/>
</linearGradient></defs>
<text class="rise" {dl(0.1)} x="40" y="110" font-family="{FONT}" font-size="64" fill="url(#g)">{NAME}</text>
<text class="rise" {dl(0.5)} x="42" y="160" font-family="{SANS}" font-size="19" fill="{MUTED}">{LINE}</text>
<circle cx="44" cy="205" r="5" fill="{ACCENT}"/>
<circle class="ring" cx="44" cy="205" r="6" fill="none" stroke="{ACCENT}"/>
<text x="58" y="210" font-family="{SANS}" font-size="15" fill="{INK}">github.com/{USER}</text>
{art}
''', "hero")

# ---------- tiles ----------
vals = [total, active, streak]
subs = ["contributions", "active days", "day streak"]
for i, ((label, color), v, sub) in enumerate(zip(TILES, vals, subs)):
    t0 = 0.3 + i * 0.25
    frames = ""
    for k in range(1, 11):
        n = round(v * k / 10)
        last = (k == 10)
        vis = "visible" if (STATIC and last) else "hidden"
        timing = 'fill="freeze"' if last else 'dur="0.06s"'
        begin = f"{t0 + 0.5 + k*0.06:.2f}s"
        frames += (f'<text x="30" y="110" font-family="{FONT}" font-size="56" fill="#fff" '
                   f'visibility="{vis}">{n}'
                   f'<set attributeName="visibility" to="visible" begin="{begin}" {timing}/></text>')
    svg(290, 170, f'''
<g class="swing" {dl(t0)}><rect x="10" y="10" width="270" height="150" rx="16" fill="{color}"/>
<text x="30" y="46" font-family="{SANS}" font-size="13" letter-spacing="3" fill="#fff" opacity=".85">{label}</text>
{frames}
<text x="30" y="140" font-family="{SANS}" font-size="15" fill="#fff" opacity=".85">{sub}</text>
<circle class="ring" cx="250" cy="40" r="6" fill="none" stroke="#fff"/></g>''', f"tile{i}")

# ---------- monthly bars + stats ----------
mx = max(c for _, c in months) or 1
best = max(range(len(months)), key=lambda i: months[i][1])
b = ""
for i, (m, c) in enumerate(months):
    h = max(2, c / mx * 120); x = 40 + i * 68
    col = ACCENT if i == best else INK
    b += f'<rect class="grow" {dl(0.2+i*0.07)} x="{x}" y="{200-h:.1f}" width="44" height="{h:.1f}" rx="6" fill="{col}"/>'
    b += (f'<text x="{x+22}" y="222" text-anchor="middle" font-family="{SANS}" font-size="12" '
          f'fill="{MUTED}">{dt.date(int(m[:4]), int(m[5:]), 1):%b}</text>')
b += (f'<text class="pop" {dl(1.2)} x="{40+best*68+22}" y="{200-max(2,months[best][1]/mx*120)-8:.1f}" '
      f'text-anchor="middle" font-family="{SANS}" font-size="14" fill="{ACCENT}">{months[best][1]}</text>')
b += (f'<text x="40" y="44" font-family="{FONT}" font-size="30" fill="{INK}">{total} contributions</text>'
      f'<text x="40" y="68" font-family="{SANS}" font-size="14" fill="{MUTED}">'
      f'{streak}-day streak · {active} active days · busiest day {best_day[1]} on {best_day[0]}</text>')
svg(900, 240, b, "activity")

# ---------- blue graph ----------
mxd = max(c for _, c in days) or 1
def shade(c):
    if not c: return "#e8e4da"
    r = c / mxd
    return "#c7d3ff" if r < .25 else "#8fa8ff" if r < .5 else "#4f74ff" if r < .75 else ACCENT
g = ""
for wi, w in enumerate(weeks):
    for di, (d, c) in enumerate(w):
        g += (f'<rect class="pop" {dl(wi*0.03)} x="{30+wi*16}" y="{30+di*16}" width="12" '
              f'height="12" rx="3" fill="{shade(c)}"/>')
svg(900, 160, g, "graph")
