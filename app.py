import time
import streamlit as st
from dataclasses import dataclass, field
from typing import List, Iterable

EMOJIS = {
    "fazendeiro": "🧑‍🌾",
    "lobo": "🐺",
    "cabra": "🐐",
    "alface": "🥬",
    "barco": "🚣",
}

@dataclass
class Travessia:
    margem_esquerda: set = field(default_factory=lambda: {'lobo', 'cabra', 'alface'})
    margem_direita: set = field(default_factory=set)
    posicao_barco: str = 'esquerda'

    def reset(self):
        self.margem_esquerda = {'lobo', 'cabra', 'alface'}
        self.margem_direita = set()
        self.posicao_barco = 'esquerda'

    def problema_resolvido(self) -> bool:
        return len(self.margem_direita) == 3 and self.posicao_barco == 'direita'

    def estado_bits(self) -> str:
        def bit(nome: str) -> int:
            return 1 if nome in self.margem_direita else 0
        F = 1 if self.posicao_barco == 'direita' else 0
        L = bit('lobo'); C = bit('cabra'); A = bit('alface')
        return f"{F}{L}{C}{A}"

    def _seguro(self) -> bool:
        esq = set(self.margem_esquerda)
        dir = set(self.margem_direita)
        lado_sem_faz = dir if self.posicao_barco == 'esquerda' else esq
        if 'lobo' in lado_sem_faz and 'cabra' in lado_sem_faz:
            return False
        if 'cabra' in lado_sem_faz and 'alface' in lado_sem_faz:
            return False
        return True

    def mover_por_acao(self, acao: str):
        if acao not in {"F","FL","FC","FA"}:
            return False, "Ação inválida.", self.estado_bits(), None

        passageiro = None
        if acao == "FL": passageiro = "lobo"
        if acao == "FC": passageiro = "cabra"
        if acao == "FA": passageiro = "alface"

        origem = self.margem_esquerda if self.posicao_barco == 'esquerda' else self.margem_direita
        if passageiro and passageiro not in origem:
            return False, f"{EMOJIS.get(passageiro,'')} '{passageiro}' não está no mesmo lado do fazendeiro.", self.estado_bits(), None

        if passageiro: origem.remove(passageiro)
        lado_antes = self.posicao_barco
        self.posicao_barco = 'direita' if self.posicao_barco == 'esquerda' else 'esquerda'
        destino = self.margem_direita if self.posicao_barco == 'direita' else self.margem_esquerda
        if passageiro: destino.add(passageiro)

        if not self._seguro():
            if passageiro:
                destino.remove(passageiro)
                origem.add(passageiro)
            self.posicao_barco = lado_antes
            return False, "❌ Movimento inválido: alguém seria comido!", self.estado_bits(), None

        return True, "✅ Movimento realizado!", self.estado_bits(), passageiro

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

def apply_action(state: str, action: str):
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

def neighbors(s: str):
    res = []
    for a in SIGMA:
        ns = apply_action(s, a)
        if ns is not None:
            res.append((ns, a))
    return res

def edges():
    es = []
    for s in safe_states():
        for v,a in neighbors(s):
            if s < v:
                es.append((s,v,a))
    return es

def bfs_solution():
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

def _layout_by_levels():
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

def svg_diagrama(current: str = "0000", last_edge: tuple|None = None) -> str:
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
    δ = {s: {a: (apply_action(s,a) or "⊥") for a in Σ} for s in safe_states()}
    δ["⊥"] = {a: "⊥" for a in Σ}
    return K, Σ, δ, q0, F

st.set_page_config(page_title="Travessia — Lobo, Cabra e Alface", page_icon="🚣", layout="wide")

if "game" not in st.session_state:
    st.session_state.game = Travessia()
if "hist" not in st.session_state:
    st.session_state.hist = []
if "last_edge" not in st.session_state:
    st.session_state.last_edge = None
if "anim_speed" not in st.session_state:
    st.session_state.anim_speed = 0.05
if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = []

game: Travessia = st.session_state.game

st.title("🚣 Problema da Travessia — Lobo, Cabra e Alface")
st.caption("Leve todos para a direita sem ninguém comer ninguém. Estados como **F L C A** (0=esq, 1=dir).")

col_cfg1, col_cfg2, col_cfg3, col_cfg4 = st.columns([1,1,1,1])
st.session_state.anim_speed = col_cfg1.slider("Velocidade da animação (frames)", 0.01, 0.2, st.session_state.anim_speed, 0.01)

if col_cfg2.button("🔁 Reiniciar"):
    game.reset(); st.session_state.hist.clear(); st.session_state.undo_stack.clear(); st.session_state.last_edge=None
    st.rerun()

if col_cfg3.button("↩️ Desfazer"):
    if st.session_state.undo_stack:
        prev_state = st.session_state.undo_stack.pop()
        game.margem_esquerda, game.margem_direita, game.posicao_barco = prev_state
        st.session_state.last_edge = None
        if st.session_state.hist: st.session_state.hist.pop()
        st.rerun()

if col_cfg4.button("💡 Aplicar solução ótima"):
    sol = bfs_solution()
    if sol:
        game.reset(); st.session_state.hist.clear(); st.session_state.undo_stack.clear()
        for s, a in sol:
            ok, msg, new_s, passageiro = game.mover_por_acao(a)
            st.session_state.hist.append((s, a, ok, msg, new_s))
            st.session_state.last_edge = (s, new_s, a)
        st.success("Solução aplicada! 🎯")
        st.balloons()
        st.rerun()
    else:
        st.warning("Não encontrei solução.")

left_col, mid_col, right_col = st.columns([1.2, 0.6, 1.2])
left_ph = left_col.empty()
mid_ph = mid_col.empty()
right_ph = right_col.empty()

def render_bank(ph, title, items, farmer_here=False):
    with ph.container():
        st.markdown(f"**{title}**")
        linha = []
        if farmer_here:
            linha.append(f"{EMOJIS['fazendeiro']} fazendeiro")
        if items:
            linha += [f"{EMOJIS.get(it,'')} {it}" for it in sorted(items)]
        if linha:
            st.write(" · ".join(linha))
        else:
            st.markdown("_Vazio_")

def render_all():
    render_bank(
        left_ph, "Margem Esquerda", game.margem_esquerda,
        farmer_here=(game.posicao_barco == "esquerda")
    )
    with mid_ph.container():
        st.markdown("**Rio**")
        st.write(
            "Barco:",
            f"◀️ esquerda {EMOJIS['barco']}{EMOJIS['fazendeiro']}" if game.posicao_barco=="esquerda"
            else f"{EMOJIS['barco']}{EMOJIS['fazendeiro']} direita ▶️"
        )
        st.markdown("**Alfabeto Σ (Ações)**")
        c1,c2,c3,c4 = st.columns(4)
        if c1.button("F", use_container_width=True, key="btnF"): do_action("F")
        if c2.button("F+L", use_container_width=True, key="btnFL"): do_action("FL")
        if c3.button("F+C", use_container_width=True, key="btnFC"): do_action("FC")
        if c4.button("F+A", use_container_width=True, key="btnFA"): do_action("FA")
    render_bank(
        right_ph, "Margem Direita", game.margem_direita,
        farmer_here=(game.posicao_barco == "direita")
    )

def animate_cross(passageiro: str|None, indo_para_direita: bool):
    frames = 16
    holder = mid_col.empty()
    barquinho = EMOJIS["barco"] + EMOJIS["fazendeiro"] + (EMOJIS.get(passageiro, "") if passageiro else "")
    wave = "~"
    for i in range(frames):
        t = i / (frames-1)
        pos = int(t*10) if indo_para_direita else int((1-t)*10)
        river = wave*pos + barquinho + wave*(10-pos)
        with holder.container():
            st.markdown("**Rio**")
            st.markdown(f"<div style='text-align:center;font-size:28px'>{river}</div>", unsafe_allow_html=True)
        time.sleep(st.session_state.anim_speed)
    holder.empty()

def do_action(act_code: str):
    estado_inicial = game.estado_bits()
    prev_state = (set(game.margem_esquerda), set(game.margem_direita), game.posicao_barco)
    lado_antes = game.posicao_barco
    ok, msg, new_state, passageiro = game.mover_por_acao(act_code)
    if ok:
        st.session_state.undo_stack.append(prev_state)
        st.session_state.hist.append((estado_inicial, act_code, ok, msg, new_state))
        st.session_state.last_edge = (estado_inicial, new_state, act_code)
        animate_cross(passageiro, indo_para_direita=(lado_antes=="esquerda"))
        st.toast("Ação executada!", icon="✅")
        st.rerun()
    else:
        st.session_state.hist.append((estado_inicial, act_code, ok, msg, estado_inicial))
        st.session_state.last_edge = None
        st.error(msg)

render_all()

if game.problema_resolvido():
    st.success(f"🏁 Objetivo atingido! Estado {game.estado_bits()}")
    st.balloons()
else:
    st.info(f"Estado atual: `{game.estado_bits()}`")

st.markdown("### 📜 Histórico")
if st.session_state.hist:
    for s, a, ok, msg, ns in st.session_state.hist[-12:]:
        label = {"F":"F","FL":"F+L","FC":"F+C","FA":"F+A"}[a]
        icon = "✅" if ok else "❌"
        st.write(f"`{s}` — **{label}** → `{ns}` {icon} {msg}")
else:
    st.caption("Sem movimentos ainda.")

st.markdown("---")
left_g, right_g = st.columns([1,1])
with left_g:
    st.subheader("📈 Diagrama de estados (seguros)")
    from html import escape
    svg = svg_diagrama(game.estado_bits(), st.session_state.last_edge)
    st.components.v1.html(svg, height=600, scrolling=False)
    st.caption("Nó azul = estado atual. Nó verde = objetivo (1111). Aresta azul = última ação.")
with right_g:
    st.subheader("📚 Teoria — AF ⟨K, Σ, δ, q₀, F⟩")
    K, Σ, δ, q0, F = formal_afd()
    st.markdown(f"- **Σ**: {', '.join(['F','F+L','F+C','F+A'])}")
    st.markdown(f"- **q₀**: `{q0}`  |  **Finais**: {', '.join(F)}")
    with st.expander("Ver K (estados)"):
        st.write(", ".join(K))
    with st.expander("Amostra de δ (com estado-poço ⊥)"):
        mostra = ["0000","0101","1010","1111","⊥"]
        for s in mostra:
            if s not in δ: continue
            linha = " | ".join(f"{a}→{δ[s][a]}" for a in ["F","FL","FC","FA"])
            st.code(f"{s}: {linha}")
