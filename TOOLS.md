<!-- LOCKED:START -->
# TOOLS.md (LOCKED Baseline)

## 工具优先策略

1. 有 Skill 先用 Skill；无 Skill 再落脚本。
2. 优先使用一等工具（平台原生工具）而不是临时 shell 拼接。
3. 涉及批量写入时，先 dry-run，再正式执行。

## 凭证与配置

1. 所有凭证从本地环境读取（env / ssh / credential helper）。
2. 禁止在脚本与仓库中写入个人 token / 密码 / 私钥。
3. 配置变更必须最小化，并记录改动原因与回滚点。

## 路径与环境一致性

1. 先确认当前机器与 workspace，再执行自动化。
2. 多环境（主机/WSL/容器）路径映射必须先校验。
3. 不确认环境不执行破坏性操作。

## 质量与稳定性

1. 关键命令必须有可复现验证。
2. 长耗时命令默认后台/异步，避免会话超时丢结果。
3. 报错先定位根因，不凭假设改配置。
<!-- LOCKED:END --><!-- TEMPLATE:START -->
## 引擎组专属工具

### UE Editor 命令行
**用途**：运行时性能监控和调试

**性能统计命令**：
```
stat fps / stat unit / stat unitgraph    # 帧率与线程耗时
stat scenerendering                       # 渲染统计（Draw Call、三角形数）
stat memory / stat memoryplatform         # 内存使用
stat slate / stat particles / stat audio  # 各子系统统计
```

**对象和内存命令**：
```
obj list [class=Texture2D]   # UObject 列表（可按类型过滤）
memreport -full              # 完整内存报告（输出到 Saved/Profiling/MemReports/）
```

**渲染调试命令**：
```
r.ScreenPercentage 50        # 降低渲染分辨率（测试 GPU bound）
showflag.wireframe 1         # 线框模式
freezerendering              # 冻结渲染（分析当前帧，记得 unfreezerendering）
```

**常见坑**：stat 命令在 Shipping 下部分不可用（需 STATS 宏）

### RenderDoc
**用途**：GPU 帧捕获与逐 Draw Call 分析

**代码 Capture Markers**：
```cpp
SCOPED_DRAW_EVENT(RHICmdList, MyCustomPass);
SCOPED_DRAW_EVENTF(RHICmdList, MyPass, TEXT("MyPass %d objects"), NumObjects);
```

**常见坑**：
- Nanite 在 RenderDoc 中可能显示为单个大 Draw Call
- Lumen 光追部分在某些 GPU 上捕获可能失败
- 确保 RenderDoc 版本与 GPU 驱动兼容

### Visual Studio Profiler
- **Sampling**（推荐初始）：低开销找热点；**Instrumentation**：精确计时深度分析
- 只用 Development/Test 配置数据，Debug 配置数据不可参考
- 确保使用匹配 PDB；Release 优化可能导致调用栈不准确

### Unreal Insights
**启动参数**：
```
-trace=cpu,gpu,frame,bookmark,memory -statnamedevents
```
- .utrace 文件在 `Saved/TraceSessions/`
- 注意 Trace 文件可能 GB 级，分析时建议 16GB+ 内存

### 补充规则（从实践经验提炼）
- **网络代理注意**：`NO_PROXY` 需包含外部 API 域名，否则代理干扰 TLS
- **web_search 中文**：`search_lang` 必须用 `zh-hans`（不是 `zh`），否则 422 错误
- **新工具做完必须立刻写 TOOLS.md** — 不能只存 episode 日志，否则换会话就丢失
- **凭证安全**：API Key / 密码 / token 只写在本地 CUSTOM 区，TEMPLATE 禁止出现凭证

## Refined additions from root CUSTOM

**`search_lang` 中文必须用 `zh-hans`，不能用 `zh`！** `zh` 会导致 422 错误。大多数情况省略 `search_lang` 即可。

<!-- LOCAL-EXTENSIONS -->
<!-- LOCAL-EXTENSIONS -->
<!-- LOCAL-EXTENSIONS -->
Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.
- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.
- **默认浏览器:** Microsoft Edge
- **网页登录优先使用 Edge**
- **牛逼闪闪的猜忌互啄群:** `https://open.feishu.cn/open-apis/bot/v2/hook/7fea2a65-4d06-4e5f-bbcf-99f89188568a`
```bash
# 启动编辑器（带参数）
UE4Editor.exe <ProjectPath> <MapName> -game -ResX=1920 -ResY=1080
# 打包项目
UE4Editor-Cmd.exe <ProjectPath> -run=BuildCookRun -targetplatform=Win64 -clientconfig=Development -serverconfig=Development -cook -allmaps -build -stage -pak -archive -archivedirectory=<OutputPath>
# 编译着色器
UE4Editor-Cmd.exe <ProjectPath> -run=ShaderCompileWorker -config=Development
# 批量处理资源
UE4Editor-Cmd.exe <ProjectPath> -run=AssetRegistry -commandlet=ResavePackagesCommandlet
# 运行自动化测试
UE4Editor-Cmd.exe <ProjectPath> -run=AutomationTool -script=<TestScript>
**启动捕获：**
1. 选择 UE4Editor.exe 或游戏进程
2. 设置 Working Directory 为项目目录
3. 点击 "Capture Launch" 启动带捕获的进程
4. 按 F12 手动触发帧捕获，或设置自动捕获条件
**常用分析技巧：**
- **Draw Call 分析**：查看 Events 面板，识别高开销的渲染调用
- **纹理查看**：在 Textures 标签查看各阶段使用的纹理资源
- **Pipeline State 检查**：确认 PSO 是否符合预期，识别冗余状态切换
- **GPU 耗时分析**：使用 GPU Timing 查看各 Pass 的时间消耗
**性能排查流程：**
1. 捕获问题帧（卡顿/掉帧时刻）
2. 查看 GPU 耗时分布，定位瓶颈 Pass
3. 分析该 Pass 的 Draw Call 和纹理使用
4. 对比正常帧，找出差异
5. 定位到具体代码/资源
**CPU 性能分析：**
```bash
# 启动性能分析会话
devenv.exe <SolutionPath> /Profile
# 或使用命令行
vsperfreport.exe <DataFile>.vsp /summary
**关键指标：**
- **Inclusive Time**：函数总耗时（含子调用）
- **Exclusive Time**：函数自身耗时（不含子调用）
- **Call Count**：调用次数
- **Hot Path**：最耗时的调用链
**分析流程：**
1. 启动性能分析（Sampling 或 Instrumentation）
2. 执行目标操作（如加载场景、播放特效）
3. 停止分析，生成报告
4. 查看 Hot Path，识别瓶颈
5. 下钻到具体函数，分析代码
**启动 Trace 捕获：**
```bash
# 启动 Unreal Insights
UnrealInsights.exe
**常用 Trace 通道：**
- **LogMessages**：UE 日志流
- **Performance**：帧时间、线程活动
- **Memory**：内存分配/释放
- **Loading**：资源加载时序
- **Network**：网络复制/ RPC
**分析技巧：**
1. 使用 Session Browser 连接运行中的游戏
2. 开始捕获，复现问题
3. 停止捕获，分析时间线
4. 使用 Query 功能过滤特定事件
5. 导出报告或截图保存
**Minidump 分析：**
```bash
# 使用 WinDbg 分析 Dump
windbg.exe -z <CrashDump>.dmp -y <SymbolPath>
# 常用命令
!analyze -v          # 自动分析崩溃原因
kv                   # 查看调用栈
lm                   # 列出加载的模块
!peb                 # 查看进程环境块
**UE 崩溃日志位置：**
<Saved>/Logs/<ProjectName>.log
<Saved>/Crashes/<CrashID>/
**常见崩溃模式：**
- **Access Violation**：空指针/野指针访问
- **Stack Overflow**：递归过深/大栈变量
- **Heap Corruption**：内存越界/重复释放
- **Deadlock**：线程锁竞争
Add whatever helps you do your job. This is your cheat sheet.
Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.
- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.
- **默认浏览器:** Microsoft Edge
- **网页登录优先使用 Edge**
- **牛逼闪闪的猜忌互啄群:** `https://open.feishu.cn/open-apis/bot/v2/hook/7fea2a65-4d06-4e5f-bbcf-99f89188568a`
```bash
# 启动编辑器（带参数）
UE4Editor.exe <ProjectPath> <MapName> -game -ResX=1920 -ResY=1080
# 打包项目
UE4Editor-Cmd.exe <ProjectPath> -run=BuildCookRun -targetplatform=Win64 -clientconfig=Development -serverconfig=Development -cook -allmaps -build -stage -pak -archive -archivedirectory=<OutputPath>
# 编译着色器
UE4Editor-Cmd.exe <ProjectPath> -run=ShaderCompileWorker -config=Development
# 批量处理资源
UE4Editor-Cmd.exe <ProjectPath> -run=AssetRegistry -commandlet=ResavePackagesCommandlet
# 运行自动化测试
UE4Editor-Cmd.exe <ProjectPath> -run=AutomationTool -script=<TestScript>
**启动捕获：**
1. 选择 UE4Editor.exe 或游戏进程
2. 设置 Working Directory 为项目目录
3. 点击 "Capture Launch" 启动带捕获的进程
4. 按 F12 手动触发帧捕获，或设置自动捕获条件
**常用分析技巧：**
- **Draw Call 分析**：查看 Events 面板，识别高开销的渲染调用
- **纹理查看**：在 Textures 标签查看各阶段使用的纹理资源
- **Pipeline State 检查**：确认 PSO 是否符合预期，识别冗余状态切换
- **GPU 耗时分析**：使用 GPU Timing 查看各 Pass 的时间消耗
**性能排查流程：**
1. 捕获问题帧（卡顿/掉帧时刻）
2. 查看 GPU 耗时分布，定位瓶颈 Pass
3. 分析该 Pass 的 Draw Call 和纹理使用
4. 对比正常帧，找出差异
5. 定位到具体代码/资源
**CPU 性能分析：**
```bash
# 启动性能分析会话
devenv.exe <SolutionPath> /Profile
# 或使用命令行
vsperfreport.exe <DataFile>.vsp /summary
**关键指标：**
- **Inclusive Time**：函数总耗时（含子调用）
- **Exclusive Time**：函数自身耗时（不含子调用）
- **Call Count**：调用次数
- **Hot Path**：最耗时的调用链
**分析流程：**
1. 启动性能分析（Sampling 或 Instrumentation）
2. 执行目标操作（如加载场景、播放特效）
3. 停止分析，生成报告
4. 查看 Hot Path，识别瓶颈
5. 下钻到具体函数，分析代码
**启动 Trace 捕获：**
```bash
# 启动 Unreal Insights
UnrealInsights.exe
**常用 Trace 通道：**
- **LogMessages**：UE 日志流
- **Performance**：帧时间、线程活动
- **Memory**：内存分配/释放
- **Loading**：资源加载时序
- **Network**：网络复制/ RPC
**分析技巧：**
1. 使用 Session Browser 连接运行中的游戏
2. 开始捕获，复现问题
3. 停止捕获，分析时间线
4. 使用 Query 功能过滤特定事件
5. 导出报告或截图保存
**Minidump 分析：**
```bash
# 使用 WinDbg 分析 Dump
windbg.exe -z <CrashDump>.dmp -y <SymbolPath>
# 常用命令
!analyze -v          # 自动分析崩溃原因
kv                   # 查看调用栈
lm                   # 列出加载的模块
!peb                 # 查看进程环境块
**UE 崩溃日志位置：**
<Saved>/Logs/<ProjectName>.log
<Saved>/Crashes/<CrashID>/
**常见崩溃模式：**
- **Access Violation**：空指针/野指针访问
- **Stack Overflow**：递归过深/大栈变量
- **Heap Corruption**：内存越界/重复释放
- **Deadlock**：线程锁竞争
Add whatever helps you do your job. This is your cheat sheet.
Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.
- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.
- **默认浏览器:** Microsoft Edge
- **网页登录优先使用 Edge**
- **牛逼闪闪的猜忌互啄群:** `https://open.feishu.cn/open-apis/bot/v2/hook/7fea2a65-4d06-4e5f-bbcf-99f89188568a`
```bash
# 启动编辑器（带参数）
UE4Editor.exe <ProjectPath> <MapName> -game -ResX=1920 -ResY=1080
# 打包项目
UE4Editor-Cmd.exe <ProjectPath> -run=BuildCookRun -targetplatform=Win64 -clientconfig=Development -serverconfig=Development -cook -allmaps -build -stage -pak -archive -archivedirectory=<OutputPath>
# 编译着色器
UE4Editor-Cmd.exe <ProjectPath> -run=ShaderCompileWorker -config=Development
# 批量处理资源
UE4Editor-Cmd.exe <ProjectPath> -run=AssetRegistry -commandlet=ResavePackagesCommandlet
# 运行自动化测试
UE4Editor-Cmd.exe <ProjectPath> -run=AutomationTool -script=<TestScript>
**启动捕获：**
1. 选择 UE4Editor.exe 或游戏进程
2. 设置 Working Directory 为项目目录
3. 点击 "Capture Launch" 启动带捕获的进程
4. 按 F12 手动触发帧捕获，或设置自动捕获条件
**常用分析技巧：**
- **Draw Call 分析**：查看 Events 面板，识别高开销的渲染调用
- **纹理查看**：在 Textures 标签查看各阶段使用的纹理资源
- **Pipeline State 检查**：确认 PSO 是否符合预期，识别冗余状态切换
- **GPU 耗时分析**：使用 GPU Timing 查看各 Pass 的时间消耗
**性能排查流程：**
1. 捕获问题帧（卡顿/掉帧时刻）
2. 查看 GPU 耗时分布，定位瓶颈 Pass
3. 分析该 Pass 的 Draw Call 和纹理使用
4. 对比正常帧，找出差异
5. 定位到具体代码/资源
**CPU 性能分析：**
```bash
# 启动性能分析会话
devenv.exe <SolutionPath> /Profile
# 或使用命令行
vsperfreport.exe <DataFile>.vsp /summary
**关键指标：**
- **Inclusive Time**：函数总耗时（含子调用）
- **Exclusive Time**：函数自身耗时（不含子调用）
- **Call Count**：调用次数
- **Hot Path**：最耗时的调用链
**分析流程：**
1. 启动性能分析（Sampling 或 Instrumentation）
2. 执行目标操作（如加载场景、播放特效）
3. 停止分析，生成报告
4. 查看 Hot Path，识别瓶颈
5. 下钻到具体函数，分析代码
**启动 Trace 捕获：**
```bash
# 启动 Unreal Insights
UnrealInsights.exe
**常用 Trace 通道：**
- **LogMessages**：UE 日志流
- **Performance**：帧时间、线程活动
- **Memory**：内存分配/释放
- **Loading**：资源加载时序
- **Network**：网络复制/ RPC
**分析技巧：**
1. 使用 Session Browser 连接运行中的游戏
2. 开始捕获，复现问题
3. 停止捕获，分析时间线
4. 使用 Query 功能过滤特定事件
5. 导出报告或截图保存
**Minidump 分析：**
```bash
# 使用 WinDbg 分析 Dump
windbg.exe -z <CrashDump>.dmp -y <SymbolPath>
# 常用命令
!analyze -v          # 自动分析崩溃原因
kv                   # 查看调用栈
lm                   # 列出加载的模块
!peb                 # 查看进程环境块
**UE 崩溃日志位置：**
<Saved>/Logs/<ProjectName>.log
<Saved>/Crashes/<CrashID>/
**常见崩溃模式：**
- **Access Violation**：空指针/野指针访问
- **Stack Overflow**：递归过深/大栈变量
- **Heap Corruption**：内存越界/重复释放
- **Deadlock**：线程锁竞争
Add whatever helps you do your job. This is your cheat sheet.

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

- **默认浏览器:** Microsoft Edge
- **网页登录优先使用 Edge**

- **牛逼闪闪的猜忌互啄群:** `https://open.feishu.cn/open-apis/bot/v2/hook/7fea2a65-4d06-4e5f-bbcf-99f89188568a`

```bash
# 启动编辑器（带参数）
UE4Editor.exe <ProjectPath> <MapName> -game -ResX=1920 -ResY=1080

# 打包项目
UE4Editor-Cmd.exe <ProjectPath> -run=BuildCookRun -targetplatform=Win64 -clientconfig=Development -serverconfig=Development -cook -allmaps -build -stage -pak -archive -archivedirectory=<OutputPath>

# 编译着色器
UE4Editor-Cmd.exe <ProjectPath> -run=ShaderCompileWorker -config=Development

# 批量处理资源
UE4Editor-Cmd.exe <ProjectPath> -run=AssetRegistry -commandlet=ResavePackagesCommandlet

# 运行自动化测试
UE4Editor-Cmd.exe <ProjectPath> -run=AutomationTool -script=<TestScript>
```

**启动捕获：**
1. 选择 UE4Editor.exe 或游戏进程
2. 设置 Working Directory 为项目目录
3. 点击 "Capture Launch" 启动带捕获的进程
4. 按 F12 手动触发帧捕获，或设置自动捕获条件

**常用分析技巧：**
- **Draw Call 分析**：查看 Events 面板，识别高开销的渲染调用
- **纹理查看**：在 Textures 标签查看各阶段使用的纹理资源
- **Pipeline State 检查**：确认 PSO 是否符合预期，识别冗余状态切换
- **GPU 耗时分析**：使用 GPU Timing 查看各 Pass 的时间消耗

**性能排查流程：**
1. 捕获问题帧（卡顿/掉帧时刻）
2. 查看 GPU 耗时分布，定位瓶颈 Pass
3. 分析该 Pass 的 Draw Call 和纹理使用
4. 对比正常帧，找出差异
5. 定位到具体代码/资源

**CPU 性能分析：**
```bash
# 启动性能分析会话
devenv.exe <SolutionPath> /Profile

# 或使用命令行
vsperfreport.exe <DataFile>.vsp /summary
```

**关键指标：**
- **Inclusive Time**：函数总耗时（含子调用）
- **Exclusive Time**：函数自身耗时（不含子调用）
- **Call Count**：调用次数
- **Hot Path**：最耗时的调用链

**分析流程：**
1. 启动性能分析（Sampling 或 Instrumentation）
2. 执行目标操作（如加载场景、播放特效）
3. 停止分析，生成报告
4. 查看 Hot Path，识别瓶颈
5. 下钻到具体函数，分析代码

**启动 Trace 捕获：**
```bash
# 启动 Unreal Insights
UnrealInsights.exe

**常用 Trace 通道：**
- **LogMessages**：UE 日志流
- **Performance**：帧时间、线程活动
- **Memory**：内存分配/释放
- **Loading**：资源加载时序
- **Network**：网络复制/ RPC

**分析技巧：**
1. 使用 Session Browser 连接运行中的游戏
2. 开始捕获，复现问题
3. 停止捕获，分析时间线
4. 使用 Query 功能过滤特定事件
5. 导出报告或截图保存

**Minidump 分析：**
```bash
# 使用 WinDbg 分析 Dump
windbg.exe -z <CrashDump>.dmp -y <SymbolPath>

# 常用命令
!analyze -v          # 自动分析崩溃原因
kv                   # 查看调用栈
lm                   # 列出加载的模块
!peb                 # 查看进程环境块
```

**UE 崩溃日志位置：**
```
<Saved>/Logs/<ProjectName>.log
<Saved>/Crashes/<CrashID>/
```

**常见崩溃模式：**
- **Access Violation**：空指针/野指针访问
- **Stack Overflow**：递归过深/大栈变量
- **Heap Corruption**：内存越界/重复释放
- **Deadlock**：线程锁竞争

Add whatever helps you do your job. This is your cheat sheet.
<!-- TEMPLATE:END -->



# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Browser

- **默认浏览器:** Microsoft Edge
- **网页登录优先使用 Edge**

## Feishu (飞书) Webhooks

- **牛逼闪闪的猜忌互啄群:** `https://open.feishu.cn/open-apis/bot/v2/hook/7fea2a65-4d06-4e5f-bbcf-99f89188568a`

---

## 🎮 UE 引擎开发工具链（Engine Agent 融合）

### UE 命令行工具

```bash
# 启动编辑器（带参数）
UE4Editor.exe <ProjectPath> <MapName> -game -ResX=1920 -ResY=1080

# 打包项目
UE4Editor-Cmd.exe <ProjectPath> -run=BuildCookRun -targetplatform=Win64 -clientconfig=Development -serverconfig=Development -cook -allmaps -build -stage -pak -archive -archivedirectory=<OutputPath>

# 编译着色器
UE4Editor-Cmd.exe <ProjectPath> -run=ShaderCompileWorker -config=Development

# 批量处理资源
UE4Editor-Cmd.exe <ProjectPath> -run=AssetRegistry -commandlet=ResavePackagesCommandlet

# 运行自动化测试
UE4Editor-Cmd.exe <ProjectPath> -run=AutomationTool -script=<TestScript>
```

### RenderDoc 使用指南

**启动捕获：**
1. 选择 UE4Editor.exe 或游戏进程
2. 设置 Working Directory 为项目目录
3. 点击 "Capture Launch" 启动带捕获的进程
4. 按 F12 手动触发帧捕获，或设置自动捕获条件

**常用分析技巧：**
- **Draw Call 分析**：查看 Events 面板，识别高开销的渲染调用
- **纹理查看**：在 Textures 标签查看各阶段使用的纹理资源
- **Pipeline State 检查**：确认 PSO 是否符合预期，识别冗余状态切换
- **GPU 耗时分析**：使用 GPU Timing 查看各 Pass 的时间消耗

**性能排查流程：**
1. 捕获问题帧（卡顿/掉帧时刻）
2. 查看 GPU 耗时分布，定位瓶颈 Pass
3. 分析该 Pass 的 Draw Call 和纹理使用
4. 对比正常帧，找出差异
5. 定位到具体代码/资源

### VS Profiler 使用指南

**CPU 性能分析：**
```bash
# 启动性能分析会话
devenv.exe <SolutionPath> /Profile

# 或使用命令行
vsperfreport.exe <DataFile>.vsp /summary
```

**关键指标：**
- **Inclusive Time**：函数总耗时（含子调用）
- **Exclusive Time**：函数自身耗时（不含子调用）
- **Call Count**：调用次数
- **Hot Path**：最耗时的调用链

**分析流程：**
1. 启动性能分析（Sampling 或 Instrumentation）
2. 执行目标操作（如加载场景、播放特效）
3. 停止分析，生成报告
4. 查看 Hot Path，识别瓶颈
5. 下钻到具体函数，分析代码

### Unreal Insights 使用指南

**启动 Trace 捕获：**
```bash
# 启动 Unreal Insights
UnrealInsights.exe

# 或从编辑器菜单：Tools -> Unreal Insights
```

**常用 Trace 通道：**
- **LogMessages**：UE 日志流
- **Performance**：帧时间、线程活动
- **Memory**：内存分配/释放
- **Loading**：资源加载时序
- **Network**：网络复制/ RPC

**分析技巧：**
1. 使用 Session Browser 连接运行中的游戏
2. 开始捕获，复现问题
3. 停止捕获，分析时间线
4. 使用 Query 功能过滤特定事件
5. 导出报告或截图保存

### 崩溃调试工具

**Minidump 分析：**
```bash
# 使用 WinDbg 分析 Dump
windbg.exe -z <CrashDump>.dmp -y <SymbolPath>

# 常用命令
!analyze -v          # 自动分析崩溃原因
kv                   # 查看调用栈
lm                   # 列出加载的模块
!peb                 # 查看进程环境块
```

**UE 崩溃日志位置：**
```
<Saved>/Logs/<ProjectName>.log
<Saved>/Crashes/<CrashID>/
```

**常见崩溃模式：**
- **Access Violation**：空指针/野指针访问
- **Stack Overflow**：递归过深/大栈变量
- **Heap Corruption**：内存越界/重复释放
- **Deadlock**：线程锁竞争

---

Add whatever helps you do your job. This is your cheat sheet.
## Harness 工程化补充（2026-03-25）

- **先找硬约束入口**：遇到反复提醒类问题，优先考虑 pre-check、post-check、schema、模板、脚本、hook，而不是继续补提示词。
- **验证必须显式化**：执行命令前先写清楚预期成功信号；没有成功信号的命令不算完整方案。
- **单一信源优先**：同类配置/规则避免散落在多个 md；优先在一个权威位置维护，其余位置只放引用。
- **失败信息要可定位**：脚本/检查最好给出明确失败原因，避免只报“failed”。
- **留痕比口头总结重要**：新的工具套路、命令前置条件、环境坑点，要写进 TOOLS.md 或脚本注释，不只写在聊天里。
