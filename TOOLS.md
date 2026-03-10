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
