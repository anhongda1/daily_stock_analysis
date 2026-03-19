# -*- coding: utf-8 -*-
"""
Shared defaults for trading skills.

This module centralises:
1. The default active skill set used by agent entrypoints
2. The fallback skill subset used by the multi-agent router
3. Common prompt fragments that previously drifted across multiple files
4. Helper utilities for skill-specific agent naming
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional


DEFAULT_ACTIVE_SKILL_IDS: tuple[str, ...] = (
    "bull_trend",
    "ma_golden_cross",
    "volume_breakout",
    "shrink_pullback",
)

DEFAULT_ROUTER_SKILL_IDS: tuple[str, ...] = (
    "bull_trend",
    "shrink_pullback",
)

PRIMARY_DEFAULT_SKILL_ID = DEFAULT_ACTIVE_SKILL_IDS[0]

REGIME_SKILL_IDS: Dict[str, List[str]] = {
    "trending_up": ["bull_trend", "volume_breakout", "ma_golden_cross"],
    "trending_down": ["shrink_pullback", "bottom_volume"],
    "sideways": ["box_oscillation", "shrink_pullback"],
    "volatile": ["chan_theory", "wave_theory"],
    "sector_hot": ["dragon_head", "emotion_cycle"],
}

SKILL_AGENT_PREFIX = "skill_"
LEGACY_STRATEGY_AGENT_PREFIX = "strategy_"
SKILL_CONSENSUS_AGENT_NAME = "skill_consensus"
LEGACY_STRATEGY_CONSENSUS_AGENT_NAME = "strategy_consensus"

CORE_TRADING_SKILL_POLICY_ZH = """## 默认技能基线（必须严格遵守）

当前激活的 skills 可以补充细化分析视角，但默认风险控制和交易节奏必须遵守以下基线。

### 1. 严进策略（不追高）
- **绝对不追高**：当股价偏离 MA5 超过 5% 时，坚决不买入
- 乖离率 < 2%：最佳买点区间
- 乖离率 2-5%：可小仓介入
- 乖离率 > 5%：严禁追高！直接判定为"观望"

### 2. 趋势交易（顺势而为）
- **多头排列必须条件**：MA5 > MA10 > MA20
- 只做多头排列的股票，空头排列坚决不碰
- 均线发散上行优于均线粘合

### 3. 效率优先（筹码结构）
- 关注筹码集中度：90%集中度 < 15% 表示筹码集中
- 获利比例分析：70-90% 获利盘时需警惕获利回吐
- 平均成本与现价关系：现价高于平均成本 5-15% 为健康

### 4. 买点偏好（回踩支撑）
- **最佳买点**：缩量回踩 MA5 获得支撑
- **次优买点**：回踩 MA10 获得支撑
- **观望情况**：跌破 MA20 时观望

### 5. 风险排查重点
- 减持公告、业绩预亏、监管处罚、行业政策利空、大额解禁

### 6. 估值关注（PE/PB）
- PE 明显偏高时需在风险点中说明

### 7. 强势趋势股放宽
- 强势趋势股可适当放宽乖离率要求，轻仓追踪但需设止损
"""

TECHNICAL_SKILL_RULES_EN = """## Default Skill Baseline

Treat the currently activated skills as the primary analysis lens, but keep the
following default risk controls as the shared baseline:

- Bullish alignment: MA5 > MA10 > MA20
- Bias from MA5 < 2% -> ideal buy zone; 2-5% -> small position; > 5% -> no chase
- Shrink-pullback to MA5 is the preferred entry rhythm
- Below MA20 -> hold off unless the active skill explicitly proves a better setup
"""


def get_default_active_skill_ids(max_count: Optional[int] = None) -> List[str]:
    skills = list(DEFAULT_ACTIVE_SKILL_IDS)
    if max_count is None:
        return skills
    return skills[:max_count]


def get_default_router_skill_ids(max_count: Optional[int] = None) -> List[str]:
    skills = list(DEFAULT_ROUTER_SKILL_IDS)
    if max_count is None:
        return skills
    return skills[:max_count]


def get_primary_default_skill_id(available_skill_ids: Optional[Iterable[str]] = None) -> str:
    if available_skill_ids is None:
        return PRIMARY_DEFAULT_SKILL_ID

    available = [skill_id for skill_id in available_skill_ids if isinstance(skill_id, str) and skill_id]
    if not available:
        return ""

    for skill_id in DEFAULT_ACTIVE_SKILL_IDS:
        if skill_id in available:
            return skill_id
    return available[0]


def build_skill_agent_name(skill_id: str) -> str:
    return f"{SKILL_AGENT_PREFIX}{skill_id}"


def extract_skill_id(agent_name: Optional[str]) -> Optional[str]:
    if not agent_name or not isinstance(agent_name, str):
        return None
    for prefix in (SKILL_AGENT_PREFIX, LEGACY_STRATEGY_AGENT_PREFIX):
        if agent_name.startswith(prefix):
            return agent_name[len(prefix):]
    return None


def is_skill_agent_name(agent_name: Optional[str]) -> bool:
    return extract_skill_id(agent_name) is not None


def is_skill_consensus_name(agent_name: Optional[str]) -> bool:
    return agent_name in {SKILL_CONSENSUS_AGENT_NAME, LEGACY_STRATEGY_CONSENSUS_AGENT_NAME}
