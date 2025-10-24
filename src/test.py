import yfinance as yf
import pandas as pd
import sys

print("="*60)
print("ENVIRONMENT TEST")
print("="*60)
print(f"Python: {sys.version}")
print(f"Location: {sys.executable}")
print(f"Pandas: {pd.__version__}")
print(f"YFinance: {yf.__version__}")

print("\n" + "="*60)
print("DATA DOWNLOAD TEST")
print("="*60)

stock = yf.Ticker("AAPL")
info = stock.info
print(f"✓ Company: {info['longName']}")
print(f"✓ Sector: {info['sector']}")
print(f"✓ Price: ${info.get('currentPrice', 'N/A')}")

print("\n✅ ALL TESTS PASSED - READY TO BUILD!")
