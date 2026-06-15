# MACD Calculator Skill

MACD指标计算技能模块 - 提供专业的MACD技术指标计算功能。

## 功能特点

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

## 安装

```bash
pip install pandas numpy openpyxl
```

## 快速开始

### Python API

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

### 命令行

```bash
python macd_calculator_skill.py \
    --input 000001靶机.xlsx \
    --output result.xlsx \
    --fast 12 \
    --slow 26 \
    --signal 9
```

## 项目结构

```
macd-calculator-skill/
├── SKILL.md                      # 技能配置文档
├── macd_calculator_skill.py      # 核心计算模块
├── __init__.py                   # 包初始化文件
├── README.md                     # 项目说明文档
├── .gitignore                    # Git忽略文件
└── tests/
    └── test_macd_calculator.py   # 单元测试
```

## 测试

运行单元测试：

```bash
pytest tests/test_macd_calculator.py -v
```

## 许可证

MIT License

## 作者

MACD Calculator Skill Team
