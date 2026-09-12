const bl = require('../../reference/bullet-library.json');
const arch = bl['Entrepreneur'];
console.log('--- EXPERIENCE BULLETS ---');
arch.EXPERIENCE.forEach(e => {
  console.log('Exp:', e.id);
  e.bullets.forEach((b, i) => {
    const plain = b.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/\*\*/g, '');
    const len = plain.length;
    const ok = (len >= 95 && len <= 115) || (len >= 180 && len <= 230);
    console.log('  [' + (i+1) + '] len=' + len + ' (ok=' + ok + '): ' + plain);
  });
});
console.log('--- PROJECTS BULLETS ---');
arch.PROJECTS.forEach(p => {
  console.log('Proj:', p.id);
  p.bullets.forEach((b, i) => {
    const plain = b.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/\*\*/g, '');
    const len = plain.length;
    const ok = (len >= 95 && len <= 115) || (len >= 180 && len <= 230);
    console.log('  [' + (i+1) + '] len=' + len + ' (ok=' + ok + '): ' + plain);
  });
});
