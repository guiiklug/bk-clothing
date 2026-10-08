/* BK Gestão (demonstração): telas e toques. Os dados e as regras estão em base.js. */
(() => {
'use strict';

const B = window.BK;
const $ = (s, el) => (el || document).querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const norm = s => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const moeda = v => 'R$ ' + Number(v).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const moeda0 = v => 'R$ ' + Math.round(v).toLocaleString('pt-BR');
const dois = n => String(n).padStart(2, '0');
const hora = t => { const d = new Date(t); return dois(d.getHours()) + ':' + dois(d.getMinutes()); };
const SEM = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb'];
const MES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
const MESL = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
const dataCurta = t => { const d = new Date(t); return SEM[d.getDay()] + ', ' + d.getDate() + ' ' + MES[d.getMonth()]; };
const dataHora = t => { const d = new Date(t); return dois(d.getDate()) + '/' + dois(d.getMonth() + 1) + ' ' + hora(t); };
const rotDia = t => { const h0 = B.tudo().hoje0, z = B.zero(t); return z === h0 ? 'Hoje' : z === B.diasAtras(h0, 1) ? 'Ontem' : dataCurta(t); };
const ha = t => { const m = Math.max(1, Math.round((B.agora() - t) / B.MIN)); return m < 60 ? 'há ' + m + ' min' : m < 1440 ? 'há ' + Math.floor(m / 60) + ' h' : 'há ' + Math.floor(m / 1440) + ' d'; };
const plural = (n, um, mais) => n + ' ' + (n === 1 ? um : mais);
const lista = a => (a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' e ' + a[a.length - 1]);
const numero = v => { const s = String(v).trim(); return Number(s.indexOf(',') >= 0 ? s.replace(/\./g, '').replace(',', '.') : s) || 0; };
const PG = { pix: 'Pix', credito: 'Crédito', debito: 'Débito', dinheiro: 'Dinheiro' };
const CANAL = { Loja: 'Na loja', WhatsApp: 'Pelo WhatsApp', Site: 'Pelo site' };

const svg = d => '<svg viewBox="0 0 24 24" aria-hidden="true">' + d + '</svg>';
const I = {
  inicio: svg('<path d="M4 10.5 12 4l8 6.5V20h-5.5v-6h-5v6H4z"/>'),
  estoque: svg('<path d="M4 8l8-4 8 4v9l-8 4-8-4z"/><path d="M4 8l8 4 8-4M12 12v9"/>'),
  mais: svg('<path d="M12 5v14M5 12h14"/>'),
  vendas: svg('<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>'),
  menu: svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
  busca: svg('<circle cx="11" cy="11" r="6"/><path d="M16 16l4 4"/>'),
  voltar: svg('<path d="M14 5l-7 7 7 7"/>'),
  seta: svg('<path d="M9 5l7 7-7 7"/>'),
  x: svg('<path d="M6 6l12 12M18 6L6 18"/>'),
  check: svg('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
  camera: svg('<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>'),
  marca: '<svg viewBox="0 0 30 34" aria-hidden="true"><path d="M10 2H2v30h8M20 2h8v30h-8"/><text x="15" y="21" text-anchor="middle" font-family="Jost,sans-serif" font-weight="300" font-size="11" fill="currentColor" stroke="none">BK</text></svg>',
};

/* o que está na tela agora (não fica guardado) */
const U = {
  est: { q: '', st: '', cat: '' },
  vd: { q: '', cat: '' },
  en: { q: '', feitas: [], tmp: {} },
  car: [], pct: 0, pg: 'pix', canal: 'Loja', cli: '',
  aba: 'historico', per: 7,
  par: { sel: null, pct: 20 },
  novo: null, instalar: null,
};

const elTopo = $('#topo'), elTela = $('#tela'), elAbas = $('#abas'), elCobrar = $('#cobrar');
const elVeu = $('#veu'), elFolha = $('#folha'), elAviso = $('#aviso');

/* ---------- peças de tela ---------- */
const sub = p => [p.b, p.cor].filter(Boolean).join(' · ');
function stRot(p) {
  if (p.status === 'zero') return ['zero', 'Esgotada'];
  if (p.status === 'baixo') return ['baixo', p.falta.length ? 'Falta ' + p.falta.join(', ') : 'Acabando'];
  if (p.parado) return ['par', 'Parada'];
  return ['', ''];
}
function linhaProd(p, acao) {
  const st = stRot(p);
  const dentro = '<img class="mini" src="' + esc(p.img) + '" alt="" loading="lazy">' +
    '<span class="it-c"><b>' + esc(p.n) + '</b><small>' + esc(sub(p)) + '</small>' +
    (p.s.length > 1 ? '<span class="tams">' + p.s.map(s => '<i class="' + (p.est[s] ? '' : 'z') + '">' + esc(s) + ' <b>' + p.est[s] + '</b></i>').join('') + '</span>' : '') + '</span>' +
    '<span class="it-d"><b class="it-q">' + p.total + '</b>' + (st[1] ? '<span class="st ' + st[0] + '">' + st[1] + '</span>' : '') + '</span>';
  return acao
    ? '<button class="it" data-a="' + acao + '" data-id="' + p.id + '">' + dentro + '</button>'
    : '<a class="it" href="#/estoque/p/' + p.id + '">' + dentro + '</a>';
}
function itensRot(v) {
  const p = B.tudo().porId[v.itens[0].pid];
  const n = v.itens.reduce((a, i) => a + i.q, 0);
  return esc(p ? p.n : 'Peça') + (n > 1 ? ' + ' + (n - 1) : '');
}
function linhaVenda(v, comDia) {
  return '<a class="ln' + (v.canc ? ' canc' : '') + '" href="#/vendas/v/' + v.id + '"><span class="ln-h">' + hora(v.t) + '</span>' +
    '<span class="ln-c"><b>' + itensRot(v) + '</b><small>' + [comDia ? rotDia(v.t) : '', PG[v.pg], CANAL[v.canal], v.cli].filter(Boolean).map(esc).join(' · ') + (v.canc ? ' · cancelada' : '') + '</small></span>' +
    '<b class="ln-v">' + moeda(v.total) + '</b></a>';
}
function linhaItem(it, dir) {
  const p = B.tudo().porId[it.pid] || { n: 'Peça', img: '', cor: '' };
  return '<div class="ln"><img class="mini p" src="' + esc(p.img) + '" alt=""><span class="ln-c"><b>' + (it.q > 1 ? it.q + 'x ' : '') + esc(p.n) + '</b><small>' +
    esc([p.cor, 'tam. ' + it.tam].filter(Boolean).join(' · ')) + '</small></span>' + (dir || '<b class="ln-v">' + moeda(it.pu * it.q) + '</b>') + '</div>';
}
const chip = (rot, on, attrs, n) => '<button class="chip' + (on ? ' on' : '') + '" ' + attrs + '>' + esc(rot) + (n === undefined ? '' : ' <b>' + n + '</b>') + '</button>';
const barra = (rot, v, tot) => '<div class="hb"><div class="hb-l"><span>' + esc(rot) + '</span><b>' + moeda(v) + ' · ' + Math.round(v / (tot || 1) * 100) + '%</b></div><i style="width:' + Math.max(1, v / (tot || 1) * 100).toFixed(1) + '%"></i></div>';
const fh = (t, s, img) => '<div class="fh">' + (img ? '<img class="mini p" src="' + esc(img) + '" alt="">' : '') + '<div><b>' + esc(t) + '</b>' + (s ? '<small>' + esc(s) + '</small>' : '') + '</div><button class="ic" data-a="fechar" aria-label="Fechar">' + I.x + '</button></div>';

function abrirFolha(html) {
  elFolha.innerHTML = html;
  elVeu.hidden = elFolha.hidden = false;
  void elFolha.offsetWidth;
  elVeu.classList.add('on'); elFolha.classList.add('on');
  elFolha.scrollTop = 0;
}
function fecharFolha() {
  elVeu.classList.remove('on'); elFolha.classList.remove('on');
  setTimeout(() => { if (!elFolha.classList.contains('on')) elVeu.hidden = elFolha.hidden = true; }, 320);
}
let tAviso = 0;
function aviso(txt) {
  elAviso.textContent = txt; elAviso.hidden = false;
  void elAviso.offsetWidth; elAviso.classList.add('on');
  clearTimeout(tAviso);
  tAviso = setTimeout(() => elAviso.classList.remove('on'), 2200);
}
function folhaMsg(titulo, texto, nota) {
  abrirFolha(fh(titulo, nota || 'Mensagem pronta para enviar') + '<pre class="msg" id="msg">' + esc(texto) + '</pre>' +
    '<div class="pz col" style="padding-top:0"><a class="btn cheio" target="_blank" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent(texto) + '">Abrir no WhatsApp</a>' +
    '<button class="btn" data-a="copiar">Copiar texto</button></div>');
}

/* ---------- carrinho ---------- */
const noCar = (pid, tam) => (U.car.find(i => i.pid === pid && i.tam === tam) || { q: 0 }).q;
function totalCar() {
  const D = B.tudo();
  const s = B.arred(U.car.reduce((a, i) => a + D.porId[i.pid].p * i.q, 0));
  const d = B.arred(s * U.pct / 100);
  return { sub: s, desc: d, total: B.arred(s - d), n: U.car.reduce((a, i) => a + i.q, 0) };
}
function folhaTam(p) {
  abrirFolha(fh(p.n, sub(p) + ' · ' + moeda(p.p), p.img) + '<div class="pz"><p class="fl">Toque ' + (p.s.length > 1 ? 'no tamanho ' : '') + 'para pôr na venda</p>' +
    '<div class="tm' + (p.s.length === 1 ? ' um' : '') + '">' + p.s.map(s => {
      const d = p.est[s] - noCar(p.id, s);
      return '<button data-a="add" data-id="' + p.id + '" data-tam="' + esc(s) + '"' + (d > 0 ? '' : ' disabled') + '><b>' + esc(s) + '</b><span>' + (d > 0 ? d + ' em estoque' : 'esgotado') + '</span></button>';
    }).join('') + '</div></div>');
}

/* ---------- textos para o WhatsApp ---------- */
function txtComprovante(v) {
  const D = B.tudo();
  const l = ['*BK Clothing*', 'Comprovante da compra #' + v.n, dataHora(v.t), ''];
  v.itens.forEach(i => { const p = D.porId[i.pid]; l.push(i.q + 'x ' + (p ? p.n : 'Peça') + ' (' + [p && p.cor, i.tam].filter(Boolean).join(', ') + ') ' + moeda(i.pu * i.q)); });
  l.push('');
  if (v.desc) l.push('Desconto: ' + moeda(v.desc));
  l.push('Total: ' + moeda(v.total), 'Pagamento: ' + PG[v.pg], '', 'Obrigado pela compra.');
  return l.join('\n');
}
function txtFechamento() {
  const D = B.tudo(), R = B.resumo(D.hoje0, D.hoje0 + B.DIA);
  const l = ['*Fechamento BK Clothing*', dataCurta(D.t), '', 'Vendas: ' + R.n, 'Peças: ' + R.pecas, 'Total: ' + moeda(R.total), ''];
  Object.keys(PG).forEach(k => { if (R.pg[k]) l.push(PG[k] + ': ' + moeda(R.pg[k])); });
  if (R.desc) l.push('', 'Descontos dados: ' + moeda(R.desc));
  return l.join('\n');
}
function txtReposicao() {
  const l = ['*Pedido de reposição BK Clothing*', ''];
  B.reposicao().forEach(x => l.push(x.p.n + (x.p.cor ? ' (' + x.p.cor + ')' : '') + ': ' + x.pedir.map(t => t.q + ' ' + t.tam).join(', ')));
  return l.join('\n');
}
function txtOferta() {
  const D = B.tudo();
  const l = ['*Seleção do grupo VIP*', U.par.pct + '% de desconto nestas peças, enquanto durar o estoque:', ''];
  D.parados.filter(p => U.par.sel[p.id]).forEach(p => {
    l.push(p.n + (p.cor ? ' (' + p.cor + ')' : '') + ': de ' + moeda(p.p) + ' por ' + moeda(p.p * (1 - U.par.pct / 100)) + (p.s.length > 1 ? ' · ' + p.s.filter(s => p.est[s]).join(', ') : ''));
  });
  l.push('', 'Responda aqui para reservar a sua.');
  return l.join('\n');
}

/* ---------- telas ---------- */
function telaInicio() {
  const D = B.tudo(), d = new Date(D.t);
  const h = B.resumo(D.hoje0, D.hoje0 + B.DIA);
  const s = B.serie(7), max = Math.max.apply(null, s.map(x => x.total).concat(1)), sete = s.reduce((a, x) => a + x.total, 0);
  const ped = B.pedidos();
  const nomes = a => esc(a.slice(0, 3).map(p => p.n).join(', ') + (a.length > 3 ? '…' : ''));
  const at = [];
  if (ped.length) at.push('<a class="at" href="#/vendas" data-a="ir-pedidos"><b class="at-n">' + ped.length + '</b><span class="at-c">' + (ped.length === 1 ? 'pedido do site aguardando' : 'pedidos do site aguardando') + '<small>' + esc(ped.map(p => p.cli).join(', ')) + '</small></span>' + I.seta + '</a>');
  if (D.zerados.length) at.push('<a class="at" href="#/estoque" data-a="ir-estoque" data-st="zero"><b class="at-n r">' + D.zerados.length + '</b><span class="at-c">' + (D.zerados.length === 1 ? 'peça esgotada' : 'peças esgotadas') + '<small>' + nomes(D.zerados) + '</small></span>' + I.seta + '</a>');
  if (D.baixos.length) at.push('<a class="at" href="#/estoque" data-a="ir-estoque" data-st="baixo"><b class="at-n a">' + D.baixos.length + '</b><span class="at-c">acabando ou sem algum tamanho<small>' + nomes(D.baixos.slice().sort((a, b) => b.v30 - a.v30)) + '</small></span>' + I.seta + '</a>');
  if (D.parados.length) at.push('<a class="at" href="#/mais/paradas"><b class="at-n">' + D.parados.length + '</b><span class="at-c">paradas há mais de ' + B.PARADO + ' dias<small>' + moeda0(D.valorParado) + ' em estoque sem girar</small></span>' + I.seta + '</a>');
  const ult = D.vendas.slice(0, 4);
  return {
    semTopo: true,
    html: '<section class="hoje"><div class="hoje-t"><span class="marca">' + I.marca + 'Gestão</span><span>' + SEM[d.getDay()] + ', ' + d.getDate() + ' de ' + MESL[d.getMonth()] + '</span></div>' +
      '<p class="hoje-r">Vendido hoje</p><p class="hoje-v"><small>R$</small>' + h.total.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) + '</p>' +
      '<p class="hoje-s"><b>' + plural(h.n, 'venda', 'vendas') + '</b> · ' + plural(h.pecas, 'peça', 'peças') + ' · ticket médio ' + moeda(h.ticket) + '</p>' +
      '<div class="sem">' + s.map((x, i) => '<div class="' + (i === 6 ? 'h' : '') + '"><i style="height:' + Math.round(x.total / max * 100) + '%"></i>' + SEM[new Date(x.t0).getDay()] + '</div>').join('') + '</div>' +
      '<p class="sem-l"><span>Últimos 7 dias</span><b>' + moeda(sete) + '</b></p></section>' +
      '<div class="dupla"><a class="btn cheio" href="#/vender">Nova venda</a><a class="btn" href="#/estoque/entrada">Entrada de peças</a></div>' +
      (at.length ? '<h2 class="sec">Precisa de atenção</h2>' + at.join('') : '') +
      '<h2 class="sec">Últimas vendas <a href="#/vendas" data-a="ir-historico">Ver todas</a></h2>' + (ult.length ? ult.map(v => linhaVenda(v, B.zero(v.t) !== D.hoje0)).join('') : '<p class="vazio">Nenhuma venda ainda.</p>') +
      '<p class="nota">Demonstração. As peças e os preços são do catálogo da BK; quantidades, custos, clientes e vendas são de exemplo.</p>',
  };
}

function filtrados() {
  const D = B.tudo(), f = U.est, termos = norm(f.q).split(/\s+/).filter(Boolean);
  let a = D.prods.filter(p => {
    if (f.cat && p.c !== f.cat) return false;
    if (f.st === 'zero' && p.status !== 'zero') return false;
    if (f.st === 'baixo' && p.status !== 'baixo') return false;
    if (f.st === 'parado' && !p.parado) return false;
    if (termos.length) { const alvo = norm(p.n + ' ' + p.b + ' ' + p.cor + ' ' + p.c); if (!termos.every(t => alvo.indexOf(t) >= 0)) return false; }
    return true;
  });
  a = a.slice().sort((x, y) => (y.criado || 0) - (x.criado || 0) || y.v30 - x.v30 || y.total - x.total);
  return a;
}
function chipsEstoque() {
  const D = B.tudo(), f = U.est;
  return '<div class="chips">' + chip('Todas', !f.st, 'data-a="f-st" data-v=""', D.prods.length) + chip('Acabando', f.st === 'baixo', 'data-a="f-st" data-v="baixo"', D.baixos.length) +
    chip('Esgotadas', f.st === 'zero', 'data-a="f-st" data-v="zero"', D.zerados.length) + chip('Paradas', f.st === 'parado', 'data-a="f-st" data-v="parado"', D.parados.length) + '</div>' +
    '<div class="chips">' + chip('Todas as categorias', !f.cat, 'data-a="f-cat" data-v=""') + B.categorias().map(c => chip(c, f.cat === c, 'data-a="f-cat" data-v="' + esc(c) + '"')).join('') + '</div>';
}
function telaEstoque() {
  const D = B.tudo(), a = filtrados();
  return {
    titulo: 'Estoque',
    acao: '<a class="ic" href="#/estoque/novo" aria-label="Cadastrar peça">' + I.mais + '</a>',
    html: '<div class="cab"><label class="busca">' + I.busca + '<input id="q" type="search" placeholder="Buscar peça, marca ou cor" autocomplete="off" value="' + esc(U.est.q) + '"></label>' +
      '<p class="conta">' + D.prods.length + ' produtos · ' + D.pecas + ' peças · ' + moeda0(D.valorVenda) + ' em preço de venda</p><div id="chips">' + chipsEstoque() + '</div></div>' +
      '<div id="lista">' + (a.length ? a.map(p => linhaProd(p)).join('') : '<p class="vazio">Nenhuma peça com esse filtro.</p>') + '</div>',
    pronto() {
      $('#q').addEventListener('input', e => { U.est.q = e.target.value; const b = filtrados(); $('#lista').innerHTML = b.length ? b.map(p => linhaProd(p)).join('') : '<p class="vazio">Nenhuma peça com esse filtro.</p>'; });
    },
  };
}

function telaProduto(id) {
  const D = B.tudo(), p = D.porId[id];
  if (!p) { ir('/estoque', true); return null; }
  const st = stRot(p);
  const mg = p.p && p.custo ? Math.round((1 - p.custo / p.p) * 100) + '%' : 'sem custo';
  const disp = p.s.filter(s => p.est[s]);
  const site = p.criado ? 'Ainda não publicada' : !p.total ? 'Aparece como esgotada' : p.s.length === 1 ? 'Disponível' : p.falta.length ? lista(disp) + ' à venda · ' + lista(p.falta) + ' esgotado' : 'Todos os tamanhos à venda';
  const ult = p.ult ? (p.dias === 0 ? 'hoje' : p.dias === 1 ? 'ontem' : 'há ' + p.dias + ' dias') : p.criado ? 'ainda não vendeu' : 'nenhuma em ' + B.JANELA + ' dias';
  let dica = '';
  if (p.total && p.v30 >= 2) dica = 'Vendeu ' + p.v30 + ' em 30 dias. Nesse ritmo, o estoque dura cerca de ' + Math.max(1, Math.round(p.total / (p.v30 / 30))) + ' dias.';
  else if (p.parado) dica = 'Parada: ' + moeda0(p.total * p.p) + ' em estoque sem vender há ' + (p.dias === null ? 'mais de ' + B.JANELA : p.dias) + ' dias.';
  else if (!p.total && p.v30) dica = 'Esgotou e estava vendendo: ' + p.v30 + ' em 30 dias. Está na lista de reposição.';
  const mov = B.movimentos(id).slice(0, 12);
  const rotMov = m => (m.tipo === 'venda' ? 'Venda #' + m.ref : m.tipo === 'cancelamento' ? 'Venda #' + m.ref + ' cancelada' : m.tipo === 'entrada' ? 'Entrada' : 'Ajuste') + (m.tam && p.s.length > 1 ? ' · ' + m.tam : '');
  return {
    titulo: p.n, voltar: '#/estoque',
    html: '<div class="foto' + (p.std && !p.foto ? ' alta' : '') + '"><img src="' + esc(p.imgG) + '" alt=""></div>' +
      '<div class="pd"><small>' + esc([p.b, p.c].filter(Boolean).join(' · ')) + '</small><h2>' + esc(p.n) + '</h2>' +
      '<div class="pd-l"><span class="pd-p">' + moeda(p.p) + (p.cor ? ' <small>· ' + esc(p.cor) + '</small>' : '') + '</span>' + (st[1] ? '<span class="st ' + st[0] + '">' + st[1] + '</span>' : '<span class="st ok">Em dia</span>') + '</div></div>' +
      '<h3 class="sec">Estoque por tamanho <span>' + plural(p.total, 'peça', 'peças') + '</span></h3>' +
      '<div class="tg">' + p.s.map(s => '<div class="tg-c' + (p.est[s] ? '' : ' z') + '"><span>' + esc(s) + '</span><b>' + p.est[s] + '</b><div class="tg-b">' +
        '<button data-a="aj" data-id="' + p.id + '" data-tam="' + esc(s) + '" data-q="-1" aria-label="Tirar uma"' + (p.est[s] ? '' : ' disabled') + '>−</button>' +
        '<button data-a="aj" data-id="' + p.id + '" data-tam="' + esc(s) + '" data-q="1" aria-label="Somar uma">+</button></div></div>').join('') + '</div>' +
      (dica ? '<p class="dica">' + esc(dica) + '</p>' : '') +
      '<div class="dupla"><button class="btn cheio" data-a="escolher" data-id="' + p.id + '"' + (p.total ? '' : ' disabled') + '>Vender</button><button class="btn" data-a="entrada" data-id="' + p.id + '">Entrada</button></div>' +
      '<h3 class="sec">Preço e giro <a href="#" data-a="editar" data-id="' + p.id + '">Editar</a></h3>' +
      '<div class="kv"><span>Preço de venda</span><b>' + moeda(p.p) + '</b></div><div class="kv"><span>Custo</span><b>' + (p.custo ? moeda(p.custo) : 'não informado') + '</b></div>' +
      '<div class="kv"><span>Margem</span><b>' + mg + '</b></div><div class="kv"><span>Vendidas em 30 dias</span><b>' + p.v30 + '</b></div>' +
      '<div class="kv"><span>Última venda</span><b>' + ult + '</b></div><div class="kv"><span>No site</span><b>' + esc(site) + '</b></div>' +
      '<h3 class="sec">Movimentações</h3>' + (mov.length ? mov.map(m => '<div class="mv"><span>' + dataHora(m.t) + '</span><span>' + esc(rotMov(m)) + '</span><b class="' + (m.q < 0 ? 'n' : 'p') + '">' + (m.q > 0 ? '+' : '−') + Math.abs(m.q) + '</b></div>').join('') : '<p class="vazio">Sem movimentação.</p>'),
  };
}

function gradeVender() {
  const D = B.tudo(), f = U.vd, termos = norm(f.q).split(/\s+/).filter(Boolean);
  const a = D.prods.filter(p => (!f.cat || p.c === f.cat) && (!termos.length || termos.every(t => norm(p.n + ' ' + p.b + ' ' + p.cor + ' ' + p.c).indexOf(t) >= 0)))
    .sort((x, y) => (y.total > 0) - (x.total > 0) || y.v30 - x.v30);
  if (!a.length) return '<p class="vazio">Nenhuma peça com esse nome.</p>';
  return '<div class="grade">' + a.map(p => {
    const c = U.car.filter(i => i.pid === p.id).reduce((s, i) => s + i.q, 0);
    return '<button class="tile' + (p.total ? '' : ' z') + '" data-a="escolher" data-id="' + p.id + '"><img src="' + esc(p.img) + '" alt="" loading="lazy">' +
      '<span class="tile-q">' + (p.total ? p.total : 'Esgotada') + '</span>' + (c ? '<span class="tile-c">' + c + '</span>' : '') +
      '<span class="tile-n">' + esc(p.n) + (p.cor ? ' <span style="display:inline;padding:0" class="mute">' + esc(p.cor) + '</span>' : '') + '</span><span class="tile-p">' + moeda(p.p) + '</span></button>';
  }).join('') + '</div>';
}
function telaVender() {
  return {
    titulo: 'Nova venda',
    acao: U.car.length ? '<button class="ic" data-a="limpar" aria-label="Esvaziar a venda">' + I.x + '</button>' : '',
    html: '<div class="cab"><label class="busca">' + I.busca + '<input id="q" type="search" placeholder="Buscar peça para vender" autocomplete="off" value="' + esc(U.vd.q) + '"></label>' +
      '<div class="chips">' + chip('Tudo', !U.vd.cat, 'data-a="v-cat" data-v=""') + B.categorias().map(c => chip(c, U.vd.cat === c, 'data-a="v-cat" data-v="' + esc(c) + '"')).join('') + '</div></div>' +
      '<div id="lista">' + gradeVender() + '</div>',
    pronto() { $('#q').addEventListener('input', e => { U.vd.q = e.target.value; $('#lista').innerHTML = gradeVender(); }); },
  };
}

function telaCobrar() {
  if (!U.car.length) { ir('/vender', true); return null; }
  const D = B.tudo(), T = totalCar();
  return {
    titulo: 'Cobrar', voltar: '#/vender',
    html: U.car.map((i, k) => {
      const p = D.porId[i.pid];
      return '<div class="car"><img class="mini" src="' + esc(p.img) + '" alt=""><span class="ln-c"><b>' + esc(p.n) + '</b><small>' + esc([p.cor, 'tam. ' + i.tam].filter(Boolean).join(' · ')) + '</small><small class="num" style="color:var(--fg)">' + moeda(p.p * i.q) + '</small></span>' +
        '<div class="qt"><button data-a="car-q" data-k="' + k + '" data-q="-1" aria-label="Tirar">−</button><b>' + i.q + '</b><button data-a="car-q" data-k="' + k + '" data-q="1" aria-label="Somar"' + (i.q < p.est[i.tam] ? '' : ' disabled') + '>+</button></div></div>';
    }).join('') +
      '<div class="bl"><p class="fl">Forma de pagamento</p><div class="pgs">' + Object.keys(PG).map(k => '<button class="pg' + (U.pg === k ? ' on' : '') + '" data-a="pg" data-v="' + k + '">' + PG[k] + '</button>').join('') + '</div></div>' +
      '<div class="bl"><p class="fl">Desconto</p><div class="chips fixo">' + [0, 5, 10, 15].map(v => chip(v ? v + '%' : 'Sem desconto', U.pct === v, 'data-a="pct" data-v="' + v + '"')).join('') + '</div></div>' +
      '<div class="bl"><p class="fl">Onde foi a venda</p><div class="chips fixo">' + ['Loja', 'WhatsApp'].map(v => chip(CANAL[v], U.canal === v, 'data-a="canal" data-v="' + v + '"')).join('') + '</div></div>' +
      '<div class="bl"><label class="campo" style="margin:0"><span>Cliente (opcional)</span><input id="cli" list="dl-cli" placeholder="Nome de quem comprou" autocomplete="off" value="' + esc(U.cli) + '"></label>' +
      '<datalist id="dl-cli">' + B.clientes().slice(0, 40).map(c => '<option value="' + esc(c.nome) + '">').join('') + '</datalist></div>' +
      '<div class="tot"><div class="kv"><span>Subtotal · ' + plural(T.n, 'peça', 'peças') + '</span><b>' + moeda(T.sub) + '</b></div>' + (T.desc ? '<div class="kv"><span>Desconto de ' + U.pct + '%</span><b>− ' + moeda(T.desc) + '</b></div>' : '') +
      '<div class="kv g"><span>Total</span><b>' + moeda(T.total) + '</b></div></div>' +
      '<div class="pz"><button class="btn cheio" data-a="concluir">Concluir venda</button></div>',
    pronto() { $('#cli').addEventListener('input', e => { U.cli = e.target.value; }); },
  };
}

function telaOk(id) {
  const D = B.tudo(), v = D.vendas.find(x => x.id === id);
  if (!v) { ir('/vender', true); return null; }
  return {
    titulo: 'Venda #' + v.n,
    html: '<div class="okb"><div class="okc">' + I.check + '</div><h2>Venda registrada</h2><p class="okv">' + moeda(v.total) + '</p>' +
      '<p class="mute">' + esc([PG[v.pg], CANAL[v.canal], v.cli, hora(v.t)].filter(Boolean).join(' · ')) + '</p></div>' +
      '<h3 class="sec">Estoque atualizado</h3>' +
      v.itens.map(i => {
        const p = D.porId[i.pid], dep = p ? p.est[i.tam] : 0, ant = i.antes === undefined ? dep + i.q : i.antes;
        return linhaItem(i, '<span class="dp' + (dep ? '' : ' z') + '">' + ant + ' → <b>' + dep + '</b></span>') +
          (dep === 0 ? '<p class="alerta">' + esc(p.n) + (p.s.length > 1 ? ' ' + i.tam : '') + ' esgotou.' + (p.v30 >= 3 ? ' Já está na lista de reposição.' : '') + '</p>' : dep === 1 ? '<p class="alerta" style="color:var(--warn)">Só resta 1 ' + esc(p.n) + (p.s.length > 1 ? ' ' + i.tam : '') + '.</p>' : '');
      }).join('') +
      '<div class="pz col"><button class="btn cheio" data-a="comprovante" data-id="' + v.id + '">Enviar comprovante</button><a class="btn" href="#/vender">Nova venda</a></div><a class="lk" href="#/">Voltar ao início</a>',
  };
}

function telaVendas() {
  const D = B.tudo(), ped = B.pedidos();
  let corpo = '';
  if (U.aba === 'historico') {
    const dias = [];
    for (const v of D.vendas) {
      const z = B.zero(v.t);
      let g = dias[dias.length - 1];
      if (!g || g.z !== z) { if (dias.length === 14) break; dias.push(g = { z, v: [], tot: 0, n: 0 }); }
      g.v.push(v); if (!v.canc) { g.tot += v.total; g.n++; }
    }
    corpo = dias.map(g => '<div class="dia">' + rotDia(g.z) + '<span>' + moeda(g.tot) + ' · ' + plural(g.n, 'venda', 'vendas') + '</span></div>' + g.v.map(v => linhaVenda(v)).join('')).join('');
  } else if (U.aba === 'resumo') {
    const de = B.diasAtras(D.hoje0, U.per - 1), R = B.resumo(de, D.hoje0 + B.DIA);
    const ord = o => Object.keys(o).sort((a, b) => o[b] - o[a]);
    corpo = '<div class="chips">' + [[1, 'Hoje'], [7, '7 dias'], [30, '30 dias']].map(x => chip(x[1], U.per === x[0], 'data-a="per" data-v="' + x[0] + '"')).join('') + '</div>' +
      '<div class="rs" style="padding-top:.25rem"><p class="fl" style="margin:0">Vendido ' + (U.per === 1 ? 'hoje' : 'nos últimos ' + U.per + ' dias') + '</p><p class="rs-v">' + moeda(R.total) + '</p>' +
      '<div class="fatos"><div><span>Vendas</span><b>' + R.n + '</b></div><div><span>Peças</span><b>' + R.pecas + '</b></div><div><span>Ticket médio</span><b>' + moeda(R.ticket) + '</b></div><div><span>Lucro bruto estimado</span><b>' + moeda0(R.lucro) + '</b></div></div></div>' +
      (R.n ? '<h3 class="sec">Forma de pagamento</h3>' + ord(R.pg).map(k => barra(PG[k], R.pg[k], R.total)).join('') +
        '<h3 class="sec">Mais vendidas</h3>' + R.top.slice(0, 6).map(x => '<a class="ln" href="#/estoque/p/' + x.p.id + '"><img class="mini p" src="' + esc(x.p.img) + '" alt="" loading="lazy"><span class="ln-c"><b>' + esc(x.p.n) + '</b><small>' + esc(sub(x.p)) + ' · restam ' + x.p.total + '</small></span><b class="ln-v">' + x.q + ' un.</b></a>').join('') +
        '<h3 class="sec">Por categoria</h3>' + ord(R.cat).slice(0, 6).map(k => barra(k, R.cat[k], R.total)).join('') +
        '<h3 class="sec">Onde vendeu</h3>' + ord(R.canal).map(k => barra(CANAL[k], R.canal[k], R.total)).join('') : '<p class="vazio">Sem venda nesse período.</p>') +
      '<div class="pz" style="padding-top:1.5rem"><button class="btn" data-a="fechamento">Fechamento de hoje</button></div>';
  } else {
    corpo = '<p class="dica" style="padding-bottom:.25rem">Pedidos feitos pela sacola do site. Ao confirmar o pagamento, o pedido vira venda e o estoque baixa.</p>' +
      (ped.length ? ped.map(p => '<div class="ped"><div class="ped-h"><b>' + esc(p.cli) + '</b><span>' + CANAL[p.canal] + ' · ' + ha(p.t) + '</span></div>' + p.itens.map(i => linhaItem(i)).join('') +
        '<div class="kv"><span>Total do pedido</span><b>' + moeda(p.total) + '</b></div><div class="dupla"><button class="btn cheio" data-a="ped-ok" data-id="' + p.id + '">Confirmar</button><button class="btn" data-a="ped-x" data-id="' + p.id + '">Recusar</button></div></div>').join('')
        : '<p class="vazio">Nenhum pedido aguardando.</p>');
  }
  return {
    titulo: 'Vendas',
    html: '<div class="seg"><button class="' + (U.aba === 'historico' ? 'on' : '') + '" data-a="aba" data-v="historico">Histórico</button><button class="' + (U.aba === 'resumo' ? 'on' : '') + '" data-a="aba" data-v="resumo">Resumo</button>' +
      '<button class="' + (U.aba === 'pedidos' ? 'on' : '') + '" data-a="aba" data-v="pedidos">Pedidos' + (ped.length ? ' <b>' + ped.length + '</b>' : '') + '</button></div>' + corpo,
  };
}

function telaVenda(id) {
  const D = B.tudo(), v = D.vendas.find(x => x.id === id);
  if (!v) { ir('/vendas', true); return null; }
  return {
    titulo: 'Venda #' + v.n, voltar: '#/vendas',
    html: (v.canc ? '<p class="alerta">Venda cancelada. As peças voltaram para o estoque.</p>' : '') +
      '<div class="kv"><span>Quando</span><b>' + rotDia(v.t) + ', ' + hora(v.t) + '</b></div><div class="kv"><span>Onde</span><b>' + CANAL[v.canal] + '</b></div>' +
      '<div class="kv"><span>Cliente</span><b>' + (v.cli ? esc(v.cli) : 'não informado') + '</b></div><div class="kv"><span>Pagamento</span><b>' + PG[v.pg] + '</b></div>' +
      '<h3 class="sec">Peças</h3>' + v.itens.map(i => linhaItem(i)).join('') +
      '<div class="tot" style="margin-top:0;border-top:0"><div class="kv"><span>Subtotal</span><b>' + moeda(v.sub) + '</b></div>' + (v.desc ? '<div class="kv"><span>Desconto</span><b>− ' + moeda(v.desc) + '</b></div>' : '') +
      '<div class="kv g"><span>Total</span><b>' + moeda(v.total) + '</b></div></div>' +
      (v.canc ? '' : '<div class="pz col"><button class="btn cheio" data-a="comprovante" data-id="' + v.id + '">Enviar comprovante</button><button class="btn perigo" data-a="cancelar" data-id="' + v.id + '">Cancelar venda</button></div>'),
  };
}

function telaMais() {
  const D = B.tudo(), rep = B.reposicao(), escuro = B.tema() === 'escuro';
  const item = (attrs, t, s) => '<a class="ln" ' + attrs + '><span class="ln-c"><b>' + t + '</b><small>' + s + '</small></span>' + I.seta + '</a>';
  return {
    titulo: 'Mais',
    html: item('href="#/estoque/entrada"', 'Entrada de peças', 'Chegou mercadoria: some ao estoque por tamanho') +
      item('href="#/mais/reposicao"', 'Lista de reposição', plural(rep.length, 'peça que vende e está faltando', 'peças que vendem e estão faltando')) +
      item('href="#/mais/paradas"', 'Peças paradas', plural(D.parados.length, 'peça', 'peças') + ' · ' + moeda0(D.valorParado) + ' sem girar') +
      item('href="#/mais/clientes"', 'Clientes', 'Quem comprou, quanto e quando') +
      item('href="#" data-a="fechamento"', 'Fechamento de hoje', 'Total do dia por forma de pagamento') +
      item('href="#/estoque/novo"', 'Cadastrar peça', 'Foto, preço, custo e tamanhos') +
      '<h3 class="sec">Aplicativo</h3>' +
      item('href="#" data-a="tema"', escuro ? 'Usar tema claro' : 'Usar tema escuro', 'Hoje está no ' + (escuro ? 'escuro' : 'claro')) +
      item('href="#" data-a="instalar"', 'Pôr na tela do celular', 'Abre como aplicativo, sem barra do navegador') +
      item('href="#" data-a="reiniciar"', 'Reiniciar a demonstração', B.alterado() ? 'Apaga o que foi feito aqui e volta ao começo' : 'Nada foi alterado ainda') +
      '<p class="nota">Demonstração feita para a BK Clothing. As peças, marcas e preços vêm do catálogo atual; quantidades, custos, clientes e vendas são de exemplo. O que você fizer aqui fica só neste aparelho.</p>',
  };
}

function listaEntrada() {
  const termos = norm(U.en.q).split(/\s+/).filter(Boolean);
  const a = B.tudo().prods.filter(p => !termos.length || termos.every(t => norm(p.n + ' ' + p.b + ' ' + p.cor + ' ' + p.c).indexOf(t) >= 0)).sort((x, y) => y.v30 - x.v30);
  return a.length ? a.map(p => linhaProd(p, 'entrada')).join('') : '<p class="vazio">Nenhuma peça com esse nome.</p>';
}
function telaEntrada() {
  const D = B.tudo();
  const feitas = U.en.feitas.map(f => { const p = D.porId[f.pid]; return p ? '<div class="mv"><span>' + hora(f.t) + '</span><span>' + esc(p.n) + (p.cor ? ' · ' + esc(p.cor) : '') + '</span><b class="p">+' + f.n + '</b></div>' : ''; }).join('');
  return {
    titulo: 'Entrada de peças', voltar: '#/estoque',
    html: '<div class="cab" style="padding-bottom:.75rem"><label class="busca">' + I.busca + '<input id="q" type="search" placeholder="Qual peça chegou?" autocomplete="off" value="' + esc(U.en.q) + '"></label></div>' +
      (feitas ? '<h3 class="sec" style="padding-top:1rem">Entradas de agora <span>' + plural(U.en.feitas.reduce((a, f) => a + f.n, 0), 'peça', 'peças') + '</span></h3>' + feitas + '<h3 class="sec">Todas as peças</h3>' : '') +
      '<div id="lista">' + listaEntrada() + '</div>',
    pronto() { $('#q').addEventListener('input', e => { U.en.q = e.target.value; $('#lista').innerHTML = listaEntrada(); }); },
  };
}
function folhaEntrada(p) {
  const n = p.s.reduce((a, s) => a + (U.en.tmp[s] || 0), 0);
  abrirFolha(fh('Entrada: ' + p.n, sub(p), p.img) + p.s.map(s => '<div class="en"><span>' + esc(s) + '<small>tem ' + p.est[s] + '</small></span><div class="qt"><button data-a="en-q" data-id="' + p.id + '" data-tam="' + esc(s) + '" data-q="-1" aria-label="Tirar">−</button><b>' + (U.en.tmp[s] || 0) + '</b>' +
    '<button data-a="en-q" data-id="' + p.id + '" data-tam="' + esc(s) + '" data-q="1" aria-label="Somar">+</button></div></div>').join('') +
    '<div class="pz"><button class="btn cheio" data-a="en-ok" data-id="' + p.id + '"' + (n ? '' : ' disabled') + '>' + (n ? 'Confirmar entrada de ' + plural(n, 'peça', 'peças') : 'Informe as quantidades') + '</button></div>');
}

function telaNovo() {
  if (!U.novo) U.novo = { n: '', b: '', c: B.categorias()[0], cor: '', p: '', custo: '', unico: false, q: { P: 0, M: 0, G: 0, GG: 0, 'Único': 0 }, foto: '' };
  const N = U.novo, tams = N.unico ? ['Único'] : ['P', 'M', 'G', 'GG'];
  return {
    titulo: 'Cadastrar peça', voltar: '#/estoque',
    html: '<div class="pz" style="padding-bottom:0"><label class="fotoin">' + (N.foto ? '<img src="' + N.foto + '" alt="">' : '<span class="ic" style="border:1px solid var(--line);width:4.5rem;height:4.5rem">' + I.camera + '</span>') +
      '<span><b style="font-weight:500">' + (N.foto ? 'Trocar a foto' : 'Tirar foto da peça') + '</b><br><small class="mute">Abre a câmera do celular</small></span><input id="foto" type="file" accept="image/*" capture="environment" hidden></label>' +
      '<label class="campo"><span>Nome da peça</span><input data-n="n" placeholder="Ex.: Moletom Canguru" value="' + esc(N.n) + '"></label>' +
      '<div class="par"><label class="campo"><span>Marca</span><input data-n="b" list="dl-b" value="' + esc(N.b) + '"><datalist id="dl-b">' + B.marcas().map(m => '<option value="' + esc(m) + '">').join('') + '</datalist></label>' +
      '<label class="campo"><span>Cor</span><input data-n="cor" value="' + esc(N.cor) + '"></label></div>' +
      '<label class="campo"><span>Categoria</span><select data-n="c">' + B.categorias().map(c => '<option' + (c === N.c ? ' selected' : '') + '>' + esc(c) + '</option>').join('') + '</select></label>' +
      '<div class="par"><label class="campo"><span>Preço de venda (R$)</span><input data-n="p" inputmode="decimal" placeholder="0,00" value="' + esc(N.p) + '"></label>' +
      '<label class="campo"><span>Custo (R$)</span><input data-n="custo" inputmode="decimal" placeholder="0,00" value="' + esc(N.custo) + '"></label></div></div>' +
      '<div class="bl"><p class="fl">Tamanhos e quantidade que chegou</p><div class="chips fixo">' + chip('P, M, G, GG', !N.unico, 'data-a="n-grade" data-v=""') + chip('Tamanho único', N.unico, 'data-a="n-grade" data-v="1"') + '</div></div>' +
      '<div style="margin-top:.75rem;border-top:1px solid var(--line)">' + tams.map(s => '<div class="en"><span>' + s + '</span><div class="qt"><button data-a="n-q" data-tam="' + s + '" data-q="-1" aria-label="Tirar">−</button><b>' + N.q[s] + '</b><button data-a="n-q" data-tam="' + s + '" data-q="1" aria-label="Somar">+</button></div></div>').join('') + '</div>' +
      '<div class="pz"><button class="btn cheio" data-a="n-salvar">Salvar peça</button></div>',
    pronto() {
      elTela.querySelectorAll('[data-n]').forEach(el => el.addEventListener('input', () => { N[el.dataset.n] = el.value; }));
      $('#foto').addEventListener('change', e => {
        const arq = e.target.files[0]; if (!arq) return;
        const img = new Image();
        img.onload = () => {
          const l = 640, c = document.createElement('canvas'), m = Math.min(img.width, img.height);
          c.width = c.height = l;
          c.getContext('2d').drawImage(img, (img.width - m) / 2, (img.height - m) / 2, m, m, 0, 0, l, l);
          N.foto = c.toDataURL('image/jpeg', 0.8); URL.revokeObjectURL(img.src); desenhar();
        };
        img.src = URL.createObjectURL(arq);
      });
    },
  };
}

function telaClientes() {
  const a = B.clientes();
  return {
    titulo: 'Clientes', voltar: '#/mais',
    html: '<p class="conta" style="padding-bottom:.75rem;border-bottom:1px solid var(--line)">' + a.length + ' clientes com compra nos últimos ' + B.JANELA + ' dias, do que mais comprou para o que menos comprou.</p>' +
      a.map(c => '<a class="ln" href="#/mais/clientes/' + encodeURIComponent(c.nome) + '"><span class="ln-c"><b>' + esc(c.nome) + '</b><small>' + plural(c.n, 'compra', 'compras') + (c.ult ? ' · última ' + rotDia(c.ult).toLowerCase() : '') + '</small></span><b class="ln-v">' + moeda(c.total) + '</b></a>').join(''),
  };
}
function telaCliente(nome) {
  const c = B.clientes().find(x => x.nome === nome);
  if (!c) { ir('/mais/clientes', true); return null; }
  return {
    titulo: c.nome, voltar: '#/mais/clientes',
    html: '<div class="rs"><p class="fl" style="margin:0">Comprou em ' + B.JANELA + ' dias</p><p class="rs-v">' + moeda(c.total) + '</p>' +
      '<div class="fatos"><div><span>Compras</span><b>' + c.n + '</b></div><div><span>Ticket médio</span><b>' + moeda0(c.n ? c.total / c.n : 0) + '</b></div></div></div>' +
      '<div class="pz"><button class="btn" data-a="msg-cli" data-nome="' + esc(c.nome) + '">Avisar de novidade no WhatsApp</button></div>' +
      '<h3 class="sec" style="padding-top:.5rem">Compras</h3>' + c.vendas.map(v => linhaVenda(v, true)).join(''),
  };
}

function telaReposicao() {
  const a = B.reposicao(), n = a.reduce((s, x) => s + x.q, 0);
  return {
    titulo: 'Reposição', voltar: '#/mais',
    html: '<p class="conta" style="padding-bottom:.75rem">Peças que venderam 3 ou mais em 30 dias e estão sem tamanho ou com uma só. A quantidade sugerida cobre cerca de um mês no ritmo atual.</p>' +
      (a.length ? '<div class="pz" style="padding-top:0"><button class="btn cheio" data-a="msg-rep">Enviar pedido de ' + plural(n, 'peça', 'peças') + '</button></div><div style="border-top:1px solid var(--line)">' +
        a.map(x => '<a class="ln" href="#/estoque/p/' + x.p.id + '"><img class="mini" src="' + esc(x.p.img) + '" alt="" loading="lazy"><span class="ln-c"><b>' + esc(x.p.n) + '</b><small>' + esc(sub(x.p)) + ' · vendeu ' + x.p.v30 + '</small>' +
          '<span class="tams">' + x.pedir.map(t => '<i>' + esc(t.tam) + ' <b>+' + t.q + '</b></i>').join('') + '</span></span><b class="it-q">' + x.q + '</b></a>').join('') + '</div>'
        : '<p class="vazio">Nada para repor agora.</p>'),
  };
}

function telaParadas() {
  const D = B.tudo(), P = U.par;
  if (!P.sel) { P.sel = {}; D.parados.slice(0, 5).forEach(p => { P.sel[p.id] = 1; }); }
  const n = D.parados.filter(p => P.sel[p.id]).length;
  return {
    titulo: 'Peças paradas', voltar: '#/mais',
    html: '<div class="rs"><p class="fl" style="margin:0">Em estoque sem vender há mais de ' + B.PARADO + ' dias</p><p class="rs-v">' + moeda(D.valorParado) + '</p>' +
      '<p class="mute" style="font-size:.875rem;margin-top:.25rem">' + plural(D.parados.length, 'peça', 'peças') + ', em preço de venda. Marque as que entram na oferta.</p></div>' +
      '<div class="bl"><p class="fl">Desconto da oferta</p><div class="chips fixo">' + [10, 20, 30].map(v => chip(v + '%', P.pct === v, 'data-a="par-pct" data-v="' + v + '"')).join('') + '</div></div>' +
      '<div class="pz"><button class="btn cheio" data-a="msg-oferta"' + (n ? '' : ' disabled') + '>Montar oferta para o grupo VIP · ' + n + '</button></div><div style="border-top:1px solid var(--line)">' +
      D.parados.map(p => '<button class="ln' + (P.sel[p.id] ? ' on' : '') + '" data-a="par-sel" data-id="' + p.id + '"><span class="ck">' + I.check + '</span><img class="mini p" src="' + esc(p.img) + '" alt="" loading="lazy">' +
        '<span class="ln-c"><b>' + esc(p.n) + '</b><small>' + esc(sub(p)) + ' · ' + plural(p.total, 'peça', 'peças') + ' · ' + (p.dias === null ? 'mais de ' + B.JANELA : p.dias) + ' dias</small></span><b class="ln-v">' + moeda(p.p) + '</b></button>').join('') + '</div>',
  };
}

/* ---------- rotas ---------- */
const ROTAS = [
  [/^\/$/, telaInicio, 'inicio'],
  [/^\/estoque$/, telaEstoque, 'estoque'],
  [/^\/estoque\/novo$/, telaNovo, 'estoque'],
  [/^\/estoque\/entrada$/, telaEntrada, 'estoque'],
  [/^\/estoque\/p\/([\w-]+)$/, telaProduto, 'estoque'],
  [/^\/vender$/, telaVender, 'vender'],
  [/^\/vender\/cobrar$/, telaCobrar, 'vender'],
  [/^\/vender\/ok\/([\w-]+)$/, telaOk, 'vender'],
  [/^\/vendas$/, telaVendas, 'vendas'],
  [/^\/vendas\/v\/([\w-]+)$/, telaVenda, 'vendas'],
  [/^\/mais$/, telaMais, 'mais'],
  [/^\/mais\/clientes$/, telaClientes, 'mais'],
  [/^\/mais\/clientes\/(.+)$/, telaCliente, 'mais'],
  [/^\/mais\/reposicao$/, telaReposicao, 'mais'],
  [/^\/mais\/paradas$/, telaParadas, 'mais'],
];
// Aberto dentro de outra página (artefato do Claude, palco do vídeo) o aplicativo guarda o próprio caminho,
// sem mexer no endereço; aberto direto no navegador usa o #, e o botão voltar do celular funciona.
const EMBUTIDO = (() => { try { return window.top !== window.self; } catch (e) { return true; } })();
const pilha = ['/'];
const rota = () => (EMBUTIDO ? pilha[pilha.length - 1] : location.hash.replace(/^#/, '') || '/');
let rotaAtual = null, passos = 0;
const rolagens = {};
function ir(r, trocar) {
  r = r.replace(/^#/, '') || '/';
  if (!EMBUTIDO) { if (trocar) location.replace('#' + r); else location.hash = '#' + r; return; }
  if (rotaAtual !== null) rolagens[rotaAtual] = elTela.scrollTop;
  if (trocar) pilha[pilha.length - 1] = r; else if (r !== rota()) pilha.push(r);
  fecharFolha(); desenhar(true);
}
function voltarRota(reserva) {
  if (!EMBUTIDO) { if (passos > 0) history.back(); else location.hash = reserva; return; }
  if (rotaAtual !== null) rolagens[rotaAtual] = elTela.scrollTop;
  if (pilha.length > 1) pilha.pop(); else pilha[0] = reserva.replace(/^#/, '');
  fecharFolha(); desenhar(true);
}

function desenhar(troca) {
  const r = rota();
  let m = null, def = null;
  for (const R of ROTAS) { m = r.match(R[0]); if (m) { def = R; break; } }
  if (!def) { ir('/', true); return; }
  const T = def[1](m[1] ? decodeURIComponent(m[1]) : undefined);
  if (!T) return;   // a tela mandou para outro lugar
  const y = elTela.scrollTop;
  elTopo.hidden = !!T.semTopo;
  elTopo.className = 'topo' + (T.voltar ? ' volta' : '');
  elTopo.innerHTML = (T.voltar ? '<a class="ic" href="' + T.voltar + '" data-a="voltar" aria-label="Voltar">' + I.voltar + '</a>' : '') + '<h1>' + esc(T.titulo || '') + '</h1>' + (T.acao || '');
  elTela.innerHTML = T.html;
  for (const a of elAbas.children) a.classList.toggle('on', a.dataset.aba === def[2]);
  const C = totalCar();
  elCobrar.hidden = !(r === '/vender' && C.n);
  if (!elCobrar.hidden) elCobrar.innerHTML = '<span>' + plural(C.n, 'peça', 'peças') + '</span><b>Cobrar ' + moeda(C.total) + I.seta + '</b>';
  if (troca) {
    const voltando = rotaAtual && rotaAtual.indexOf(r + '/') === 0;
    elTela.scrollTop = voltando ? (rolagens[r] || 0) : 0;
    elTela.classList.remove('entra'); void elTela.offsetWidth; elTela.classList.add('entra');
  } else elTela.scrollTop = y;
  rotaAtual = r;
  if (T.pronto) T.pronto();
}
window.addEventListener('hashchange', () => { if (rotaAtual !== null) rolagens[rotaAtual] = elTela.scrollTop; passos++; fecharFolha(); desenhar(true); });

/* ---------- toques ---------- */
const A = {
  voltar(el) { voltarRota(el.getAttribute('href')); },
  fechar: fecharFolha,
  'ir-estoque'(el) { U.est = { q: '', st: el.dataset.st, cat: '' }; ir('/estoque'); },
  'ir-pedidos'() { U.aba = 'pedidos'; ir('/vendas'); },
  'ir-historico'() { U.aba = 'historico'; ir('/vendas'); },
  'f-st'(el) { U.est.st = el.dataset.v; desenhar(); elTela.scrollTop = 0; },
  'f-cat'(el) { U.est.cat = el.dataset.v; desenhar(); elTela.scrollTop = 0; },
  'v-cat'(el) { U.vd.cat = el.dataset.v; desenhar(); elTela.scrollTop = 0; },
  aj(el) { B.ajustar(el.dataset.id, el.dataset.tam, Number(el.dataset.q)); desenhar(); },
  escolher(el) {
    const p = B.tudo().porId[el.dataset.id];
    if (!p.total) { aviso(p.n + ' está esgotada'); return; }
    folhaTam(p);
  },
  add(el) {
    const p = B.tudo().porId[el.dataset.id], tam = el.dataset.tam;
    const i = U.car.find(x => x.pid === p.id && x.tam === tam);
    if (i) i.q++; else U.car.push({ pid: p.id, tam, q: 1 });
    fecharFolha();
    aviso(p.n + (p.s.length > 1 ? ' ' + tam : '') + ' na venda');
    if (rota() === '/vender') desenhar(); else ir('/vender');
  },
  limpar() { U.car = []; U.pct = 0; desenhar(); },
  'car-q'(el) {
    const i = U.car[Number(el.dataset.k)];
    i.q += Number(el.dataset.q);
    if (i.q <= 0) U.car.splice(Number(el.dataset.k), 1);
    desenhar();
  },
  pg(el) { U.pg = el.dataset.v; desenhar(); },
  pct(el) { U.pct = Number(el.dataset.v); desenhar(); },
  canal(el) { U.canal = el.dataset.v; desenhar(); },
  concluir() {
    const v = B.registrarVenda({ itens: U.car, pct: U.pct, pg: U.pg, canal: U.canal, cli: U.cli });
    U.car = []; U.pct = 0; U.cli = ''; U.pg = 'pix'; U.canal = 'Loja';
    ir('/vender/ok/' + v.id, true);
  },
  comprovante(el) { const v = B.tudo().vendas.find(x => x.id === el.dataset.id); if (v) folhaMsg('Comprovante', txtComprovante(v)); },
  cancelar(el) {
    abrirFolha(fh('Cancelar esta venda?', 'As peças voltam para o estoque') + '<div class="pz col"><button class="btn perigo" data-a="cancelar-ok" data-id="' + el.dataset.id + '">Cancelar a venda</button><button class="btn" data-a="fechar">Manter</button></div>');
  },
  'cancelar-ok'(el) { B.cancelarVenda(el.dataset.id); fecharFolha(); desenhar(); aviso('Venda cancelada, estoque devolvido'); },
  aba(el) { U.aba = el.dataset.v; desenhar(); elTela.scrollTop = 0; },
  per(el) { U.per = Number(el.dataset.v); desenhar(); },
  fechamento() {
    const D = B.tudo(), R = B.resumo(D.hoje0, D.hoje0 + B.DIA);
    abrirFolha(fh('Fechamento de hoje', dataCurta(D.t)) + '<div class="rs"><p class="rs-v">' + moeda(R.total) + '</p><p class="mute" style="font-size:.875rem">' + plural(R.n, 'venda', 'vendas') + ' · ' + plural(R.pecas, 'peça', 'peças') + '</p></div>' +
      '<div style="margin-top:1rem;border-top:1px solid var(--fg)">' + Object.keys(PG).map(k => '<div class="kv"><span>' + PG[k] + '</span><b>' + moeda(R.pg[k] || 0) + '</b></div>').join('') + '</div>' +
      '<div class="pz"><button class="btn cheio" data-a="msg-fech">Enviar fechamento</button></div>');
  },
  'msg-fech'() { folhaMsg('Fechamento de hoje', txtFechamento()); },
  'msg-rep'() { folhaMsg('Pedido de reposição', txtReposicao(), 'Para mandar ao fornecedor'); },
  'msg-oferta'() { folhaMsg('Oferta para o grupo VIP', txtOferta(), 'Para colar no grupo'); },
  'msg-cli'(el) { folhaMsg('Mensagem para ' + el.dataset.nome, 'Oi, ' + el.dataset.nome.split(' ')[0] + '. Chegou peça nova na BK Clothing e separei algumas no teu tamanho. Quer que eu te mande as fotos?'); },
  copiar() {
    const t = $('#msg').textContent;
    (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => aviso('Texto copiado'), () => aviso('Selecione o texto para copiar'));
  },
  'ped-ok'(el) {
    abrirFolha(fh('Como foi o pagamento?', 'O pedido vira venda e o estoque baixa') + '<div class="pz"><div class="pgs">' + Object.keys(PG).map(k => '<button class="pg" data-a="ped-pg" data-id="' + el.dataset.id + '" data-v="' + k + '">' + PG[k] + '</button>').join('') + '</div></div>');
  },
  'ped-pg'(el) { const v = B.confirmarPedido(el.dataset.id, el.dataset.v); fecharFolha(); if (v) ir('/vender/ok/' + v.id); },
  'ped-x'(el) { B.recusarPedido(el.dataset.id); desenhar(); aviso('Pedido recusado'); },
  entrada(el) { U.en.tmp = {}; folhaEntrada(B.tudo().porId[el.dataset.id]); },
  'en-q'(el) { const t = el.dataset.tam; U.en.tmp[t] = Math.max(0, (U.en.tmp[t] || 0) + Number(el.dataset.q)); folhaEntrada(B.tudo().porId[el.dataset.id]); },
  'en-ok'(el) {
    const p = B.tudo().porId[el.dataset.id], n = B.entrada(p.id, U.en.tmp);
    U.en.feitas.unshift({ pid: p.id, n, t: B.agora() }); U.en.tmp = {};
    fecharFolha(); desenhar(); aviso('+' + plural(n, 'peça', 'peças') + ' em ' + p.n);
  },
  editar(el) {
    const p = B.tudo().porId[el.dataset.id];
    abrirFolha(fh('Preço e custo', p.n, p.img) + '<div class="pz" style="padding-top:0"><div class="par"><label class="campo"><span>Preço de venda (R$)</span><input id="ep" inputmode="decimal" value="' + p.p.toFixed(2).replace('.', ',') + '"></label>' +
      '<label class="campo"><span>Custo (R$)</span><input id="ec" inputmode="decimal" value="' + (p.custo || 0).toFixed(2).replace('.', ',') + '"></label></div><button class="btn cheio" style="margin-top:1rem" data-a="editar-ok" data-id="' + p.id + '">Salvar</button></div>');
  },
  'editar-ok'(el) {
    const p = numero($('#ep').value), c = numero($('#ec').value);
    if (!p) { aviso('Informe o preço de venda'); return; }
    B.editarProduto(el.dataset.id, { p, custo: c }); fecharFolha(); desenhar(); aviso('Preço atualizado');
  },
  'n-grade'(el) { U.novo.unico = !!el.dataset.v; desenhar(); },
  'n-q'(el) { const t = el.dataset.tam; U.novo.q[t] = Math.max(0, U.novo.q[t] + Number(el.dataset.q)); desenhar(); },
  'n-salvar'() {
    const N = U.novo, p = numero(N.p);
    if (!N.n.trim()) { aviso('Dê um nome para a peça'); return; }
    if (!p) { aviso('Informe o preço de venda'); return; }
    const s = N.unico ? ['Único'] : ['P', 'M', 'G', 'GG'];
    const id = B.novoProduto({ n: N.n.trim(), b: N.b.trim(), c: N.c, cor: N.cor.trim(), p, custo: numero(N.custo), s, q: N.q, foto: N.foto });
    U.novo = null; aviso('Peça cadastrada');
    ir('/estoque/p/' + id, true);
  },
  'par-sel'(el) { const s = U.par.sel; if (s[el.dataset.id]) delete s[el.dataset.id]; else s[el.dataset.id] = 1; desenhar(); },
  'par-pct'(el) { U.par.pct = Number(el.dataset.v); desenhar(); },
  tema() { B.tema(B.tema() === 'escuro' ? '' : 'escuro'); aplicarTema(); desenhar(); },
  instalar() {
    if (U.instalar) { U.instalar.prompt(); U.instalar = null; return; }
    abrirFolha(fh('Pôr na tela do celular', 'Fica com ícone próprio, como um aplicativo') + '<p class="fl" style="padding:1rem 1rem 0;margin:0">No iPhone (Safari)</p><ol class="passos"><li>Toque no botão de compartilhar, embaixo.</li><li>Escolha "Adicionar à Tela de Início".</li></ol>' +
      '<p class="fl" style="padding:1rem 1rem 0;margin:0">No Android (Chrome)</p><ol class="passos"><li>Toque nos três pontos, em cima.</li><li>Escolha "Instalar aplicativo" ou "Adicionar à tela inicial".</li></ol>');
  },
  reiniciar() {
    abrirFolha(fh('Reiniciar a demonstração?', 'Apaga vendas, entradas e peças feitas neste aparelho') + '<div class="pz col"><button class="btn perigo" data-a="reiniciar-ok">Apagar e recomeçar</button><button class="btn" data-a="fechar">Manter</button></div>');
  },
  'reiniciar-ok'() { B.reiniciar(); U.car = []; U.en.feitas = []; U.par.sel = null; fecharFolha(); ir('/'); desenhar(true); aviso('Demonstração reiniciada'); },
};

document.addEventListener('click', e => {
  const el = e.target.closest('[data-a]');
  if (el) {
    if (el.disabled) return;
    const f = A[el.dataset.a];
    if (!f) return;
    e.preventDefault();
    f(el, e);
    return;
  }
  const a = e.target.closest('a[href^="#/"]');
  if (a && EMBUTIDO) { e.preventDefault(); ir(a.getAttribute('href')); }
});
elVeu.addEventListener('click', fecharFolha);
window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); U.instalar = e; });

function aplicarTema() {
  const escuro = B.tema() === 'escuro';
  if (escuro) document.documentElement.dataset.tema = 'escuro'; else delete document.documentElement.dataset.tema;
  const m = $('meta[name="theme-color"]'); if (m) m.content = '#0b0b0b';
}
aplicarTema();
desenhar(true);
})();
