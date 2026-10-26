// 从真正的插件包生成「仓库根目录清单」—— <repoRoot>/package.json。
//
// 为什么需要它：社区自动发现（如 vbarter/dsh-plugin-registry）只读仓库**根目录**
// 的 package.json 来判定 dsh.bundle，而本仓库根是 Python 包（pyproject.toml），
// 插件实现放在 dsh-plugin/qubitclient-panel/。根清单只做两件事：
//   1. 让扫描器在根目录读到 dsh.bundle.patch；
//   2. 让 cordis.patch.yml 里 insert 的 name（qubitclient-dsh-panel）能被解析到，
//      并把 exports 转发到子目录里的真实实现。
// 它不是第二份事实源：内容全部由子包 package.json 推导，改完子包重跑本脚本即可。
//
// 用法（仓库任意目录）：
//   node dsh-plugin/scripts/sync-root-manifest.mjs          # 写入/刷新根 package.json
//   node dsh-plugin/scripts/sync-root-manifest.mjs --check   # 只校验是否漂移，漂移则 exit 1
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const pluginDir = path.resolve(here, '..', 'qubitclient-panel')
const repoRoot = path.resolve(here, '..', '..')
const rootManifestPath = path.join(repoRoot, 'package.json')

const checkOnly = process.argv.slice(2).includes('--check')

/** 把子包里的相对路径改写成「从仓库根出发」的相对路径。 */
const fromRoot = (relative) => {
  const joined = path.posix.normalize(
    path.posix.join(path.relative(repoRoot, pluginDir).split(path.sep).join('/'), relative),
  )
  return joined.startsWith('.') ? joined : `./${joined}`
}

const pluginPkg = JSON.parse(fs.readFileSync(path.join(pluginDir, 'package.json'), 'utf8'))

// 只转发 exports 里存在的条目；子包里没有的就不在根清单里凭空造。
const exports = {}
for (const [subpath, target] of Object.entries(pluginPkg.exports ?? {})) {
  exports[subpath] = fromRoot(target)
}
if (Object.keys(exports).length === 0) {
  throw new Error('子包 package.json 没有 exports，无法推导根清单入口')
}

const patch = pluginPkg.dsh?.bundle?.patch
if (!patch) throw new Error('子包 package.json 缺少 dsh.bundle.patch')
const client = pluginPkg.dsh?.client

const manifest = {
  name: pluginPkg.name,
  version: pluginPkg.version,
  description: pluginPkg.description,
  type: pluginPkg.type,
  license: 'GPL-3.0',
  author: 'Yaqiang Sun <sunyaking@163.com>',
  keywords: ['dsh-plugin', 'deepseek-harness', 'quantum-computing', 'pipeline', 'results'],
  repository: {
    type: 'git',
    url: 'git+https://github.com/yaqiangsun/QubitClient.git',
    directory: path.relative(repoRoot, pluginDir).split(path.sep).join('/'),
  },
  publishConfig: { access: 'public' },
  main: exports['.'],
  exports,
  files: [path.relative(repoRoot, pluginDir).split(path.sep).join('/')],
  dsh: {
    bundle: { patch: fromRoot(patch) },
    ...(client ? { client } : {}),
  },
}

const text = `${JSON.stringify(manifest, null, 2)}\n`
const current = fs.existsSync(rootManifestPath) ? fs.readFileSync(rootManifestPath, 'utf8') : ''

if (checkOnly) {
  if (current === text) {
    console.log('根清单与子包一致 ✅')
    process.exit(0)
  }
  console.log('根清单与子包不一致 ❌')
  if (!current) {
    console.log('  根 package.json 不存在')
  } else {
    const want = text.split('\n')
    const have = current.split('\n')
    for (let i = 0; i < Math.max(want.length, have.length); i += 1) {
      if (want[i] !== have[i]) console.log(`  第 ${i + 1} 行: 期望 ${JSON.stringify(want[i])} 实际 ${JSON.stringify(have[i])}`)
    }
  }
  console.log('\n修复: node dsh-plugin/scripts/sync-root-manifest.mjs')
  process.exit(1)
}

fs.writeFileSync(rootManifestPath, text, 'utf8')
console.log(`已写入 ${path.relative(process.cwd(), rootManifestPath) || rootManifestPath}`)
console.log(`  name   : ${manifest.name}@${manifest.version}`)
console.log(`  main   : ${manifest.main}`)
console.log(`  patch  : ${manifest.dsh.bundle.patch}`)
console.log(`  子包   : ${path.relative(repoRoot, pluginDir).split(path.sep).join('/')}`)
