// 生成 DSH 插件市场索引（format 1）—— dsh-plugin/market-index.json。
//
// 用途：把本仓库的 dsh-plugin/qubitclient-panel 发布成一个「可被添加为索引源」的市场条目。
// 索引固定到当前 git commit，因此任何人添加这个索引 URL 后装到的都是同一份代码。
// 每次发版/推送后重跑一次即可刷新索引。
//
// 用法（仓库任意目录）：
//   node dsh-plugin/scripts/make-market-index.mjs
//   node dsh-plugin/scripts/make-market-index.mjs --repo https://github.com/<you>/<repo>
//
// 校验：DSH 侧「插件 → 发现 → 添加索引源」会用它自己的 format 1 校验器解析；
// 本脚本只保证形状完整，不重新实现官方规则。
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const pluginDir = path.resolve(here, '..', 'qubitclient-panel')
const repoRoot = path.resolve(here, '..', '..')
const outPath = path.resolve(here, '..', 'market-index.json')

const argv = process.argv.slice(2)
const arg = (name, fallback) => {
  const index = argv.indexOf(`--${name}`)
  return index >= 0 && argv[index + 1] ? argv[index + 1] : fallback
}

const repositoryUrl = arg('repo', 'https://github.com/yaqiangsun/QubitClient').replace(/\.git$/, '')
const relativePath = path.relative(repoRoot, pluginDir).split(path.sep).join('/')

const git = (...args) => execFileSync('git', ['-C', repoRoot, ...args], { encoding: 'utf8' }).trim()
const commit = git('rev-parse', 'HEAD')
const publishTimestamp = Number(git('log', '-1', '--format=%ct'))
if (!/^[0-9a-f]{40}$/u.test(commit)) throw new Error(`git HEAD 不是完整 commit sha: ${commit}`)
if (!Number.isInteger(publishTimestamp) || publishTimestamp <= 0) throw new Error('拿不到提交时间')

const pkg = JSON.parse(fs.readFileSync(path.join(pluginDir, 'package.json'), 'utf8'))
const zh = JSON.parse(fs.readFileSync(path.join(pluginDir, 'locale', 'zh.json'), 'utf8'))
const en = JSON.parse(fs.readFileSync(path.join(pluginDir, 'locale', 'en.json'), 'utf8'))
const iconSvg = fs.readFileSync(path.join(pluginDir, 'icon.svg'))
const icon = `data:image/svg+xml;base64,${iconSvg.toString('base64')}`

const index = {
  format: 1,
  title: { en: 'QubitClient DSH plugins', zh: 'QubitClient DSH 插件' },
  description: {
    en: 'Plugins that bring QubitClient pipeline results into DeepSeek Harness.',
    zh: '把 QubitClient 的 pipeline 结果接进 DeepSeek Harness 的插件。',
  },
  plugins: [
    {
      name: pkg.name,
      title: { en: en.meta.title, zh: zh.meta.title },
      description: { en: en.meta.description, zh: zh.meta.description },
      icon,
      author: 'yaqiangsun',
      homepage: `${repositoryUrl}/tree/main/${relativePath}`,
      repository: { url: repositoryUrl, directory: relativePath },
      metadata: {
        keywords: ['dsh-plugin', 'deepseek-harness', 'quantum-computing', 'pipeline', 'results'],
      },
      versions: [
        {
          version: pkg.version,
          publishTimestamp,
          source: {
            type: 'git',
            url: repositoryUrl,
            commit,
            path: relativePath,
          },
        },
      ],
    },
  ],
}

fs.writeFileSync(outPath, `${JSON.stringify(index, null, 2)}\n`, 'utf8')
console.log(`已写入 ${path.relative(process.cwd(), outPath) || outPath}`)
console.log(`  plugin : ${pkg.name}@${pkg.version}`)
console.log(`  source : git ${repositoryUrl}#${commit} path:/${relativePath}`)
console.log(`  时间戳 : ${publishTimestamp}`)
