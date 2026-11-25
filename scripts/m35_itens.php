<?php
// Lista congelada dos 40 itens de verificação de M3.5 (preservação na atualização), issue #71.
// Congelada em 22/11/2026, antes da primeira atualização medida (regra R1), porque o piloto (#66)
// não foi feito. 30 contagens + nota final (total do curso AVAL-CAT) de est01 a est10.
//
// Uso (no servidor, como www-data): php m35_itens.php --moodle=/var/www/<inst> [--recalcular]
//   --recalcular  só ANTES da atualização: calcula as notas finais (o total do curso não é gravado
//                 até o primeiro cálculo). DEPOIS da atualização, lê o valor gravado, sem recalcular.
// Saída: CSV "item,descricao,valor" na saída padrão.
define('CLI_SCRIPT', true);
$o = getopt('', ['moodle:', 'recalcular']);
require(rtrim($o['moodle'], '/') . '/config.php');
require_once($CFG->libdir . '/gradelib.php');
\core\session\manager::set_user(get_admin());

$cat = $DB->get_field('course', 'id', ['shortname' => 'AVAL-CAT'], MUST_EXIST);
$ora = $DB->get_field('course', 'id', ['shortname' => 'AVAL-ORACULO'], MUST_EXIST);
$rest = $DB->get_field('course', 'id', ['shortname' => 'AVAL-REST'], MUST_EXIST);
if (isset($o['recalcular'])) {
    grade_regrade_final_grades($cat);
}
$c = fn($sql, $p = []) => (string) $DB->count_records_sql($sql, $p);
$mod = fn($nome) => $DB->get_field('modules', 'id', ['name' => $nome]);
$itens = [
    ['I01', 'usuários não excluídos', $c("SELECT COUNT(*) FROM {user} WHERE deleted = 0")],
    ['I02', 'usuários com e-mail @example.invalid', $c("SELECT COUNT(*) FROM {user} WHERE deleted = 0 AND email LIKE '%@example.invalid'")],
    ['I03', 'cursos (sem o site)', $c("SELECT COUNT(*) FROM {course} WHERE id <> :s", ['s' => SITEID])],
    ['I04', 'categorias de curso', $c("SELECT COUNT(*) FROM {course_categories}")],
    ['I05', 'matrículas em AVAL-CAT', $c("SELECT COUNT(*) FROM {user_enrolments} ue JOIN {enrol} e ON e.id = ue.enrolid WHERE e.courseid = :c", ['c' => $cat])],
    ['I06', 'matrículas em AVAL-ORACULO', $c("SELECT COUNT(*) FROM {user_enrolments} ue JOIN {enrol} e ON e.id = ue.enrolid WHERE e.courseid = :c", ['c' => $ora])],
    ['I07', 'matrículas em AVAL-REST', $c("SELECT COUNT(*) FROM {user_enrolments} ue JOIN {enrol} e ON e.id = ue.enrolid WHERE e.courseid = :c", ['c' => $rest])],
    ['I08', 'atribuições de papel', $c("SELECT COUNT(*) FROM {role_assignments}")],
    ['I09', 'módulos de atividade em AVAL-CAT', $c("SELECT COUNT(*) FROM {course_modules} WHERE course = :c", ['c' => $cat])],
    ['I10', 'módulos de atividade em AVAL-ORACULO', $c("SELECT COUNT(*) FROM {course_modules} WHERE course = :c", ['c' => $ora])],
    ['I11', 'seções de AVAL-CAT', $c("SELECT COUNT(*) FROM {course_sections} WHERE course = :c", ['c' => $cat])],
    ['I12', 'tarefas (assign)', $c("SELECT COUNT(*) FROM {assign}")],
    ['I13', 'envios de tarefa com status submitted', $c("SELECT COUNT(*) FROM {assign_submission} WHERE status = 'submitted'")],
    ['I14', 'envios de texto online', $c("SELECT COUNT(*) FROM {assignsubmission_onlinetext}")],
    ['I15', 'questionários (quiz)', $c("SELECT COUNT(*) FROM {quiz}")],
    ['I16', 'tentativas de questionário', $c("SELECT COUNT(*) FROM {quiz_attempts}")],
    ['I17', 'questões', $c("SELECT COUNT(*) FROM {question}")],
    ['I18', 'fóruns', $c("SELECT COUNT(*) FROM {forum}")],
    ['I19', 'discussões de fórum', $c("SELECT COUNT(*) FROM {forum_discussions}")],
    ['I20', 'posts de fórum', $c("SELECT COUNT(*) FROM {forum_posts}")],
    ['I21', 'recursos (resource)', $c("SELECT COUNT(*) FROM {resource}")],
    ['I22', 'arquivos de mod_resource (sem diretórios)', $c("SELECT COUNT(*) FROM {files} WHERE component = 'mod_resource' AND filename <> '.'")],
    ['I23', 'arquivos de envio de tarefa (sem diretórios)', $c("SELECT COUNT(*) FROM {files} WHERE component = 'assignsubmission_file' AND filename <> '.'")],
    ['I24', 'itens de nota em AVAL-CAT', $c("SELECT COUNT(*) FROM {grade_items} WHERE courseid = :c", ['c' => $cat])],
    ['I25', 'itens de nota em AVAL-ORACULO', $c("SELECT COUNT(*) FROM {grade_items} WHERE courseid = :c", ['c' => $ora])],
    ['I26', 'categorias de nota em AVAL-ORACULO', $c("SELECT COUNT(*) FROM {grade_categories} WHERE courseid = :c", ['c' => $ora])],
    ['I27', 'notas com finalgrade em itens manuais de AVAL-CAT', $c("SELECT COUNT(*) FROM {grade_grades} g JOIN {grade_items} i ON i.id = g.itemid WHERE i.courseid = :c AND i.itemtype = 'manual' AND g.finalgrade IS NOT NULL", ['c' => $cat])],
    ['I28', 'soma das notas dos itens manuais de AVAL-CAT', (string) round((float) $DB->get_field_sql("SELECT SUM(g.finalgrade) FROM {grade_grades} g JOIN {grade_items} i ON i.id = g.itemid WHERE i.courseid = :c AND i.itemtype = 'manual'", ['c' => $cat]), 5)],
    ['I29', 'eventos de calendário de AVAL-CAT', $c("SELECT COUNT(*) FROM {event} WHERE courseid = :c AND eventtype = 'course'", ['c' => $cat])],
    ['I30', 'módulos de tarefa em AVAL-ORACULO', $c("SELECT COUNT(*) FROM {course_modules} WHERE course = :c AND module = :m", ['c' => $ora, 'm' => $mod('assign')])],
];
$total = $DB->get_record('grade_items', ['courseid' => $cat, 'itemtype' => 'course'], 'id', MUST_EXIST);
for ($i = 1; $i <= 10; $i++) {
    $u = sprintf('est%02d', $i);
    $uid = $DB->get_field('user', 'id', ['username' => $u, 'deleted' => 0]);
    $g = $uid ? $DB->get_field('grade_grades', 'finalgrade', ['itemid' => $total->id, 'userid' => $uid]) : null;
    $itens[] = [sprintf('I%02d', 30 + $i), "nota final de $u em AVAL-CAT", $g === null || $g === false ? 'sem nota' : (string) round((float) $g, 5)];
}
$out = fopen('php://stdout', 'w');
fputcsv($out, ['item', 'descricao', 'valor']);
foreach ($itens as $l) {
    fputcsv($out, $l);
}
