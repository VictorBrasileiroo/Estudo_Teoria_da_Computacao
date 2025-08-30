# automato.py
from typing import List, Dict, Tuple, Iterable

SIGMA = ["F", "FL", "FC", "FA"]

def encode(state: List[int]) -> str:
    return "".join(str(b) for b in state)

def decode(bits: str) -> List[int]:
    return [int(c) for c in bits]

def is_safe(state_bits: Iterable[int]) -> bool:
    F,L,C,A = state_bits
    if L == C and F != L: return False
    if C == A and F != C: return False
    return True

def can_apply(state: str, action: str) -> bool:
    F,L,C,A = decode(state)
    if action == "F": return True
    if action == "FL": return F == L
    if action == "FC": return F == C
    if action == "FA": return F == A
    return False

def apply_action(state: str, action: str) -> str | None:
    if not can_apply(state, action): return None
    F,L,C,A = decode(state)
    flip = lambda x: 1-x
    if action == "F":  F = flip(F)
    if action == "FL": F, L = flip(F), flip(L)
    if action == "FC": F, C = flip(F), flip(C)
    if action == "FA": F, A = flip(F), flip(A)
    ns = [F,L,C,A]
    return encode(ns) if is_safe(ns) else None

def all_states() -> List[str]:
    return [encode([(i>>3)&1, (i>>2)&1, (i>>1)&1, i&1]) for i in range(16)]

def safe_states() -> List[str]:
    return [s for s in all_states() if is_safe(decode(s))]

def neighbors(s: str) -> List[Tuple[str,str]]:
    res = []
    for a in SIGMA:
        ns = apply_action(s, a)
        if ns is not None:
            res.append((ns, a))
    return res

def edges() -> List[Tuple[str,str,str]]:
    es = []
    for s in safe_states():
        for v,a in neighbors(s):
            if s < v:
                es.append((s,v,a))
    return es

def bfs_solution() -> List[Tuple[str,str]]:
    start, goal = "0000", "1111"
    from collections import deque
    q = deque([start])
    prev = {start: None}
    while q:
        u = q.popleft()
        if u == goal: break
        for v,a in neighbors(u):
            if v not in prev:
                prev[v] = (u,a)
                q.append(v)
    if goal not in prev: return []
    path = []
    cur = goal
    while cur != start:
        pu, act = prev[cur]
        path.append((pu, act))
        cur = pu
    path.reverse()
    return path

# ---- layout e SVG (com destaque do estado atual e da última aresta) ----
def _layout_by_levels() -> Dict[str, Tuple[float,float]]:
    from collections import deque
    start = "0000"
    dist = {start:0}
    Q = deque([start])
    while Q:
        u = Q.popleft()
        for v,_ in neighbors(u):
            if v not in dist:
                dist[v] = dist[u] + 1
                Q.append(v)
    layers = {}
    for s in safe_states():
        d = dist.get(s, 99)
        layers.setdefault(d, []).append(s)

    W,H = 900,520
    mx,my = 60,40
    pos = {}
    maxL = max(layers) if layers else 0
    for d, arr in sorted(layers.items()):
        x = mx + (W-2*mx) * (0 if maxL == 0 else d/maxL)
        gap = (H-2*my)/(len(arr)+1)
        for i,s in enumerate(arr,1):
            y = my + gap*i
            pos[s] = (x,y)
    return pos

def svg_diagrama(current: str = "0000", last_edge: tuple[str,str,str] | None = None) -> str:
    pos = _layout_by_levels()
    es = edges()
    W,H = 900,560

    def line(u,v,a):
        x1,y1 = pos[u]; x2,y2 = pos[v]
        active = (last_edge is not None) and ({u,v} == {last_edge[0], last_edge[1]} and a == last_edge[2])
        stroke = "#7aa2f7" if active else "rgba(255,255,255,0.18)"
        sw = 2.4 if active else 1.2
        return (f'<g class="edge">'
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"/>'
                f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2 - 6}" font-size="10" fill="#9aa0b4" text-anchor="middle">{a}</text>'
                f'</g>')

    def circle(s):
        cx,cy = pos[s]
        if s == current:
            stroke, sw = "#7aa2f7", 3
        elif s == "1111":
            stroke, sw = "#a6da95", 3
        else:
            stroke, sw = "rgba(255,255,255,0.35)", 1.2
        return (f'<g class="node">'
                f'<circle cx="{cx}" cy="{cy}" r="18" fill="#232746" stroke="{stroke}" stroke-width="{sw}"/>'
                f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-size="11" fill="#e7eaf6">{s}</text>'
                f'</g>')

    svg_edges = "\n".join(line(u,v,a) for (u,v,a) in es)
    svg_nodes = "\n".join(circle(s) for s in safe_states())
    style = """
    <style>
      svg { background: radial-gradient(900px 400px at 90% 0%, rgba(255,255,255,.03), rgba(255,255,255,.01)); border-radius: 12px; }
      text { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; }
    </style>
    """
    return f'''{style}
    <svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagrama de estados">
      {svg_edges}
      {svg_nodes}
    </svg>
    '''

def formal_afd():
    K = sorted(safe_states() + ["⊥"])
    Σ = SIGMA
    q0 = "0000"
    F = ["1111"]
    # δ total com estado-poço
    δ = {s: {a: (apply_action(s,a) or "⊥") for a in Σ} for s in safe_states()}
    δ["⊥"] = {a: "⊥" for a in Σ}
    return K, Σ, δ, q0, F
