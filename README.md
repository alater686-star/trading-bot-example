# Trading Bot Example

This is a simple educational trading bot that simulates a basic RSI-based strategy on historical price data.

Important:
- This is for learning and testing only.
- It does not guarantee profits.
- Do not use it with real money without understanding the strategy, risk, and market conditions.

## What it does

- reads price data from a CSV file
- calculates the Relative Strength Index (RSI)
- buys when RSI is below 30
- sells when RSI is above 70
- simulates cash and position tracking
- prints a simple performance summary
- optionally plots equity curve

## Files

- `bot.py` – trading bot logic
- `data/sample_prices.csv` – sample price data for testing
- `requirements.txt` – Python dependencies

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python bot.py --csv data/sample_prices.csv --initial-cash 1000
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python bot.py --csv data/sample_prices.csv --initial-cash 1000
```

## Output

The script prints:
- final portfolio value
- total profit/loss
- number of trades
- win/loss summary (if enabled)

## Customize

You can replace the sample CSV with real market data or change:
- RSI period
- buy threshold
- sell threshold
- initial cash

This project is intended for educational use only.
