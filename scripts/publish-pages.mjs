import { execFileSync } from 'node:child_process';
import { cpSync, existsSync, mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

// Run only after committing/pushing source and building: node scripts/publish-pages.mjs owner/repository
const repository=process.argv[2];
if(!repository||! /^[\w.-]+\/[\w.-]+$/.test(repository)) throw new Error('Expected owner/repository');
if(!existsSync('dist/index.html')) throw new Error('Run npm run build first');
const run=(cmd,args,cwd=process.cwd())=>execFileSync(cmd,args,{cwd,encoding:'utf8',stdio:['ignore','pipe','inherit']}).trim();
const directory=mkdtempSync(join(tmpdir(),'newjeans-pages-'));
try {
 cpSync(resolve('dist'),directory,{recursive:true});
 writeFileSync(join(directory,'.nojekyll'),'');
 const sha=run('git',['rev-parse','HEAD']);
 writeFileSync(join(directory,'build.json'),JSON.stringify({source:sha,builtAt:new Date().toISOString()},null,2));
 run('git',['init','-b','gh-pages'],directory);
 run('git',['add','.'],directory);
 run('git',['commit','-m',`Deploy ${sha.slice(0,7)}`],directory);
 run('git',['remote','add','origin',`https://github.com/${repository}.git`],directory);
 run('git',['push','--force','origin','gh-pages'],directory);
 console.log(`Published build ${sha.slice(0,7)} to ${repository}:gh-pages`);
} finally { rmSync(directory,{recursive:true,force:true}); }
