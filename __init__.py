#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MACD指标计算技能包 (MACD Calculator Skill Package)

提供专业的MACD技术指标计算功能。
"""

try:
    from .macd_calculator_skill import MACDCalculator, calculate_macd
except ImportError:
    from macd_calculator_skill import MACDCalculator, calculate_macd

__version__ = '1.0.0'
__author__ = 'MACD Calculator Skill Team'
__all__ = ['MACDCalculator', 'calculate_macd']

__doc__ = """
MACD指标计算技能包

功能:
- 计算MACD技术指标（DIF、DEA、MACD柱）
- 检测金叉和死叉交易信号
- 提供指标统计分析

快速开始:
    from macd_calculator_skill import MACDCalculator
    
    calculator = MACDCalculator()
    result = calculator.calculate(input_file='data.xlsx', output_file='result.xlsx')
"""
