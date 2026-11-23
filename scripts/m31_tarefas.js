// M3.1 (adaptabilidade a ambientes de acesso), issue #70: executa as tarefas T02, T03, T04, T05, T06,
// T08, T09 e T11 do plano da Fase 3 em um ambiente de acesso, pela interface web do Moodle, com
// Playwright. Cada papel usa uma sessão limpa (contexto novo, regra R2). Salva uma captura por tarefa
// em dados/avaliacao/evidencias/ e acrescenta as linhas em dados/avaliacao/M3.1/execucoes.csv.
//
// Uso:
//   PW_CORE=<caminho do playwright-core> node scripts/m31_tarefas.js <A1|A3|A4> <estudante> [url]
//   A1: Chrome do Windows por CDP (CDP_URL, padrão http://127.0.0.1:9333), iniciado antes
//   A2: Firefox do Windows pelo WebDriver BiDi (scripts/firefox_windows.sh; TMPDIR numa pasta do Windows)
//   A3: Firefox (build do Playwright) no Ubuntu do WSL
//   A4: Chromium com o perfil "Pixel 7" do Playwright (Android emulado; não é um aparelho real)
// Senha das contas da massa: MASSA_SENHA (padrão Aval#2026, fictícia e pública, ver massa/README.md).

const path = require("path");
const fs = require("fs");
const pw = require(process.env.PW_CORE || "playwright-core");

const [amb, estudante, URL = "http://localhost:8080"] = process.argv.slice(2);
const SENHA = process.env.MASSA_SENHA || "Aval#2026";
const RAIZ = path.resolve(__dirname, "..");
// M31_SAIDA: pasta alternativa para depuração (nada é gravado em dados/avaliacao/).
const EVID = process.env.M31_SAIDA || path.join(RAIZ, "dados", "avaliacao", "evidencias");
const CSV = process.env.M31_SAIDA ? path.join(process.env.M31_SAIDA, "execucoes.csv")
  : path.join(RAIZ, "dados", "avaliacao", "M3.1", "execucoes.csv");
const DATA = "2026-11-22", INIC = "JPSM";
const PREFIXO = process.env.M31_PREFIXO || "M3.1";   // M3.2 grava as evidências como M3.2_<tarefa>_<php>_...
const CURSO = 2, CM_T04 = 2, CM_T05 = 3, CM_QUIZ = 4, DISCUSSAO = 1;
const NOTAS = Object.fromEntries(fs.readFileSync(path.join(RAIZ, "dados", "avaliacao", "massa", "notas.csv"), "utf8")
  .trim().split("\n").slice(1).map((l) => l.split(",")).map(([e, ...n]) => [e.split("@")[0], n.map(Number)]));

const QUIZ = {  // respostas corretas da massa (massa.json, questionario)
  "Qual norma define o modelo": "ISO/IEC 25010", "Qual destas é uma característica": "Compatibilidade",
  "No método GQM": "Questões", "12 x 12": "144", "7,5 x 4": "30",
};

function arquivo(nome) {
  return { name: nome, mimeType: "text/plain", buffer: Buffer.from(`Arquivo fictício de ${nome} (M3.1).\n`) };
}

async function login(ctx, usuario) {
  const p = await ctx.newPage();
  await p.goto(`${URL}/login/index.php`);
  await p.fill("#username", usuario);
  await p.fill("#password", SENHA);
  await Promise.all([p.waitForLoadState("load"), p.click("#loginbtn")]);
  return p;
}

async function envia(p, nome) {  // gerenciador de arquivos do Moodle: Add... > Upload a file
  await p.locator(".fp-btn-add a, .fp-btn-add button, a[title='Add...']").first().click();
  await p.locator(".fp-repo-name", { hasText: "Upload a file" }).first().click();
  // O painel "Upload a file" é montado de forma assíncrona; o campo só é usado depois de estável e o
  // envio só é clicado depois de confirmar que o campo recebeu o arquivo.
  const campo = p.locator("input[type=file][name=repo_upload_file]").last();
  for (let i = 0; i < 3; i++) {
    await campo.waitFor({ state: "attached", timeout: 15000 });
    await p.waitForTimeout(700);
    await campo.setInputFiles(arquivo(nome));
    if (await campo.evaluate((e) => e.files.length) > 0) break;
  }
  const enviar = p.locator("button.fp-upload-btn:visible").last();
  await enviar.evaluate((e) => e.scrollIntoView({ block: "center" }));
  await enviar.click();
  await p.locator(".fp-filename", { hasText: nome }).first().waitFor({ timeout: 20000 });
}

// Salva o formulário e devolve o texto dos erros de validação, se a página não sair do formulário.
async function salva(p) {
  // Em telas pequenas a página é longa e a rolagem suave mexe o botão enquanto ele entra na tela:
  // rola até ele e espera a rolagem terminar antes de tocar, como uma pessoa faria.
  // Em telas pequenas o Moodle põe os botões num rodapé fixo (#sticky-footer) que se esconde ao rolar
  // para baixo e reaparece ao rolar para cima: rola até o fim e depois um pouco para cima, como uma pessoa.
  const botao = p.locator("#id_submitbutton2");
  await botao.evaluate((e) => e.scrollIntoView({ block: "center" }));
  await p.waitForTimeout(800);
  if (await p.locator("#sticky-footer").count()) {
    await p.evaluate(() => window.scrollBy(0, -150));
    await p.waitForTimeout(1200);
  }
  await botao.click();
  await p.waitForURL(/course\/view\.php/, { timeout: 30000 }).catch(() => {});
  if (/course\/view\.php/.test(p.url())) return "";
  return (await p.locator(".invalid-feedback:visible, .error:visible, .alert-danger:visible").allInnerTexts())
    .join(" | ").replace(/\s+/g, " ").slice(0, 200) || "o formulário não foi enviado";
}

function data(d) { return { day: String(d.getDate()), month: String(d.getMonth() + 1), year: String(d.getFullYear()) }; }
async function poeData(p, campo, d) {
  const v = data(d);
  for (const k of ["day", "month", "year"]) await p.selectOption(`#id_${campo}_${k}`, v[k]);
}

const TAREFAS = {
  async T02(c) {
    const p = await login(c.docente, "docente01");
    await p.goto(`${URL}/course/modedit.php?add=resource&course=${CURSO}&section=1`);
    await p.fill("#id_name", `Material T02 ${amb}`);
    await envia(p, `material-${amb}.txt`);
    await salva(p);
    const ok = (await p.locator("#region-main").getByText(`Material T02 ${amb}`).count()) > 0;
    return [p, ok, ok ? "material publicado e visível no curso" : "material não aparece no curso"];
  },
  async T03(c) {
    const p = await login(c.docente, "docente01");
    await p.goto(`${URL}/course/modedit.php?add=assign&course=${CURSO}&section=1`);
    await p.fill("#id_name", `Tarefa T03 ${amb}`);
    const hoje = new Date();
    await poeData(p, "duedate", new Date(hoje.getTime() + 7 * 864e5));
    if (!(await p.isChecked("#id_cutoffdate_enabled"))) await p.check("#id_cutoffdate_enabled");
    await poeData(p, "cutoffdate", new Date(hoje.getTime() + 9 * 864e5));
    const erro = await salva(p);
    const m = p.url().match(/#module-(\d+)/);
    if (m) c.estado.cmT03 = Number(m[1]);
    const ok = !!m && (await p.locator("#region-main").getByText(`Tarefa T03 ${amb}`).count()) > 0;
    return [p, ok, ok ? "tarefa criada com data de entrega (D+7) e data limite (D+9)" : `tarefa não criada${erro ? ": " + erro : ""}`];
  },
  async T04(c) {
    const p = await login(c.estudante, estudante);
    await p.goto(`${URL}/mod/assign/view.php?id=${c.estado.cmT03 || CM_T04}`);
    await p.getByRole("button", { name: "Add submission" }).or(p.getByRole("link", { name: "Add submission" })).first().click();
    await envia(p, `envio-${amb}.txt`);
    await Promise.all([p.waitForLoadState("load"), p.click("#id_submitbutton")]);
    const ok = await p.getByText("Submitted for grading").first().isVisible();
    return [p, ok, (ok ? "arquivo enviado; status Submitted for grading" : "envio sem o status Submitted for grading")
      + (c.estado.cmT03 ? " (tarefa criada em T03)" : " (tarefa da massa, porque T03 falhou)")];
  },
  async T05(c) {
    const p = await login(c.estudante, estudante);
    await p.goto(`${URL}/mod/assign/view.php?id=${CM_T05}`);
    const botao = await p.getByRole("button", { name: /Add submission|Edit submission/ })
      .or(p.getByRole("link", { name: /Add submission|Edit submission/ })).count();
    const ok = botao === 0;
    return [p, ok, ok ? "envio bloqueado: sem botão de envio após a data limite" : "botão de envio disponível após a data limite"];
  },
  async T06(c) {
    const p = await login(c.docente, "docente01");
    await p.goto(`${URL}/mod/assign/view.php?id=${c.estado.cmT03 || CM_T04}&action=grader&userid=${c.userid}`);
    const nota = p.locator("input[name=grade]");
    await nota.waitFor({ timeout: 30000 });
    await nota.fill("8.5");
    const comentario = `Bom trabalho (${amb}).`;
    const iframe = p.locator("iframe[id^=id_assignfeedbackcomments_editor]");
    await iframe.or(p.locator("textarea[name^=assignfeedbackcomments_editor]")).first().waitFor({ timeout: 20000 });
    if (await iframe.count()) await p.frameLocator("iframe[id^=id_assignfeedbackcomments_editor]").locator("body").fill(comentario);
    else await p.locator("textarea[name^=assignfeedbackcomments_editor]").fill(comentario);
    await p.locator("button[name=savechanges]").click();
    const ok = await p.getByText(/changes to the grade and feedback were saved/i).first()
      .waitFor({ timeout: 20000 }).then(() => true, () => false);
    return [p, ok, ok ? "nota 8.5 e comentário salvos" : "sem confirmação de nota salva"];
  },
  async T08(c) {
    const p = await login(c.estudante, estudante);
    await p.goto(`${URL}/mod/quiz/view.php?id=${CM_QUIZ}`);
    await p.getByRole("button", { name: /Attempt quiz|Re-attempt quiz|Continue your attempt/ }).click();
    const iniciar = p.getByRole("button", { name: "Start attempt" });
    if (await iniciar.isVisible().catch(() => false)) await iniciar.click();
    for (let pag = 0; pag < 10; pag++) {
      await p.waitForLoadState("load");
      for (const q of await p.locator(".que").all()) {
        const texto = await q.locator(".qtext").innerText();
        const chave = Object.keys(QUIZ).find((k) => texto.includes(k));
        if (!chave) continue;
        const campo = q.locator("input[type=text]");
        if (await campo.count()) await campo.fill(QUIZ[chave]);
        else await q.locator("label, .d-flex", { hasText: QUIZ[chave] }).first().click();
      }
      const fim = p.locator("#mod_quiz-next-nav");
      const rotulo = await fim.inputValue().catch(async () => await fim.innerText());
      await Promise.all([p.waitForLoadState("load"), fim.click()]);
      if (/Finish attempt/i.test(rotulo)) break;
    }
    await p.getByRole("button", { name: "Submit all and finish" }).first().click();
    const modal = p.locator(".modal-dialog").getByRole("button", { name: "Submit all and finish" });
    if (await modal.waitFor({ timeout: 5000 }).then(() => true, () => false)) await modal.click();
    await p.waitForURL(/review\.php/);
    const nota = await p.locator("table.quizreviewsummary").innerText();
    const ok = /10\.00 out of 10\.00/.test(nota);
    return [p, ok, ok ? "questionário enviado; nota automática 10.00 de 10.00" : `nota obtida: ${nota.replace(/\s+/g, " ").slice(0, 120)}`];
  },
  async T09(c) {
    let ok = true; const obs = [];
    let p;
    for (const [ctx, usuario] of [[c.docente, "docente01"], [c.estudante, estudante]]) {
      p = await login(ctx, usuario);
      await p.goto(`${URL}/mod/forum/discuss.php?d=${DISCUSSAO}`);
      await p.locator('a[data-action="collapsible-link"][title="Reply"]').first().click();
      const msg = `Resposta de ${usuario} no ambiente ${amb}.`;
      await p.locator("textarea:visible").first().fill(msg);
      await p.locator("button:visible", { hasText: "Post to forum" }).first().click();
      const viu = await p.getByText(msg).first().waitFor({ timeout: 20000 }).then(() => true, () => false);
      ok = ok && viu; obs.push(`${usuario}: ${viu ? "resposta publicada" : "resposta não apareceu"}`);
    }
    return [p, ok, obs.join("; ")];
  },
  async T11(c) {
    const p = await login(c.estudante, estudante);
    await p.goto(`${URL}/grade/report/user/index.php?id=${CURSO}`);
    const texto = await p.locator("table.user-grade").innerText();
    const esperado = NOTAS[estudante] || [];
    const ok = esperado.length > 0 && esperado.every((v) => texto.includes(v.toFixed(2)));
    return [p, ok, ok ? `notas próprias exibidas (${esperado.map((v) => v.toFixed(2)).join(", ")})` : "notas da massa não encontradas no relatório"];
  },
};

async function navegador() {
  if (amb === "A1") {
    const b = await pw.chromium.connectOverCDP(process.env.CDP_URL || "http://127.0.0.1:9333");
    return { b, opcoes: { viewport: { width: 1366, height: 768 } } };
  }
  if (amb === "A2") {  // Firefox do Windows pelo WebDriver BiDi (ponte scripts/firefox_windows.sh)
    const b = await pw.firefox.launch({ channel: "moz-firefox", executablePath: path.join(__dirname, "firefox_windows.sh") });
    return { b, opcoes: { viewport: { width: 1366, height: 768 } } };
  }
  if (amb === "A3") return { b: await pw.firefox.launch(), opcoes: { viewport: { width: 1366, height: 768 } } };
  if (amb === "A4") return { b: await pw.chromium.launch(), opcoes: { ...pw.devices["Pixel 7"] } };
  // Outros nomes (por exemplo, php83 e php84 em M3.2): Chromium de computador, como navegador de referência.
  return { b: await pw.chromium.launch(), opcoes: { viewport: { width: 1366, height: 768 } } };
}

(async () => {
  const { b, opcoes } = await navegador();
  const userid = Number(process.env.USERID);
  const linhas = [], estado = {};
  // TAREFAS=T02,T08 repete só essas tarefas (seção 1 do plano: repete-se qualquer falha uma vez).
  // A repetição grava "repetição" no resultado e um sufixo _rep na captura.
  const so = process.env.TAREFAS ? process.env.TAREFAS.split(",") : null;
  const rep = so ? "_rep" : "";
  for (const t of Object.keys(TAREFAS).filter((x) => !so || so.includes(x))) {
    const c = { docente: await b.newContext(opcoes), estudante: await b.newContext(opcoes), userid, estado };
    const evid = `${PREFIXO}_${t}_${amb}_${DATA}_${INIC}${rep}.png`;
    let ok = false, obs = "", p;
    try {
      [p, ok, obs] = await TAREFAS[t](c);
    } catch (e) {
      obs = `erro: ${String(e.message).split("\n")[0].slice(0, 160)}`;
      p = c.estudante.pages()[0] || c.docente.pages()[0];
    }
    if (p) await p.screenshot({ path: path.join(EVID, evid), fullPage: false }).catch(() => {});
    const quando = new Date().toISOString();
    linhas.push([amb, t, t === "T02" || t === "T03" || t === "T06" ? "docente01" : t === "T09" ? `docente01 e ${estudante}` : estudante,
      quando, ok ? "sim" : "não", (so ? "repetição: " : "") + obs, evid]);
    console.log(`${amb} ${t} ${ok ? "ok " : "NÃO"} ${obs}`);
    await c.docente.close(); await c.estudante.close();
  }
  const ua = await (async () => { const x = await b.newContext(opcoes); const pg = await x.newPage(); const u = await pg.evaluate(() => navigator.userAgent); await x.close(); return u; })();
  const novo = !fs.existsSync(CSV);
  const esc = (s) => `"${String(s).replace(/"/g, '""')}"`;
  fs.appendFileSync(CSV, (novo ? "ambiente,tarefa,usuario,data_hora,concluida,resultado_observado,evidencia,user_agent\n" : "")
    + linhas.map((l) => [...l, ua].map(esc).join(",")).join("\n") + "\n");
  await b.close();
})();
