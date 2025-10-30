# Fundamental Analyst AI Agent

An automated financial analysis tool that downloads financial data, calculates key ratios, performs DCF valuation, and generates AI-powered investment memos using GPT-4.

## Features

- **Automated Data Collection**: Downloads financial statements from Yahoo Finance
- **Financial Analysis**: Calculates profitability, leverage, and growth metrics
- **DCF Valuation**: Performs discounted cash flow analysis to estimate intrinsic value
- **AI-Powered Memos**: Generates professional investment recommendations using OpenAI's GPT-4

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Quick Start

Analyze a stock and generate an investment memo:

```bash
python run_demo.py AAPL
```

Replace `AAPL` with any valid stock ticker (e.g., `MSFT`, `TSLA`, `GOOGL`).

### What It Does

1. **Collects Financial Data**: Downloads income statements, balance sheets, cash flow statements, and historical prices
2. **Computes Financial Ratios**: 
   - Profitability: Net profit margin, ROA, ROE
   - Leverage: Debt-to-equity, debt-to-assets
   - Growth: YoY revenue and income growth
3. **Performs DCF Valuation**: Estimates enterprise value using discounted cash flow analysis
4. **Generates Investment Memo**: Creates a structured investment recommendation with AI

### Output

The script generates:
- `outputs/{TICKER}_analysis.json` - Complete financial analysis data
- `outputs/{TICKER}_investment_memo.md` - Professional investment memo
- `data/raw/{TICKER}_*.csv` - Raw financial statements

## Project Structure

```
├── data_collector.py       # Downloads financial data from Yahoo Finance
├── financial_analyser.py   # Calculates ratios and performs valuation
├── llm_agents.py           # Generates investment memos using GPT-4
├── run_demo.py             # Main script to run complete analysis
├── test.py                 # Environment verification script
└── requirements.txt        # Python dependencies
```

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for data downloads

## Key Dependencies

- `yfinance` - Financial data download
- `pandas` - Data manipulation
- `openai` - GPT-4 integration
- `python-dotenv` - Environment variable management

## Testing

Verify your environment is set up correctly:

```bash
python test.py
```

## Example Output

The tool generates investment memos with the following sections:
- Executive Summary
- Investment Thesis
- Financial Analysis
- Valuation Assessment
- Key Risks
- Recommendation (Buy/Hold/Sell)

## Notes

- DCF valuation uses simplified assumptions (5% growth, 10% discount rate)
- Analysis is based on publicly available financial statements
- Investment memos are AI-generated and should be used for educational purposes
- Always conduct additional research before making investment decisions

## License

This project is for educational and research purposes.
