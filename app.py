import yfinance as yf
import json
from datetime import datetime
import time
import threading

def monitor_stock(stock_name, direction, percent_change):
    percent_change = float(percent_change)
    stock = yf.Ticker(stock_name)
    initial_price = stock.history(period="1d")["Close"][0]
    if direction == "up":
        target_price = initial_price * (1 + percent_change/100)
    else:
        target_price = initial_price * (1 - percent_change/100)
    print(f"Monitoring {stock_name} for {percent_change:.2f}% {direction}ward movement from {initial_price:.2f} to {target_price:.2f}...")
    start_date = None
    while True:
        current_price = stock.history(period="1d")["Close"][0]
        days_elapsed = 0
        hit_goal = False
        if direction == "up" and current_price >= target_price:
            if start_date is None:
                start_date = datetime.today().date()
            end_date = datetime.today().date()
            days_elapsed = (end_date - start_date).days
            hit_goal = True
        elif direction == "down" and current_price <= target_price:
            if start_date is None:
                start_date = datetime.today().date()
            end_date = datetime.today().date()
            days_elapsed = (end_date - start_date).days
            hit_goal = True
        if hit_goal:
            data = {
                "stock_name": stock_name,
                "direction": direction,
                "target_price": target_price,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "days_elapsed": days_elapsed,
                "hit_goal": hit_goal,
            }
            with open(f"{stock_name}_{direction}.json", "w") as f:
                json.dump(data, f)
            print(f"{stock_name} has hit the {target_price:.2f} target price {direction}ward!")
            break
        else:
            print(f"{stock_name} has not hit the {target_price:.2f} target price {direction}ward.")
        time.sleep(900) # wait for 15 minutes

def monitor_stocks():
    threads = []
    while True:
        with open("stocks.txt", "r") as f:
            existing_tickers = set([thread.name for thread in threads])
            for line in f:
                stock_name, direction, percent_change = line.strip().split(",")
                if stock_name not in existing_tickers:
                    thread = threading.Thread(target=monitor_stock, args=(stock_name, direction, percent_change), name=stock_name)
                    threads.append(thread)
                    thread.start()
        time.sleep(1800) # wait for 30 minutes

if __name__ == "__main__":
    print("Monitoring stocks...")
    monitor_stocks()
