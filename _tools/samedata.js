// Vérifie que des fichiers de contenu traduits ont la même structure : mêmes clés, mêmes tailles, mêmes valeurs non textuelles.
// node samedata.js "NOM1,NOM2,..." data.fr.js data.en.js data.es.js
const fs = require('fs'), vm = require('vm');
const [names, ...files] = process.argv.slice(2);
const load = f => {
  const ctx = { window: {}, console };
  const src = fs.readFileSync(f, 'utf8');
  if (names.startsWith('window.')) { vm.runInNewContext(src, ctx); return { [names.slice(7)]: ctx.window[names.slice(7)] }; }
  return vm.runInNewContext(src + `;({${names}})`, ctx);
};
const [ref, ...others] = files.map(load);
let errs = 0;
const TEXT_OK = new Set(['name', 'aka', 'where', 'label', 'hint', 'tab', 'title', 'lede', 'note', 'priceNote', 'cta', 'desc', 'origin', 'temps', 'conseil']);
function cmp(a, b, path) {
  if (typeof a === 'function' || typeof b === 'function') {
    if (typeof a !== typeof b) { errs++; console.log('type', path); }
    return;
  }
  if (Array.isArray(a)) {
    if (!Array.isArray(b) || a.length !== b.length) { errs++; console.log('taille', path, a.length, b && b.length); return; }
    a.forEach((x, i) => cmp(x, b[i], `${path}[${i}]`));
    return;
  }
  if (a && typeof a === 'object') {
    const ka = Object.keys(a).sort().join(), kb = b && typeof b === 'object' ? Object.keys(b).sort().join() : '';
    if (ka !== kb) { errs++; console.log('clés', path, ka, '≠', kb); return; }
    Object.keys(a).forEach(k => cmp(a[k], b[k], `${path}.${k}`));
    return;
  }
  if (typeof a === 'string' && typeof b === 'string') return; // texte : traduit librement
  if (a !== b) { errs++; console.log('valeur', path, JSON.stringify(a), '≠', JSON.stringify(b)); }
}
others.forEach((o, i) => { Object.keys(ref).forEach(k => cmp(ref[k], o[k], files[i + 1] + ':' + k)); });
// les identifiants ne se traduisent pas
const ID = /(^|\.)(id|img|zone|cut|productId|tag|mode|usages|cat|couleur|unite|ratio|whatsapp|telephone|url|tifinagh)$/;
function ids(a, b, path) {
  if (Array.isArray(a)) return a.forEach((x, i) => ids(x, b[i], `${path}[${i}]`));
  if (a && typeof a === 'object') return Object.keys(a).forEach(k => ids(a[k], b[k], `${path}.${k}`));
  if (typeof a === 'string' && ID.test(path) && !/couleurs\.\w+\.zone$/.test(path) && a !== b) { errs++; console.log('identifiant traduit', path, a, '≠', b); }
}
others.forEach((o, i) => Object.keys(ref).forEach(k => ids(ref[k], o[k], files[i + 1] + ':' + k)));
console.log(errs ? `${errs} écart(s)` : 'structure identique');
process.exit(errs ? 1 : 0);
