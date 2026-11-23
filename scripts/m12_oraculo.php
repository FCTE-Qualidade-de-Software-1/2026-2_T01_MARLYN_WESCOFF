<?php
// M1.2 (correção funcional), issue #67: executa um caso do oráculo (dados/avaliacao/M1.2/oraculo.csv) no
// curso AVAL-ORACULO criado pela parte "oraculo" de gera_massa.py, pela API do próprio Moodle, e imprime
// uma linha JSON com o resultado observado.
//
//   Q-01..Q-10  tentativa do estudante com as respostas do oráculo (Correta, Parcial 50% ou Incorreta);
//               observado = nota do questionário (quiz_rescale_grade, a mesma exibida ao estudante)
//   A-01..A-06  notas do oráculo lançadas nos itens da categoria; observado = total da categoria após
//               o recálculo do livro de notas (grade_format_gradevalue, formato real, 2 casas)
//   P-01..P-04  envio ou tentativa no horário do oráculo. O horário vem do relógio do processo: rodar com
//               faketime (por exemplo, faketime '2026-11-22 23:58:00' php ...), com D = --dia-prazo da massa
//
// Uso (no servidor, como www-data):
//   [faketime '<data hora>'] php m12_oraculo.php --moodle=/var/www/<inst> --caso=Q-01 [--estudante=est01]
define('CLI_SCRIPT', true);
$o = getopt('', ['moodle:', 'caso:', 'estudante:']);
require(rtrim($o['moodle'], '/') . '/config.php');
require_once($CFG->dirroot . '/mod/quiz/locallib.php');
require_once($CFG->dirroot . '/mod/assign/locallib.php');
require_once($CFG->libdir . '/gradelib.php');

$caso = $o['caso'];
$est = $DB->get_record('user', ['username' => $o['estudante'] ?? 'est01', 'deleted' => 0], '*', MUST_EXIST);
$curso = $DB->get_record('course', ['shortname' => 'AVAL-ORACULO'], '*', MUST_EXIST);
$saida = ['caso' => $caso, 'estudante' => $est->username, 'relogio' => date('Y-m-d H:i:s T', time())];

if ($caso[0] === 'Q') {
    $respostas = ['Q-01' => 'CCI', 'Q-02' => 'CCICC', 'Q-03' => 'CICI', 'Q-04' => 'CCCCCCCIII', 'Q-05' => 'CCPCI',
        'Q-06' => 'CCIC', 'Q-07' => 'CCCCCI', 'Q-08' => 'CCCCCCII', 'Q-09' => 'CPC', 'Q-10' => str_repeat('C', 19) . 'I'];
    $texto = ['C' => 'Correta', 'P' => 'Parcial (50%)', 'I' => 'Incorreta A'];
    $quiz = $DB->get_record('quiz', ['course' => $curso->id, 'name' => "$caso Questionário do oráculo"], '*', MUST_EXIST);
    \core\session\manager::set_user($est);
    $quizobj = \mod_quiz\quiz_settings::create($quiz->id, $est->id);
    $quba = question_engine::make_questions_usage_by_activity('mod_quiz', $quizobj->get_context());
    $quba->set_preferred_behaviour($quizobj->get_quiz()->preferredbehaviour);
    $agora = time();
    $num = $DB->count_records('quiz_attempts', ['quiz' => $quiz->id, 'userid' => $est->id]) + 1;
    $tentativa = quiz_create_attempt($quizobj, $num, null, $agora, false, $est->id);
    quiz_start_new_attempt($quizobj, $quba, $tentativa, $num, $agora);
    quiz_attempt_save_started($quizobj, $quba, $tentativa);
    $ao = \mod_quiz\quiz_attempt::create($tentativa->id);
    $simulado = [];
    $marcadas = [];
    foreach ($ao->get_slots() as $slot) {
        $nome = $ao->get_question_attempt($slot)->get_question()->name;   // "Q-05 questão 3"
        preg_match('/(\d+)$/', $nome, $m);
        $letra = $respostas[$caso][(int) $m[1] - 1];
        $simulado[$slot] = ['answer' => $texto[$letra]];
        $marcadas[] = $m[1] . $letra;
    }
    $ao->process_submitted_actions($agora, false, $simulado);
    $ao->process_finish($agora, false);
    $soma = $DB->get_field('quiz_attempts', 'sumgrades', ['id' => $tentativa->id]);
    $nota = quiz_rescale_grade($soma, $quiz, false);
    $saida += ['observado' => sprintf('%.2f', $nota), 'detalhe' => 'respostas ' . implode(' ', $marcadas)
        . sprintf('; soma das marcas %.4f de %.4f; nota máxima %s', $soma, $quiz->sumgrades, $quiz->grade)];
} elseif ($caso[0] === 'A') {
    $valores = ['A-01' => ['A-01 P1' => 7.5, 'A-01 P2' => 8.0], 'A-02' => ['A-02 N1' => 6, 'A-02 N2' => 8, 'A-02 N3' => 10],
        'A-03' => ['A-03 N1' => 9, 'A-03 N2' => 7, 'A-03 N3' => 8], 'A-04' => ['A-04 categoria 1' => 18, 'A-04 categoria 2' => 35],
        'A-05' => ['A-05 N1' => 5, 'A-05 N2' => 7, 'A-05 N3' => 8, 'A-05 N4' => 9],
        'A-06' => ['A-06 Questionário 1' => 8.5, 'A-06 Tarefa 1' => 9.2]];
    \core\session\manager::set_user(get_admin());
    foreach ($valores[$caso] as $nome => $v) {
        $item = grade_item::fetch(['courseid' => $curso->id, 'itemname' => $nome]);
        $item->update_final_grade($est->id, $v, 'import');
    }
    grade_regrade_final_grades($curso->id);
    $cat = grade_category::fetch(['courseid' => $curso->id, 'fullname' => "$caso Agregação"]);
    $total = $cat->load_grade_item();
    $grade = new grade_grade(['itemid' => $total->id, 'userid' => $est->id]);
    $real = grade_format_gradevalue($grade->finalgrade, $total, true, GRADE_DISPLAY_TYPE_REAL, 2);
    $pct = grade_format_gradevalue($grade->finalgrade, $total, true, GRADE_DISPLAY_TYPE_PERCENTAGE, 2);
    $saida += ['observado' => $real, 'detalhe' => sprintf('total da categoria %s de %s (%s); notas lançadas: %s',
        $real, format_float($total->grademax, 2), $pct, json_encode($valores[$caso], JSON_UNESCAPED_UNICODE)),
        'porcentagem' => $pct, 'nota_maxima' => (float) $total->grademax];
} else {
    $tarefas = ['P-01' => 'P-01 e P-02 Tarefa com prazo', 'P-02' => 'P-01 e P-02 Tarefa com prazo', 'P-03' => 'P-03 Tarefa com prazo'];
    \core\session\manager::set_user($est);
    if (isset($tarefas[$caso])) {
        $inst = $DB->get_record('assign', ['course' => $curso->id, 'name' => $tarefas[$caso]], '*', MUST_EXIST);
        $cm = get_coursemodule_from_instance('assign', $inst->id, $curso->id, false, MUST_EXIST);
        $assign = new assign(context_module::instance($cm->id), $cm, $curso);
        if (!$assign->submissions_open($est->id)) {
            $saida += ['observado' => 'bloqueado', 'detalhe' => 'submissions_open = false: o Moodle não aceita envio'];
        } else {
            $dados = (object) ['onlinetext_editor' => ['text' => "Envio do caso $caso", 'format' => FORMAT_HTML,
                'itemid' => file_get_unused_draft_itemid()]];
            $avisos = [];
            $ok = $assign->save_submission($dados, $avisos);
            $envio = $assign->get_user_submission($est->id, false);
            $atraso = $envio && $inst->duedate && $envio->timemodified > $inst->duedate;
            $saida += ['observado' => !$ok || !$envio ? 'erro' : ($atraso ? 'aceito_com_atraso' : 'aceito'),
                'detalhe' => sprintf('status %s; enviado em %s; vencimento %s; data limite %s%s', $envio->status ?? '-',
                    date('Y-m-d H:i', $envio->timemodified ?? 0), date('Y-m-d H:i', $inst->duedate),
                    date('Y-m-d H:i', $inst->cutoffdate), $avisos ? '; avisos: ' . implode(' ', $avisos) : '')];
        }
    } else {
        $quiz = $DB->get_record('quiz', ['course' => $curso->id, 'name' => 'P-04 Questionário com prazo'], '*', MUST_EXIST);
        $quizobj = \mod_quiz\quiz_settings::create($quiz->id, $est->id);
        $acesso = $quizobj->get_access_manager(time());
        $motivos = array_merge($acesso->prevent_access(), $acesso->prevent_new_attempt(0, null));
        $saida += ['observado' => $motivos ? 'bloqueado' : 'aceito',
            'detalhe' => ($motivos ? 'acesso negado: ' . strip_tags(implode(' ', $motivos)) : 'tentativa permitida')
                . '; fecha em ' . date('Y-m-d H:i', $quiz->timeclose)];
    }
}
echo json_encode($saida, JSON_UNESCAPED_UNICODE), "\n";
