# -*- coding: utf-8 -*-
"""Generate Obsidian Canvas knowledge graph for the book. One-shot helper."""
from __future__ import annotations

import json
import secrets
from pathlib import Path

BOOK = "book/深入理解 AI Agent.md"

ids: dict[str, str] = {}


def nid(name: str) -> str:
    if name not in ids:
        ids[name] = secrets.token_hex(8)
    return ids[name]


def text(name, x, y, w, h, body, color=None):
    n = {
        "id": nid(name),
        "type": "text",
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "text": body,
    }
    if color:
        n["color"] = color
    return n


def file_node(name, x, y, w, h, subpath, color=None):
    n = {
        "id": nid(name),
        "type": "file",
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "file": BOOK,
        "subpath": subpath,
    }
    if color:
        n["color"] = color
    return n


def group(name, x, y, w, h, label, color=None):
    n = {
        "id": nid(name),
        "type": "group",
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "label": label,
    }
    if color:
        n["color"] = color
    return n


def edge(name, src, dst, side_from="right", side_to="left", label=None, color=None):
    e = {
        "id": nid(name),
        "fromNode": nid(src),
        "fromSide": side_from,
        "toNode": nid(dst),
        "toSide": side_to,
        "toEnd": "arrow",
    }
    if label:
        e["label"] = label
    if color:
        e["color"] = color
    return e


# Groups first (bottom z-index)
nodes = [
    group("g-core", 20, 20, 4780, 280, "核心公式 · 三层同一对象", "5"),
    group("g-build", 20, 340, 4780, 1220, "第一部分 · 如何构建 Agent（第1–6章）", "4"),
    group("g-pattern", 20, 1600, 4780, 280, "贯穿全书的设计模式", "3"),
    group("g-improve", 20, 1920, 3180, 1120, "第二部分 · 如何提升 Agent 能力（第7–9章）", "6"),
    group("g-collab", 3260, 1920, 1540, 1120, "协作 · 第10章 多 Agent", "1"),
]

# --- Core row ---
nodes += [
    text(
        "n-title",
        50,
        60,
        420,
        200,
        "# 深入理解 AI Agent\n\n知识图谱\n点击章节卡片跳转正文",
        "5",
    ),
    text(
        "n-hub",
        500,
        60,
        520,
        200,
        "# Agent = LLM + 上下文 + 工具\n\n大脑 + 眼睛 + 手脚\nPolicy + Observation + Action",
        "5",
    ),
    text(
        "n-llm",
        1060,
        60,
        300,
        200,
        "## LLM · 大脑\n\n决策内核 / Policy\n预训练知识 + 后训练策略",
        "6",
    ),
    text(
        "n-ctx",
        1390,
        60,
        300,
        200,
        "## 上下文 · 眼睛\n\n模型能看到的一切\n含工具定义与轨迹",
        "4",
    ),
    text(
        "n-tool",
        1720,
        60,
        300,
        200,
        "## 工具 · 手脚\n\n感知 / 改变世界\nAction Space",
        "2",
    ),
    text(
        "n-harness",
        2050,
        60,
        340,
        200,
        "## Harness = Model 之外\n\n约束 · 验证 · 纠正\n模型会一层层吃掉它",
        "3",
    ),
    file_node("f-intro", 2430, 60, 380, 90, "#引言", "5"),
    file_node("f-after", 2430, 170, 380, 90, "#后记：回到 Agent = LLM + 上下文 + 工具", "5"),
    text(
        "n-legend",
        2860,
        60,
        560,
        200,
        "## 图例\n\n青=公式　紫=模型　绿=上下文\n橙=工具　黄=模式　红=协作/风险",
        "5",
    ),
    file_node("f-answers", 3470, 60, 400, 90, "#思考题参考答案"),
    text(
        "n-code",
        3470,
        170,
        400,
        90,
        "实验代码 → `code/chapter1`–`chapter10`",
    ),
    text(
        "n-react",
        3920,
        60,
        840,
        200,
        "## ReAct 循环\n\n思考 → 行动 → 观察 → 再思考\n轨迹只增不改，任务在循环里推进",
        "5",
    ),
]

# --- Build: 6 chapter columns ---
# col x: 50, 840, 1630, 2420, 3210, 4000
chapters = [
    {
        "key": "c1",
        "x": 50,
        "sub": "#第1章 AI Agent 入门",
        "color": "5",
        "cards": [
            ("c1-space", "## 观察空间 / 动作空间\n\n模型与世界的接口"),
            ("c1-react", "## ReAct 与核心循环\n\n思考 · 行动 · 观察"),
            ("c1-harness", "## Harness 五要素\n\n上下文 · 工具 · 约束 · 验证 · 纠正"),
            ("c1-orch", "## 编排光谱\n\n提示 → 工作流 → 自主 Agent"),
            ("c1-update", "## 三条更新路径\n\n上下文内 · 外部产物 · 参数"),
        ],
    },
    {
        "key": "c2",
        "x": 840,
        "sub": "#第2章 上下文工程",
        "color": "4",
        "cards": [
            ("c2-msg", "## 上下文 = 消息列表\n\n系统 / 用户 / 助手 / 工具"),
            ("c2-kv", "## KV Cache 友好\n\n前缀稳定 · 只增不改"),
            ("c2-prompt", "## 提示工程 + 注入攻防\n\n流程驱动，而非规则堆砌"),
            ("c2-skill", "## Agent Skills\n\n元数据常驻，正文按需加载"),
            ("c2-comp", "## 状态栏 · 分层压缩\n\n隔离优于压缩（子 Agent）"),
        ],
    },
    {
        "key": "c3",
        "x": 1630,
        "sub": "#第3章 用户记忆和知识库",
        "color": "4",
        "cards": [
            ("c3-mem", "## 用户记忆\n\n四格式 · 三层次评估"),
            ("c3-rag", "## RAG 管道\n\n分块 · 稠密/稀疏 · 混合检索"),
            ("c3-org", "## 知识组织\n\n结构化索引 · 文件系统范式"),
            ("c3-agentic", "## Agentic RAG\n\n检索工具化，Agent 自决"),
            ("c3-priv", "## 更新与隐私\n\n事件式记忆 · 日志脱敏"),
        ],
    },
    {
        "key": "c4",
        "x": 2420,
        "sub": "#第4章 工具",
        "color": "2",
        "cards": [
            ("c4-kind", "## 工具分类\n\n感知 · 执行 · 协作 · 事件 · 沟通"),
            ("c4-design", "## 设计原则\n\n专用 / 通用执行器 / Skill"),
            ("c4-mcp", "## MCP 与 Skill Hub\n\n互操作与生态"),
            ("c4-disc", "## 工具太多\n\n层次化 + 主动发现"),
            ("c4-safe", "## 执行安全\n\n权限 · 不可逆操作 · Sidecar"),
        ],
    },
    {
        "key": "c5",
        "x": 3210,
        "sub": "#第5章 Coding Agent 与通用 Agent",
        "color": "2",
        "cards": [
            ("c5-core", "## Coding 是通用内核\n\nManus → OpenClaw"),
            ("c5-flow", "## 流程与 Harness\n\n搜索 · 编辑 · 测试 · 恢复"),
            ("c5-meta", "## 代码的六种角色\n\n思考 · 规则 · 媒体 · 适配 · UI · 自举"),
            ("c5-boot", "## Agent 自举\n\n代码创造代码"),
            ("c5-sec", "## Coding 安全\n\n沙箱 · 责任归属"),
        ],
    },
    {
        "key": "c6",
        "x": 4000,
        "sub": "#第6章 交互：观察与动作空间的扩展",
        "color": "2",
        "cards": [
            ("c6-async", "## 异步与事件驱动\n\n世界主动找上门"),
            ("c6-voice", "## 语音三范式\n\n级联 · Omni · 全双工"),
            ("c6-gui", "## Computer Use\n\nGrounding · 世界模型"),
            ("c6-robot", "## 机器人 / VLA\n\n规划 + 低层控制"),
            ("c6-prim", "## 共享原语\n\n唤醒 · 取消 · 快慢路径"),
        ],
    },
]

for ch in chapters:
    x = ch["x"]
    nodes.append(file_node(ch["key"], x, 400, 740, 88, ch["sub"], ch["color"]))
    y = 510
    for key, body in ch["cards"]:
        nodes.append(text(key, x, y, 740, 112, body, ch["color"]))
        y += 132

# --- Patterns ---
patterns = [
    ("p-pr", 50, "## 提议者—审核者\n\n产出与评判分上下文。自审不可靠。→ 知识更新 / 工具审批 / 评估 / 协作"),
    ("p-pd", 1000, "## 渐进式披露\n\n先给目录，再按需加载。→ Skills / 分层检索 / 工具发现 / Agent 发现"),
    ("p-ao", 1950, "## 只增不改\n\n可缓存、可重放、可审计。→ KV Cache 前缀 / 事件记忆 / 工具 schema"),
    ("p-br", 2900, "## 边界集 + 保留集\n\n该变的变、不该变的稳住。→ 回归 / 训评隔离 / 更新提案"),
    ("p-md", 3850, "## 最小 diff + 可回滚\n\n小改、带来源、能撤回。→ 知识补丁 / 代码补丁 / Prompt 更新"),
]
for key, x, body in patterns:
    nodes.append(text(key, x, 1660, 900, 180, body, "3"))

# --- Improve ---
improve = [
    {
        "key": "c7",
        "x": 50,
        "sub": "#第7章 Agent 的评估",
        "color": "6",
        "cards": [
            ("c7-task", "## 任务解剖 · τ²-bench\n\n环境 · 用户 · 工具 · 成功标准"),
            ("c7-metric", "## Pass@k vs Pass^k\n\n上限能力 ≠ 业务可靠性"),
            ("c7-judge", "## LLM-as-a-Judge\n\n失败归因 · 轨迹前缀回归"),
            ("c7-obs", "## 可观测性 → 改进闭环\n\n消融 · AB · 特性开关"),
            ("c7-sim", "## 仿真环境\n\n评估到后训练的桥梁"),
        ],
    },
    {
        "key": "c8",
        "x": 1100,
        "sub": "#第8章 模型后训练",
        "color": "6",
        "cards": [
            ("c8-4", "## 四阶段\n\n预训练 → Mid → SFT → RL"),
            ("c8-sft", "## SFT 记忆 · RL 泛化\n\n数据与环境比算法更重要"),
            ("c8-env", "## RL 环境与多轮\n\n信用分配 · 工具即环境"),
            ("c8-rew", "## 奖励设计\n\n规则 / 偏好 / 模型 · RLVP"),
            ("c8-dist", "## 蒸馏与案例回流\n\n过早结束 · 编辑失败"),
        ],
    },
    {
        "key": "c9",
        "x": 2150,
        "sub": "#第9章 Agent 的持续进化",
        "color": "6",
        "cards": [
            ("c9-sig", "## 学习信号\n\n环境结果 · 过程规则 · Rubric"),
            ("c9-k", "## 经验 → 知识文档"),
            ("c9-i", "## 经验 → 指令 / Skills"),
            ("c9-p", "## 经验 → 程序 / Harness"),
            ("c9-w", "## 经验 → 参数 · 睡眠学习"),
        ],
    },
]
for ch in improve:
    x = ch["x"]
    nodes.append(file_node(ch["key"], x, 1980, 1000, 88, ch["sub"], ch["color"]))
    y = 2090
    for key, body in ch["cards"]:
        nodes.append(text(key, x, y, 1000, 160, body, ch["color"]))
        y += 180

# --- Collab ---
nodes += [
    file_node("c10", 3300, 1980, 1460, 88, "#第10章 多 Agent 协作", "1"),
    text("c10-dim", 3300, 2090, 710, 160, "## 分类两维度\n\n上下文共享？ × 对等 / 管理者 / 去中心", "1"),
    text("c10-when", 4050, 2090, 710, 160, "## 何时优于单 Agent\n\n不是辩论，是隔离与并行", "1"),
    text("c10-share", 3300, 2270, 710, 160, "## 共享上下文\n\n协调快，多样性差", "1"),
    text("c10-noshare", 4050, 2270, 710, 160, "## 不共享 + 文件系统\n\n通信 · 控制 · A2A", "1"),
    text("c10-fail", 3300, 2450, 1460, 200, "## 六种失败模式\n\n并发冲突 · 错误级联 · 同质趋同 · 互相扯皮 · 循环失控 · 理解债", "1"),
    text("c10-soc", 3300, 2670, 1460, 160, "## Agent 社会 / 经济\n\nAI 小镇 · Agentopia · Moltbook · Vending-Bench", "1"),
    text(
        "n-cloud",
        3300,
        2850,
        1460,
        150,
        "## 后记两朵乌云\n\n① 实时流式交互（→ 第6章）　② 上岗后持续学习（→ 第3、9章）",
        "5",
    ),
]

# --- Edges ---
edges = [
    # formula
    edge("e-hub-llm", "n-hub", "n-llm", "right", "left", color="5"),
    edge("e-hub-ctx", "n-hub", "n-ctx", "right", "left", color="5"),
    edge("e-hub-tool", "n-hub", "n-tool", "right", "left", color="5"),
    edge("e-hub-harness", "n-hub", "n-harness", "bottom", "left", "生产形态", "3"),
    edge("e-hub-react", "n-hub", "n-react", "right", "left", "运行时", "5"),
    edge("e-intro-hub", "f-intro", "n-hub", "left", "right", color="5"),
    edge("e-after-hub", "f-after", "n-hub", "left", "bottom", "回到公式", "5"),
    # pillars to chapters
    edge("e-llm-c1", "n-llm", "c1", "bottom", "top", color="6"),
    edge("e-llm-c8", "n-llm", "c8", "bottom", "top", "策略写入参数", "6"),
    edge("e-ctx-c2", "n-ctx", "c2", "bottom", "top", "会话内眼睛", "4"),
    edge("e-ctx-c3", "n-ctx", "c3", "bottom", "top", "跨会话延伸", "4"),
    edge("e-tool-c4", "n-tool", "c4", "bottom", "top", color="2"),
    edge("e-tool-c5", "n-tool", "c5", "bottom", "top", "元能力", "2"),
    edge("e-tool-c6", "n-tool", "c6", "bottom", "top", "空间扩展", "2"),
    edge("e-harness-c1", "n-harness", "c1-harness", "bottom", "top", color="3"),
    edge("e-react-c1", "n-react", "c1-react", "bottom", "top", color="5"),
    # build chain
    edge("e-c1-c2", "c1", "c2", "right", "left", "先看清眼睛", "4"),
    edge("e-c2-c3", "c2", "c3", "right", "left", "超出当前会话", "4"),
    edge("e-c3-c4", "c3", "c4", "right", "left", "知识变成行动", "2"),
    edge("e-c4-c5", "c4", "c5", "right", "left", "用代码创造工具", "2"),
    edge("e-c5-c6", "c5", "c6", "right", "left", "动作空间出文本", "2"),
    # harness mapping
    edge("e-h-c2", "c1-harness", "c2", "right", "left", "上下文管理", "3"),
    edge("e-h-c3", "c1-harness", "c3", "bottom", "left", "跨会话", "3"),
    edge("e-h-c4", "c1-harness", "c4", "bottom", "left", "接口与约束", "3"),
    edge("e-h-c5", "c1-harness", "c5", "bottom", "left", "验证与纠正", "3"),
    # key concept links
    edge("e-skill-disc", "c2-skill", "c4-disc", "right", "left", "按需查阅", "3"),
    edge("e-skill-c9", "c2-skill", "c9-i", "bottom", "top", color="4"),
    edge("e-kv-ao", "c2-kv", "p-ao", "bottom", "top", color="3"),
    edge("e-comp-iso", "c2-comp", "c10-noshare", "bottom", "top", "隔离优于压缩", "4"),
    edge("e-agentic-c4", "c3-agentic", "c4", "right", "left", "检索工具化", "4"),
    edge("e-mem-c9", "c3-mem", "c9-k", "bottom", "top", "经验沉淀", "4"),
    edge("e-c5-boot-c9", "c5-boot", "c9-p", "bottom", "top", "改自己的程序", "2"),
    edge("e-c6-cloud", "c6-async", "n-cloud", "bottom", "top", "乌云① 实时", "2"),
    # improve chain
    edge("e-c6-c7", "c6", "c7", "bottom", "top", "先能量化再进化", "6"),
    edge("e-c7-c8", "c7", "c8", "right", "left", "评估环境 → 训练场", "6"),
    edge("e-c7-c9", "c7-obs", "c9", "right", "left", "没有评估就没有进步", "6"),
    edge("e-c8-c9w", "c8", "c9-w", "right", "left", "参数载体", "6"),
    edge("e-c7-sim-c8", "c7-sim", "c8-env", "right", "left", "同一座桥", "6"),
    edge("e-update-c9", "c1-update", "c9", "bottom", "top", "三条路径展开", "6"),
    edge("e-c9-hub", "c9", "n-hub", "top", "bottom", "进化回到公式", "5"),
    # collab
    edge("e-c2-c10", "c2", "c10-dim", "bottom", "top", "上下文是否共享", "1"),
    edge("e-c5-c10", "c5-core", "c10-noshare", "bottom", "left", "文件系统协作", "1"),
    edge("e-c10-pr", "p-pr", "c10-when", "bottom", "top", "不能自审", "1"),
    edge("e-cloud-c9", "n-cloud", "c9-sig", "left", "right", "乌云② 学习", "5"),
    # patterns to chapters
    edge("e-pr-c3", "p-pr", "c3-org", "top", "bottom", color="3"),
    edge("e-pr-c7", "p-pr", "c7-judge", "bottom", "top", color="3"),
    edge("e-pd-c2", "p-pd", "c2-skill", "top", "bottom", color="3"),
    edge("e-br-c7", "p-br", "c7-metric", "bottom", "top", color="3"),
    edge("e-md-c5", "p-md", "c5-flow", "top", "bottom", color="3"),
    edge("e-md-c9", "p-md", "c9-p", "bottom", "top", color="3"),
    # flywheel
    edge("e-fly-h", "n-harness", "c8-sft", "bottom", "top", "Harness 坑 → 训练信号", "6"),
    edge("e-fly-m", "c8", "n-harness", "top", "bottom", "模型内化 → 删掉一层", "6"),
]

canvas = {"nodes": nodes, "edges": edges}

# validate
node_ids = [n["id"] for n in nodes]
edge_ids = [e["id"] for e in edges]
all_ids = node_ids + edge_ids
assert len(all_ids) == len(set(all_ids)), "duplicate ids"
idset = set(node_ids)
for e in edges:
    assert e["fromNode"] in idset, e
    assert e["toNode"] in idset, e
    assert e.get("fromSide") in {None, "top", "right", "bottom", "left"}
    assert e.get("toSide") in {None, "top", "right", "bottom", "left"}

out = Path(__file__).with_name("知识图谱.canvas")
out.write_text(json.dumps(canvas, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {out}")
print(f"nodes={len(nodes)} edges={len(edges)}")
