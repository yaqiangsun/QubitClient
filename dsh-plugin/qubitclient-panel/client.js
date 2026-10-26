/**
 * Client 半：跑在 DSH 的浏览器页面里，负责「界面」。
 *
 * 做两件事，都围绕同一个服务：QubitClient 的结果页服务
 * （`qubitclient ui start`，默认 http://127.0.0.1:8581/，独立的 FastAPI + SSE 单页）。
 *
 *   1) 右侧栏新增一种 tab 类型「QubitClient 结果」——正文是一个 iframe，
 *      直接把那个结果页面原样搬进 DSH，配一条极简工具栏（状态 / 刷新 / 外部打开）；
 *   2) 输入框下方一枚状态徽标——显示服务在线状态与最近一次 pipeline，
 *      点「打开面板」直接在右侧栏开 tab。
 *
 * 关键 API（详见 @deepseek-ai/dsh-client-ui-sidebar-right 的 README）：
 *   - ctx.sidebarRightTabs.register({ id, kind, title, guide, keepMounted }) 登记 tab 类型；
 *   - ctx.slots.register({ name: 'sidebar.right.pane.tab', key: id }, Body) 登记正文；
 *   - 正文不接收平铺 props：导航参数只能通过框架注入的 useTabInfo() 读，
 *     即 useTabInfo().tab.navigation.params；
 *   - ctx.sidebarRight.openTab(kind, { params }) 打开/聚焦 tab（无会话时会 throw）。
 *
 * 三条硬规则：工厂函数无副作用；只用 --dsw-alias-* 主题 token 上色；
 * React 从模块表 require('react') 拿。
 */
window.__ModuleLoader__.load({
  id: 'qubitclient-dsh-panel',
  factory(require) {
    const React = require('react')
    const h = React.createElement

    /** 本插件在右侧栏 tab 系统里的实现 id（全局唯一；同时也是正文插槽的 key）。 */
    const PANEL_ID = 'qubitclient-dsh-panel/results'
    /** tab 的类型名；页类型按 kind 打开，不需要 patterns。 */
    const PANEL_KIND = 'qubitclient-results'
    /** 结果页服务默认地址（与 index.js / cordis.patch.yml 的默认值保持一致）。 */
    const DEFAULT_PAGE_URL = 'http://127.0.0.1:8581/'
    /** 浏览器侧覆盖地址：localStorage 键（离线提示里改端口时写入）。 */
    const URL_KEY = 'dsh.qubitclient.pageUrl'
    const HEALTH_TIMEOUT_MS = 4000

    // ---- 地址读写 ---------------------------------------------------------
    function normalizeUrl(value) {
      const raw = typeof value === 'string' ? value.trim() : ''
      if (raw === '') return DEFAULT_PAGE_URL
      return raw.endsWith('/') ? raw : `${raw}/`
    }

    function readPageUrl() {
      try {
        const stored = window.localStorage.getItem(URL_KEY)
        if (stored && stored.trim() !== '') return normalizeUrl(stored)
      } catch (_error) {
        /* 隐私模式 / 禁用存储时退回默认值 */
      }
      return DEFAULT_PAGE_URL
    }

    function rememberPageUrl(value) {
      try {
        window.localStorage.setItem(URL_KEY, normalizeUrl(value))
      } catch (_error) {
        /* 存不下就算了：本次会话仍按 state 生效 */
      }
    }

    // ---- 服务健康检查 -----------------------------------------------------
    /**
     * 轮询 /api/runs?limit=1 判断服务是否在线，并顺带拿到总数与最近一条记录。
     * 跨域没问题：结果服务开着 CORSMiddleware(allow_origins=["*"])。
     */
    function useResultsHealth(pageUrl, intervalMs) {
      const [state, setState] = React.useState({
        status: 'checking',
        total: 0,
        latest: null,
        error: '',
      })

      const check = React.useCallback(() => {
        const controller = typeof AbortController === 'function' ? new AbortController() : null
        const timer = setTimeout(() => {
          if (controller) controller.abort()
        }, HEALTH_TIMEOUT_MS)

        fetch(`${pageUrl}api/runs?limit=1`, {
          cache: 'no-store',
          signal: controller ? controller.signal : undefined,
        })
          .then((response) => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`)
            return response.json()
          })
          .then((body) => {
            const items = Array.isArray(body && body.items) ? body.items : []
            const latest = items[0]
              ? {
                  taskName: typeof items[0].task_name === 'string' ? items[0].task_name : '',
                  status: typeof items[0].status === 'string' ? items[0].status : '',
                }
              : null
            setState({
              status: 'online',
              total: typeof body?.total === 'number' ? body.total : items.length,
              latest,
              error: '',
            })
          })
          .catch((error) => {
            const aborted = error && error.name === 'AbortError'
            setState({
              status: 'offline',
              total: 0,
              latest: null,
              error: aborted ? `连接超时（${HEALTH_TIMEOUT_MS}ms）` : String((error && error.message) || error),
            })
          })
          .finally(() => clearTimeout(timer))
      }, [pageUrl])

      React.useEffect(() => {
        check()
        const timer = setInterval(check, intervalMs)
        return () => clearInterval(timer)
      }, [check, intervalMs])

      return [state, check]
    }

    function healthColor(status) {
      if (status === 'online') return 'var(--dsw-alias-state-success-primary)'
      if (status === 'offline') return 'var(--dsw-alias-state-error-primary)'
      return 'var(--dsw-alias-state-warn-primary)'
    }

    // compact：输入框徽标位置窄，省掉记录条数，只留「最近一次任务」。
    function healthLabel(health, options = {}) {
      const compact = options.compact === true
      if (health.status === 'online') {
        const latest = health.latest
        if (!latest) return '已连接 · 暂无记录'
        const task = latest.taskName || '未知任务'
        const state = latest.status || '?'
        return compact
          ? `已连接 · ${task}（${state}）`
          : `已连接 · 共 ${health.total} 条 · 最近 ${task}（${state}）`
      }
      if (health.status === 'offline') return `未连接：${health.error || '无法访问'}`
      return '正在连接…'
    }

    // ---- 样式（只用宿主主题 token，明暗自动跟随）-------------------------
    const styles = {
      root: {
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        width: '100%',
        minHeight: 0,
        background: 'var(--dsw-alias-bg-layer-1)',
        color: 'var(--dsw-alias-label-primary)',
        fontSize: '12px',
      },
      toolbar: {
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        flex: '0 0 auto',
        padding: '0 8px',
        height: '32px',
        borderBottom: '1px solid var(--dsw-alias-border-l2)',
        background: 'var(--dsw-alias-bg-layer-1)',
        overflow: 'hidden',
      },
      dot: { width: '6px', height: '6px', borderRadius: '999px', flex: '0 0 auto' },
      status: {
        flex: '1 1 auto',
        minWidth: 0,
        overflow: 'hidden',
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
        color: 'var(--dsw-alias-label-secondary)',
      },
      action: {
        flex: '0 0 auto',
        padding: '2px 8px',
        borderRadius: '6px',
        border: '1px solid var(--dsw-alias-border-l2)',
        background: 'transparent',
        color: 'var(--dsw-alias-label-primary)',
        font: 'inherit',
        cursor: 'pointer',
      },
      frameWrap: { position: 'relative', flex: '1 1 auto', minHeight: 0, display: 'flex' },
      frame: { flex: '1 1 auto', width: '100%', border: 0, display: 'block', background: '#fff' },
      offline: {
        flex: '1 1 auto',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        padding: '20px',
        overflow: 'auto',
      },
      offlineTitle: { margin: 0, fontSize: '14px', fontWeight: 600 },
      offlineText: { margin: 0, color: 'var(--dsw-alias-label-secondary)', lineHeight: '20px' },
      code: {
        padding: '2px 6px',
        borderRadius: '4px',
        background: 'var(--dsw-alias-markdown-inline-code)',
        fontFamily: 'ui-monospace, SFMono-Regular, Consolas, monospace',
        fontSize: '11px',
      },
      input: {
        flex: '1 1 auto',
        minWidth: 0,
        padding: '4px 8px',
        borderRadius: '6px',
        border: '1px solid var(--dsw-alias-border-l2)',
        background: 'var(--dsw-alias-bg-layer-1)',
        color: 'var(--dsw-alias-label-primary)',
        font: 'inherit',
      },
      row: { display: 'flex', alignItems: 'center', gap: '8px' },
      primary: {
        flex: '0 0 auto',
        padding: '4px 10px',
        borderRadius: '6px',
        border: '1px solid var(--dsw-alias-border-l2)',
        background: 'var(--dsw-alias-button-tool-bar-fill)',
        color: 'var(--dsw-alias-label-primary)',
        font: 'inherit',
        cursor: 'pointer',
      },
      dock: {
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        margin: '0 auto 8px',
        padding: '4px 10px',
        width: 'fit-content',
        borderRadius: '999px',
        border: '1px solid var(--dsw-alias-border-l2)',
        background: 'var(--dsw-alias-bg-layer-1)',
        color: 'var(--dsw-alias-label-secondary)',
        font: 'inherit',
        fontSize: '12px',
        lineHeight: '18px',
      },
      dockText: { color: 'var(--dsw-alias-label-primary)' },
      linkButton: {
        padding: 0,
        border: 'none',
        background: 'transparent',
        color: 'var(--dsw-alias-link)',
        font: 'inherit',
        cursor: 'pointer',
      },
    }

    // ---- 引导页 / 插件列表用的小图标 -------------------------------------
    function PanelIcon() {
      return h(
        'svg',
        { viewBox: '0 0 24 24', width: 20, height: 20, 'aria-hidden': true },
        h('circle', { cx: 12, cy: 12, r: 3.2, fill: 'currentColor' }),
        h('ellipse', {
          cx: 12,
          cy: 12,
          rx: 9,
          ry: 4.2,
          fill: 'none',
          stroke: 'currentColor',
          strokeWidth: 1.5,
          transform: 'rotate(35 12 12)',
        }),
        h('ellipse', {
          cx: 12,
          cy: 12,
          rx: 9,
          ry: 4.2,
          fill: 'none',
          stroke: 'currentColor',
          strokeWidth: 1.5,
          opacity: 0.55,
          transform: 'rotate(-35 12 12)',
        }),
      )
    }

    // ---- 面板挂载状态（徽标据此把「打开面板」换成「聚焦面板」） -------------
    // 挂载即视为已打开：keepMounted 只保证切 tab/切会话时不重建 iframe，
    // 用户关掉 tab 时正文会卸载，所以挂载数就是「当前有几个结果面板开着」。
    function createPanelPresence() {
      let mounted = 0
      const listeners = new Set()
      const emit = () => {
        for (const listener of listeners) listener()
      }
      return {
        get: () => mounted > 0,
        enter() {
          mounted += 1
          emit()
          return () => {
            mounted = Math.max(0, mounted - 1)
            emit()
          }
        },
        subscribe(listener) {
          listeners.add(listener)
          return () => listeners.delete(listener)
        },
      }
    }
    const panelPresence = createPanelPresence()

    function usePanelOpen() {
      const [open, setOpen] = React.useState(panelPresence.get)
      React.useEffect(() => {
        // 订阅期间状态可能已变，先对齐一次再监听。
        setOpen(panelPresence.get())
        return panelPresence.subscribe(() => setOpen(panelPresence.get()))
      }, [])
      return open
    }

    // ---- 右侧栏 tab 正文 --------------------------------------------------
    function QubitResultsPanel(props) {
      const useTabInfo = props && props.useTabInfo
      const info = typeof useTabInfo === 'function' ? useTabInfo() : null
      // 从 openTab(kind, { params: { url } }) 传进来的地址；引导页打开的 tab 没有 params。
      const paramUrl = info && info.tab && info.tab.navigation && info.tab.navigation.params
        ? info.tab.navigation.params.url
        : undefined

      const [savedUrl, setSavedUrl] = React.useState(readPageUrl)
      const pageUrl = paramUrl ? normalizeUrl(paramUrl) : savedUrl
      const [draftUrl, setDraftUrl] = React.useState(pageUrl)
      const [health, recheck] = useResultsHealth(pageUrl, 15000)
      const [reloadToken, setReloadToken] = React.useState(0)

      // 本面板挂载期间向徽标报「已打开」，卸载（关掉 tab）时自动撤销。
      React.useEffect(() => panelPresence.enter(), [])

      const reload = React.useCallback(() => {
        setReloadToken((value) => value + 1)
        recheck()
      }, [recheck])

      const openExternal = React.useCallback(() => {
        try {
          window.open(pageUrl, '_blank', 'noopener,noreferrer')
        } catch (_error) {
          /* 弹窗被拦就算了 */
        }
      }, [pageUrl])

      const applyUrl = React.useCallback(() => {
        const next = normalizeUrl(draftUrl)
        rememberPageUrl(next)
        setSavedUrl(next)
        setDraftUrl(next)
        recheck()
      }, [draftUrl, recheck])

      const broken = health.status === 'offline'

      return h(
        'div',
        { style: styles.root },
        h(
          'div',
          { style: styles.toolbar },
          h('span', { style: { ...styles.dot, background: healthColor(health.status) } }),
          h('span', { style: styles.status, title: pageUrl }, healthLabel(health)),
          h('button', { type: 'button', style: styles.action, onClick: reload }, '刷新'),
          h('button', { type: 'button', style: styles.action, onClick: openExternal }, '外部打开'),
        ),
        broken
          ? h(
              'div',
              { style: styles.offline },
              h('h3', { style: styles.offlineTitle }, '结果页服务未连接'),
              h(
                'p',
                { style: styles.offlineText },
                '这个面板只是把 QubitClient 自带的结果页（FastAPI + SSE）嵌进来。请先在仓库根目录启动它：',
              ),
              h('p', { style: styles.offlineText }, h('code', { style: styles.code }, 'qubitclient ui start')),
              h(
                'p',
                { style: styles.offlineText },
                '默认监听 8581 端口；如果换了端口/主机，把下面的地址改成实际地址再点「保存并重试」。',
              ),
              h(
                'div',
                { style: styles.row },
                h('input', {
                  style: styles.input,
                  value: draftUrl,
                  spellCheck: false,
                  'aria-label': '结果页服务地址',
                  onChange: (event) => setDraftUrl(event.target.value),
                  onKeyDown: (event) => {
                    if (event.key === 'Enter') applyUrl()
                  },
                }),
                h('button', { type: 'button', style: styles.primary, onClick: applyUrl }, '保存并重试'),
                h(
                  'button',
                  { type: 'button', style: styles.action, onClick: openExternal },
                  '在浏览器打开',
                ),
              ),
              h('p', { style: styles.offlineText }, `当前地址：${pageUrl}`),
            )
          : h(
              'div',
              { style: styles.frameWrap },
              h('iframe', {
                key: `${pageUrl}#${reloadToken}`,
                src: pageUrl,
                title: 'QubitClient 结果页',
                style: styles.frame,
                sandbox: 'allow-scripts allow-forms allow-same-origin allow-popups allow-popups-to-escape-sandbox',
                referrerPolicy: 'no-referrer',
              }),
            ),
      )
    }

    // ---- 输入框下方的状态徽标 --------------------------------------------
    function createDock(openPanel) {
      return function QubitDock() {
        const [pageUrl] = React.useState(readPageUrl)
        const [health] = useResultsHealth(pageUrl, 30000)
        // 面板已开着就别再喊「打开面板」：同一动作改成「聚焦面板」，
        // 侧栏被收起时点它仍会把面板调出来。
        const panelOpen = usePanelOpen()
        return h(
          'div',
          { style: styles.dock },
          h('span', { style: { ...styles.dot, background: healthColor(health.status) } }),
          h('span', { style: styles.dockText }, 'QubitClient 结果'),
          h('span', { style: { color: 'var(--dsw-alias-label-secondary)' } }, healthLabel(health, { compact: true })),
          h(
            'button',
            { type: 'button', style: styles.linkButton, onClick: openPanel },
            panelOpen ? '聚焦面板' : '打开面板',
          ),
        )
      }
    }

    return {
      // slots: 往插槽里塞 UI；sidebarRightTabs: 右侧栏 tab 类型注册表；
      // sidebarRight: 编程式 opened tab（输入框徽标用）。
      inject: ['slots', 'sidebarRightTabs', 'sidebarRight'],
      apply(ctx) {
        const openPanel = () => {
          try {
            ctx.sidebarRight.openTab(PANEL_KIND, { params: { url: readPageUrl() } })
          } catch (error) {
            // 没有选中会话时 openTab 会 throw；插件不该因此崩溃。
            console.warn('[qubitclient-panel] 打开结果面板失败:', error)
          }
        }

        // ---- 1) 输入框下方的状态徽标 ------------------------------------
        const QubitDock = createDock(openPanel)
        ctx.slots.inject('conversation.composer.dock', () =>
          ctx.slots.register(
            { name: 'conversation.composer.dock', id: 'qubitclient-dock', order: 6 },
            QubitDock,
          ),
        )

        // ---- 2) 右侧栏的新 tab 类型 -------------------------------------
        // 阶段一：登记类型（静态声明，没有运行时钩子）。
        ctx.effect(
          () =>
            ctx.sidebarRightTabs.register({
              id: PANEL_ID,
              kind: PANEL_KIND,
              title: () => 'QubitClient 结果',
              // keepMounted：切 tab / 切会话 / 收起右栏时保留 iframe，
              // 页面的 SSE 连接和滚动位置不会被反复重建。
              keepMounted: true,
              guide: [
                {
                  id: 'qubitclient-results',
                  order: 72,
                  title: () => 'QubitClient 结果',
                  description: () => '把 QubitClient 的 pipeline 结果页嵌进右侧栏（需先启动结果服务）',
                  icon: PanelIcon,
                },
              ],
            }),
          'qubitclient-panel: sidebar tab',
        )

        // 阶段二：登记正文。key 必须等于类型的 id。
        ctx.slots.inject('sidebar.right.pane.tab', () =>
          ctx.slots.register(
            { name: 'sidebar.right.pane.tab', key: PANEL_ID },
            QubitResultsPanel,
          ),
        )
      },
    }
  },
})
