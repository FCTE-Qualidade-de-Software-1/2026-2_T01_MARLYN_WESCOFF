<?php
// Executor da etapa "aplicar" de scripts/gera_massa.py (issue #63). Não chame este arquivo direto:
// o gera_massa.py monta a entrada (massa.json) e grava o registro do que foi criado.
//
// Cria a massa com os geradores de dados do próprio Moodle (os mesmos que o admin/tool/generator usa
// em linha de comando), dentro de uma única transação: se qualquer passo falhar, nada fica gravado.
//
// Uso: php gera_massa_moodle.php --config=/var/www/m53php83/config.php --entrada=massa.json --saida=resultado.json

define('CLI_SCRIPT', true);

$opcoes = [];
foreach (array_slice($argv, 1) as $arg) {
    if (preg_match('/^--(config|entrada|saida)=(.+)$/', $arg, $m)) {
        $opcoes[$m[1]] = $m[2];
    }
}
foreach (['config', 'entrada', 'saida'] as $obrigatoria) {
    if (empty($opcoes[$obrigatoria])) {
        fwrite(STDERR, "uso: php gera_massa_moodle.php --config=... --entrada=... --saida=...\n");
        exit(2);
    }
}

require($opcoes['config']);
require_once($CFG->libdir . '/gradelib.php');
require_once($CFG->libdir . '/grade/constants.php');
require_once($CFG->dirroot . '/calendar/lib.php');
require_once($CFG->dirroot . '/mod/quiz/locallib.php');

$massa = json_decode(file_get_contents($opcoes['entrada']), true, 512, JSON_THROW_ON_ERROR);
$resultado = ['moodle_release' => $CFG->release, 'criado' => [], 'ignorado' => [], 'erro' => null];

function registra(string $tipo, string $nome, $id = null): void {
    global $resultado;
    $resultado['criado'][] = ['tipo' => $tipo, 'nome' => $nome, 'id' => $id];
    mtrace("  + {$tipo}: {$nome}");
}

function grava_resultado(): void {
    global $resultado, $opcoes;
    file_put_contents($opcoes['saida'], json_encode($resultado, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
}

/** Gerador de dados: a 5.x o expõe em \core\test\phpunit; a 4.5, em lib/phpunit. */
function gerador(): testing_data_generator {
    global $CFG;
    if (class_exists('\core\test\phpunit\phpunit_util')) {
        return \core\test\phpunit\phpunit_util::get_data_generator();
    }
    require_once($CFG->dirroot . '/lib/phpunit/classes/util.php');
    return phpunit_util::get_data_generator();
}

function usuario(string $username): stdClass {
    global $DB, $CFG;
    return $DB->get_record('user', ['username' => $username, 'mnethostid' => $CFG->mnet_localhost_id], '*', MUST_EXIST);
}

function exige_curso_novo(string $shortname): void {
    global $DB;
    if ($DB->record_exists('course', ['shortname' => $shortname])) {
        throw new moodle_exception('generalexceptionmessage', 'error', '',
            "o curso {$shortname} já existe; a massa é aplicada uma vez, em instância nova");
    }
}

function cria_curso(testing_data_generator $g, array $curso): stdClass {
    exige_curso_novo($curso['shortname']);
    $c = $g->create_course(['shortname' => $curso['shortname'], 'fullname' => $curso['fullname'],
        'numsections' => 4, 'summary' => 'Curso fictício da avaliação do Moodle 5.3 (massa de dados).']);
    registra('curso', $curso['shortname'], (int) $c->id);
    return $c;
}

function matricula(testing_data_generator $g, stdClass $curso, array $usernames, string $papel): void {
    foreach ($usernames as $u) {
        $g->enrol_user(usuario($u)->id, $curso->id, $papel);
    }
    registra('matrícula', "{$curso->shortname}: " . count($usernames) . " como {$papel}");
}

/**
 * Questão salva pelo mesmo caminho do formulário de edição do banco de questões (save_question do tipo).
 * O gerador de questões do Moodle não serve aqui: ele carrega classes do PHPUnit, que não existem
 * em uma instalação de produção.
 */
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

function cria_questionario(testing_data_generator $g, stdClass $curso, array $cfg): stdClass {
    $quiz = $g->create_module('quiz', ['course' => $curso->id, 'name' => $cfg['nome'],
        'grade' => $cfg['nota_maxima'], 'sumgrades' => 0, 'decimalpoints' => 2, 'questiondecimalpoints' => -1,
        'questionsperpage' => 0, 'shuffleanswers' => 0, 'attempts' => 0, 'grademethod' => QUIZ_GRADEHIGHEST,
        'preferredbehaviour' => 'deferredfeedback',
        'timeopen' => $cfg['abre'] ?? 0, 'timeclose' => $cfg['fecha'] ?? 0]);
    $contexto = context_module::instance($quiz->cmid);
    $categoria = $g->get_plugin_generator('core_question')->create_question_category(
        ['contextid' => $contexto->id, 'name' => "Questões de {$cfg['nome']}"]);
    foreach ($cfg['questoes'] as $q) {
        $questao = cria_questao((int) $categoria->id, $q);
        quiz_add_quiz_question($questao->id, $quiz, 0, $q['nota_max_slot']);
    }
    if (class_exists('\mod_quiz\quiz_settings')) {
        \mod_quiz\quiz_settings::create($quiz->id)->get_grade_calculator()->recompute_quiz_sumgrades();
    } else {
        quiz_update_sumgrades($quiz);
    }
    registra('questionário', "{$cfg['nome']} (" . count($cfg['questoes']) . " questões)", (int) $quiz->cmid);
    return $quiz;
}

function cria_tarefa(testing_data_generator $g, stdClass $curso, array $cfg): stdClass {
    $tarefa = $g->create_module('assign', ['course' => $curso->id, 'name' => $cfg['nome'], 'grade' => 10,
        'submissiondrafts' => 0, 'allowsubmissionsfromdate' => $cfg['abre'], 'duedate' => $cfg['vencimento'],
        'cutoffdate' => $cfg['data_limite'], 'gradingduedate' => 0,
        'assignsubmission_onlinetext_enabled' => 1, 'assignsubmission_file_enabled' => 1,
        'assignsubmission_file_maxfiles' => 1, 'assignsubmission_file_maxsizebytes' => 0]);
    registra('tarefa', $cfg['nome'], (int) $tarefa->cmid);
    return $tarefa;
}

/** Categoria de nota com a agregação do caso; a nota máxima vai para o item total da categoria. */
function cria_categoria_nota(testing_data_generator $g, stdClass $curso, array $cfg, ?int $pai = null,
                             ?float $peso = null): grade_category {
    $agregacao = ['media_ponderada' => GRADE_AGGREGATE_WEIGHTED_MEAN, 'media_simples' => GRADE_AGGREGATE_MEAN,
        'soma_natural' => GRADE_AGGREGATE_SUM][$cfg['agregacao']];
    $registro = ['courseid' => $curso->id, 'fullname' => $cfg['nome'], 'aggregation' => $agregacao,
        'droplow' => $cfg['descartar_menores'] ?? 0];
    if ($pai) {
        $registro['parent'] = $pai;
    }
    $rec = $g->create_grade_category($registro);
    $categoria = grade_category::fetch(['id' => $rec->id]);
    $total = $categoria->load_grade_item();
    if (!empty($cfg['nota_maxima'])) {
        $total->grademax = $cfg['nota_maxima'];
    }
    if ($peso !== null) {
        $total->aggregationcoef = $peso;
    }
    $total->update();
    foreach ($cfg['itens'] as $item) {
        $g->create_grade_item(['courseid' => $curso->id, 'itemname' => $item['nome'], 'itemtype' => 'manual',
            'grademax' => $item['nota_maxima'], 'categoryid' => $categoria->id,
            'aggregationcoef' => $item['peso'] ?? 0]);
    }
    foreach ($cfg['subcategorias'] ?? [] as $sub) {
        cria_categoria_nota($g, $curso, $sub, (int) $categoria->id, (float) $sub['peso']);
    }
    registra('categoria de nota', "{$cfg['nome']} (" . count($cfg['itens']) . " itens, "
        . count($cfg['subcategorias'] ?? []) . " subcategorias)", (int) $categoria->id);
    return $categoria;
}

// ---------------------------------------------------------------------------------------------
function parte_contas(testing_data_generator $g, array $m, string $senha): void {
    global $DB, $CFG, $resultado;
    mtrace('Contas');
    $contas = $m['contas']['estudantes'];
    $contas[] = $m['contas']['docente'];
    foreach ($contas as $c) {
        $existente = $DB->get_record('user', ['username' => $c['username'], 'mnethostid' => $CFG->mnet_localhost_id]);
        if ($existente) {
            // Aceita contas já criadas pela importação de usuarios.csv (F1), desde que os dados batam.
            foreach (['firstname', 'lastname', 'email'] as $campo) {
                if ($existente->$campo !== $c[$campo]) {
                    throw new moodle_exception('generalexceptionmessage', 'error', '',
                        "a conta {$c['username']} já existe com {$campo} diferente da massa");
                }
            }
            $resultado['ignorado'][] = ['tipo' => 'conta', 'nome' => $c['username'], 'motivo' => 'já existia'];
            continue;
        }
        $u = $g->create_user($c + ['password' => $senha, 'auth' => 'manual', 'timezone' => $m['fuso']]);
        registra('conta', $c['username'], (int) $u->id);
    }
}

function parte_catalogo(testing_data_generator $g, array $m): void {
    global $USER;
    mtrace('Curso completo e curso vazio');
    $cat = $m['catalogo'];
    $estudantes = array_column($m['contas']['estudantes'], 'username');
    $docente = $m['contas']['docente']['username'];
    exige_curso_novo($cat['curso_vazio']['shortname']);

    $curso = cria_curso($g, $cat['curso']);
    matricula($g, $curso, $estudantes, 'student');
    matricula($g, $curso, [$docente], 'editingteacher');

    $material = $g->create_module('resource', ['course' => $curso->id, 'name' => $cat['material']['nome'],
        'defaultfilename' => $cat['material']['arquivo']]);
    registra('arquivo', $cat['material']['nome'], (int) $material->cmid);

    $tarefas = [];
    foreach ($cat['tarefas'] as $t) {
        $tarefas[$t['nome']] = cria_tarefa($g, $curso, $t);
    }
    $alvo = $tarefas[$cat['envios']['tarefa']];
    foreach ($cat['envios']['estudantes'] as $u) {
        $g->get_plugin_generator('mod_assign')->create_submission(['userid' => usuario($u)->id,
            'cmid' => $alvo->cmid, 'onlinetext' => "Envio fictício de {$u} para a massa de dados."]);
    }
    registra('envio de tarefa', "{$cat['envios']['tarefa']}: " . count($cat['envios']['estudantes']) . ' envios');

    cria_questionario($g, $curso, $cat['questionario']);

    $forum = $g->create_module('forum', ['course' => $curso->id, 'name' => $cat['forum']['nome'], 'type' => 'general']);
    $fg = $g->get_plugin_generator('mod_forum');
    $topico = $fg->create_discussion(['course' => $curso->id, 'forum' => $forum->id,
        'userid' => usuario($docente)->id, 'name' => $cat['forum']['topico'], 'message' => $cat['forum']['mensagem']]);
    foreach ($cat['forum']['respostas'] as $u) {
        $fg->create_post(['discussion' => $topico->id, 'parent' => $topico->firstpost, 'userid' => usuario($u)->id,
            'subject' => "Re: {$cat['forum']['topico']}", 'message' => "Resposta fictícia de {$u}."]);
    }
    registra('fórum', "{$cat['forum']['nome']} (1 tópico, " . count($cat['forum']['respostas']) . ' respostas)',
        (int) $forum->cmid);

    $itens = [];
    foreach ($cat['itens_nota'] as $nome) {
        $rec = $g->create_grade_item(['courseid' => $curso->id, 'itemname' => $nome, 'itemtype' => 'manual',
            'grademax' => 10, 'decimals' => 2]);
        $itens[] = grade_item::fetch(['id' => $rec->id]);
    }
    foreach ($cat['notas'] as $username => $notas) {
        $uid = usuario($username)->id;
        foreach ($notas as $i => $valor) {
            $itens[$i]->update_final_grade($uid, $valor, 'gera_massa');
        }
    }
    registra('notas', count($cat['notas']) . ' estudantes x ' . count($itens) . ' itens');

    foreach ($cat['eventos'] as $e) {
        calendar_event::create((object) ['name' => $e['titulo'], 'description' => '', 'format' => FORMAT_HTML,
            'courseid' => $curso->id, 'groupid' => 0, 'userid' => $USER->id, 'modulename' => '0',
            'instance' => 0, 'eventtype' => 'course', 'timestart' => $e['inicio'],
            'timeduration' => $e['duracao_min'] * 60, 'visible' => 1], false);
    }
    registra('eventos do calendário', count($cat['eventos']) . ' eventos de curso');

    cria_curso($g, $cat['curso_vazio']);
}

function parte_oraculo(testing_data_generator $g, array $m): void {
    mtrace('Curso do oráculo de M1.2');
    $o = $m['oraculo'];
    $curso = cria_curso($g, $o['curso']);
    matricula($g, $curso, $o['estudantes'], 'student');
    matricula($g, $curso, [$m['contas']['docente']['username']], 'editingteacher');

    foreach ($o['questionarios'] as $q) {
        cria_questionario($g, $curso, $q);
    }
    foreach ($o['agregacoes'] as $a) {
        cria_categoria_nota($g, $curso, $a);
    }
    foreach ($o['prazos'] as $p) {
        if ($p['tipo'] === 'tarefa') {
            cria_tarefa($g, $curso, $p);
        } else {
            cria_questionario($g, $curso, $p + ['nota_maxima' => 10]);
        }
    }
    grade_regrade_final_grades($curso->id);
}

// ---------------------------------------------------------------------------------------------
\core\session\manager::set_user(get_admin());
$g = gerador();
$transacao = $DB->start_delegated_transaction();
try {
    if (in_array('contas', $massa['partes'])) {
        parte_contas($g, $massa, $massa['senha']);
    }
    if (in_array('catalogo', $massa['partes'])) {
        parte_catalogo($g, $massa);
    }
    if (in_array('oraculo', $massa['partes'])) {
        parte_oraculo($g, $massa);
    }
    $transacao->allow_commit();
} catch (Throwable $e) {
    $resultado['erro'] = $e->getMessage();
    $resultado['criado'] = [];
    grava_resultado();
    fwrite(STDERR, "erro: {$e->getMessage()}\nNada foi gravado (a transação foi desfeita).\n");
    try {
        $transacao->rollback($e);
    } catch (Throwable $ignorado) {
        // rollback() relança a exceção original; o erro já foi registrado acima.
    }
    exit(1);
}
purge_all_caches();
grava_resultado();
mtrace('Massa aplicada: ' . count($resultado['criado']) . ' itens criados, '
    . count($resultado['ignorado']) . ' ignorados.');
