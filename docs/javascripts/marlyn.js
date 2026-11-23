/* Interações da GitPage do Grupo Marlyn Wescoff.
   Sem dependências externas. Respeita "prefers-reduced-motion". */
(function () {
  "use strict";

  var reduzido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.documentElement.classList.add("mw-js");

  /* ---------- Dados do plano GQM (espelham docs/fase-2) ---------- */
  var GQM = [
    {
      id: "G1", nome: "Adequação funcional", decisao: "D1",
      objetivo: "<b>Analisar</b> o núcleo do Moodle 5.3 LTS <b>para o propósito de</b> entender <b>com respeito à</b> adequação funcional das tarefas acadêmicas essenciais <b>do ponto de vista da</b> Coordenação de TI <b>no contexto da</b> decisão de adoção/atualização (D1).",
      questoes: [
        { id: "Q1.1", q: "O núcleo do Moodle, sem plugins, dá conta das tarefas acadêmicas essenciais da instituição?", h: "H1.1: sim; função para as 12 tarefas (12 de 12) e só uma com contorno.",
          m: [{ id: "M1.1", n: "Cobertura funcional", f: "1 − Tf/Tt" }, { id: "M1.3", n: "Pertinência funcional", f: "1 − Tc/Tt" }] },
        { id: "Q1.2", q: "O Moodle calcula notas e controla prazos como a instituição espera?", h: "H1.2: sim; todos os casos iguais ao oráculo.",
          m: [{ id: "M1.2", n: "Correção funcional", f: "Cc/Ct" }] },
        { id: "Q1.3", q: "Docentes e gestão conseguem fazer as tarefas pelo caminho previsto, sem improvisar passos?", h: "H1.3: quase sempre; só a restauração de backup exige contorno (11 de 12).",
          m: [{ id: "M1.3", n: "Pertinência funcional", f: "1 − Tc/Tt" }] }
      ]
    },
    {
      id: "G2", nome: "Compatibilidade", decisao: "D2",
      objetivo: "<b>Analisar</b> o núcleo do Moodle 5.3 LTS e suas interfaces de troca de dados <b>para o propósito de</b> entender <b>com respeito à</b> compatibilidade (interoperabilidade e coexistência) <b>do ponto de vista da</b> Coordenação de TI <b>no contexto da</b> decisão sobre as integrações (D2).",
      questoes: [
        { id: "Q2.1", q: "A instituição consegue levar dados para o Moodle e tirá-los dele nos arquivos que os outros sistemas usam?", h: "H2.1: sim, com no máximo uma exceção (6 ou 7 de 7 formatos).",
          m: [{ id: "M2.1", n: "Intercâmbio de formatos", f: "Fs/Ft" }] },
        { id: "Q2.2", q: "Os dados que passam entre o Moodle e os outros sistemas chegam ao destino como saíram?", h: "H2.2: sim; todos os registros iguais à referência (risco: acentuação no CSV).",
          m: [{ id: "M2.1", n: "Intercâmbio de formatos", f: "Fs/Ft" }, { id: "M2.2", n: "Integridade dos dados", f: "Rc/Rt" }] },
        { id: "Q2.3", q: "Um sistema externo consegue consultar e alterar dados do Moodle pelos serviços web, sem intervenção manual?", h: "H2.3: sim; as 6 funções respondem sem erro (6 de 6).",
          m: [{ id: "M2.3", n: "Conectividade REST", f: "Ws/Wt" }] },
        { id: "Q2.4", q: "O Moodle pode dividir o servidor com outras aplicações sem atrapalhá-las?", h: "H2.4: sim; nenhuma das 3 entidades vizinhas é afetada (3 de 3).",
          m: [{ id: "M2.4", n: "Coexistência disponível", f: "Ec/Et" }] }
      ]
    },
    {
      id: "G3", nome: "Flexibilidade", decisao: "D3",
      objetivo: "<b>Analisar</b> o Moodle 5.3 LTS e seus procedimentos oficiais de instalação e atualização <b>para o propósito de</b> entender <b>com respeito à</b> flexibilidade (adaptabilidade e instalabilidade) <b>do ponto de vista da</b> Coordenação de TI <b>no contexto da</b> definição do procedimento de migração (D3).",
      questoes: [
        { id: "Q3.1", q: "Estudantes e docentes conseguem usar o Moodle a partir dos computadores e celulares que já têm?", h: "H3.1: quase todos; desktops 8 de 8 e Android com no máximo uma falha.",
          m: [{ id: "M3.1", n: "Adaptabilidade ao acesso", f: "min(1 − Tfa/Tta)" }] },
        { id: "Q3.2", q: "A TI pode escolher entre as versões de PHP suportadas sem que o Moodle mude de comportamento?", h: "H3.2: sim; mesmo resultado nas 12 tarefas com PHP 8.3 e 8.4.",
          m: [{ id: "M3.2", n: "Adaptabilidade ao PHP", f: "min(1 − Tfp/Ttp)" }] },
        { id: "Q3.3", q: "A TI consegue instalar e atualizar o Moodle seguindo só a documentação oficial, em tempo previsível?", h: "H3.3: sim, com um tropeço; uma atualização falha na 1ª tentativa por causa de public/ (5 de 6); instalação limpa em menos de 15 min.",
          m: [{ id: "M3.3", n: "Sucesso de instalação", f: "Ps/Pt" }, { id: "M3.4", n: "Tempo de instalação", f: "mediana(tfim − tinício)" }] },
        { id: "Q3.4", q: "A atualização da 4.5 para a 5.3 mantém os dados acadêmicos que já existem?", h: "H3.4: sim; os 40 itens iguais antes e depois (40 de 40).",
          m: [{ id: "M3.5", n: "Preservação de dados", f: "Ip/It" }] }
      ]
    }
  ];

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  /* ---------- Explorador GQM ---------- */
  function montarExplorador(raiz) {
    if (!raiz || raiz.dataset.pronto) return;
    raiz.dataset.pronto = "1";
    var abas = el("div", "gqm-abas");
    abas.setAttribute("role", "tablist");
    abas.setAttribute("aria-label", "Objetivos de medição");
    var painel = el("div", "gqm-painel");
    painel.setAttribute("role", "tabpanel");
    var botoes = [];

    function mostrar(i) {
      var g = GQM[i];
      botoes.forEach(function (b, j) {
        b.setAttribute("aria-selected", j === i ? "true" : "false");
        b.tabIndex = j === i ? 0 : -1;
      });
      painel.innerHTML = "";
      painel.appendChild(el("div", "gqm-objetivo", "<b>" + g.id + "</b> · " + g.objetivo));
      var arvore = el("div", "gqm-arvore");
      g.questoes.forEach(function (q, k) {
        var linha = el("div", "gqm-questao");
        linha.style.animationDelay = (reduzido ? 0 : k * 90) + "ms";
        linha.appendChild(el("div", "gqm-q", "<b>" + q.id + "</b>" + q.q + '<span class="gqm-h">' + q.h + "</span>"));
        var ms = el("div", "gqm-ms");
        q.m.forEach(function (m) {
          ms.appendChild(el("div", "gqm-m", "<b>" + m.id + "</b>" + m.n + " · <code>" + m.f + "</code>"));
        });
        linha.appendChild(ms);
        arvore.appendChild(linha);
      });
      painel.appendChild(arvore);
    }

    GQM.forEach(function (g, i) {
      var b = el("button", "gqm-aba", g.id + " · " + g.nome + "<small>" + g.questoes.length + " questões · decisão " + g.decisao + "</small>");
      b.type = "button";
      b.setAttribute("role", "tab");
      b.addEventListener("click", function () { mostrar(i); });
      b.addEventListener("keydown", function (ev) {
        var d = ev.key === "ArrowRight" ? 1 : ev.key === "ArrowLeft" ? -1 : 0;
        if (d) {
          var n = (i + d + GQM.length) % GQM.length;
          mostrar(n);
          botoes[n].focus();
        }
      });
      botoes.push(b);
      abas.appendChild(b);
    });
    raiz.appendChild(abas);
    raiz.appendChild(painel);
    mostrar(0);
  }

  /* ---------- Fundo do hero: fichas com módulos e formatos do Moodle ---------- */
  var TERMOS = ["mod_assign", "mod_quiz", "mod_forum", "mod_resource", "gradebook", "backup .mbz",
    "CSV", "XLSX", "GIFT", "Moodle XML", "iCal", "REST", "webservice", "cron.php", "upgrade.php",
    "install.php", "PHP 8.3", "PHP 8.4", "PostgreSQL 17", "public/", "tema Boost", "enrol_manual",
    "course/view.php", "5.3 LTS", "4.5 LTS", "moodledata", "sodium"];

  function montarFundo(canvas) {
    if (!canvas) return;
    var ctx = canvas.getContext("2d");
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var fichas = [], mouse = { x: -999, y: -999 }, w = 0, h = 0;

    function nova(y) {
      var t = TERMOS[Math.floor(Math.random() * TERMOS.length)];
      return { t: t, x: Math.random() * w, y: y === undefined ? Math.random() * h : y,
        v: 0.15 + Math.random() * 0.35, a: 0.08 + Math.random() * 0.22, s: 10 + Math.random() * 4, dx: 0 };
    }
    function dimensionar() {
      var r = canvas.getBoundingClientRect();
      w = r.width; h = r.height;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(w * h / 16000);
      fichas = [];
      for (var i = 0; i < n; i++) fichas.push(nova());
    }
    function desenhar() {
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < fichas.length; i++) {
        var f = fichas[i];
        var ddx = f.x - mouse.x, ddy = f.y - mouse.y, d = Math.sqrt(ddx * ddx + ddy * ddy);
        if (d < 110) f.dx += (ddx / (d || 1)) * 0.4;
        f.dx *= 0.92;
        f.x += f.dx;
        f.y -= f.v;
        if (f.y < -20) fichas[i] = nova(h + 20);
        var perto = d < 140 ? (1 - d / 140) : 0;
        ctx.font = "500 " + f.s + "px 'IBM Plex Mono', monospace";
        var largura = ctx.measureText(f.t).width;
        ctx.globalAlpha = Math.min(0.9, f.a + perto * 0.6);
        ctx.strokeStyle = perto ? "#ffb000" : "#38b2ac";
        ctx.lineWidth = 1;
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(f.x - 6, f.y - f.s, largura + 12, f.s + 8, 4);
        else ctx.rect(f.x - 6, f.y - f.s, largura + 12, f.s + 8);
        ctx.stroke();
        ctx.fillStyle = perto ? "#ffd36b" : "#cfe7f0";
        ctx.fillText(f.t, f.x, f.y);
      }
      ctx.globalAlpha = 1;
      if (!reduzido) requestAnimationFrame(desenhar);
    }
    dimensionar();
    window.addEventListener("resize", dimensionar);
    var hero = canvas.parentElement;
    hero.addEventListener("mousemove", function (e) {
      var r = canvas.getBoundingClientRect();
      mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
    });
    hero.addEventListener("mouseleave", function () { mouse.x = mouse.y = -999; });
    requestAnimationFrame(desenhar);
  }

  /* ---------- Texto digitado (troca a palavra conforme a cena) ---------- */
  var alvoDigitado = null, timerDigitado = null;
  function digitarPalavra(palavra) {
    if (!alvoDigitado) return;
    clearTimeout(timerDigitado);
    if (reduzido) { alvoDigitado.textContent = palavra; return; }
    var atual = alvoDigitado.textContent.trim();
    (function apagar() {
      if (atual.length) {
        atual = atual.slice(0, -1);
        alvoDigitado.textContent = atual || " ";
        timerDigitado = setTimeout(apagar, 30);
      } else {
        var j = 0;
        (function escrever() {
          j++;
          alvoDigitado.textContent = palavra.slice(0, j);
          if (j < palavra.length) timerDigitado = setTimeout(escrever, 70);
        })();
      }
    })();
  }

  /* ---------- Janela de demonstração: três cenas, uma por objetivo ---------- */
  var TERMINAL = [
    '<span class="t-p">$</span> php admin/cli/checks.php',
    '  PHP 8.3 (64 bits) ........ <span class="t-ok">ok</span>',
    '  extensão sodium .......... <span class="t-ok">ok</span>',
    '  PostgreSQL 17 ............ <span class="t-ok">ok</span>',
    '  raiz web em public/ ...... <span class="t-av">verificar</span>',
    '<span class="t-p">$</span> php admin/cli/upgrade.php --non-interactive',
    '  4.5 LTS  →  5.3 LTS',
    '  [<span class="t-ok">BARRA</span>] PCT%',
    '  itens a conferir após a atualização: 40'
  ];

  function montarDemo(raiz) {
    if (!raiz) return;
    var abas = raiz.querySelectorAll(".mw-demo__abas button");
    var cenas = raiz.querySelectorAll(".mw-demo__cena");
    var palavras = ["adequação funcional", "compatibilidade", "flexibilidade"];
    var DURACAO = 8000, atual = -1, timers = [], ciclo = null;
    raiz.style.setProperty("--mw-duracao-cena", DURACAO + "ms");

    function limpar() { timers.forEach(clearTimeout); timers = []; }
    function depois(ms, fn) { timers.push(setTimeout(fn, reduzido ? 0 : ms)); }

    function cenaFuncional(c) {
      var itens = c.querySelectorAll(".mw-curso__lista li");
      var cont = c.querySelector(".mw-demo__contador");
      var total = parseInt(cont.dataset.total, 10);
      itens.forEach(function (li) { li.className = ""; li.querySelector(".mw-st").textContent = "aguardando"; });
      cont.textContent = "0/" + total + " tarefas exercitadas";
      itens.forEach(function (li, k) {
        depois(400 + k * 1000, function () {
          li.className = "mw-testando";
          li.querySelector(".mw-st").textContent = "em teste...";
        });
        depois(1100 + k * 1000, function () {
          li.className = "mw-registrado";
          li.querySelector(".mw-st").textContent = "evidência registrada";
          cont.textContent = Math.round((k + 1) / itens.length * total) + "/" + total + " tarefas exercitadas";
        });
      });
    }

    function cenaFlexivel(c) {
      var code = c.querySelector(".mw-terminal code");
      var amb = c.querySelectorAll(".mw-ambientes span");
      amb.forEach(function (a) { a.classList.remove("mw-on"); });
      code.innerHTML = "";
      var linhas = [];
      TERMINAL.forEach(function (l, k) {
        depois(250 + k * 520, function () {
          if (l.indexOf("BARRA") >= 0) {
            var passo = 0;
            (function barra() {
              passo++;
              var cheio = Math.min(20, passo);
              linhas[k] = l.replace("BARRA", "#".repeat(cheio) + ".".repeat(20 - cheio)).replace("PCT", String(cheio * 5));
              code.innerHTML = linhas.join("\n");
              if (cheio < 20) depois(60, barra);
            })();
          } else {
            linhas[k] = l;
            code.innerHTML = linhas.join("\n");
          }
        });
      });
      amb.forEach(function (a, k) { depois(5600 + k * 400, function () { a.classList.add("mw-on"); }); });
    }

    function mostrar(i, manual) {
      if (i === atual && !manual) return;
      atual = i;
      limpar();
      abas.forEach(function (b, j) { b.setAttribute("aria-selected", j === i ? "true" : "false"); });
      cenas.forEach(function (c, j) { c.classList.toggle("mw-ativa", j === i); });
      // reinicia a barra de tempo da aba
      var ativa = abas[i];
      ativa.style.animation = "none"; void ativa.offsetWidth; ativa.style.animation = "";
      if (i === 0) cenaFuncional(cenas[0]);
      if (i === 2) cenaFlexivel(cenas[2]);
      digitarPalavra(palavras[i]);
      clearTimeout(ciclo);
      if (!reduzido) ciclo = setTimeout(function () { mostrar((i + 1) % cenas.length); }, DURACAO);
    }

    abas.forEach(function (b, i) { b.addEventListener("click", function () { mostrar(i, true); }); });
    raiz.addEventListener("mouseenter", function () { clearTimeout(ciclo); });
    raiz.addEventListener("mouseleave", function () {
      clearTimeout(ciclo);
      if (!reduzido) ciclo = setTimeout(function () { mostrar((atual + 1) % cenas.length); }, DURACAO);
    });
    mostrar(0);
  }

  /* ---------- Contadores ---------- */
  function contar(e) {
    var fim = parseInt(e.dataset.contar, 10);
    if (reduzido) { e.textContent = fim; return; }
    var inicio = performance.now(), dur = 1200;
    (function quadro(agora) {
      var p = Math.min(1, (agora - inicio) / dur);
      e.textContent = Math.round(fim * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(quadro);
    })(inicio);
  }

  /* ---------- Revelação ao rolar ---------- */
  function revelar() {
    var alvos = document.querySelectorAll(".mw-revelar, .mw-linha-tempo, [data-contar]");
    var aoVer = function (e) {
      e.classList.add("mw-visivel");
      if (e.dataset.contar) contar(e);
      if (e.classList.contains("mw-linha-tempo")) {
        var etapas = e.querySelectorAll(".mw-etapa");
        var feitas = parseInt(e.dataset.concluidas || "0", 10);
        e.style.setProperty("--mw-progresso-fases", ((feitas - 0.5) / etapas.length * 100) + "%");
        etapas.forEach(function (s, k) {
          if (k < feitas) setTimeout(function () { s.classList.add("mw-feita"); }, reduzido ? 0 : 400 + k * 450);
        });
      }
    };
    if (!("IntersectionObserver" in window)) { alvos.forEach(aoVer); return; }
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) { aoVer(en.target); obs.unobserve(en.target); }
      });
    }, { threshold: 0.2 });
    alvos.forEach(function (a) { obs.observe(a); });
  }

  /* ---------- Brilho que segue o mouse nos cartões ---------- */
  function cartoes() {
    document.querySelectorAll(".mw-cartao").forEach(function (c) {
      c.addEventListener("mousemove", function (e) {
        var r = c.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        c.style.setProperty("--mx", x * 100 + "%");
        c.style.setProperty("--my", y * 100 + "%");
        if (!reduzido) c.style.transform = "perspective(700px) rotateX(" + ((0.5 - y) * 6) + "deg) rotateY(" + ((x - 0.5) * 6) + "deg)";
      });
      c.addEventListener("mouseleave", function () { c.style.transform = ""; });
    });
  }

  /* ---------- Barra de progresso de leitura ---------- */
  function progressoLeitura() {
    if (document.querySelector(".mw-progresso")) return;
    var barra = el("div", "mw-progresso");
    barra.setAttribute("aria-hidden", "true");
    document.body.appendChild(barra);
    function atualizar() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      barra.style.transform = "scaleX(" + (h > 0 ? window.scrollY / h : 0) + ")";
    }
    window.addEventListener("scroll", atualizar, { passive: true });
    atualizar();
  }

  function iniciar() {
    montarExplorador(document.getElementById("gqm-explorer"));
    alvoDigitado = document.querySelector(".mw-digitando");
    montarFundo(document.querySelector(".mw-hero__painel"));
    montarDemo(document.querySelector(".mw-demo"));
    revelar();
    cartoes();
    progressoLeitura();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar);
  else iniciar();
})();
