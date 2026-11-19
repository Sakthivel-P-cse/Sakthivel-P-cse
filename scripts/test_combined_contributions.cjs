const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const source = fs.readFileSync('.github/actions/profile-cards/dist/index.js', 'utf8');
const merge = source.match(/function combineAccountDays\(first, second\) \{[\s\S]*?\n\}/)[0];
const streaks = source.slice(source.indexOf('const DAY_MS ='), source.indexOf('// src/fonts.generated.ts'));
const { combineAccountDays, computeStreaks } = vm.runInNewContext(`${merge}\n${streaks}\n({ combineAccountDays, computeStreaks })`);
const days = combineAccountDays(
  [{ date: '2026-11-17', count: 2, level: 1 }, { date: '2026-11-19', count: 0, level: 0 }],
  [{ date: '2026-11-17', count: 3, level: 2 }, { date: '2026-11-18', count: 1, level: 1 }],
);
assert.equal(days.map((day) => day.count).join(','), '5,1,0');
assert.equal(days[0].level, 2);
assert.equal(computeStreaks(days).current, 2);
assert.equal(computeStreaks(days).longest, 2);
console.log('Combined contribution counts and streaks pass');
