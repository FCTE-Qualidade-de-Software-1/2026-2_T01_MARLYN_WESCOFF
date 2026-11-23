<?php
// M2.1/M2.2 (issue #68): passos dos formatos executados no servidor, com as rotinas do próprio Moodle.
// F2 e F3 (exportação do livro de notas) vão pela interface (scripts/m21_notas.js).
//
//   --passo=F1   exporta a lista de usuários importada pelo uploaduser (formato de dados CSV do Moodle)
//   --passo=F4   importa o GIFT de referência no banco de questões do curso AVAL-CAT e exporta em GIFT
//   --passo=F5a  exporta em Moodle XML as questões do banco de AVAL-CAT (referência de F5)
//   --passo=F5b  importa esse XML no banco de AVAL-REST e exporta de novo em Moodle XML
//   --passo=F6   exporta em iCal os eventos do curso AVAL-CAT, pela URL de exportação do calendário
//   --passo=F7   restaura o backup de AVAL-CAT (--arquivo) no curso vazio AVAL-REST
// Uso (como www-data): php m21_formatos.php --moodle=/var/www/m21 --passo=F4 --entrada=ARQ --saida=ARQ
define('CLI_SCRIPT', true);
$o = getopt('', ['moodle:', 'passo:', 'entrada:', 'saida:', 'arquivo:']);
require(rtrim($o['moodle'], '/') . '/config.php');
require_once($CFG->libdir . '/questionlib.php');
require_once($CFG->dirroot . '/question/format.php');
require_once($CFG->dirroot . '/question/format/gift/format.php');
require_once($CFG->dirroot . '/question/format/xml/format.php');
require_once($CFG->dirroot . '/calendar/lib.php');
require_once($CFG->dirroot . '/backup/util/includes/restore_includes.php');
\core\session\manager::set_user(get_admin());
$curso = fn($s) => get_course($GLOBALS['DB']->get_field('course', 'id', ['shortname' => $s], MUST_EXIST));
$info = fn(array $d) => print(json_encode($d, JSON_UNESCAPED_UNICODE) . "\n");

/** Categoria superior do banco de questões compartilhado do curso (na 5.x, uma instância de mod_qbank). */
function categoria_do_banco(stdClass $c): stdClass {
    $banco = \core_question\local\bank\question_bank_helper::get_default_open_instance_system_type($c, true);
    $ctx = context_module::instance($banco->id);
    return question_get_default_category($ctx->id, true);
}

function exporta(string $classe, stdClass $cat, string $saida): int {
    $f = new $classe();
    $f->setCategory($cat);
    $f->setContexts([context::instance_by_id($cat->contextid)]);
    $f->setCattofile(false);
    $f->setContexttofile(false);
    $texto = $f->exportprocess();
    file_put_contents($saida, $texto);
    return substr_count($texto, $classe === 'qformat_xml' ? '<question type=' : '::') - ($classe === 'qformat_xml'
        ? substr_count($texto, '<question type="category">') : 0);
}

function importa(string $classe, stdClass $c, stdClass $cat, string $arquivo): bool {
    $f = new $classe();
    $f->setCategory($cat);
    $f->setContexts([context::instance_by_id($cat->contextid)]);
    $f->setCourse($c);
    $f->setFilename($arquivo);
    $f->setRealfilename(basename($arquivo));
    $f->setMatchgrades('error');
    $f->setCatfromfile(false);
    $f->setContextfromfile(false);
    $f->setStoponerror(true);
    ob_start();
    $ok = $f->importpreprocess() && $f->importprocess() && $f->importpostprocess();
    $GLOBALS['log_importacao'] = trim(strip_tags(ob_get_clean()));
    return (bool) $ok;
}

switch ($o['passo']) {
    case 'F1':
        $us = $DB->get_records_select('user', "username LIKE 'est%' AND deleted = 0", null, 'username',
            'id, username, firstname, lastname, email, idnumber');
        // Mesmas colunas da exportação em massa de usuários; o CSV é escrito direto (o gravador de dados do
        // Moodle recusou a pasta de saída na CLI).
        $fh = fopen($o['saida'], 'w');
        fputcsv($fh, ['username', 'firstname', 'lastname', 'email', 'idnumber']);
        foreach ($us as $u) {
            fputcsv($fh, [$u->username, $u->firstname, $u->lastname, $u->email, $u->idnumber]);
        }
        fclose($fh);
        $info(['passo' => 'F1', 'exportados' => count($us)]);
        break;
    case 'F4':
        $c = $curso('AVAL-CAT');
        $cat = categoria_do_banco($c);
        $ok = importa('qformat_gift', $c, $cat, $o['entrada']);
        $n = $DB->count_records_sql('SELECT COUNT(*) FROM {question_bank_entries} WHERE questioncategoryid = ?', [$cat->id]);
        $exp = $ok ? exporta('qformat_gift', $cat, $o['saida']) : 0;
        $info(['passo' => 'F4', 'importou' => $ok, 'questoes_no_banco' => $n, 'log' => mb_substr($GLOBALS['log_importacao'], -300)]);
        break;
    case 'F5a':
        $cat = categoria_do_banco($curso('AVAL-CAT'));
        $info(['passo' => 'F5a', 'exportadas' => exporta('qformat_xml', $cat, $o['saida'])]);
        break;
    case 'F5b':
        $c = $curso('AVAL-REST');
        $cat = categoria_do_banco($c);
        $ok = importa('qformat_xml', $c, $cat, $o['entrada']);
        $info(['passo' => 'F5b', 'importou' => $ok, 'exportadas' => $ok ? exporta('qformat_xml', $cat, $o['saida']) : 0,
            'log' => mb_substr($GLOBALS['log_importacao'], -300)]);
        break;
    case 'F6':
        $doc = $DB->get_record('user', ['username' => 'docente01'], '*', MUST_EXIST);
        $url = new moodle_url('/calendar/export_execute.php', ['userid' => $doc->id,
            'authtoken' => calendar_get_export_token($doc), 'preset_what' => 'courses', 'preset_time' => 'custom']);
        $info(['passo' => 'F6', 'url' => $url->out(false)]);
        break;
    case 'F7':
        $c = $curso('AVAL-REST');
        $pasta = 'm21_' . random_string(8);
        get_file_packer('application/vnd.moodle.backup')->extract_to_pathname($o['arquivo'], make_backup_temp_directory($pasta));
        $rc = new restore_controller($pasta, $c->id, backup::INTERACTIVE_NO, backup::MODE_GENERAL, get_admin()->id,
            backup::TARGET_EXISTING_ADDING);
        $ok = $rc->execute_precheck();
        $rc->execute_plan();
        $rc->destroy();
        $info(['passo' => 'F7', 'precheck' => $ok, 'atividades_restauradas' => $DB->count_records('course_modules', ['course' => $c->id])]);
        break;
}
