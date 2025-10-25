"""
Complete Demo Script for Fundamental Analyst AI Agent

This script runs the entire workflow:
1. Collects financial data
2. Performs fundamental analysis
3. Generates AI-powered investment memo

Run this to demonstrate the complete agent.
"""

from src.data_collector import YFinanceDataCollector
from src.financial_analyser import FundamentalAnalyzer
from src.llm_agents import InvestmentMemoGenerator
from pathlib import Path
import json
import sys

def main(ticker="AAPL"):
    """
    Run complete fundamental analysis workflow.
    
    Args:
        ticker: Stock ticker to analyze (default: AAPL)
    """
    
    print("="*70)
    print("FUNDAMENTAL ANALYST AI AGENT - COMPLETE DEMO")
    print("="*70)
    print(f"\nAnalyzing: {ticker}")
    print("="*70)
    
    # ========================================
    # STEP 1: Data Collection
    # ========================================
    print("\n📥 STEP 1: COLLECTING FINANCIAL DATA")
    print("-"*70)
    
    collector = YFinanceDataCollector(ticker)
    data = collector.collect_all_data()
    summary = collector.get_summary_stats()
    
    print("\n📊 Company Summary:")
    for key, value in summary.items():
        if value is not None:
            if isinstance(value, (int, float)) and abs(value) > 1_000_000:
                print(f"  {key}: ${value:,.0f}")
            else:
                print(f"  {key}: {value}")
    
    # ========================================
    # STEP 2: Financial Analysis
    # ========================================
    print("\n" + "="*70)
    print("📊 STEP 2: COMPUTING FINANCIAL RATIOS & VALUATION")
    print("-"*70)
    
    analyzer = FundamentalAnalyzer(ticker)
    analysis = analyzer.generate_analysis_summary()
    
    # Display profitability
    print("\n💰 Profitability Ratios:")
    for key, value in analysis['Profitability Ratios'].items():
        if isinstance(value, (int, float)):
            print(f"  {key}: {value:.2f}")
    
    # Display leverage
    print("\n⚖️  Leverage Ratios:")
    for key, value in analysis['Leverage Ratios'].items():
        if isinstance(value, (int, float)):
            print(f"  {key}: {value:.2f}")
    
    # Display growth
    print("\n📈 Growth Metrics:")
    for key, value in analysis['Growth Metrics'].items():
        if isinstance(value, (int, float)):
            print(f"  {key}: {value:.2f}%")
        else:
            print(f"  {key}: {value}")
    
    # Display valuation
    print("\n💵 DCF Valuation:")
    dcf = analysis['DCF Valuation']
    if dcf:
        print(f"  Enterprise Value: ${dcf.get('Enterprise Value', 0):,.0f}")
        print(f"  Current FCF: ${dcf.get('Current FCF', 0):,.0f}")
        print(f"  Assumptions: {dcf.get('Assumptions', {})}")
    
    # ========================================
    # STEP 3: Generate Investment Memo
    # ========================================
    print("\n" + "="*70)
    print("🤖 STEP 3: GENERATING AI-POWERED INVESTMENT MEMO")
    print("-"*70)
    
    memo_gen = InvestmentMemoGenerator()
    memo = memo_gen.generate_memo(analysis, ticker)
    
    # ========================================
    # STEP 4: Save Outputs
    # ========================================
    print("\n" + "="*70)
    print("💾 STEP 4: SAVING OUTPUTS")
    print("-"*70)
    
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    
    # Save analysis as JSON
    analysis_file = outputs_dir / f"{ticker}_analysis.json"
    with open(analysis_file, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    print(f"✓ Analysis saved: {analysis_file}")
    
    # Save memo
    memo_file = outputs_dir / f"{ticker}_investment_memo.md"
    memo_gen.save_memo(memo, memo_file)
    
    # ========================================
    # FINAL OUTPUT: Display Memo
    # ========================================
    print("\n" + "="*70)
    print("📄 INVESTMENT MEMO")
    print("="*70)
    print(memo)
    
    # ========================================
    # Summary
    # ========================================
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    print(f"\n📁 Outputs saved to: {outputs_dir.absolute()}")
    print(f"  - Analysis (JSON): {analysis_file.name}")
    print(f"  - Investment Memo: {memo_file.name}")
    print(f"  - Raw Data: data/raw/{ticker}_*.csv")
    print("\n" + "="*70)


if __name__ == "__main__":
    """
    Run the demo.
    
    Usage:
        python run_demo.py           # Analyze Apple (AAPL)
        python run_demo.py MSFT      # Analyze Microsoft
        python run_demo.py TSLA      # Analyze Tesla
    """
    
    # Get ticker from command line or use default
    if len(sys.argv) > 1:
        ticker = sys.argv[1].upper()
    else:
        ticker = "AAPL"
    
    try:
        main(ticker)
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)