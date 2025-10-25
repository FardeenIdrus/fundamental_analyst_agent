"""
LLM-Powered Investment Memo Generator
Uses OpenAI API to generate professional investment analysis
"""

import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class InvestmentMemoGenerator:
    """
    Generates investment memos using GPT-4.
    
    Takes financial analysis data and creates a structured,
    professional investment recommendation memo.
    """
    
    def __init__(self, model="gpt-4o-mini"):
        """
        Initialize the memo generator.
        
        Args:
            model: OpenAI model to use
                   - "gpt-4o-mini" is cheaper and faster (recommended)
                   - "gpt-4o" is more expensive but slightly better
        """
        self.model = model
        
    def generate_memo(self, analysis_data, ticker):
        """
        Generate investment memo from analysis data.
        
        Args:
            analysis_data: Dictionary with financial ratios and valuation
            ticker: Stock ticker symbol
            
        Returns:
            str: Investment memo text
        """
        
        # Create prompt with all the financial data
        prompt = self._create_prompt(analysis_data, ticker)
        
        print(f"\n🤖 Generating investment memo for {ticker}...")
        print("⏳ This may take 10-30 seconds...\n")
        
        try:
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a senior equity research analyst at a top-tier 
                        asset management firm. Write clear, professional investment memos 
                        based on fundamental analysis. Be concise but thorough. Always cite 
                        specific numbers from the data provided. Be objective and highlight 
                        both positives and risks."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,  # Balance between creativity and consistency
                max_tokens=2000   # Maximum length of response
            )
            
            # Extract the memo text from API response
            memo = response.choices[0].message.content
            
            print("✅ Memo generated successfully!\n")
            
            return memo
            
        except openai.AuthenticationError:
            return "❌ ERROR: Invalid OpenAI API key. Check your .env file."
        except openai.RateLimitError:
            return "❌ ERROR: OpenAI rate limit exceeded. Wait a moment and try again."
        except openai.APIError as e:
            return f"❌ ERROR: OpenAI API error: {str(e)}"
        except Exception as e:
            return f"❌ ERROR: {str(e)}"
    
    def _create_prompt(self, data, ticker):
        """
        Create structured prompt for LLM.
        
        This formats all the financial data into a clear prompt
        that guides the LLM to produce a good investment memo.
        
        Args:
            data: Analysis data dictionary
            ticker: Stock ticker
            
        Returns:
            str: Formatted prompt
        """
        
        # Format the data nicely for the LLM
        prompt = f"""
Please write a professional 1-2 page investment memo for {ticker} based on the following fundamental analysis:

## Company: {ticker}

## Financial Ratios:

### Profitability:
{self._format_dict(data.get('Profitability Ratios', {}))}

### Leverage:
{self._format_dict(data.get('Leverage Ratios', {}))}

### Growth:
{self._format_dict(data.get('Growth Metrics', {}))}

## Valuation (DCF Analysis):
{self._format_dict(data.get('DCF Valuation', {}))}

---

Please structure the memo as follows:

1. **Executive Summary** (2-3 sentences)
   - Quick overview and recommendation

2. **Investment Thesis** 
   - Why buy/sell/hold?
   - Key value drivers

3. **Financial Analysis**
   - Profitability assessment (cite specific margins and returns)
   - Balance sheet strength (cite leverage ratios)
   - Growth trajectory (cite YoY growth rates)

4. **Valuation**
   - DCF results interpretation
   - Is the company undervalued or overvalued?
   - Fair value estimate

5. **Key Risks**
   - What could go wrong?
   - Financial vulnerabilities
   - Market/competitive risks

6. **Recommendation** 
   - Clear Buy/Hold/Sell rating
   - Conviction level (High/Medium/Low)
   - Key catalysts to watch

**Important Instructions:**
- Use professional language but keep it clear
- Cite specific numbers from the analysis (e.g., "With an ROE of 164%...")
- Be objective - mention both strengths and weaknesses
- Make a clear, actionable recommendation
- Keep the total memo to 500-800 words
"""
        return prompt
    
    def _format_dict(self, d):
        """
        Format dictionary nicely for the prompt.
        
        Args:
            d: Dictionary to format
            
        Returns:
            str: Formatted string
        """
        if not d:
            return "No data available"
        
        lines = []
        for key, value in d.items():
            if isinstance(value, dict):
                # Handle nested dictionaries (like DCF assumptions)
                lines.append(f"**{key}:**")
                for sub_key, sub_value in value.items():
                    lines.append(f"  - {sub_key}: {sub_value}")
            elif isinstance(value, (int, float)):
                # Format numbers nicely
                if abs(value) > 1_000_000:
                    lines.append(f"- {key}: ${value:,.0f}")
                else:
                    lines.append(f"- {key}: {value:.2f}")
            else:
                lines.append(f"- {key}: {value}")
        
        return "\n".join(lines)
    
    def save_memo(self, memo, filename):
        """
        Save memo to file.
        
        Args:
            memo: Memo text
            filename: Path to save file
        """
        with open(filename, 'w') as f:
            f.write(memo)
        print(f"✓ Memo saved to {filename}")


# Test code
if __name__ == "__main__":
    """
    Test the LLM agent by generating a memo for Apple.
    
    Prerequisites:
    1. Run data_collector.py first
    2. Run financial_analyzer.py
    3. Have OpenAI API key in .env file
    """
    
    from financial_analyser import FundamentalAnalyzer
    
    print("="*60)
    print("TESTING LLM INVESTMENT MEMO GENERATOR")
    print("="*60)
    
    # Run analysis
    print("\n📊 Running financial analysis...")
    analyzer = FundamentalAnalyzer("AAPL")
    analysis = analyzer.generate_analysis_summary()
    
    # Generate memo using LLM
    print("\n🤖 Calling OpenAI API...")
    memo_gen = InvestmentMemoGenerator()
    memo = memo_gen.generate_memo(analysis, "AAPL")
    
    # Print the memo
    print("\n" + "="*60)
    print("INVESTMENT MEMO")
    print("="*60)
    print(memo)
    
    # Save to file
    print("\n" + "="*60)
    from pathlib import Path
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    memo_gen.save_memo(memo, output_dir / "AAPL_investment_memo.md")
    
    print("\n✅ TEST COMPLETE!")
    print("="*60)