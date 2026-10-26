// 不安装、不重启就能做的插件自检。
//
// 用法（在仓库根目录）：
//   node dsh-plugin/scripts/check-plugin.mjs
//   node dsh-plugin/scripts/check-plugin.mjs dsh-plugin/qubitclient-panel
//
// 检查项：
//   1. package.json 必备字段 / exports 指向的文件存在 / locale 是合法 JSON；
//   2. cordis.patch.yml 是 - insert: [{id, name, config}] 形状，且 name 与包名一致；
//   3. Host 半 import 后能拿到 apply()，在假 ctx 里跑一遍，工具形状完整，
//      execute() 能正确解析 /api/runs（用假 fetch，不真的联网）；
//   4. Client 半能在假 window 里完成一次插槽注册：tab 类型 id/kind/guide/key 一致，
//      输入框徽标的「打开面板」按钮确实调用 ctx.sidebarRight.openTab(kind, {params})；
//   5. 两侧组件的函数式渲染不抛错（假 React，只验证不炸）。
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath, pathToFileURL } from 'node:url'

const here = path.dirname(fileURLToPath(import.meta.url))
const pkgDir = path.resolve(process.argv[2] ?? path.join(here, '..', 'qubitclient-panel'))
const fail = []
const ok = (msg) => console.log(`  ok   ${msg}`)
const bad = (msg) => {
  fail.push(msg)
  console.log(`  FAIL ${msg}`)
}

console.log(`检查插件目录: ${pkgDir}\n`)

// ---- 1. 清单 -------------------------------------------------------------
console.log('[1/5] package.json')
const manifest = JSON.parse(fs.readFileSync(path.join(pkgDir, 'package.json'), 'utf8'))
for (const key of ['name', 'version', 'type', 'exports']) {
  manifest[key] ? ok(`有 ${key}`) : bad(`缺少 ${key}`)
}
manifest.type === 'module' ? ok('type = module') : bad('type 应为 module')
const bundle = manifest.dsh?.bundle?.patch
bundle ? ok(`bundle patch: ${bundle}`) : bad('缺少 dsh.bundle.patch')
const client = manifest.dsh?.client
client ? ok(`client 半: platform=${client.platform}`) : bad('缺少 dsh.client')
if (client) {
  Array.isArray(client.inject) && client.inject.length > 0
    ? ok(`dsh.client.inject: ${client.inject.join(', ')}`)
    : bad('dsh.client.inject 应为非空数组（排序用）')
}

// ---- 2. exports / patch ------------------------------------------------
console.log('\n[2/5] exports 与 patch')
for (const [subpath, target] of Object.entries(manifest.exports ?? {})) {
  if (subpath.includes('*')) continue
  const abs = path.join(pkgDir, target)
  fs.existsSync(abs) ? ok(`export ${subpath} -> ${target}`) : bad(`export ${subpath} -> ${target} 不存在`)
}
if (bundle) {
  const patchPath = path.join(pkgDir, bundle)
  fs.existsSync(patchPath) ? ok(`patch 文件存在: ${bundle}`) : bad(`patch 文件不存在: ${bundle}`)
  const text = fs.existsSync(patchPath) ? fs.readFileSync(patchPath, 'utf8') : ''
  const hasInsert = /^\s*-\s*insert:/m.test(text)
  const hasId = /^\s+-\s+id:\s*\S+/m.test(text)
  const hasName = new RegExp(`^\\s+name:\\s*'?${manifest.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}'?\\s*$`, 'm').test(text)
  hasInsert && hasId && hasName
    ? ok('patch 是 - insert: [{id, name: <包名>}] 形状')
    : bad('patch 形状不对，或 name 与包名不一致')
  const hasBaseUrl = /^\s+baseUrl:/m.test(text)
  hasBaseUrl ? ok('patch 带 config.baseUrl（Host 工具用）') : bad('patch 缺少 config.baseUrl')
}

// ---- 3. locale ----------------------------------------------------------
console.log('\n[3/5] locale')
// locale 目录可能在子目录里（根目录清单只转发 exports），因此从 exports 推导。
const localeExport = manifest.exports?.['./locale/*.json']
const localeDir = localeExport
  ? path.join(pkgDir, localeExport.slice(0, localeExport.indexOf('*')))
  : path.join(pkgDir, 'locale')
if (fs.existsSync(localeDir)) {
  for (const file of fs.readdirSync(localeDir).filter((f) => f.endsWith('.json'))) {
    const doc = JSON.parse(fs.readFileSync(path.join(localeDir, file), 'utf8'))
    doc.meta?.title && doc.meta?.description
      ? ok(`locale/${file} 有 meta.title / meta.description`)
      : bad(`locale/${file} 缺少 meta.title 或 meta.description`)
  }
} else {
  bad('缺少 locale/ 目录（插件列表会退回包名和默认图标）')
}

// ---- 4. Host 半 ---------------------------------------------------------
console.log('\n[4/5] Host 半')
const hostModule = await import(
  pathToFileURL(path.join(pkgDir, manifest.exports['.'] ?? './index.js')).href
)
typeof hostModule.apply === 'function' ? ok('导出 apply(ctx, config)') : bad('没有导出 apply(ctx, config)')
Array.isArray(hostModule.inject) ? ok(`inject: ${hostModule.inject.join(', ')}`) : bad('没有声明 inject')

const registered = []
const fakeCtx = {
  tools: { register: (def) => registered.push(def) },
  effect: (fn) => fn(),
  on: () => () => {},
}
try {
  hostModule.apply(fakeCtx, { baseUrl: 'http://127.0.0.1:8581/' })
  ok(`apply() 执行通过，注册了 ${registered.length} 个工具: ${registered.map((t) => t.name).join(', ') || '(无)'}`)
} catch (error) {
  bad(`apply() 抛错: ${error.message}`)
}

const tool = registered.find((def) => def?.name === 'qubitclient_results')
if (!tool) {
  bad('没有注册 qubitclient_results 工具')
} else {
  tool.description && tool.parameters && tool.output?.render && typeof tool.execute === 'function'
    ? ok('工具形状完整（description/parameters/output.render/execute）')
    : bad('工具形状不完整')
  try {
    const text = tool.output.render([], {
      ok: true,
      baseUrl: 'http://127.0.0.1:8581',
      total: 1,
      runs: [
        {
          id: 'abcdef0123456789',
          taskName: 's21peakmulti',
          taskType: 's21peakmulti_pipeline',
          status: 'completed',
          qubits: ['q0', 'q1'],
          createdAt: '2026-10-23T16:00:00',
          completedAt: '2026-10-23T16:01:00',
          plotCount: 2,
          error: '',
        },
      ],
      error: '',
    })
    text?.[0]?.type === 'text' && String(text[0].text).includes('s21peakmulti')
      ? ok('render 能产出可读文本')
      : bad('render 输出不符合预期')
  } catch (error) {
    bad(`render 抛错: ${error.message}`)
  }

  // 假 fetch：验证 /api/runs 的解析与字段压缩，不真的联网。
  const realFetch = globalThis.fetch
  globalThis.fetch = async (url) => {
    const text = String(url)
    if (!text.includes('/api/runs')) throw new Error(`意外的 URL: ${text}`)
    return {
      ok: true,
      json: async () => ({
        items: [
          {
            id: 'abcdef0123456789',
            task_name: 't1',
            task_type: 't1_pipeline',
            status: 'completed',
            qubits: ['q0'],
            created_at: '2026-10-23T16:00:00',
            completed_at: null,
            plot_paths: ['a.png', 'b.png'],
            error: null,
          },
        ],
        total: 1,
      }),
    }
  }
  try {
    const value = await tool.execute({ limit: 5, taskName: 't1' })
    value.ok === true &&
    value.total === 1 &&
    value.runs[0].taskName === 't1' &&
    value.runs[0].plotCount === 2 &&
    value.runs[0].completedAt === '' &&
    value.baseUrl === 'http://127.0.0.1:8581'
      ? ok('execute() 能解析 /api/runs 并压缩字段')
      : bad(`execute() 返回不符合预期: ${JSON.stringify(value)}`)
  } catch (error) {
    bad(`execute() 抛错: ${error.message}`)
  } finally {
    globalThis.fetch = realFetch
  }
}

// ---- 5. Client 半 -------------------------------------------------------
console.log('\n[5/5] Client 半')
const clientTarget = manifest.dsh?.client ? manifest.exports['./client'] : undefined
if (!clientTarget) {
  bad('没有 client 半入口')
} else {
  const source = fs.readFileSync(path.join(pkgDir, clientTarget), 'utf8')
  const React = {
    createElement: (type, props, ...children) => ({ type, props, children }),
    Fragment: Symbol('Fragment'),
    useState: (initial) => [typeof initial === 'function' ? initial() : initial, () => {}],
    // 挂载期效果立即执行（清理函数丢弃）：这样才能验证「面板挂载 → 徽标改文案」。
    useEffect: (effect) => {
      effect()
    },
    useMemo: (factory) => factory(),
    useCallback: (fn) => fn,
    useRef: (value) => ({ current: value }),
  }
  let loaded
  const window = {
    __ModuleLoader__: {
      load: ({ id, factory }) => {
        loaded = { id, factory }
      },
    },
    localStorage: { getItem: () => null, setItem: () => {} },
    open: () => {},
  }
  const sandbox = {
    window,
    console,
    fetch: async () => ({ ok: false, status: 503, json: async () => ({}) }),
    // 组件里的轮询/延迟只是注册，这里不需要真跑，给空实现避免 "setTimeout is not defined"。
    setTimeout: () => 0,
    clearTimeout: () => {},
    setInterval: () => 0,
    clearInterval: () => {},
  }
  try {
    vm.runInNewContext(source, sandbox, { filename: clientTarget })
  } catch (error) {
    bad(`client.js 求值抛错: ${error.message}`)
  }

  if (!loaded) {
    bad('client.js 没有调用 window.__ModuleLoader__.load')
  } else {
    loaded.id === manifest.name
      ? ok(`client 模块 id 与包名一致: ${loaded.id}`)
      : bad(`client 模块 id (${loaded.id}) 应等于包名 (${manifest.name})`)

    const registrations = []
    const tabTypes = []
    const openCalls = []
    const ctx = {
      slots: {
        inject: (ownerKey, factory) => {
          registrations.push({ ownerKey, entry: factory() })
        },
        register: (options, Component) => ({ options, Component }),
      },
      sidebarRightTabs: {
        register: (definition) => {
          tabTypes.push(definition)
          return () => {}
        },
      },
      sidebarRight: {
        openTab: (kind, options) => openCalls.push({ kind, options }),
      },
      effect: (fn) => fn(),
    }
    let plugin
    try {
      plugin = loaded.factory((name) => {
        if (name === 'react') return React
        throw new Error(`unexpected require(${name})`)
      })
    } catch (error) {
      bad(`factory 抛错: ${error.message}`)
    }
    if (plugin) {
      for (const service of ['slots', 'sidebarRightTabs', 'sidebarRight']) {
        plugin.inject?.includes(service) ? ok(`声明了 inject: ${service}`) : bad(`没有声明 inject: ${service}`)
      }

      const panelBodyProps = {
        useTabInfo: () => ({ sidebar: {}, panel: { id: 'p' }, tab: { navigation: { params: {}, revision: 1 } } }),
      }
      try {
        plugin.apply(ctx)
        ok(`apply() 完成 ${registrations.length} 次插槽注册`)
      } catch (error) {
        bad(`apply() 抛错: ${error.message}`)
      }

      const dock = registrations.find((r) => r.ownerKey === 'conversation.composer.dock')
      dock ? ok(`注册到插槽 conversation.composer.dock（id=${dock.entry.options.id}）`) : bad('没有注册输入框徽标')

      const body = registrations.find((r) => r.ownerKey === 'sidebar.right.pane.tab')
      body ? ok(`注册到插槽 sidebar.right.pane.tab（key=${body.entry.options.key}）`) : bad('没有注册 tab 正文')

      const definition = tabTypes[0]

      // 徽标：面板没打开时显示「打开面板」，点了要真的调用 openTab(kind, {params})
      if (dock) {
        try {
          const tree = dock.entry.Component({})
          const button = findButton(tree, '打开面板')
          if (!button) {
            bad('输入框徽标里找不到「打开面板」按钮（面板未打开时应显示它）')
          } else {
            button.props.onClick()
            const call = openCalls[0]
            call && definition && call.kind === definition.kind && typeof call.options?.params?.url === 'string'
              ? ok(`「打开面板」调用 openTab(${call.kind}, {params:{url:${call.options.params.url}}})`)
              : bad('「打开面板」没有按预期调用 openTab(kind, {params})')
            const text = collectText(tree)
            text.includes('共')
              ? bad('输入框徽标不该显示记录条数（太长）')
              : ok('徽标文案精简（不显示记录条数）')
            text.includes('QubitClient 结果') ? ok('徽标保留插件名') : bad('徽标缺少插件名')
          }
        } catch (error) {
          bad(`输入框徽标渲染/点击抛错: ${error.message}`)
        }
      }

      if (!definition) {
        bad('没有注册右侧栏 tab 类型')
      } else {
        definition.id && definition.kind && typeof definition.title === 'function'
          ? ok(`tab 类型: id=${definition.id} kind=${definition.kind}`)
          : bad('tab 类型缺少 id/kind/title')
        definition.keepMounted === true ? ok('keepMounted = true（切 tab 不重建 iframe）') : bad('建议 keepMounted: true')
        const entry = definition.guide?.[0]
        entry ? ok(`引导页入口: ${entry.id}（order=${entry.order}）`) : bad('没有 guide 入口，用户点不进去')
        entry?.icon && typeof entry.icon === 'function' ? ok('引导页入口带图标组件') : bad('guide.icon 应是组件')
        body && body.entry.options.key === definition.id
          ? ok('sidebar.right.pane.tab 的 key 等于 tab 类型 id')
          : bad('sidebar.right.pane.tab 的 key 必须等于 tab 类型 id')
        // 正文能渲染（假 React）
        try {
          const tree = body?.entry.Component(panelBodyProps)
          tree ? ok('tab 正文可渲染（含 iframe 分支）') : bad('tab 正文返回空')
        } catch (error) {
          bad(`tab 正文渲染抛错: ${error.message}`)
        }
        // 面板挂载之后，徽标不该再喊「打开面板」
        if (dock) {
          try {
            const reopened = findButton(dock.entry.Component({}), '聚焦面板')
            reopened ? ok('面板已挂载 → 徽标改为「聚焦面板」') : bad('面板已挂载但徽标仍显示「打开面板」')
          } catch (error) {
            bad(`徽标二次渲染抛错: ${error.message}`)
          }
        }
      }
    }
  }
}

/** 收集假 React 元素树里的可见文字。 */
function collectText(node) {
  if (node === null || node === undefined) return ''
  if (typeof node === 'string') return node
  if (typeof node !== 'object') return ''
  const children = Array.isArray(node.children) ? node.children : []
  return children.map(collectText).join('')
}

/** 在假 React 元素树里按可见文字找按钮。 */
function findButton(node, label) {  if (!node || typeof node !== 'object') return undefined
  if (node.type === 'button' && node.children) {
    const text = node.children
      .map((child) => (typeof child === 'string' ? child : ''))
      .join('')
    if (text.includes(label)) return node
  }
  for (const child of node.children ?? []) {
    const hit = findButton(child, label)
    if (hit) return hit
  }
  return undefined
}

console.log(fail.length === 0 ? '\n全部检查通过 ✅' : `\n${fail.length} 项未通过 ❌`)
process.exit(fail.length === 0 ? 0 : 1)
