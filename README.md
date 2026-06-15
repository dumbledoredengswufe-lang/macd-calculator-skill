# MACD Calculator Skill

MACD指标计算技能模块 - 提供专业的MACD技术指标计算功能。

## 功能特点

- **MACD指标计算**: DIF、DEA、MACD柱状图
- **EMA计算**: 支持自定义周期的指数移动平均
- **信号分析**: 自动检测金叉和死叉信号
- **统计分析**: 提供指标统计信息

## 安装

```bash
pip install pandas numpy openpyxl
```

## 快速开始

```python
from macd_calculator_skill import MACDCalculator

calculator = MACDCalculator()
result = calculator.calculate(
    input_file='000001靶机.xlsx',
    output_file='000001_MACD.xlsx'
)
```

## 许可证

MIT License
