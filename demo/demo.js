/* Dados e regras da demo de reservas — Raquel Rocha Cerâmica.
   Tudo fica no navegador (localStorage). Nada é cobrado nem enviado de verdade.
   Para ajustar a demo, edite CONFIG abaixo. */
(function (w) {
  'use strict';

  var IMG = '/ceramica/assets/framerusercontent.com/images/';

  var CONFIG = {
    nome: 'Raquel Rocha Cerâmica',
    cidade: 'Cunha · SP',
    instagram: 'https://instagram.com/rrochaceramica',
    whatsappLink: 'https://wa.link/huxk0b',
    mapa: 'https://maps.google.com/?q=Cunha+SP',
    abre: '10:00',          // primeiro início
    fecha: '17:00',         // último início
    passoMin: 30,           // de quanto em quanto tempo aparece um horário
    intervaloMin: 0,        // pausa entre uma turma e outra (configurável)
    sinal: 0.5,             // 50% de sinal
    pixMinutos: 15,         // tempo para pagar o Pix antes de a vaga voltar
    remarcarHoras: 48,
    valeMeses: 6,
    // Valores de exemplo: trocar pelos da Raquel.
    oficinas: [
      { id: 'casal', nome: 'Oficina de Casal', curto: 'Casal', desc: 'Uma tarde no barro a dois. Cada um modela a sua peça, lado a lado.',
        dur: 90, preco: 280, porPessoa: false, min: 1, max: 1, unidade: 'casal', capacidade: 2, destaque: 'Mais procurada',
        img: IMG + 'pBye4SLmcbj9cwwzjeSIbAiQeA.webp', cor: '#a65a3d' },
      { id: 'familia', nome: 'Oficina em Família', curto: 'Família', desc: 'Pais, filhos e avós na mesma mesa, cada um com a sua peça.',
        dur: 90, preco: 90, porPessoa: true, min: 2, max: 6, unidade: 'pessoa', capacidade: 8,
        img: IMG + 'FkHT22wYhk5caanD7hTk2LIh0.webp', cor: '#55594a' },
      { id: 'infantil', nome: 'Oficina Infantil', curto: 'Infantil', desc: 'Modelagem para crianças, sempre com um adulto junto.',
        dur: 90, preco: 80, porPessoa: true, min: 1, max: 4, unidade: 'criança', capacidade: 6,
        img: IMG + 'nxI5dEc30UG9ZMDijEn1tELSqK4.webp', cor: '#c79c4e' },
      { id: 'noturna', nome: 'Aula Noturna', curto: 'Noturna', desc: 'Depois do expediente, com luz baixa e tempo para o barro.',
        dur: 90, preco: 120, porPessoa: true, min: 1, max: 6, unidade: 'pessoa', capacidade: 6,
        img: IMG + 'ad2KA1o5R39dx0C60w5WHDgQR58.webp', cor: '#3f4b6e', horarios: ['17:00'] }
    ],
    fechadoDiasSemana: [1],     // segunda-feira fechado (exemplo)
    feriados: ['2026-12-25', '2027-01-01'],
    valeCodigoExemplo: 'PRESENTE-8K2Q'
  };

  var KEY_RES = 'rr_reservas_v1', KEY_VALES = 'rr_vales_v1', KEY_CFG = 'rr_config_v1';

  function load(k, def) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch (e) { return def; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  // Ajustes feitos no painel (preço, vagas, liga/desliga) sobrepõem o CONFIG.
  function oficinas() {
    var o = load(KEY_CFG, {});
    return CONFIG.oficinas.map(function (x) {
      var p = o[x.id] || {};
      return Object.assign({}, x, { preco: p.preco != null ? p.preco : x.preco, capacidade: p.capacidade != null ? p.capacidade : x.capacidade, ativa: p.ativa !== false });
    });
  }
  function setOficina(id, patch) { var o = load(KEY_CFG, {}); o[id] = Object.assign({}, o[id] || {}, patch); save(KEY_CFG, o); broadcast({ type: 'config' }); }
  function oficina(id) { return oficinas().filter(function (x) { return x.id === id; })[0]; }

  // Datas
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function iso(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function parseISO(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function today() { var d = new Date(); d.setHours(0, 0, 0, 0); return d; }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  var DOW = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];
  var DOW3 = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb'];
  var MES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
  function dataLonga(s) { var d = parseISO(s); return DOW[d.getDay()] + ', ' + d.getDate() + ' de ' + MES[d.getMonth()]; }
  function dataCurta(s) { var d = parseISO(s); return DOW3[d.getDay()] + ', ' + d.getDate() + '/' + pad(d.getMonth() + 1); }
  function toMin(h) { var p = h.split(':'); return +p[0] * 60 + +p[1]; }
  function toHora(m) { return pad(Math.floor(m / 60)) + ':' + pad(m % 60); }
  function horaBR(h) { var p = h.split(':'); return +p[0] + 'h' + (p[1] === '00' ? '' : p[1]); }

  function money(v) { return 'R$ ' + Math.round(v).toLocaleString('pt-BR'); }

  // Reservas de exemplo para a semana atual (geradas de forma estável).
  function rand(seed) { var x = Math.sin(seed) * 10000; return x - Math.floor(x); }
  function seedReservas() {
    var out = [], t = today();
    var nomes = [['Ana e Pedro', 'casal', 1], ['Família Souza', 'familia', 4], ['Luísa Martins', 'noturna', 1], ['Bruna e Caio', 'casal', 1],
      ['Marina (Theo, 6 anos)', 'infantil', 1], ['Rafael e Júlia', 'casal', 1], ['Família Andrade', 'familia', 3], ['Carla e Beto', 'casal', 1],
      ['Paula (Lis e Bento)', 'infantil', 2], ['Diego e Nara', 'casal', 1], ['Família Rocha Lima', 'familia', 5], ['Gabi e Léo', 'casal', 1]];
    var horas = ['10:00', '11:30', '14:00', '15:30', '10:30', '16:00', '13:00', '14:30', '11:00', '15:00', '10:00', '16:30'];
    var dia = 0;
    for (var i = 0; i < nomes.length; i++) {
      var d = addDays(t, dia);
      while (fechado(d)) { dia++; d = addDays(t, dia); }
      var of = nomes[i][1];
      out.push({ id: 'RR-S' + (100 + i), seed: true, nome: nomes[i][0], whats: '(12) 9' + Math.floor(1000 + rand(i + 3) * 8999) + '-' + Math.floor(1000 + rand(i + 9) * 8999),
        oficina: of, data: iso(d), hora: of === 'noturna' ? '17:00' : horas[i], qtd: nomes[i][2], status: i % 5 === 2 ? 'pendente' : 'pago',
        obs: i === 4 ? 'Primeira vez da criança com argila' : '', criada: Date.now() - (i + 1) * 3600e3 });
      if (i % 2 === 1) dia++;
    }
    return out;
  }
  function reservas() {
    var r = load(KEY_RES, null);
    if (!r) { r = seedReservas(); save(KEY_RES, r); }
    return r;
  }
  function addReserva(r) { var all = reservas(); all.push(r); save(KEY_RES, all); broadcast({ type: 'reserva', reserva: r }); }
  function updateReserva(id, patch) { var all = reservas().map(function (r) { return r.id === id ? Object.assign({}, r, patch) : r; }); save(KEY_RES, all); broadcast({ type: 'update' }); }
  function resetDemo() { try { localStorage.removeItem(KEY_RES); localStorage.removeItem(KEY_VALES); localStorage.removeItem(KEY_CFG); localStorage.removeItem('rr_bloqueios_v1'); } catch (e) {} broadcast({ type: 'reset' }); }

  // Bloqueios manuais (painel)
  function bloqueios() { return load('rr_bloqueios_v1', { dias: [], horarios: [] }); }
  function setBloqueios(b) { save('rr_bloqueios_v1', b); broadcast({ type: 'config' }); }

  function fechado(d) {
    var s = iso(d), b = bloqueios();
    return CONFIG.fechadoDiasSemana.indexOf(d.getDay()) !== -1 || CONFIG.feriados.indexOf(s) !== -1 || b.dias.indexOf(s) !== -1;
  }

  // Horários de início possíveis para uma oficina.
  function inicios(of) {
    if (of.horarios) return of.horarios.slice();
    var out = [], a = toMin(CONFIG.abre), z = toMin(CONFIG.fecha);
    for (var m = a; m <= z; m += CONFIG.passoMin) out.push(toHora(m));
    return out;
  }

  // O ateliê atende uma turma por vez: cada reserva ocupa a duração + intervalo.
  function ocupacao(dataISO) {
    return reservas().filter(function (r) { return r.data === dataISO && r.status !== 'cancelada'; });
  }
  function slotsDoDia(ofId, dataISO) {
    var of = oficina(ofId), res = ocupacao(dataISO), b = bloqueios();
    return inicios(of).map(function (h) {
      var ini = toMin(h), fim = ini + of.dur + CONFIG.intervaloMin;
      var mesma = 0, conflito = false;
      res.forEach(function (r) {
        var o2 = oficina(r.oficina) || of, ri = toMin(r.hora), rf = ri + o2.dur + CONFIG.intervaloMin;
        var sobrepoe = ini < rf && ri < fim;
        if (!sobrepoe) return;
        if (r.oficina === ofId && r.hora === h) mesma += r.qtd; else conflito = true;
      });
      // Horário bloqueado no painel: ocupa 1h30 a partir do início marcado.
      b.horarios.forEach(function (k) {
        if (k.slice(0, 10) !== dataISO) return;
        var bi = toMin(k.slice(11)), bf = bi + 90;
        if (ini < bf && bi < fim) conflito = true;
      });
      var cap = of.capacidade;
      var livres = conflito ? 0 : Math.max(0, cap - mesma);
      return { hora: h, livres: livres, cap: cap };
    });
  }
  function resumoDia(ofId, d) {
    if (d < today() || fechado(d)) return { estado: 'fechado' };
    var s = slotsDoDia(ofId, iso(d)), livres = s.filter(function (x) { return x.livres > 0; }).length;
    if (!livres) return { estado: 'lotado' };
    return { estado: livres <= 3 ? 'poucas' : 'ok', livres: livres };
  }

  function total(of, qtd) { return of.porPessoa ? of.preco * qtd : of.preco; }
  function codigo(prefix) { var c = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789', s = ''; for (var i = 0; i < 4; i++) s += c[Math.floor(Math.random() * c.length)]; return prefix + s; }

  // Vales-presente
  function vales() {
    var v = load(KEY_VALES, null);
    if (!v) {
      var t = today();
      v = [
        { codigo: CONFIG.valeCodigoExemplo, tipo: 'casal', valor: 280, de: 'Marcos', para: 'Lia', status: 'ativo', validade: iso(addDays(t, 150)), criado: iso(addDays(t, -30)) },
        { codigo: 'PRESENTE-T7WM', tipo: 'familia', valor: 360, de: 'Vó Cida', para: 'Família Prado', status: 'usado', validade: iso(addDays(t, 60)), criado: iso(addDays(t, -120)) },
        { codigo: 'PRESENTE-9HDA', tipo: 'livre', valor: 150, de: 'Equipe Lumi', para: 'Renata', status: 'vencido', validade: iso(addDays(t, -10)), criado: iso(addDays(t, -190)) }
      ];
      save(KEY_VALES, v);
    }
    return v;
  }
  function addVale(v) { var all = vales(); all.push(v); save(KEY_VALES, all); broadcast({ type: 'vale', vale: v }); }
  function valeValido(cod) {
    cod = (cod || '').trim().toUpperCase();
    var v = vales().filter(function (x) { return x.codigo === cod; })[0];
    if (!v) return { ok: false, msg: 'Código não encontrado.' };
    if (v.status === 'usado') return { ok: false, msg: 'Este vale já foi usado.' };
    if (v.status === 'vencido' || parseISO(v.validade) < today()) return { ok: false, msg: 'Este vale venceu.' };
    return { ok: true, vale: v };
  }
  function usarVale(cod) { var all = vales().map(function (v) { return v.codigo === cod ? Object.assign({}, v, { status: 'usado' }) : v; }); save(KEY_VALES, all); }

  // Avisa o painel (aberto em outra aba) na hora.
  var bc = null; try { bc = new BroadcastChannel('rr-demo'); } catch (e) {}
  var listeners = [];
  function broadcast(msg) { try { bc && bc.postMessage(msg); } catch (e) {} }
  function onMessage(fn) { listeners.push(fn); }
  if (bc) bc.onmessage = function (e) { listeners.forEach(function (fn) { fn(e.data); }); };
  w.addEventListener('storage', function (e) { if (e.key && e.key.indexOf('rr_') === 0) listeners.forEach(function (fn) { fn({ type: 'storage' }); }); });

  // QR decorativo (não é um Pix de verdade).
  function qrSVG(text) {
    var n = 29, cells = '', h = 0;
    for (var i = 0; i < text.length; i++) h = (h * 31 + text.charCodeAt(i)) >>> 0;
    function finder(x, y) { return '<rect x="' + x + '" y="' + y + '" width="7" height="7" fill="#242720"/><rect x="' + (x + 1) + '" y="' + (y + 1) + '" width="5" height="5" fill="#fff"/><rect x="' + (x + 2) + '" y="' + (y + 2) + '" width="3" height="3" fill="#242720"/>'; }
    function inFinder(x, y) { return (x < 8 && y < 8) || (x > n - 9 && y < 8) || (x < 8 && y > n - 9); }
    for (var y = 0; y < n; y++) for (var x = 0; x < n; x++) {
      if (inFinder(x, y)) continue;
      h = (h * 1103515245 + 12345) >>> 0;
      if ((h >>> 16) % 100 < 47) cells += '<rect x="' + x + '" y="' + y + '" width="1" height="1"/>';
    }
    return '<svg viewBox="-1 -1 ' + (n + 2) + ' ' + (n + 2) + '" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges" role="img" aria-label="QR Code de demonstração"><rect x="-1" y="-1" width="' + (n + 2) + '" height="' + (n + 2) + '" fill="#fff"/><g fill="#242720">' + cells + '</g>' + finder(0, 0) + finder(n - 7, 0) + finder(0, n - 7) + '</svg>';
  }

  function toast(el, html, ms) {
    el.innerHTML = html; el.classList.add('on');
    clearTimeout(el._t); el._t = setTimeout(function () { el.classList.remove('on'); }, ms || 4200);
  }

  w.RR = {
    CONFIG: CONFIG, oficinas: oficinas, oficina: oficina, setOficina: setOficina,
    reservas: reservas, addReserva: addReserva, updateReserva: updateReserva, resetDemo: resetDemo,
    bloqueios: bloqueios, setBloqueios: setBloqueios, fechado: fechado,
    slotsDoDia: slotsDoDia, resumoDia: resumoDia, inicios: inicios,
    vales: vales, addVale: addVale, valeValido: valeValido, usarVale: usarVale,
    total: total, codigo: codigo, money: money, onMessage: onMessage, qrSVG: qrSVG, toast: toast,
    iso: iso, parseISO: parseISO, today: today, addDays: addDays, dataLonga: dataLonga, dataCurta: dataCurta,
    horaBR: horaBR, toMin: toMin, toHora: toHora, MES: MES, DOW3: DOW3
  };
})(window);
