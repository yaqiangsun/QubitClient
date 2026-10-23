/**
 * Host 半：跑在 DSH 主机进程里，负责「能力」。
 *
 * 这里只做一件事：注册 qubitclient_results 工具，让模型能直接读到
 * QubitClient 结果页服务（qubitclient ui start，默认 http://127.0.0.1:8581）
 * 里的 pipeline 运行记录——不用截图、不用让用户人肉抄。
 *
 * 结果页本身的展示由 Client 半（client.js）负责：右侧栏「QubitClient 结果」tab
 * 里是一个指向该服务的 iframe。Host 与 Client 各自独立，互不依赖。
 *
 * 刻意不 import 任何 @deepseek-ai/* 包：零依赖 → 不会被「插件与 dsh 版本不兼容」
 * 拦下，也不用管 peer 版本。
 */

export const name = 'qubitclient-panel'

// 插件级依赖注入：没有 tools 服务的 profile 里静默不激活，而不是抛错。
export const inject = ['tools']

const DEFAULT_BASE_URL = 'http://127.0.0.1:8581'
const REQUEST_TIMEOUT_MS = 5000

/** 去掉结尾斜杠，允许配置里写带/不带斜杠两种形式。 */
function normalizeBaseUrl(value) {
  const raw = typeof value === 'string' && value.trim() !== '' ? value.trim() : DEFAULT_BASE_URL
  return raw.replace(/\/+$/, '')
}

/** 把一条 pipeline 记录压缩成模型够用、又不至于塞满上下文的摘要。 */
function summarizeRun(record) {
  const run = record && typeof record === 'object' ? record : {}
  return {
    id: typeof run.id === 'string' ? run.id : '',
    taskName: typeof run.task_name === 'string' ? run.task_name : '',
    taskType: typeof run.task_type === 'string' ? run.task_type : '',
    status: typeof run.status === 'string' ? run.status : '',
    qubits: Array.isArray(run.qubits) ? run.qubits.map(String) : [],
    createdAt: typeof run.created_at === 'string' ? run.created_at : '',
    completedAt: typeof run.completed_at === 'string' ? run.completed_at : '',
    plotCount: Array.isArray(run.plot_paths) ? run.plot_paths.length : 0,
    error: typeof run.error === 'string' ? run.error : '',
  }
}

/**
 * 读取 /api/runs。这是 qubitclient/ui/server.py 里已有的列表接口，
 * 返回 { items, total, limit, offset }。
 */
async function fetchRuns(baseUrl, { taskName, limit, timeoutMs }) {
  const url = new URL(`${baseUrl}/api/runs`)
  url.searchParams.set('limit', String(limit))
  if (taskName) url.searchParams.set('task_name', taskName)

  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)
  try {
    const response = await fetch(url, {
      signal: controller.signal,
      headers: { accept: 'application/json' },
    })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const body = await response.json()
    return {
      items: Array.isArray(body?.items) ? body.items : [],
      total: typeof body?.total === 'number' ? body.total : 0,
    }
  } finally {
    clearTimeout(timer)
  }
}

/** 按配置生成模型看到的工具定义（baseUrl 闭包进 execute，避免模块级可变状态）。 */
function createResultsTool(baseUrl) {
  return {
    name: 'qubitclient_results',
    description:
      'Read recent pipeline run records from the local QubitClient result service ' +
      '(started with `qubitclient ui start`, default http://127.0.0.1:8581). ' +
      'Returns task name, status, qubits, timestamps, plot count and error for each run. ' +
      'Use it to check whether a calibration pipeline finished and what it produced; ' +
      'the same data is visible to the user in the right sidebar tab "QubitClient 结果".',
    parameters: {
      type: 'object',
      properties: {
        taskName: {
          type: 'string',
          description:
            'Only return runs of this pipeline task, e.g. "s21peakmulti" or "t1". Omit to return all tasks.',
        },
        limit: {
          type: 'integer',
          description: 'Maximum number of runs to return (1-50, default 10, newest first).',
        },
      },
      required: [],
      additionalProperties: false,
    },
    output: {
      schema: {
        type: 'object',
        properties: {
          ok: { type: 'boolean' },
          baseUrl: { type: 'string' },
          total: { type: 'integer' },
          runs: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                id: { type: 'string' },
                taskName: { type: 'string' },
                taskType: { type: 'string' },
                status: { type: 'string' },
                qubits: { type: 'array', items: { type: 'string' } },
                createdAt: { type: 'string' },
                completedAt: { type: 'string' },
                plotCount: { type: 'integer' },
                error: { type: 'string' },
              },
              required: [
                'id',
                'taskName',
                'taskType',
                'status',
                'qubits',
                'createdAt',
                'completedAt',
                'plotCount',
                'error',
              ],
              additionalProperties: false,
            },
          },
          error: { type: 'string' },
        },
        required: ['ok', 'baseUrl', 'total', 'runs', 'error'],
        additionalProperties: false,
      },
      render(_args, value) {
        if (!value.ok) {
          return [
            {
              type: 'text',
              text:
                `无法连接 QubitClient 结果服务：${value.baseUrl}\n` +
                `${value.error}\n\n` +
                '先在仓库根目录启动服务：`qubitclient ui start`（默认端口 8581）。',
            },
          ]
        }
        if (value.runs.length === 0) {
          return [
            { type: 'text', text: `QubitClient 结果服务正常（${value.baseUrl}），暂无 pipeline 记录。` },
          ]
        }
        const lines = value.runs.map((run) => {
          const qubits = run.qubits.length > 0 ? run.qubits.join(',') : '-'
          const when = run.createdAt || '-'
          const tail = run.error ? ` | error: ${run.error}` : ''
          return `${run.taskName || '(unknown)'} | ${run.status || '?'} | qubits=${qubits} | ${when} | plots=${run.plotCount} | id=${run.id.slice(0, 8)}${tail}`
        })
        return [
          {
            type: 'text',
            text:
              `QubitClient 结果服务：${value.baseUrl}（共 ${value.total} 条记录，显示 ${value.runs.length} 条）\n` +
              lines.join('\n'),
          },
        ]
      },
    },
    async execute(args) {
      const taskName = typeof args?.taskName === 'string' ? args.taskName.trim() : ''
      const rawLimit = Number(args?.limit)
      const limit = Number.isFinite(rawLimit) ? Math.min(50, Math.max(1, Math.trunc(rawLimit))) : 10
      try {
        const { items, total } = await fetchRuns(baseUrl, {
          taskName,
          limit,
          timeoutMs: REQUEST_TIMEOUT_MS,
        })
        return { ok: true, baseUrl, total, runs: items.map(summarizeRun), error: '' }
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error)
        const timeout = message === 'This operation was aborted' || message === 'The operation was aborted'
        return { ok: false, baseUrl, total: 0, runs: [], error: `${message}${timeout ? '（连接超时）' : ''}` }
      }
    },
  }
}

/**
 * 插件入口。ctx 是 cordis 上下文，config 是 cordis.patch.yml 里该行的 config。
 * 所有注册都挂在 ctx 下，插件卸载时框架自动清理。
 */
export function apply(ctx, config) {
  ctx.tools.register(createResultsTool(normalizeBaseUrl(config?.baseUrl)))
}
