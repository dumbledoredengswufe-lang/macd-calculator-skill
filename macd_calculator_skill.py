#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MACD指标计算技能模块 (MACD Calculator Skill Module)

提供专业的MACD技术指标计算功能。
"""

import os
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional


class MACDCalculator:
    """
    MACD指标计算器
    
    计算股票的MACD指标，包括：
    - DIF（快线）: 12日EMA - 26日EMA
    - DEA（慢线）: DIF的9日EMA
    - MACD柱: 2 * (DIF - DEA)
    """
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        """
        初始化MACD计算器
        
        参数:
            fast_period: 快线EMA周期，默认12
            slow_period: 慢线EMA周期，默认26
            signal_period: 信号线DEA周期，默认9
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def calculate_ema(self, prices: np.ndarray, period: int) -> np.ndarray:
        """
        计算指数移动平均线（EMA）
        
        EMA计算公式：
        EMA(t) = α * price(t) + (1-α) * EMA(t-1)
        其中 α = 2 / (period + 1)
        
        参数:
            prices: 价格序列
            period: EMA周期
            
        返回:
            EMA序列
        """
        alpha = 2.0 / (period + 1)
        ema = np.zeros(len(prices))
        ema[0] = prices[0]
        
        for i in range(1, len(prices)):
            ema[i] = alpha * prices[i] + (1 - alpha) * ema[i-1]
        
        return ema
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        加载股票数据
        
        参数:
            filepath: Excel文件路径
            
        返回:
            DataFrame: 处理后的股票数据
            
        Raises:
            FileNotFoundError: 文件不存在时抛出
            ValueError: 数据为空时抛出
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        # 读取Excel文件（跳过前3行表头）
        df = pd.read_excel(filepath, header=0, skiprows=[1, 2])
        
        if df.empty:
            raise ValueError("数据文件为空")
        
        # 数据预处理
        df['Trddt'] = pd.to_datetime(df['Trddt'])
        df.set_index('Trddt', inplace=True)
        
        return df
    
    def calculate(self, input_file: str, output_file: str = None, 
                  price_column: str = 'Clsprc') -> Dict[str, Any]:
        """
        计算MACD指标
        
        参数:
            input_file: 输入Excel文件路径
            output_file: 输出Excel文件路径（可选）
            price_column: 价格列名
            
        返回:
            Dict: 包含状态、统计信息和信号的字典
        """
        try:
            # 设置默认输出文件
            if output_file is None:
                output_file = f"{os.path.splitext(input_file)[0]}_MACD.xlsx"
            
            # 加载数据
            df = self.load_data(input_file)
            
            if price_column not in df.columns:
                return {
                    'status': 'error',
                    'output_file': None,
                    'message': f"找不到指定的价格列: {price_column}",
                    'statistics': None,
                    'signals': None
                }
            
            # 提取价格数据
            prices = df[price_column].values
            
            # 计算EMA和MACD
            ema_fast = self.calculate_ema(prices, self.fast_period)
            ema_slow = self.calculate_ema(prices, self.slow_period)
            dif = ema_fast - ema_slow
            dea = self.calculate_ema(dif, self.signal_period)
            macd_histogram = 2 * (dif - dea)
            
            # 添加到DataFrame
            df['EMA12'] = ema_fast
            df['EMA26'] = ema_slow
            df['DIF'] = dif
            df['DEA'] = dea
            df['MACD'] = macd_histogram
            
            # 获取统计信息
            statistics = self.get_statistics(df)
            
            # 分析交易信号
            signals = self.analyze_signals(df)
            
            # 保存结果
            df.to_excel(output_file)
            
            return {
                'status': 'success',
                'output_file': output_file,
                'message': "MACD指标计算完成",
                'statistics': statistics,
                'signals': signals
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'output_file': None,
                'message': str(e),
                'statistics': None,
                'signals': None
            }
    
    def get_statistics(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        获取MACD指标统计信息
        
        参数:
            df: 包含MACD指标的DataFrame
            
        返回:
            dict: 统计信息字典
        """
        return {
            'DIF': {
                'mean': float(df['DIF'].mean()),
                'std': float(df['DIF'].std()),
                'max': float(df['DIF'].max()),
                'min': float(df['DIF'].min())
            },
            'DEA': {
                'mean': float(df['DEA'].mean()),
                'std': float(df['DEA'].std()),
                'max': float(df['DEA'].max()),
                'min': float(df['DEA'].min())
            },
            'MACD': {
                'mean': float(df['MACD'].mean()),
                'std': float(df['MACD'].std()),
                'max': float(df['MACD'].max()),
                'min': float(df['MACD'].min())
            }
        }
    
    def analyze_signals(self, df: pd.DataFrame) -> Dict[str, List[Dict[str, Any]]]:
        """
        分析MACD交易信号
        
        参数:
            df: 包含MACD指标的DataFrame
            
        返回:
            dict: 信号分析结果
        """
        signals = {
            'golden_cross': [],  # 金叉（DIF上穿DEA）
            'death_cross': []    # 死叉（DIF下穿DEA）
        }
        
        for i in range(1, len(df)):
            # 金叉检测
            if df['DIF'].iloc[i-1] <= df['DEA'].iloc[i-1] and df['DIF'].iloc[i] > df['DEA'].iloc[i]:
                signals['golden_cross'].append({
                    'date': str(df.index[i].date()),
                    'price': float(df['Clsprc'].iloc[i]),
                    'DIF': float(df['DIF'].iloc[i]),
                    'DEA': float(df['DEA'].iloc[i])
                })
            
            # 死叉检测
            elif df['DIF'].iloc[i-1] >= df['DEA'].iloc[i-1] and df['DIF'].iloc[i] < df['DEA'].iloc[i]:
                signals['death_cross'].append({
                    'date': str(df.index[i].date()),
                    'price': float(df['Clsprc'].iloc[i]),
                    'DIF': float(df['DIF'].iloc[i]),
                    'DEA': float(df['DEA'].iloc[i])
                })
        
        return signals
    
    def get_latest_signal(self, df: pd.DataFrame) -> Optional[str]:
        """
        获取最新的交易信号
        
        参数:
            df: 包含MACD指标的DataFrame
            
        返回:
            str: 'golden_cross' / 'death_cross' / None
        """
        signals = self.analyze_signals(df)
        
        if len(signals['golden_cross']) == 0 and len(signals['death_cross']) == 0:
            return None
        
        # 比较最后一次金叉和死叉的日期
        if len(signals['golden_cross']) == 0:
            return 'death_cross'
        if len(signals['death_cross']) == 0:
            return 'golden_cross'
        
        last_golden = signals['golden_cross'][-1]['date']
        last_death = signals['death_cross'][-1]['date']
        
        return 'golden_cross' if last_golden > last_death else 'death_cross'


def calculate_macd(input_file: str, output_file: str = None, **kwargs) -> Dict[str, Any]:
    """
    便捷函数：计算MACD指标
    
    参数:
        input_file: 输入文件路径
        output_file: 输出文件路径
        **kwargs: 其他参数（fast_period, slow_period, signal_period, price_column）
        
    返回:
        Dict: 结果字典
    """
    calculator = MACDCalculator(
        fast_period=kwargs.get('fast_period', 12),
        slow_period=kwargs.get('slow_period', 26),
        signal_period=kwargs.get('signal_period', 9)
    )
    
    return calculator.calculate(
        input_file=input_file,
        output_file=output_file,
        price_column=kwargs.get('price_column', 'Clsprc')
    )


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='MACD指标计算工具')
    parser.add_argument('--input', '-i', required=True, help='输入Excel文件')
    parser.add_argument('--output', '-o', help='输出Excel文件')
    parser.add_argument('--fast', type=int, default=12, help='快线周期')
    parser.add_argument('--slow', type=int, default=26, help='慢线周期')
    parser.add_argument('--signal', type=int, default=9, help='信号线周期')
    
    args = parser.parse_args()
    
    result = calculate_macd(
        input_file=args.input,
        output_file=args.output,
        fast_period=args.fast,
        slow_period=args.slow,
        signal_period=args.signal
    )
    
    if result['status'] == 'success':
        print(f"✅ {result['message']}")
        print(f"📁 输出文件: {result['output_file']}")
        print(f"\n📊 统计信息:")
        for indicator, stats in result['statistics'].items():
            print(f"  {indicator}: 均值={stats['mean']:.4f}, 最大={stats['max']:.4f}, 最小={stats['min']:.4f}")
        print(f"\n📈 交易信号:")
        print(f"  金叉: {len(result['signals']['golden_cross'])}次")
        print(f"  死叉: {len(result['signals']['death_cross'])}次")
    else:
        print(f"❌ {result['message']}")
