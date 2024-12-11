from utils import Symbol, ShortTicker 
import opportunity_detection

if __name__ == "__main__":
    # Define some sample tickers.
    # Define the tickers
    tickers = [
        ShortTicker(symbol=Symbol('BTC', 'USDT'), last_price=30000),
        ShortTicker(symbol=Symbol('ETH', 'BTC'), last_price=0.3),
        ShortTicker(symbol=Symbol('ETH', 'USDT'), last_price=2000),
        ShortTicker(symbol=Symbol('ETH', 'USDC'), last_price=1900),
        ShortTicker(symbol=Symbol('BTC', 'USDC'), last_price=35000),
        ShortTicker(symbol=Symbol('USDC', 'USDT'), last_price=1.1),
        ShortTicker(symbol=Symbol('USDC', 'TUSD'), last_price=0.95),
        ShortTicker(symbol=Symbol('ETH', 'TUSD'), last_price=1950),
        ShortTicker(symbol=Symbol('BTC', 'TUSD'), last_price=32500),
    ]

    best_cycle, profit = opportunity_detection.get_best_opportunity(tickers)
    profit = round(profit, 3)

    if best_cycle:
        print("\nBest Arbitrage Opportunity:")
        for ticker in best_cycle:
            print(ticker)
        print(f"Total Profit: {profit}")
    else:
        print("No profitable arbitrage opportunity detected.")
