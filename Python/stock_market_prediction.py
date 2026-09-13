import time
import numpy as np
import alpaca_trade_api as tradeapi
import yfinance as yf
from stable_baselines3 import PPO

# 🔑 Alpaca API Credentials
API_KEY = "your_alpaca_api_key"
API_SECRET = "your_alpaca_secret_key"
BASE_URL = "https://paper-api.alpaca.markets"  # Use for paper trading, change for live trading

# 📡 Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# 🎯 Trading Parameters
SYMBOL = "AAPL"  # Change for different stocks
MODEL_PATH = "ppo_stock_trading"  # Load trained PPO model
STOP_LOSS_PERCENT = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENT = 0.05  # 5% take profit
TRADE_QUANTITY = 1  # Number of shares per trade

# 🎓 Load Trained RL Model
model = PPO.load(MODEL_PATH)

# 📊 Get Real-Time Stock Price
def get_latest_price(symbol):
    barset = api.get_barset(symbol, 'minute', limit=1)
    return barset[symbol][0].c  # Closing price

# 📊 Fetch Account Balance
def get_cash_balance():
    account = api.get_account()
    return float(account.cash)

# 📈 Trading Bot Loop
def run_trading_bot():
    while True:
        try:
            # ✅ Fetch latest stock price
            latest_price = get_latest_price(SYMBOL)
            print(f"Latest {SYMBOL} Price: ${latest_price}")

            # ✅ Prepare state for RL model
            state = np.array([latest_price])  # Modify based on features
            action, _ = model.predict(state)

            # ✅ Execute Trade
            if action == 0:
                print("🤖 HOLD")
            elif action == 1:
                print("✅ BUY ORDER PLACED")
                api.submit_order(
                    symbol=SYMBOL,
                    qty=TRADE_QUANTITY,
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )
            elif action == 2:
                print("❌ SELL ORDER PLACED")
                api.submit_order(
                    symbol=SYMBOL,
                    qty=TRADE_QUANTITY,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )

            # 🚀 Apply Risk Management
            positions = api.list_positions()
            for position in positions:
                if position.symbol == SYMBOL:
                    avg_entry_price = float(position.avg_entry_price)
                    current_price = float(position.current_price)

                    # Stop-Loss Check
                    if current_price < avg_entry_price * (1 - STOP_LOSS_PERCENT):
                        print("⚠️ STOP-LOSS TRIGGERED: Selling position")
                        api.submit_order(symbol=SYMBOL, qty=position.qty, side='sell', type='market', time_in_force='gtc')

                    # Take-Profit Check
                    if current_price > avg_entry_price * (1 + TAKE_PROFIT_PERCENT):
                        print("🎯 TAKE-PROFIT REACHED: Selling position")
                        api.submit_order(symbol=SYMBOL, qty=position.qty, side='sell', type='market', time_in_force='gtc')

            # ⏳ Wait before next trade (1 minute)
            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(60)  # Wait and retry in case of error

# 🔥 Run Trading Bot
run_trading_bot()
