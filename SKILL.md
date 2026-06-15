---
name: "macd-calculator-skill"
description: "计算股票MACD技术指标，包括DIF、DEA和MACD柱状图。当用户需要计算MACD指标时调用。"
---

# MACD指标计算技能 (MACD Calculator Skill)

提供专业的MACD技术指标计算功能。

## 核心功能

- **MACD指标计算**: DIF、DEA、MACD柱状图
- **EMA计算**: 支持自定义周期的指数移动平均
- **信号分析**: 自动检测金叉和死叉信号
- **统计分析**: 提供指标统计信息

## MACD计算公式

| 指标 | 公式 | 说明 |
|-----|------|------|
| **DIF** | EMA(12) - EMA(26) | 快线，反映短期趋势 |
| **DEA** | EMA(DIF, 9) | 慢线，信号线 |
| **MACD** | 2 × (DIF - DEA) | 柱状图，反映动能 |

## 输入参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|-------|------|------|--------|------|
| `input_file` | str | 是 | - | 输入Excel文件路径 |
| `output_file` | str | 否 | 自动生成 | 输出Excel文件路径 |
| `fast_period` | int | 否 | 12 | 快线EMA周期 |
| `slow_period` | int | 否 | 26 | 慢线EMA周期 |
| `signal_period` | int | 否 | 9 | 信号线周期 |
| `price_column` | str | 否 | Clsprc | 价格列名 |

## 输出结果

### 返回值

```python
{
    'status': 'success',           # 状态: success/error
    'output_file': str,            # 输出文件路径
    'message': str,                # 状态消息
    'statistics': dict,            # 指标统计信息
    'signals': {                   # 交易信号
        'golden_cross': list,      # 金叉信号列表
        'death_cross': list        # 死叉信号列表
    }
}
```

### 输出文件

生成的Excel文件，包含新增列：
- **EMA12**: 12日指数移动平均
- **EMA26**: 26日指数移动平均
- **DIF**: 快线（MACD线）
- **DEA**: 慢线（信号线）
- **MACD**: MACD柱状图

## 使用示例

### 基础用法

```python
from macd_calculator_skill import MACDCalculator

# 创建计算器实例
calculator = MACDCalculator()

# 计算MACD指标
result = calculator.calculate(
    input_file='000001靶机.xlsx',
    output_file='000001_MACD.xlsx'
)

if result['status'] == 'success':
    print(f"MACD计算完成: {result['output_file']}")
    print(f"金叉信号: {len(result['signals']['golden_cross'])}次")
    print(f"死叉信号: {len(result['signals']['death_cross'])}次")
```

### 自定义参数

```python
result = calculator.calculate(
    input_file='000001靶机.xlsx',
    output_file='result.xlsx',
    fast_period=10,
    slow_period=20,
    signal_period=7
)
```

### 命令行用法

```bash
python macd_calculator_skill.py \
    --input 000001靶机.xlsx \
    --output result.xlsx \
    --fast 12 \
    --slow 26 \
    --signal 9
```

## 文件结构

```
macd-calculator-skill/
├── SKILL.md                      # 主配置文件
├── macd_calculator_skill.py      # 核心计算模块
├── __init__.py                   # 包初始化文件
├── tests/
│   └── test_macd_calculator.py   # 单元测试
└── examples/
    └── usage_examples.py         # 使用示例
```

## 技术栈

- **Python**: 3.7+
- **pandas**: 数据处理
- **numpy**: 数值计算

## 依赖安装

```bash
pip install pandas numpy openpyxl
```

## 错误处理

| 错误类型 | 返回消息 |
|---------|---------|
| 文件不存在 | "输入文件不存在" |
| 数据为空 | "数据文件为空" |
| 列不存在 | "找不到指定的价格列" |

## 交易信号说明

### 金叉（买入信号）
- **条件**: DIF从下往上穿过DEA
- **意义**: 短期均线突破长期均线，可能预示上涨趋势开始

### 死叉（卖出信号）
- **条件**: DIF从上往下穿过DEA
- **意义**: 短期均线跌破长期均线，可能预示下跌趋势开始

## 作者信息

- 版本: 1.0.0
- 创建日期: 2026-06-15
- 适用场景: 股票技术分析、量化交易策略开发
