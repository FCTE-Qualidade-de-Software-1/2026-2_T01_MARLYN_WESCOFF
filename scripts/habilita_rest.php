<?php
// Habilita os serviços web REST para M2.3 (issue #69), pela API do próprio Moodle.
//
// Cria, se ainda não existirem: o serviço externo "aval_integracao" com as 6 funções da Fase 2, o
// usuário "integracao", o papel "aval_integracao" (contexto de sistema, só com as capacidades de
// leitura que as 6 funções exigem) e um token permanente. Imprime só o token na saída padrão, para
// que quem chamou o guarde fora do repositório. O token nunca é versionado.
//
// Uso (no servidor, como www-data):
//   sudo -u www-data php8.3 scripts/habilita_rest.php --moodle=/var/www/m53php83

define('CLI_SCRIPT', true);

$opcoes = getopt('', ['moodle:']);
if (empty($opcoes['moodle'])) {
    fwrite(STDERR, "uso: php habilita_rest.php --moodle=/var/www/<instancia>\n");
    exit(1);
}
require(rtrim($opcoes['moodle'], '/') . '/config.php');
require_once($CFG->dirroot . '/user/lib.php');

\core\session\manager::set_user(get_admin());

$funcoes = [
    'core_webservice_get_site_info',
    'core_user_get_users_by_field',
    'core_course_get_courses_by_field',
    'core_enrol_get_enrolled_users',
    'mod_assign_get_assignments',
    'gradereport_user_get_grade_items',
];
$capacidades = [
    'webservice/rest:use',
    'moodle/user:viewdetails',
    'moodle/user:viewalldetails',
    'moodle/user:viewhiddendetails',
    'moodle/site:viewuseridentity',  // e-mail de outros usuários (ajuste após a tentativa 1)
    'moodle/course:view',
    'moodle/course:viewparticipants',
    'moodle/site:accessallgroups',
    'mod/assign:view',
    'gradereport/user:view',
    'moodle/grade:viewall',
];

set_config('enablewebservices', 1);
set_config('webserviceprotocols', 'rest');

$servico = $DB->get_record('external_services', ['shortname' => 'aval_integracao']);
if (!$servico) {
    $id = $DB->insert_record('external_services', (object) [
        'name' => 'Integração da avaliação (M2.3)', 'shortname' => 'aval_integracao', 'enabled' => 1,
        'restrictedusers' => 1, 'downloadfiles' => 0, 'uploadfiles' => 0,
        'timecreated' => time(), 'timemodified' => time(),
    ]);
    $servico = $DB->get_record('external_services', ['id' => $id]);
}
foreach ($funcoes as $f) {
    $chave = ['externalserviceid' => $servico->id, 'functionname' => $f];
    if (!$DB->record_exists('external_services_functions', $chave)) {
        $DB->insert_record('external_services_functions', (object) $chave);
    }
}

$usuario = $DB->get_record('user', ['username' => 'integracao', 'deleted' => 0]);
if (!$usuario) {
    $uid = user_create_user((object) [
        'username' => 'integracao', 'password' => random_string(24) . 'Aa1!', 'auth' => 'manual',
        'firstname' => 'Sistema', 'lastname' => 'Integração', 'email' => 'integracao@example.invalid',
        'confirmed' => 1, 'mnethostid' => $CFG->mnet_localhost_id,
    ]);
    $usuario = $DB->get_record('user', ['id' => $uid]);
}

$sistema = context_system::instance();
$papel = $DB->get_field('role', 'id', ['shortname' => 'aval_integracao']);
if (!$papel) {
    $papel = create_role('Integração (M2.3)', 'aval_integracao', 'Usuário de integração da avaliação');
    set_role_contextlevels($papel, [CONTEXT_SYSTEM]);
}
foreach ($capacidades as $c) {
    assign_capability($c, CAP_ALLOW, $papel, $sistema->id, true);
}
if (!user_has_role_assignment($usuario->id, $papel, $sistema->id)) {
    role_assign($papel, $usuario->id, $sistema->id);
}
$chave = ['externalserviceid' => $servico->id, 'userid' => $usuario->id];
if (!$DB->record_exists('external_services_users', $chave)) {
    $DB->insert_record('external_services_users', (object) ($chave + ['timecreated' => time()]));
}

$permanente = defined('EXTERNAL_TOKEN_PERMANENT') ? EXTERNAL_TOKEN_PERMANENT : 0;
$token = \core_external\util::generate_token($permanente, $servico, $usuario->id, $sistema);
echo $token, "\n";
