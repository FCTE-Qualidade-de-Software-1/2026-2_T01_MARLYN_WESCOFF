// M3.2: abre, como administrador, a página "Verificação de ambiente" e as páginas dos objetos criados
// pela API (T01, T07, T10, T12) em uma instância, com captura de tela, e confere HTTP 200 sem erro do Moodle.
// Uso: PW_CORE=... ADMIN_SENHA=... node scripts/m32_paginas.js <php83|php84> <url> <api.jsonl>
const fs = require("fs"), path = require("path");
const pw = require(process.env.PW_CORE || "playwright-core");
const [rot, URL, api] = process.argv.slice(2);
const SAIDA = path.resolve(__dirname, "..", "dados", "avaliacao", "M3.2");
(async () => {
  const b = await pw.chromium.launch(); const c = await b.newContext({ viewport: { width: 1366, height: 900 } }); const p = await c.newPage();
  await p.goto(`${URL}/login/index.php`); await p.fill("#username", "admin-aval"); await p.fill("#password", process.env.ADMIN_SENHA);
  await Promise.all([p.waitForLoadState("load"), p.click("#loginbtn")]);
  const paginas = [["ambiente", "/admin/environment.php"], ...fs.readFileSync(api, "utf8").trim().split("\n").map(JSON.parse).filter((j) => j.url).map((j) => [j.tarefa, j.url])];
  const linhas = [];
  for (const [nome, u] of paginas) {
    const r = await p.goto(URL + u); await p.waitForLoadState("load");
    const erro = await p.locator(".errorbox, .alert-danger .errormessage, #page-content .moodle-exception").count();
    let detalhe = "";
    if (nome === "ambiente") {
      const t = await p.locator("#page-content").innerText();
      const falhas = await p.locator("table.environmenttable .table-danger, table.environmenttable td.text-danger, .environmenttable .badge.bg-danger").count();
      detalhe = (/Your server environment meets all minimum requirements/i.test(t) ? "ambiente atende aos requisitos mínimos" : "mensagem de requisitos não encontrada") + `; itens com erro: ${falhas}`;
    }
    const arq = `M3.2_pagina_${nome}_${rot}_2026-11-22_JPSM.png`;
    await p.screenshot({ path: path.join(SAIDA, arq), fullPage: nome === "ambiente" });
    linhas.push([rot, nome, u, r.status(), erro ? "sim" : "não", detalhe, arq]);
    console.log(rot, nome, r.status(), erro ? "ERRO" : "ok", detalhe);
  }
  const csv = path.join(SAIDA, "paginas.csv"), novo = !fs.existsSync(csv);
  fs.appendFileSync(csv, (novo ? "php,pagina,url,http,erro_moodle,detalhe,evidencia\n" : "") + linhas.map((l) => l.map((x) => `"${String(x).replace(/"/g, '""')}"`).join(",")).join("\n") + "\n");
  await b.close();
})();
