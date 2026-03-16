<!-- LOCKED:START -->
# HEARTBEAT.md (LOCKED Baseline)

## 心跳执行规则（强制）

1. 每次心跳至少完成一项有效检查，不允许空转。
2. 发现异常必须输出告警与错误摘要，不可沉默。
3. 不推断历史任务，不重复旧任务，只按当前清单执行。

## 最低检查项（轮换）

- memory_search 健康检查（可用性 + 错误原因）
- 关键仓库同步状态
- 关键路径/配置漂移
- 当日代码/配置变化是否已写 episode

## 安静时段策略

- 非紧急事项在静默时段不主动打扰。
- 仅在“异常/阻塞/风险”时主动提醒。
<!-- LOCKED:END --><!-- TEMPLATE:START -->
## 引擎组检查（轮换检查，每次选 2-3 项）

### 编译健康
- [ ] 今日编译是否有新 Warning？（特别关注 deprecated API 使用）
- [ ] 今日编译是否有新 Error？（是否有人提交了编译不过的代码）
- [ ] 是否有 #pragma warning(disable:...) 新增？（可能掩盖问题）

### 崩溃监控
- [ ] 崩溃日志目录是否有新 dump？（Saved/Crashes/）
- [ ] 是否有重复出现的崩溃模式？（同一调用栈多次出现）

### 性能基线
- [ ] 帧率基线是否有回归？（对比昨日/上周数据）
- [ ] 内存使用是否有异常增长？
- [ ] Draw Call 数量是否有异常增加？

### 内存健康
- [ ] 内存泄漏检测报告是否有新发现？
- [ ] UObject 数量趋势是否正常？
- [ ] 纹理/Mesh 内存是否在预算内？

### 任务队列
- [ ] RenderDoc 分析任务队列中是否有待处理的任务？
- [ ] Bug 修复队列中是否有紧急项？

### 补充项（从实践经验提炼）
- [ ] 发现新代码/配置变更 → 写 episode 到 `memory/episodes/YYYY-MM-DD.md`
- [ ] 每周一：合并 episodes/ → MEMORY.md（提炼关键信息）
- [ ] 每周一：清理临时文件

<!-- LOCAL-EXTENSIONS -->
<!-- LOCAL-EXTENSIONS -->
<!-- LOCAL-EXTENSIONS -->

## Refined additions from root CUSTOM

# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.
### 编译检查
- [ ] 检查最近一次编译是否有警告/错误
- [ ] 检查是否有未提交的代码变更
- [ ] 检查依赖库版本是否需要更新
### 崩溃检查
- [ ] 检查是否有新的崩溃报告
- [ ] 检查崩溃趋势（增加/减少）
- [ ] 检查是否有重复崩溃需要优先处理
### 性能检查
- [ ] 检查性能测试数据是否有回归
- [ ] 检查帧率是否稳定在目标范围
- [ ] 检查内存使用是否有异常增长
### 内存检查
- [ ] 检查内存泄漏报告
- [ ] 检查资源加载是否有异常
- [ ] 检查 GC 压力是否正常
**使用说明：**
- 勾选已完成的任务
- 新增检查项时添加到对应分类
- 定期清理过期的检查项
# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.
### 内存检查
- [ ] 检查内存泄漏报告
- [ ] 检查资源加载是否有异常
- [ ] 检查 GC 压力是否正常
**使用说明：**
- 勾选已完成的任务
- 新增检查项时添加到对应分类
- 定期清理过期的检查项
# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.
### 内存检查
- [ ] 检查内存泄漏报告
- [ ] 检查资源加载是否有异常
- [ ] 检查 GC 压力是否正常
**使用说明：**
- 勾选已完成的任务
- 新增检查项时添加到对应分类
- 定期清理过期的检查项

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

### 内存检查
- [ ] 检查内存泄漏报告
- [ ] 检查资源加载是否有异常
- [ ] 检查 GC 压力是否正常

**使用说明：**
- 勾选已完成的任务
- 新增检查项时添加到对应分类
- 定期清理过期的检查项
<!-- TEMPLATE:END -->



# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

---

## 每日任务
- [ ] 早上 10:00 发送问好（早安 + 毛泽东语录 + 天气）

## 🔧 引擎组检查项（Engine Agent 融合）

### 编译检查
- [ ] 检查最近一次编译是否有警告/错误
- [ ] 检查是否有未提交的代码变更
- [ ] 检查依赖库版本是否需要更新

### 崩溃检查
- [ ] 检查是否有新的崩溃报告
- [ ] 检查崩溃趋势（增加/减少）
- [ ] 检查是否有重复崩溃需要优先处理

### 性能检查
- [ ] 检查性能测试数据是否有回归
- [ ] 检查帧率是否稳定在目标范围
- [ ] 检查内存使用是否有异常增长

### 内存检查
- [ ] 检查内存泄漏报告
- [ ] 检查资源加载是否有异常
- [ ] 检查 GC 压力是否正常

---

**使用说明：**
- 勾选已完成的任务
- 新增检查项时添加到对应分类
- 定期清理过期的检查项
