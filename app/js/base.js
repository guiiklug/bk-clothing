/* BK Gestão (demonstração): dados, regras de estoque e de venda.
   As peças, marcas e preços vêm do catálogo do site (catalogo.js). Quantidades, custos, clientes e vendas
   passadas são de exemplo, gerados sempre iguais para cada dia. O que a pessoa faz no aplicativo
   (vender, dar entrada, ajustar, cadastrar) fica guardado no próprio aparelho. */
(() => {
'use strict';

const CAT = window.BK_CATALOGO;
const par = new URLSearchParams(location.search);
const FIXO = par.get('agora') ? new Date(par.get('agora')).getTime() : 0;   // relógio fixo, para gravar o vídeo
const T0 = Date.now();
const agora = () => (FIXO ? FIXO + (Date.now() - T0) : Date.now());
const SESSAO = agora();
const DIA = 864e5, MIN = 6e4;
const JANELA = 60;        // dias de histórico de exemplo
const PARADO = 45;        // dias sem vender para a peça contar como parada

const zero = t => { const d = new Date(t); d.setHours(0, 0, 0, 0); return d.getTime(); };
const diasAtras = (t0, n) => { const d = new Date(t0); d.setDate(d.getDate() - n); return d.getTime(); };
const chaveDia = t => { const d = new Date(t); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); };
const refDia = t0 => Math.round((t0 - new Date(2026, 0, 1).getTime()) / DIA);
const arred = v => Math.round(v * 100) / 100;

function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
function sorteio(semente) {
  let a = hash(String(semente));
  return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
function escolhe(r, pares) {
  let tot = 0; for (const p of pares) tot += p[1];
  let x = r() * tot;
  for (const p of pares) { x -= p[1]; if (x < 0) return p[0]; }
  return pares[pares.length - 1][0];
}

/* ---------- o que fica guardado no aparelho ---------- */
const CHAVE = 'bk-gestao-v1';
const VAZIO = () => ({ vendas: [], movs: [], prods: [], edits: {}, canc: {}, pedidos: {}, clientes: [], tema: '' });
let L = VAZIO();
try { L = Object.assign(VAZIO(), JSON.parse(localStorage.getItem(CHAVE) || '{}')); } catch (e) { /* aparelho sem armazenamento: segue só na memória */ }
let cache = null;
const ouvintes = [];
function salvar() {
  cache = null;
  try { localStorage.setItem(CHAVE, JSON.stringify(L)); } catch (e) { /* idem */ }
  ouvintes.forEach(f => f());
}
if (typeof document !== 'undefined') setInterval(() => { cache = null; }, 60000);

/* ---------- dados de exemplo ---------- */
// estoque combinado das peças com foto limpa, para a demonstração mostrar peça cheia, acabando e esgotada
const CENA = {
  '1914784': [2, 1, 0, 2], '1914785': [2, 3, 2, 1], '1914786': [1, 2, 3, 1], '1910184': [3, 4, 2, 1], '1910186': [0, 1, 1, 0],
  '1703192': [6], '1688196': [2, 3, 3, 1], '1703184': [1, 0, 2, 1], '1678831': [1, 2, 2, 0], '1701345': [2, 2, 1, 1],
  '1703197': [3, 2, 2, 2], '1679459': [1, 1, 0, 0], '1910182': [2, 3, 2, 1], '1849978': [4, 5, 4, 2], '1910183': [3, 2, 4, 2],
  '1914792': [0, 0, 0, 0], '1688777': [3, 4, 2, 2], '1849982': [2, 2, 3, 1], '1703189': [1, 0, 1, 0], '1849694': [2, 2, 1, 1],
  '1910185': [1, 2, 1, 1], '1849734': [3], '1703193': [0], '1690115': [3, 3, 2, 1],
};
// peças que puxam a venda na demonstração
const PESO = { '1914784': 9, '1910184': 7, '1703189': 6.5, '1849734': 6, '1688777': 6 };
const CLIENTES = ['Lucas M.', 'Rafael S.', 'Matheus K.', 'João Pedro', 'Gabriel W.', 'Vinícius R.', 'Eduardo B.', 'Felipe T.', 'Thiago L.',
  'Gustavo P.', 'André F.', 'Caio N.', 'Leonardo D.', 'Henrique V.', 'Diego A.', 'Murilo C.', 'Pedro Z.', 'Igor S.', 'Renan M.',
  'Daniel K.', 'Arthur G.', 'Otávio B.', 'Samuel R.', 'Yuri H.', 'Marcelo T.', 'Alan J.', 'Wesley F.', 'Douglas R.', 'Kauã S.',
  'Fábio L.', 'Jonas E.', 'Luan C.', 'Vitor H.', 'Emanuel P.', 'Ricardo G.', 'Tiago B.', 'Nicolas A.', 'Enzo V.', 'Paulo W.', 'Cristian O.'];
const CLI_PESO = CLIENTES.map((n, i) => [n, 1 + 1.6 / (i + 1)]);

const BASE = CAT.map(p => {
  const r = sorteio('p' + p.id);
  const peso = PESO[p.id] ? PESO[p.id] : p.std ? 2.8 + r() * 3 : (r() < 0.06 ? 0 : 1 + r() * r() * 1.6);
  const custo = Math.round(p.p * (0.42 + r() * 0.14));
  const est = {};
  p.s.forEach((t, i) => {
    let n;
    if (CENA[p.id]) n = CENA[p.id][i] || 0;
    else if (p.s.length === 1) n = 1 + Math.floor(r() * 6);
    else n = Math.floor(r() * r() * [3.4, 5.2, 5.2, 3][i]) + (r() < 0.74 ? 1 : 0);
    est[t] = n;
  });
  if (!peso && !Object.values(est).some(Boolean)) est[p.s[Math.min(1, p.s.length - 1)]] = 2;   // peça parada tem estoque
  const chegou = 12 + Math.floor(r() * 40);
  return Object.assign({}, p, { peso, custo, est0: est, chegou });
});
const PESOS = BASE.filter(p => p.peso > 0).map(p => [p, p.peso]);

const memoDia = {};
function vendasDoDia(t0, minimo) {
  const k = chaveDia(t0) + (minimo || '');
  if (memoDia[k]) return memoDia[k];
  const r = sorteio('d' + chaveDia(t0));
  const dow = new Date(t0).getDay();
  let n = Math.round([0, 4, 4.2, 4.6, 5.2, 7, 9.6][dow] * (0.72 + r() * 0.56));
  if (minimo) n = Math.max(n, minimo);
  const ref = refDia(t0);
  const out = [];
  for (let i = 0; i < n; i++) {
    const t = t0 + (9.5 + r() * 10) * 36e5;
    const ni = escolhe(r, [[1, 56], [2, 31], [3, 13]]);
    const itens = [];
    for (let j = 0; j < ni; j++) {
      const p = escolhe(r, PESOS);
      const tam = p.s.length === 1 ? p.s[0] : escolhe(r, p.s.map((s, x) => [s, [2, 4, 4, 2][x] || 2]));
      const ja = itens.find(x => x.pid === p.id && x.tam === tam);
      if (ja) ja.q++; else itens.push({ pid: p.id, tam, q: 1, pu: p.p, cu: p.custo });
    }
    const sub = arred(itens.reduce((s, x) => s + x.pu * x.q, 0));
    const pct = r() < 0.14 ? (r() < 0.6 ? 5 : 10) : 0;
    const desc = arred(sub * pct / 100);
    out.push({
      id: 's' + ref + '-' + i, t, itens, sub, desc, total: arred(sub - desc),
      pg: escolhe(r, [['pix', 52], ['credito', 26], ['debito', 12], ['dinheiro', 10]]),
      canal: escolhe(r, [['Loja', 50], ['WhatsApp', 38], ['Site', 12]]),
      cli: r() < 0.46 ? escolhe(r, CLI_PESO) : '',
    });
  }
  out.sort((a, b) => a.t - b.t);
  out.forEach((v, i) => { v.n = ref * 20 + i; });
  return (memoDia[k] = out);
}

/* ---------- retrato do momento ---------- */
function tudo() {
  if (cache) return cache;
  const t = agora(), hoje0 = zero(t);
  const vendas = [];
  for (let d = JANELA; d >= 1; d--) vendas.push(...vendasDoDia(diasAtras(hoje0, d)));
  const planoHoje = vendasDoDia(hoje0, 7);
  let deHoje = planoHoje.filter(v => v.t <= t);
  if (deHoje.length < 3) {   // aberto cedo: mostra as primeiras vendas do dia assim mesmo
    deHoje = planoHoje.slice(0, 3).map((v, i) => Object.assign({}, v, { t: Math.max(hoje0 + MIN * (i + 1), t - (3 - i) * 21 * MIN) }));
  }
  vendas.push(...deHoje, ...L.vendas);
  vendas.forEach(v => { v.canc = !!L.canc[v.id]; });
  vendas.sort((a, b) => b.t - a.t);

  const delta = {};
  for (const m of L.movs) { const d = delta[m.pid] || (delta[m.pid] = {}); d[m.tam] = (d[m.tam] || 0) + m.q; }
  const giro = {};
  for (const v of vendas) {
    if (v.canc) continue;
    for (const it of v.itens) {
      const g = giro[it.pid] || (giro[it.pid] = { v7: 0, v30: 0, ult: 0 });
      if (v.t >= t - 30 * DIA) g.v30 += it.q;
      if (v.t >= t - 7 * DIA) g.v7 += it.q;
      if (v.t > g.ult) g.ult = v.t;
    }
  }
  const prods = BASE.concat(L.prods).map(b => {
    const p = Object.assign({}, b, L.edits[b.id] || {});
    const d = delta[p.id] || {};
    p.est = {};
    p.s.forEach(s => { p.est[s] = Math.max(0, ((p.est0 || {})[s] || 0) + (d[s] || 0)); });
    p.total = p.s.reduce((a, s) => a + p.est[s], 0);
    p.falta = p.total ? p.s.filter(s => !p.est[s]) : [];
    const g = giro[p.id] || { v7: 0, v30: 0, ult: 0 };
    p.v7 = g.v7; p.v30 = g.v30; p.ult = g.ult;
    p.dias = g.ult ? Math.floor((t - g.ult) / DIA) : null;
    const idade = p.criado ? (t - p.criado) / DIA : 999;
    p.parado = p.total > 0 && idade >= PARADO && (p.dias === null || p.dias >= PARADO);
    p.status = !p.total ? 'zero' : (p.total <= 2 || (p.falta.length && p.v30 >= 3)) ? 'baixo' : 'ok';
    p.img = p.foto || 'img/t/' + p.id + '.webp';
    p.imgG = p.foto || 'img/g/' + p.id + '.webp';
    return p;
  });
  const porId = {};
  prods.forEach(p => { porId[p.id] = p; });
  const soma = f => prods.reduce((a, p) => a + f(p), 0);
  cache = {
    t, hoje0, vendas, prods, porId,
    pecas: soma(p => p.total),
    valorVenda: arred(soma(p => p.total * p.p)),
    valorCusto: arred(soma(p => p.total * (p.custo || 0))),
    zerados: prods.filter(p => p.status === 'zero'),
    baixos: prods.filter(p => p.status === 'baixo'),
    parados: prods.filter(p => p.parado).sort((a, b) => (b.dias === null ? 999 : b.dias) - (a.dias === null ? 999 : a.dias) || b.total * b.p - a.total * a.p),
  };
  cache.valorParado = arred(cache.parados.reduce((a, p) => a + p.total * p.p, 0));
  return cache;
}

function resumo(de, ate) {
  const D = tudo();
  const R = { total: 0, n: 0, pecas: 0, lucro: 0, desc: 0, pg: {}, canal: {}, cat: {}, marca: {}, prod: {} };
  for (const v of D.vendas) {
    if (v.canc || v.t < de || v.t >= ate) continue;
    R.total += v.total; R.n++; R.desc += v.desc;
    R.pg[v.pg] = (R.pg[v.pg] || 0) + v.total;
    R.canal[v.canal] = (R.canal[v.canal] || 0) + v.total;
    const fator = v.sub ? v.total / v.sub : 1;
    for (const it of v.itens) {
      const p = D.porId[it.pid];
      const val = it.pu * it.q * fator;
      R.pecas += it.q;
      R.lucro += val - (it.cu || (p && p.custo) || 0) * it.q;
      if (p) {
        R.cat[p.c] = (R.cat[p.c] || 0) + val;
        R.marca[p.b || 'Sem marca'] = (R.marca[p.b || 'Sem marca'] || 0) + val;
      }
      const x = R.prod[it.pid] || (R.prod[it.pid] = { p, q: 0, valor: 0 });
      x.q += it.q; x.valor += val;
    }
  }
  R.total = arred(R.total); R.lucro = arred(R.lucro); R.desc = arred(R.desc);
  R.ticket = R.n ? arred(R.total / R.n) : 0;
  R.top = Object.values(R.prod).filter(x => x.p).sort((a, b) => b.q - a.q || b.valor - a.valor);
  return R;
}

function serie(n) {
  const D = tudo();
  const out = [];
  for (let d = n - 1; d >= 0; d--) {
    const a = diasAtras(D.hoje0, d);
    out.push({ t0: a, total: resumo(a, diasAtras(D.hoje0, d - 1)).total });
  }
  return out;
}

function movimentos(pid) {
  const D = tudo(), p = D.porId[pid], out = [];
  for (const m of L.movs) if (m.pid === pid) out.push(m);
  for (const v of D.vendas) {
    if (v.u) continue;   // as vendas feitas no aparelho já estão em L.movs
    for (const it of v.itens) if (it.pid === pid) out.push({ t: v.t, pid, tam: it.tam, q: -it.q, tipo: 'venda', ref: v.n });
  }
  if (p && p.chegou) {
    const q = p.s.reduce((a, s) => a + (p.est0[s] || 0), 0) + p.v30;
    if (q) out.push({ t: diasAtras(D.hoje0, p.chegou) + 10.5 * 36e5, pid, tam: '', q, tipo: 'entrada' });
  }
  return out.sort((a, b) => b.t - a.t);
}

function clientes() {
  const D = tudo(), m = {};
  for (const c of L.clientes) m[c.nome] = { nome: c.nome, fone: c.fone || '', n: 0, total: 0, ult: 0, vendas: [] };
  for (const v of D.vendas) {
    if (v.canc || !v.cli) continue;
    const c = m[v.cli] || (m[v.cli] = { nome: v.cli, fone: '', n: 0, total: 0, ult: 0, vendas: [] });
    c.n++; c.total = arred(c.total + v.total); if (v.t > c.ult) c.ult = v.t; c.vendas.push(v);
  }
  return Object.values(m).sort((a, b) => b.total - a.total);
}

// o que pedir ao fornecedor: peça que gira e está sem tamanho ou com uma só
function reposicao() {
  const D = tudo(), out = [];
  for (const p of D.prods) {
    if (p.v30 < 3) continue;
    const alvo = Math.max(2, Math.round(p.v30 / p.s.length * 1.1));
    const pedir = p.s.map(s => ({ tam: s, tem: p.est[s], q: p.est[s] <= 1 ? Math.max(0, alvo - p.est[s]) : 0 })).filter(x => x.q > 0);
    if (pedir.length) out.push({ p, pedir, q: pedir.reduce((a, x) => a + x.q, 0) });
  }
  return out.sort((a, b) => b.p.v30 - a.p.v30);
}

function pedidos() {
  const k = chaveDia(SESSAO);
  return [
    { id: 'ped-' + k + '-1', t: SESSAO - 18 * MIN, canal: 'Site', cli: 'Rafael S.', itens: [{ pid: '1914785', tam: 'M', q: 1 }] },
    { id: 'ped-' + k + '-2', t: SESSAO - 74 * MIN, canal: 'Site', cli: 'Caio N.', itens: [{ pid: '1678831', tam: 'G', q: 1 }, { pid: '1688777', tam: 'M', q: 1 }] },
  ].filter(p => !L.pedidos[p.id]).map(p => {
    const D = tudo();
    p.itens.forEach(i => { i.pu = D.porId[i.pid].p; });
    p.total = arred(p.itens.reduce((a, i) => a + i.pu * i.q, 0));
    return p;
  });
}

/* ---------- ações ---------- */
function registrarVenda({ itens, pct = 0, pg, canal = 'Loja', cli = '' }) {
  const D = tudo(), t = agora();
  const linhas = itens.map(i => {
    const p = D.porId[i.pid];
    return { pid: i.pid, tam: i.tam, q: i.q, pu: p.p, cu: p.custo || 0, antes: p.est[i.tam] };
  });
  const sub = arred(linhas.reduce((a, i) => a + i.pu * i.q, 0));
  const desc = arred(sub * pct / 100);
  const ref = refDia(zero(t));
  const v = {
    id: 'u' + t.toString(36), u: 1, n: ref * 20 + 12 + L.vendas.filter(x => zero(x.t) === zero(t)).length,
    t, itens: linhas, sub, desc, pct, total: arred(sub - desc), pg, canal, cli: cli.trim(),
  };
  L.vendas.push(v);
  linhas.forEach(i => L.movs.push({ t, pid: i.pid, tam: i.tam, q: -i.q, tipo: 'venda', ref: v.n }));
  salvar();
  return v;
}

function cancelarVenda(id) {
  const v = tudo().vendas.find(x => x.id === id);
  if (!v || v.canc) return;
  const t = agora();
  L.canc[id] = 1;
  v.itens.forEach(i => L.movs.push({ t, pid: i.pid, tam: i.tam, q: i.q, tipo: 'cancelamento', ref: v.n }));
  salvar();
}

function ajustar(pid, tam, q, tipo) {
  if (!q) return;
  const p = tudo().porId[pid];
  if (!p || p.est[tam] + q < 0) return;
  const t = agora(), ult = L.movs[L.movs.length - 1];
  // toques seguidos no mesmo tamanho viram uma linha só no histórico
  if (ult && ult.tipo === (tipo || 'ajuste') && ult.pid === pid && ult.tam === tam && t - ult.t < 90000) {
    ult.q += q; ult.t = t;
    if (!ult.q) L.movs.pop();
  } else L.movs.push({ t, pid, tam, q, tipo: tipo || 'ajuste' });
  salvar();
}

function entrada(pid, porTam) {
  const t = agora();
  let n = 0;
  Object.keys(porTam).forEach(tam => { if (porTam[tam] > 0) { L.movs.push({ t, pid, tam, q: porTam[tam], tipo: 'entrada' }); n += porTam[tam]; } });
  if (n) salvar();
  return n;
}

function novoProduto(d) {
  const t = agora(), id = 'n' + t.toString(36);
  L.prods.push({ id, n: d.n, b: d.b, c: d.c, cor: d.cor, p: d.p, custo: d.custo, s: d.s, foto: d.foto || '', criado: t, est0: {}, peso: 0, std: 0 });
  d.s.forEach(tam => { if (d.q[tam] > 0) L.movs.push({ t, pid: id, tam, q: d.q[tam], tipo: 'entrada' }); });
  salvar();
  return id;
}

function editarProduto(pid, campos) { L.edits[pid] = Object.assign({}, L.edits[pid], campos); salvar(); }

function confirmarPedido(id, pg) {
  const p = pedidos().find(x => x.id === id);
  if (!p) return null;
  L.pedidos[id] = 'ok';
  return registrarVenda({ itens: p.itens, pg, canal: p.canal, cli: p.cli });
}
function recusarPedido(id) { L.pedidos[id] = 'x'; salvar(); }
function salvarCliente(nome, fone) {
  const c = L.clientes.find(x => x.nome === nome);
  if (c) c.fone = fone; else L.clientes.push({ nome, fone });
  salvar();
}
function tema(v) { if (v !== undefined) { L.tema = v; salvar(); } return L.tema; }
function reiniciar() { const t = L.tema; L = VAZIO(); L.tema = t; salvar(); }
function alterado() { return L.vendas.length + L.movs.length + L.prods.length + Object.keys(L.pedidos).length > 0; }

window.BK = {
  agora, zero, diasAtras, DIA, MIN, PARADO, JANELA, arred, tudo, resumo, serie, movimentos, clientes, reposicao, pedidos,
  registrarVenda, cancelarVenda, ajustar, entrada, novoProduto, editarProduto, confirmarPedido, recusarPedido, salvarCliente,
  tema, reiniciar, alterado, aoMudar: f => ouvintes.push(f),
  categorias: () => [...new Set(tudo().prods.map(p => p.c))],
  marcas: () => [...new Set(tudo().prods.map(p => p.b).filter(Boolean))].sort(),
};
})();
