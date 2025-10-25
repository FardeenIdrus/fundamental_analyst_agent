"""
Data Collection Module for Fundamental Analysis
Downloads financial statements from Yahoo Finance
"""

import yfinance as yf
import pandas as pd
from pathlib import Path
import json

class YFinanceDataCollector:
    def __init__(self, ticker, data_dir="data/raw"):
        self.ticker = ticker
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.stock = yf.Ticker(ticker)
        
    def collect_all_data(self):
        """Collect all financial data"""
        print(f"Collecting data for {self.ticker}...")
        
        # 1. Income Statement
        income_stmt = self.stock.financials
        income_stmt.to_csv(self.data_dir / f"{self.ticker}_income_statement.csv")
        print("✓ Income Statement")
        
        # 2. Balance Sheet
        balance_sheet = self.stock.balance_sheet
        balance_sheet.to_csv(self.data_dir / f"{self.ticker}_balance_sheet.csv")
        print("✓ Balance Sheet")
        
        # 3. Cash Flow Statement
        cashflow = self.stock.cashflow
        cashflow.to_csv(self.data_dir / f"{self.ticker}_cashflow.csv")
        print("✓ Cash Flow Statement")
        
        # 4. Company Info
        info = self.stock.info
        with open(self.data_dir / f"{self.ticker}_info.json", 'w') as f:
            json.dump(info, f, indent=2)
        print("✓ Company Info")
        
        # 5. Historical Prices
        hist = self.stock.history(period="5y")
        hist.to_csv(self.data_dir / f"{self.ticker}_prices.csv")
        print("✓ Historical Prices")
        
        return {
            'income_statement': income_stmt,
            'balance_sheet': balance_sheet,
            'cashflow': cashflow,
            'info': info,
            'prices': hist
        }
    
    def get_summary_stats(self):
        """Get key statistics"""
        info = self.stock.info
        
        summary = {
            'Company': info.get('longName'),
            'Sector': info.get('sector'),
            'Industry': info.get('industry'),
            'Market Cap': info.get('marketCap'),
            'Current Price': info.get('currentPrice'),
            'P/E Ratio': info.get('trailingPE'),
            'EPS': info.get('trailingEps'),
            'Revenue': info.get('totalRevenue'),
            'Employees': info.get('fullTimeEmployees')
        }
        
        return summary

if __name__ == "__main__":
    # Test the collector
    collector = YFinanceDataCollector("AAPL")
    data = collector.collect_all_data()
    summary = collector.get_summary_stats()
    
    print("\n" + "="*60)
    print("COMPANY SUMMARY")
    print("="*60)
    for key, value in summary.items():
        print(f"{key}: {value}")
