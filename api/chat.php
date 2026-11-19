<?php
/**
 * SUBLIME CI-USA — endpoint du chatbot « Aya ».
 * Activation côté front : USE_API = true dans assets/js/chatbot.js
 *
 * Reçoit  : { "message": "...", "history": [...], "lang": "fr"|"en" }
 * Renvoie : { "reply": "..." }
 *
 * Tel quel, ce fichier renvoie une réponse d'attente : le moteur de
 * règles du navigateur suffit et reste plus rapide. Passe par ici le
 * jour où tu veux une base en MySQL ou un appel à un LLM — dans ce
 * cas la clé API reste ICI, côté serveur, jamais dans le JavaScript.
 */

declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit(json_encode(['error' => 'method']));
}

$in      = json_decode(file_get_contents('php://input'), true) ?: [];
$message = trim((string) ($in['message'] ?? ''));
$lang    = (($in['lang'] ?? 'en') === 'fr') ? 'fr' : 'en';

$len = function_exists('mb_strlen') ? mb_strlen($message) : strlen($message);
if ($message === '' || $len > 800) {
    http_response_code(400);
    exit(json_encode(['error' => 'message']));
}

// --- TODO : moteur de réponse -------------------------------------
// Piste 1 — base MySQL : table `chat_intents` (id, lang, pattern, reply),
//           on parcourt les motifs et on renvoie la première réponse.
// Piste 2 — LLM : appel cURL vers l'API, avec un prompt système qui
//           décrit Aya et la base de connaissances du bureau du tourisme.
// ------------------------------------------------------------------

$reply = $lang === 'fr'
    ? "Je n'ai pas encore la réponse à celle-là. Écrivez à <b>tourism@ambaciusa.org</b>, un collègue vous répondra."
    : "I don't have that one yet. Write to <b>tourism@ambaciusa.org</b> and a colleague will get back to you.";

echo json_encode(['reply' => $reply], JSON_UNESCAPED_UNICODE);
