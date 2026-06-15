#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MACD指标计算单元测试

使用 pytest 框架进行单元测试，验证MACD计算功能的正确性。
"""

import pytest
import pandas as pd
import numpy as np
import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from macd_calculator_skill import MACDCalculator, calculate_macd


class TestMACDCalculator:
    """MACDCalculator类测试"""
    
    def test_initialization(self):
        """测试初始化"""
        calculator = MACDCalculator()
        assert calculator is not None
        assert calculator.fast_period == 12
        assert calculator.slow_period == 26
        assert calculator.signal_period == 9
    
    def test_initialization_custom_params(self):
        """测试自定义参数初始化"""
        calculator = MACDCalculator(fast_period=10, slow_period=20, signal_period=7)
        assert calculator.fast_period == 10
        assert calculator.slow_period == 20
        assert calculator.signal_period == 7
    
    def test_calculate_ema(self):
        """测试EMA计算"""
        calculator = MACDCalculator()
        prices = np.array([10.0, 11.0, 12.0, 13.0, 14.0])
        
        ema = calculator.calculate_ema(prices, 5)
        
        assert ema is not None
        assert len(ema) == 5
        assert ema[0] == 10.0
        # EMA应该在价格范围内
        assert ema[-1] >= min(prices)
        assert ema[-1] <= max(prices)
    
    def test_calculate_ema_single_value(self):
        """测试单个值的EMA计算"""
        calculator = MACDCalculator()
        prices = np.array([100.0])
        
        ema = calculator.calculate_ema(prices, 10)
        
        assert len(ema) == 1
        assert ema[0] == 100.0
    
    def test_load_data_success(self):
        """测试数据加载成功"""
        dates = pd.date_range('2021-01-01', periods=30)
        df = pd.DataFrame({
            'Trddt': dates,
            'Clsprc': np.linspace(10, 20, 30)
        })
        
        # 模拟真实Excel文件格式，包含额外的表头行
        temp_file = 'test_macd_data.xlsx'
        csv_content = "Trddt,Clsprc\n"
        csv_content += "日期,收盘价\n"
        csv_content += "YYYY-MM-DD,元\n"
        for i in range(len(df)):
            row = df.iloc[i]
            csv_content += f"{row['Trddt'].strftime('%Y-%m-%d')},{row['Clsprc']}\n"
        
        from io import StringIO
        test_df = pd.read_csv(StringIO(csv_content))
        test_df.to_excel(temp_file, index=False)
        
        calculator = MACDCalculator()
        loaded_df = calculator.load_data(temp_file)
        
        assert loaded_df is not None
        assert len(loaded_df) == 30
        assert 'Clsprc' in loaded_df.columns
        
        os.remove(temp_file)
    
    def test_load_data_file_not_found(self):
        """测试文件不存在"""
        calculator = MACDCalculator()
        with pytest.raises(FileNotFoundError):
            calculator.load_data('nonexistent_file.xlsx')
    
    def test_calculate_macd(self):
        """测试MACD计算"""
        dates = pd.date_range('2021-01-01', periods=50)
        df = pd.DataFrame({
            'Trddt': dates,
            'Clsprc': np.linspace(10, 20, 50)
        })
        
        temp_file = 'test_macd_calc.xlsx'
        df.to_excel(temp_file, index=False)
        
        result = calculate_macd(temp_file, 'test_macd_result.xlsx')
        
        assert result['status'] == 'success'
        assert os.path.exists('test_macd_result.xlsx')
        
        # 验证结果
        result_df = pd.read_excel('test_macd_result.xlsx')
        assert 'DIF' in result_df.columns
        assert 'DEA' in result_df.columns
        assert 'MACD' in result_df.columns
        assert 'EMA12' in result_df.columns
        assert 'EMA26' in result_df.columns
        
        os.remove(temp_file)
        os.remove('test_macd_result.xlsx')
    
    def test_calculate_macd_empty_data(self):
        """测试空数据"""
        df = pd.DataFrame({'Trddt': [], 'Clsprc': []})
        temp_file = 'test_empty.xlsx'
        df.to_excel(temp_file, index=False)
        
        result = calculate_macd(temp_file, 'test_empty_result.xlsx')
        
        assert result['status'] == 'error'
        
        os.remove(temp_file)
    
    def test_analyze_signals_golden_cross(self):
        """测试金叉信号检测"""
        dates = pd.date_range('2021-01-01', periods=10)
        df = pd.DataFrame({
            'Trddt': dates,
            'Clsprc': [10, 11, 12, 13, 14, 13, 12, 11, 12, 13],
            'DIF': [-0.5, -0.3, -0.1, 0.1, 0.3, 0.2, 0.1, -0.1, -0.05, 0.05],
            'DEA': [-0.4, -0.35, -0.3, -0.2, -0.1, 0.0, 0.05, 0.02, -0.02, -0.03]
        })
        df.set_index('Trddt', inplace=True)
        
        calculator = MACDCalculator()
        signals = calculator.analyze_signals(df)
        
        assert len(signals['golden_cross']) > 0
    
    def test_analyze_signals_death_cross(self):
        """测试死叉信号检测"""
        dates = pd.date_range('2021-01-01', periods=10)
        df = pd.DataFrame({
            'Trddt': dates,
            'Clsprc': [15, 14, 13, 12, 11, 12, 13, 14, 13, 12],
            'DIF': [0.5, 0.3, 0.1, -0.1, -0.3, -0.2, -0.1, 0.1, 0.05, -0.05],
            'DEA': [0.4, 0.35, 0.3, 0.2, 0.1, 0.0, -0.05, -0.02, 0.02, 0.03]
        })
        df.set_index('Trddt', inplace=True)
        
        calculator = MACDCalculator()
        signals = calculator.analyze_signals(df)
        
        assert len(signals['death_cross']) > 0
    
    def test_get_statistics(self):
        """测试统计信息获取"""
        dates = pd.date_range('2021-01-01', periods=30)
        df = pd.DataFrame({
            'Trddt': dates,
            'Clsprc': np.linspace(10, 20, 30),
            'DIF': np.linspace(-1, 1, 30),
            'DEA': np.linspace(-0.8, 0.8, 30),
            'MACD': np.linspace(-0.4, 0.4, 30)
        })
        df.set_index('Trddt', inplace=True)
        
        calculator = MACDCalculator()
        stats = calculator.get_statistics(df)
        
        assert 'DIF' in stats
        assert 'DEA' in stats
        assert 'MACD' in stats
        assert 'mean' in stats['DIF']
        assert 'std' in stats['DIF']
        assert 'max' in stats['DIF']
        assert 'min' in stats['DIF']
    
    def test_get_latest_signal(self):
        """测试获取最新信号"""
        dates = pd.date_range('2021-01-01', periods=10)
        df = pd.DataFrame({
            'Trddt': dates,
            'Clsprc': [10, 11, 12, 13, 14, 13, 12, 11, 12, 13],
            'DIF': [-0.5, -0.3, -0.1, 0.1, 0.3, 0.2, 0.1, -0.1, -0.05, 0.05],
            'DEA': [-0.4, -0.35, -0.3, -0.2, -0.1, 0.0, 0.05, 0.02, -0.02, -0.03]
        })
        df.set_index('Trddt', inplace=True)
        
        calculator = MACDCalculator()
        signal = calculator.get_latest_signal(df)
        
        assert signal == 'golden_cross'


def run_tests():
    """运行所有测试"""
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == '__main__':
    run_tests()
