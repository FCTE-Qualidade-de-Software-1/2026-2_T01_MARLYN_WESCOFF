// M2.1 (issue #68), F2 e F3: exporta o livro de notas do curso pela interface do Moodle, em texto (CSV) e
// em planilha Excel, e salva o arquivo baixado. Uso:
//   PW_CORE=... ADMIN_SENHA=... node scripts/m21_notas.js <url> <courseid> <pasta de saída>
const path = require("path");
const pw = require(process.env.PW_CORE || "playwright-core");
const [URL, CURSO, SAIDA] = process.argv.slice(2);
(async () => {
  const b = await pw.chromium.launch(); const c = await b.newContext({ acceptDownloads: true, viewport: { width: 1366, height: 900 } });
  const p = await c.newPage();
  await p.goto(`${URL}/login/index.php`); await p.fill("#username", "admin-aval"); await p.fill("#password", process.env.ADMIN_SENHA);
  await Promise.all([p.waitForLoadState("load"), p.click("#loginbtn")]);
  // Até duas tentativas por formato (seção 1 do plano): uma mensagem de erro do Moodle é registrada e o
  // usuário segue pelo botão Continue que a própria mensagem oferece.
  for (const [fmt, plugin, nome] of [["F2", "txt", "F2_notas_exportadas.csv"], ["F3", "xls", "F3_notas_exportadas.xlsx"]]) {
    for (let t = 1; t <= 2; t++) {
      // Tentativa 2: caminho da interface (Notas > relatório de notas > Exportar), que recalcula o livro
      // de notas ao abrir o relatório. A tentativa 1 foi direto à URL de exportação.
      if (t === 2) { await p.goto(`${URL}/grade/report/grader/index.php?id=${CURSO}`); await p.waitForLoadState("load"); }
      await p.goto(`${URL}/grade/export/${plugin}/index.php?id=${CURSO}`);
      await p.screenshot({ path: path.join(SAIDA, `M2.1_${fmt}_tentativa${t}_2026-11-22_CDM.png`), fullPage: true });
      const erro = p.locator(".alert-danger, .errorbox").first();
      if (await erro.count()) {
        const msg = (await erro.innerText()).replace(/\s+/g, " ").trim();
        console.log(JSON.stringify({ formato: fmt, tentativa: t, conclui: "não", mensagem: msg }));
        const cont = p.getByRole("button", { name: "Continue" }).or(p.getByRole("link", { name: "Continue" })).first();
        if (await cont.count()) { await Promise.all([p.waitForLoadState("load"), cont.click()]); }
        continue;
      }
      const [d] = await Promise.all([p.waitForEvent("download", { timeout: 60000 }), p.locator("#id_submitbutton").click()]);
      await d.saveAs(path.join(SAIDA, nome));
      console.log(JSON.stringify({ formato: fmt, tentativa: t, conclui: "sim", arquivo: nome, sugerido: d.suggestedFilename() }));
      break;
    }
  }
  await b.close();
})();
