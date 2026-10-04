import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def load_price_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    required = {"date", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {sorted(missing)}")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi_value = 100 - (100 / (1 + rs))
    return rsi_value


def backtest_strategy(
    df: pd.DataFrame,
    initial_cash: float = 1000.0,
    buy_threshold: float = 30.0,
    sell_threshold: float = 70.0,
    rsi_period: int = 14,
) -> dict:
    cash = initial_cash
    position = 0.0
    trades = []
    equity_curve = []

    df = df.copy()
    df["rsi"] = rsi(df["close"], period=rsi_period)

    for i, row in df.iterrows():
        close_price = float(row["close"])
        rsi_value = float(row["rsi"]) if pd.notna(row["rsi"]) else np.nan

        if pd.isna(rsi_value):
            equity_curve.append(cash + position * close_price)
            continue

        # Buy signal: RSI below threshold, and we are not invested
        if rsi_value < buy_threshold and position == 0:
            position = cash / close_price
            cash = 0.0
            trades.append({"type": "buy", "date": row["date"], "price": close_price})

        # Sell signal: RSI above threshold, and we are invested
        elif rsi_value > sell_threshold and position > 0:
            cash = position * close_price
            position = 0.0
            trades.append({"type": "sell", "date": row["date"], "price": close_price})

        equity_curve.append(cash + position * close_price)

    final_value = cash + position * float(df["close"].iloc[-1])
    profit = final_value - initial_cash

    result = {
        "initial_cash": initial_cash,
        "final_value": final_value,
        "profit": profit,
        "trades": trades,
        "equity_curve": equity_curve,
        "num_trades": len(trades),
    }
    return result


def plot_equity_curve(equity_curve: list[float], dates: pd.DatetimeIndex):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, equity_curve, color="green", linewidth=2)
    plt.title("Portfolio Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Simple RSI trading bot backtest")
    parser.add_argument("--csv", type=str, required=True, help="Path to CSV with 'date' and 'close' columns")
    parser.add_argument("--initial-cash", type=float, default=1000.0, help="Starting cash")
    parser.add_argument("--buy-threshold", type=float, default=30.0, help="RSI buy threshold")
    parser.add_argument("--sell-threshold", type=float, default=70.0, help="RSI sell threshold")
    parser.add_argument("--rsi-period", type=int, default=14, help="RSI period")
    parser.add_argument("--plot", action="store_true", help="Display equity chart")
    args = parser.parse_args()

    df = load_price_data(args.csv)
    result = backtest_strategy(
        df,
        initial_cash=args.initial_cash,
        buy_threshold=args.buy_threshold,
        sell_threshold=args.sell_threshold,
        rsi_period=args.rsi_period,
    )

    print(f"Initial cash: ${args.initial_cash:,.2f}")
    print(f"Final portfolio value: ${result['final_value']:,.2f}")
    print(f"Profit/Loss: ${result['profit']:,.2f}")
    print(f"Number of trades: {result['num_trades']}")

    if args.plot:
        plot_equity_curve(result["equity_curve"], df["date"])


if __name__ == "__main__":
    main()
