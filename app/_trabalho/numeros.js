// confere os números de exemplo sem abrir o navegador:  node _trabalho/numeros.js [data-hora]
global.window = {}; global.location = { search: '?agora=' + (process.argv[2] || '2026-10-08T18:10') };
global.localStorage = { getItem() { return null; }, setItem() {} };
require('../js/catalogo.js'); require('../js/base.js');
const B = window.BK, D = B.tudo();
const m = v => v.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
console.log('prods', D.prods.length, 'pecas', D.pecas, 'valorVenda', m(D.valorVenda), 'custo', m(D.valorCusto));
console.log('zerados', D.zerados.length, 'baixos', D.baixos.length, 'parados', D.parados.length, 'valorParado', m(D.valorParado));
const h = B.resumo(D.hoje0, D.hoje0 + B.DIA); console.log('hoje', m(h.total), h.n, 'vendas', h.pecas, 'pecas ticket', m(h.ticket));
console.log('serie7', B.serie(7).map(x => Math.round(x.total)).join(' '));
const r30 = B.resumo(B.diasAtras(D.hoje0, 29), D.hoje0 + B.DIA); console.log('30d', m(r30.total), r30.n, 'lucro', m(r30.lucro));
console.log('top', r30.top.slice(0, 6).map(x => x.p.n + ' ' + x.p.cor + ' x' + x.q).join(' | '));
console.log('repos', B.reposicao().length, 'clientes', B.clientes().length, B.clientes().slice(0, 3).map(c => c.nome + ' ' + c.n + ' ' + m(c.total)).join(' | '));
console.log('ult vendas', D.vendas.slice(0, 5).map(v => '#' + v.n + ' ' + new Date(v.t).toTimeString().slice(0, 5) + ' ' + v.total + ' ' + v.pg).join(' | '));
