<?php
// M3.2 (adaptabilidade à versão de PHP), issue #70: tarefas T01, T07, T10 e T12 do catálogo pela API do
// Moodle, na versão de PHP com que o script é chamado (php8.3 ou php8.4). As tarefas T02 a T06, T08, T09
// e T11 vão pela interface (scripts/m31_tarefas.js). Imprime uma linha JSON por tarefa, com o resultado
// e o id do objeto criado, para a verificação por HTTP que vem depois.
//
// Uso (no servidor, como www-data): php8.x m32_tarefas_api.php --moodle=/var/www/<instancia>
define('CLI_SCRIPT', true);
$o = getopt('', ['moodle:']);
require(rtrim($o['moodle'], '/') . '/config.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/enrol/manual/lib.php');
require_once($CFG->libdir . '/gradelib.php');
require_once($CFG->dirroot . '/mod/quiz/locallib.php');
require_once($CFG->dirroot . '/backup/util/includes/backup_includes.php');
require_once($CFG->dirroot . '/backup/util/includes/restore_includes.php');
\core\session\manager::set_user(get_admin());
// Gerador de dados do Moodle, como em gera_massa_moodle.php (na 5.x fica em \core\test\phpunit).
$g = \core\test\phpunit\phpunit_util::get_data_generator();
// Mesma criação de questões da massa (scripts/gera_massa_moodle.php), pelo formulário de questão.
function cria_questao(int $categoriaid, array $q): stdClass {
    $vazio = ['text' => '', 'format' => FORMAT_HTML];
    $form = (object) ['category' => $categoriaid, 'name' => $q['nome'], 'defaultmark' => $q['nota_padrao'],
        'questiontext' => ['text' => $q['enunciado'], 'format' => FORMAT_HTML], 'generalfeedback' => $vazio,
        'penalty' => 0.3333333, 'idnumber' => null,
        'status' => \core_question\local\bank\question_version_status::QUESTION_STATUS_READY];
    if ($q['tipo'] === 'multichoice') {
        $n = count($q['respostas']);
        $form->single = '1';
        $form->shuffleanswers = 0;
        $form->answernumbering = 'abc';
        $form->showstandardinstruction = 0;
        $form->noanswers = $n;
        $form->answer = array_map(fn($r) => ['text' => $r['texto'], 'format' => FORMAT_PLAIN], $q['respostas']);
        $form->fraction = array_map(fn($r) => sprintf('%.7F', $r['fracao']), $q['respostas']);
        $form->feedback = array_fill(0, $n, $vazio);
        $form->correctfeedback = $vazio;
        $form->partiallycorrectfeedback = $vazio;
        $form->incorrectfeedback = $vazio;
        $form->shownumcorrect = 0;
    } else {
        $form->noanswers = 1;
        $form->answer = [(string) $q['resposta']];
        $form->tolerance = [$q['tolerancia']];
        $form->fraction = ['1.0'];
        $form->feedback = [$vazio];
        $form->unitrole = '3';          // sem unidades
        $form->unitpenalty = 0.1;
        $form->unitgradingtypes = '1';
        $form->unitsleft = '0';
        $form->nounits = 1;
        $form->multiplier = ['1.0'];
    }
    $questao = (object) ['qtype' => $q['tipo'], 'createdby' => 0, 'idnumber' => null, 'status' => $form->status];
    return question_bank::get_qtype($q['tipo'])->save_question($questao, $form);
}

$saida = fn($t, $ok, $det, $extra = []) => print(json_encode(['tarefa' => $t, 'php' => PHP_VERSION, 'concluida' => $ok ? 'sim' : 'não',
    'resultado_observado' => $det] + $extra, JSON_UNESCAPED_UNICODE) . "\n");
$usuario = fn($u) => $GLOBALS['DB']->get_record('user', ['username' => $u], '*', MUST_EXIST);

// T01: criar curso e matricular estudantes e docente
try {
    $curso = create_course((object) ['fullname' => 'Curso T01 M3.2 (PHP ' . PHP_VERSION . ')', 'shortname' => 'T01-M32-' . time(),
        'category' => $DB->get_field('course_categories', 'id', [], IGNORE_MULTIPLE), 'format' => 'topics', 'numsections' => 3]);
    $plugin = enrol_get_plugin('manual');
    $inst = $DB->get_record('enrol', ['courseid' => $curso->id, 'enrol' => 'manual'], '*', MUST_EXIST);
    $papel = fn($s) => $DB->get_field('role', 'id', ['shortname' => $s]);
    foreach (['est01', 'est02', 'est03'] as $u) {
        $plugin->enrol_user($inst, $usuario($u)->id, $papel('student'));
    }
    $plugin->enrol_user($inst, $usuario('docente01')->id, $papel('editingteacher'));
    $n = $DB->count_records('user_enrolments', ['enrolid' => $inst->id]);
    $saida('T01', $n === 4, "curso {$curso->id} criado; $n matrículas (3 estudantes e o docente)", ['url' => "/course/view.php?id={$curso->id}"]);
} catch (Throwable $e) {
    $saida('T01', false, 'erro: ' . $e->getMessage());
}

// T07: criar questionário com questões de múltipla escolha e numéricas
try {
    $quiz = $g->create_module('quiz', ['course' => $curso->id, 'name' => 'Questionário T07 M3.2', 'grade' => 10, 'sumgrades' => 0]);
    $qg = $g->get_plugin_generator('core_question');
    $cat = $qg->create_question_category(['contextid' => context_module::instance($quiz->cmid)->id]);
    $mc = cria_questao((int) $cat->id, ['tipo' => 'multichoice', 'nome' => 'T07 múltipla escolha', 'nota_padrao' => 1,
        'enunciado' => 'Qual norma define o modelo de qualidade de produto?', 'respostas' => [
        ['texto' => 'ISO/IEC 25010', 'fracao' => 1.0], ['texto' => 'ISO 9001', 'fracao' => 0.0]]]);
    $nu = cria_questao((int) $cat->id, ['tipo' => 'numerical', 'nome' => 'T07 numérica', 'nota_padrao' => 1,
        'enunciado' => 'Quanto é 12 x 12?', 'resposta' => 144, 'tolerancia' => 0]);
    quiz_add_quiz_question($mc->id, $quiz, 0, 5);
    quiz_add_quiz_question($nu->id, $quiz, 0, 5);
    \mod_quiz\quiz_settings::create($quiz->id)->get_grade_calculator()->recompute_quiz_sumgrades();
    $slots = $DB->count_records('quiz_slots', ['quizid' => $quiz->id]);
    $soma = (float) $DB->get_field('quiz', 'sumgrades', ['id' => $quiz->id]);
    $saida('T07', $slots === 2 && abs($soma - 10) < 1e-6, "questionário com $slots questões (múltipla escolha e numérica), soma das notas $soma",
        ['url' => "/mod/quiz/view.php?id={$quiz->cmid}"]);
} catch (Throwable $e) {
    $saida('T07', false, 'erro: ' . $e->getMessage());
}

// T10: configurar categorias e pesos no livro de notas
try {
    foreach ([['Provas', 60], ['Trabalhos', 40]] as [$nome, $peso]) {
        $c = $g->create_grade_category(['courseid' => $curso->id, 'fullname' => $nome, 'aggregation' => GRADE_AGGREGATE_WEIGHTED_MEAN]);
        $item = grade_category::fetch(['id' => $c->id])->load_grade_item();
        $item->aggregationcoef = $peso;
        $item->update();
    }
    $raiz = grade_category::fetch_course_category($curso->id);
    $raiz->aggregation = GRADE_AGGREGATE_WEIGHTED_MEAN;
    $raiz->update();
    grade_regrade_final_grades($curso->id);
    $pesos = $DB->get_records_sql_menu("SELECT c.fullname, i.aggregationcoef FROM {grade_categories} c
        JOIN {grade_items} i ON i.iteminstance = c.id AND i.itemtype = 'category' WHERE c.courseid = ?", [$curso->id]);
    $ok = isset($pesos['Provas'], $pesos['Trabalhos']) && (float) $pesos['Provas'] == 60 && (float) $pesos['Trabalhos'] == 40;
    $saida('T10', $ok, 'categorias com pesos: ' . json_encode(array_map('floatval', $pesos), JSON_UNESCAPED_UNICODE),
        ['url' => "/grade/edit/tree/index.php?id={$curso->id}"]);
} catch (Throwable $e) {
    $saida('T10', false, 'erro: ' . $e->getMessage());
}

// T12: fazer backup do curso e restaurá-lo como novo curso
try {
    $admin = get_admin();
    $bc = new backup_controller(backup::TYPE_1COURSE, $curso->id, backup::FORMAT_MOODLE, backup::INTERACTIVE_NO,
        backup::MODE_GENERAL, $admin->id);
    $bc->execute_plan();
    $arquivo = $bc->get_results()['backup_destination'];
    $bc->destroy();
    $pasta = 'm32_' . random_string(8);
    $arquivo->extract_to_pathname(get_file_packer('application/vnd.moodle.backup'), make_backup_temp_directory($pasta));
    $novo = restore_dbops::create_new_course('Curso T01 M3.2 restaurado', 'T01-M32-R-' . time(), $curso->category);
    $rc = new restore_controller($pasta, $novo, backup::INTERACTIVE_NO, backup::MODE_GENERAL, $admin->id, backup::TARGET_NEW_COURSE);
    $rc->execute_precheck();
    $rc->execute_plan();
    $rc->destroy();
    $mods = $DB->count_records('course_modules', ['course' => $novo]);
    $orig = $DB->count_records('course_modules', ['course' => $curso->id]);
    $saida('T12', $mods === $orig && $mods > 0, "backup de " . display_size($arquivo->get_filesize()) . " restaurado no curso $novo; atividades: $mods de $orig",
        ['url' => "/course/view.php?id=$novo"]);
} catch (Throwable $e) {
    $saida('T12', false, 'erro: ' . $e->getMessage());
}
