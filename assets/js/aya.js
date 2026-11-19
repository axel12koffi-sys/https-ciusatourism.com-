/* ============================================================
   SUBLIME CI-USA — aya.js
   Personnage animé « Aya », en SVG 2D avec un petit rig.

   Pourquoi du SVG et pas de la 3D ni du Lottie :
   le fichier pèse ~6 ko, il se colorise avec les variables CSS
   du site, il reste net sur tous les écrans, et il n'ajoute
   aucune dépendance. Une scène three.js pour le même résultat
   coûterait 600 ko et poserait un vrai problème sur mobile.

   États disponibles : idle · wave · think · talk · happy
   API : Aya.set('wave')          → état ponctuel puis retour idle
         Aya.set('think', true)   → état maintenu
         Aya.idle()               → retour au repos

   Le rig est injecté dans tout élément portant [data-aya].
   ============================================================ */
(function () {
  'use strict';

  var uid = 0;

  function rig() {
    var i = ++uid, clip = 'ayaClip' + i, grad = 'ayaBg' + i;
    return '' +
'<svg class="aya" viewBox="0 0 120 120" data-state="idle" aria-hidden="true">' +
  '<defs>' +
    '<clipPath id="' + clip + '"><circle cx="60" cy="60" r="60"/></clipPath>' +
    '<linearGradient id="' + grad + '" x1="0" y1="0" x2="1" y2="1">' +
      '<stop offset="0" stop-color="#FF9A2E"/><stop offset="1" stop-color="#E86F00"/>' +
    '</linearGradient>' +
  '</defs>' +
  '<g clip-path="url(#' + clip + ')">' +
    '<rect width="120" height="120" fill="url(#' + grad + ')"/>' +
    '<circle cx="60" cy="66" r="46" fill="#fff" opacity=".10"/>' +

    /* bulles de réflexion */
    '<g class="aya-bubbles" fill="#fff">' +
      '<circle cx="20" cy="40" r="2.6"/><circle cx="14" cy="30" r="3.6"/><circle cx="19" cy="18" r="5.4"/>' +
    '</g>' +

    '<g class="aya-body">' +
      /* buste */
      '<path class="aya-torso" d="M20 120C22 96 38 84 60 84s38 12 40 36z" fill="#0A3161"/>' +
      '<path d="M52 86c2 5 4.4 7.5 8 7.5S66 91 68 86c-2.6-1.3-5.3-2-8-2s-5.4.7-8 2z" fill="#F5F7FA" opacity=".9"/>' +
      /* bras (pivote à l'épaule) */
      '<g class="aya-arm">' +
        '<path d="M86 100C94 95 100 86 100 74" stroke="#8B5A34" stroke-width="11" stroke-linecap="round" fill="none"/>' +
        '<g class="aya-hand">' +
          '<circle cx="100" cy="66" r="8.6" fill="#96613A"/>' +
          '<path d="M96 60.5v-5M100 59.6v-6M104 60.5v-4.6" stroke="#96613A" stroke-width="3.1" stroke-linecap="round"/>' +
        '</g>' +
      '</g>' +
      /* cou */
      '<path d="M53 68h14v14a7 7 0 0 1-14 0z" fill="#77492A"/>' +
      /* tête */
      '<g class="aya-head">' +
        '<circle cx="38.5" cy="52" r="4" fill="#8B5A34"/><circle cx="81.5" cy="52" r="4" fill="#8B5A34"/>' +
        '<circle cx="38.5" cy="59" r="3.1" fill="#F77F00"/><circle cx="81.5" cy="59" r="3.1" fill="#F77F00"/>' +
        '<ellipse cx="60" cy="49" rx="20" ry="23" fill="#8B5A34"/>' +
        /* foulard */
        '<path d="M39 47c0-19 9-30 21-30s21 11 21 30c-4-12-11-17-21-17s-17 5-21 17z" fill="#009E60"/>' +
        '<path d="M78 22c5-4 10-3 11 1s-3 8-8 7-5-6-3-8z" fill="#00B26C"/>' +
        '<path d="M41 40c3-9 9-13 19-13s16 4 19 13" stroke="#00B26C" stroke-width="2" fill="none" opacity=".7"/>' +
        /* sourcils */
        '<path class="aya-brow" d="M45 41.5c2.4-1.7 5.6-1.7 8 0M67 41.5c2.4-1.7 5.6-1.7 8 0" stroke="#3A2214" stroke-width="2.2" stroke-linecap="round" fill="none"/>' +
        /* yeux */
        '<g class="aya-eyes">' +
          '<ellipse cx="49" cy="49" rx="3.2" ry="3.8" fill="#1A1008"/>' +
          '<ellipse cx="71" cy="49" rx="3.2" ry="3.8" fill="#1A1008"/>' +
          '<circle cx="50.2" cy="47.6" r="1.1" fill="#fff"/><circle cx="72.2" cy="47.6" r="1.1" fill="#fff"/>' +
        '</g>' +
        /* nez */
        '<path d="M60 52.5c-1.6 3-2.4 4.6-2.4 5.2 0 .9.9 1.4 2.4 1.4s2.4-.5 2.4-1.4c0-.6-.8-2.2-2.4-5.2z" fill="#77492A" opacity=".65"/>' +
        /* bouche : sourire au repos, ovale animé quand elle parle */
        '<path class="aya-smile" d="M53.5 62.5c2 3.4 4.2 5 6.5 5s4.5-1.6 6.5-5" stroke="#4A2415" stroke-width="2.4" stroke-linecap="round" fill="none"/>' +
        '<ellipse class="aya-mouth" cx="60" cy="64" rx="5.4" ry="3.4" fill="#4A2415"/>' +
      '</g>' +
    '</g>' +
  '</g>' +
'</svg>';
  }

  var nodes = [];
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revert = null;

  function mount() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-aya]'), function (host) {
      if (host.dataset.ayaReady) return;
      host.innerHTML = rig();
      host.dataset.ayaReady = '1';
      nodes.push(host.firstChild);
    });
  }

  var DURATION = { wave: 2100, talk: 0, think: 0, happy: 1400 };

  function set(state, hold) {
    clearTimeout(revert);
    nodes.forEach(function (n) { n.setAttribute('data-state', state); });
    if (reduce) return;
    var d = DURATION[state];
    if (!hold && d) revert = setTimeout(idle, d);
  }
  function idle() {
    clearTimeout(revert);
    nodes.forEach(function (n) { n.setAttribute('data-state', 'idle'); });
  }

  /* clignement des yeux, à intervalle irrégulier */
  function blink() {
    if (reduce) return;
    nodes.forEach(function (n) { n.classList.add('is-blink'); });
    setTimeout(function () {
      nodes.forEach(function (n) { n.classList.remove('is-blink'); });
    }, 130);
    setTimeout(blink, 2600 + Math.random() * 4200);
  }

  /* le bouton flottant fait coucou de temps en temps, tant que
     personne n'a ouvert la conversation */
  var greeted = false;
  function attract() {
    if (greeted || reduce) return;
    if (!document.hidden && !document.querySelector('#chatPanel.on')) set('wave');
    setTimeout(attract, 14000);
  }

  mount();
  blink();
  setTimeout(attract, 5000);

  window.Aya = {
    set: set,
    idle: idle,
    mount: mount,
    stopAttract: function () { greeted = true; }
  };
})();
