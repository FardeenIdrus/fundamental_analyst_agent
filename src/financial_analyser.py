"""
Financial Analysis Module
Computes financial ratios and performs DCF valuation
"""

import pandas as pd
import numpy as np
from pathlib import Path

class FundamentalAnalyzer:
    """
    Analyzes company financials and calculates key metrics.
    
    This class reads financial statements (income statement, balance sheet, cash flow)
    and computes:
    - Profitability ratios (margins, ROE, ROA)
    - Leverage ratios (debt levels)
    - Growth metrics (year-over-year changes)
    - DCF valuation (intrinsic value estimate)
    """
    
    def __init__(self, ticker, data_dir="data/raw"):
        """
        Initialize the analyzer.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            data_dir: Directory where financial data CSV files are stored
        """
        self.ticker = ticker
        self.data_dir = Path(data_dir)
        self.load_data()
        
    def load_data(self):
        """
        Load financial statements from CSV files.
        
        Reads three files created by data_collector.py:
        - Income statement (revenue, expenses, net income)
        - Balance sheet (assets, liabilities, equity)
        - Cash flow statement (operating, investing, financing cash flows)
        """
        # Read income statement - shows profitability
        self.income_stmt = pd.read_csv(
            self.data_dir / f"{self.ticker}_income_statement.csv",
            index_col=0  # First column is the row labels (e.g., "Total Revenue")
        )
        
        # Read balance sheet - shows financial position
        self.balance_sheet = pd.read_csv(
            self.data_dir / f"{self.ticker}_balance_sheet.csv",
            index_col=0
        )
        
        # Read cash flow statement - shows cash generation
        self.cashflow = pd.read_csv(
            self.data_dir / f"{self.ticker}_cashflow.csv",
            index_col=0
        )
        
        print(f"✓ Loaded financial data for {self.ticker}")
        
    def calculate_profitability_ratios(self):
        """
        Calculate profitability metrics.
        
        These ratios show how efficiently the company generates profit:
        - Net Profit Margin: What % of revenue becomes profit
        - ROA: How well assets generate profit
        - ROE: Return to shareholders
        
        Returns:
            dict: Dictionary of ratio names and values
        """
        
        # Get latest year (columns are years, most recent is first)
        latest = self.income_stmt.columns[0]
        
        try:
            # Extract key figures from financial statements
            # Revenue = total sales
            revenue = self.income_stmt.loc['Total Revenue', latest]
            
            # Net income = profit after all expenses and taxes
            net_income = self.income_stmt.loc['Net Income', latest]
            
            # Total assets = everything the company owns
            total_assets = self.balance_sheet.loc['Total Assets', latest]
            
            # Shareholders equity = net worth (assets - liabilities)
            shareholders_equity = self.balance_sheet.loc['Stockholders Equity', latest]
            
            # Calculate the ratios
            ratios = {
                # Profit margin: higher is better (company keeps more of each dollar)
                'Net Profit Margin (%)': (net_income / revenue) * 100,
                
                # ROA: higher is better (assets are productive)
                'ROA (Return on Assets %)': (net_income / total_assets) * 100,
                
                # ROE: higher is better (good return for shareholders)
                'ROE (Return on Equity %)': (net_income / shareholders_equity) * 100,
            }
            
            return ratios
            
        except KeyError as e:
            # Sometimes Yahoo Finance uses different row names
            # Print available rows to help debug
            print(f"Warning: Could not find {e}. Check row names in CSV.")
            return self._try_alternative_names()
    
    def _try_alternative_names(self):
        """
        Helper function to debug missing data.
        Prints available row names so we can see what Yahoo Finance actually provided.
        """
        latest = self.income_stmt.columns[0]
        
        # Show what rows are actually available
        print("\nAvailable Income Statement rows:")
        print(self.income_stmt.index.tolist()[:10])
        
        print("\nAvailable Balance Sheet rows:")
        print(self.balance_sheet.index.tolist()[:10])
        
        return {}
    
    def calculate_leverage_ratios(self):
        """
        Calculate leverage/debt metrics.
        
        These ratios show how much debt the company has:
        - Debt-to-Equity: How much debt vs. shareholder equity
        - Debt-to-Assets: What % of assets are financed by debt
        - Equity Multiplier: Financial leverage indicator
        
        Lower debt ratios = less risky (but may mean slower growth)
        Higher debt ratios = more risky (but can amplify returns)
        
        Returns:
            dict: Dictionary of ratio names and values
        """
        latest = self.balance_sheet.columns[0]
        
        try:
            # Total debt = all money owed
            total_debt = self.balance_sheet.loc['Total Debt', latest]
            
            # Total equity = shareholder ownership value
            total_equity = self.balance_sheet.loc['Stockholders Equity', latest]
            
            # Total assets = everything owned
            total_assets = self.balance_sheet.loc['Total Assets', latest]
            
            ratios = {
                # D/E: <1 is conservative, >2 is aggressive
                'Debt-to-Equity': total_debt / total_equity,
                
                # D/A: shows what % of assets are debt-financed
                'Debt-to-Assets': total_debt / total_assets,
                
                # Equity multiplier: measures financial leverage
                'Equity Multiplier': total_assets / total_equity
            }
            
            return ratios
            
        except KeyError as e:
            print(f"Warning: Could not find {e}")
            return {}
    
    def calculate_growth_metrics(self):
        """
        Calculate year-over-year growth rates.
        
        Compares this year vs. last year to see if company is growing.
        Positive growth = expanding business
        Negative growth = shrinking business
        
        Returns:
            dict: Growth percentages
        """
        
        # Need at least 2 years of data to calculate growth
        if len(self.income_stmt.columns) < 2:
            return {'Note': 'Insufficient data for growth calculation'}
            
        # Most recent year vs. previous year
        current_year = self.income_stmt.columns[0]
        previous_year = self.income_stmt.columns[1]
        
        try:
            # Get revenue for both years
            current_revenue = self.income_stmt.loc['Total Revenue', current_year]
            previous_revenue = self.income_stmt.loc['Total Revenue', previous_year]
            
            # Get net income for both years
            current_ni = self.income_stmt.loc['Net Income', current_year]
            previous_ni = self.income_stmt.loc['Net Income', previous_year]
            
            # Calculate % change: (new - old) / old * 100
            growth = {
                'Revenue Growth YoY (%)': ((current_revenue - previous_revenue) / previous_revenue) * 100,
                'Net Income Growth YoY (%)': ((current_ni - previous_ni) / previous_ni) * 100
            }
            
            return growth
            
        except KeyError:
            return {}
    
    def simple_dcf_valuation(self, growth_rate=0.05, discount_rate=0.10, years=5):
        """
        Discounted Cash Flow (DCF) valuation model.
        
        DCF estimates a company's intrinsic value by:
        1. Projecting future free cash flows
        2. Discounting them to present value
        3. Adding terminal value (value beyond projection period)
        
        This is a SIMPLIFIED DCF - real analysts use more complex models.
        
        Args:
            growth_rate: Expected annual FCF growth (default 5%)
            discount_rate: WACC/required return (default 10%)
            years: How many years to project (default 5)
            
        Returns:
            dict: Enterprise value and breakdown
        """
        
        try:
            # Get most recent year's data
            latest = self.cashflow.columns[0]
            
            # Try to find Free Cash Flow (FCF)
            # FCF = cash available to investors after all expenses and investments
            if 'Free Cash Flow' in self.cashflow.index:
                fcf = self.cashflow.loc['Free Cash Flow', latest]
            elif 'Operating Cash Flow' in self.cashflow.index:
                # If FCF not available, estimate it
                # FCF ≈ Operating Cash Flow - Capital Expenditures
                ocf = self.cashflow.loc['Operating Cash Flow', latest]
                capex = abs(self.cashflow.loc['Capital Expenditure', latest]) if 'Capital Expenditure' in self.cashflow.index else 0
                fcf = ocf - capex
            else:
                print("Cannot find cash flow data")
                return {}
            
            # Project future cash flows and discount to present value
            projected_fcf = []
            for year in range(1, years + 1):
                # Grow FCF by growth_rate each year
                future_fcf = fcf * ((1 + growth_rate) ** year)
                
                # Discount back to present value
                # Money in the future is worth less than money today
                pv = future_fcf / ((1 + discount_rate) ** year)
                projected_fcf.append(pv)
            
            # Terminal value: value of all cash flows beyond projection period
            # Uses perpetuity formula: FCF / (discount - growth)
            terminal_fcf = fcf * ((1 + growth_rate) ** years) * (1 + growth_rate)
            terminal_value = terminal_fcf / (discount_rate - growth_rate)
            
            # Discount terminal value to present
            pv_terminal = terminal_value / ((1 + discount_rate) ** years)
            
            # Enterprise Value = sum of all discounted cash flows
            enterprise_value = sum(projected_fcf) + pv_terminal
            
            return {
                'Enterprise Value': enterprise_value,  # Company's intrinsic value
                'Current FCF': fcf,  # Starting point
                'Projected FCF (PV)': sum(projected_fcf),  # Value from projection period
                'Terminal Value (PV)': pv_terminal,  # Value beyond projection
                'Assumptions': {
                    'Growth Rate': f"{growth_rate*100}%",
                    'Discount Rate': f"{discount_rate*100}%",
                    'Years': years
                }
            }
            
        except KeyError as e:
            print(f"Could not perform DCF: {e}")
            print("\nAvailable Cash Flow rows:")
            print(self.cashflow.index.tolist()[:10])
            return {}
    
    def generate_analysis_summary(self):
        """
        Generate complete analysis combining all metrics.
        
        This pulls together:
        - Profitability (how profitable is the company?)
        - Leverage (how much debt?)
        - Growth (is it expanding?)
        - Valuation (what's it worth?)
        
        Returns:
            dict: Complete analysis summary for LLM to use
        """
        
        # Run all analysis functions
        profitability = self.calculate_profitability_ratios()
        leverage = self.calculate_leverage_ratios()
        growth = self.calculate_growth_metrics()
        valuation = self.simple_dcf_valuation()
        
        # Package everything into one dictionary
        summary = {
            'Ticker': self.ticker,
            'Profitability Ratios': profitability,
            'Leverage Ratios': leverage,
            'Growth Metrics': growth,
            'DCF Valuation': valuation
        }
        
        return summary


# Test code - runs when you execute this file directly
if __name__ == "__main__":
    """
    Test the analyzer by running analysis on Apple.
    Make sure you've run data_collector.py first to download the data!
    """
    
    # Create analyzer instance
    analyzer = FundamentalAnalyzer("AAPL")
    
    # Print profitability ratios
    print("\n" + "="*60)
    print("PROFITABILITY RATIOS")
    print("="*60)
    prof = analyzer.calculate_profitability_ratios()
    for key, value in prof.items():
        if isinstance(value, (int, float)):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    
    # Print leverage ratios
    print("\n" + "="*60)
    print("LEVERAGE RATIOS")
    print("="*60)
    lev = analyzer.calculate_leverage_ratios()
    for key, value in lev.items():
        if isinstance(value, (int, float)):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    
    # Print growth metrics
    print("\n" + "="*60)
    print("GROWTH METRICS")
    print("="*60)
    growth = analyzer.calculate_growth_metrics()
    for key, value in growth.items():
        if isinstance(value, (int, float)):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    
    # Print DCF valuation
    print("\n" + "="*60)
    print("DCF VALUATION")
    print("="*60)
    dcf = analyzer.simple_dcf_valuation()
    if dcf:
        print(f"Enterprise Value: ${dcf.get('Enterprise Value', 0):,.0f}")
        print(f"Current FCF: ${dcf.get('Current FCF', 0):,.0f}")
        print(f"Assumptions: {dcf.get('Assumptions', {})}")