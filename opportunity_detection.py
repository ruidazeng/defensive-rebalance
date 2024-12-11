import networkx as nx
from utils import Symbol, ShortTicker 
from typing import List, Tuple, Optional

def get_best_opportunity(tickers: List[ShortTicker], max_cycle: int = 10) -> Tuple[Optional[List[ShortTicker]], float]:
    """
    Find the best arbitrage opportunity in a list of tickers.

    Args:
        tickers (List[ShortTicker]): List of ShortTicker objects representing market data.
        max_cycle (int): Maximum allowed cycle length. Defaults to 10.

    Returns:
        Tuple[Optional[List[ShortTicker]], float]: Best cycle of tickers and associated profit.
    """
    graph = nx.DiGraph()

    # Build the directed graph of currencies.
    for ticker in tickers:
        if ticker.symbol is not None:
            graph.add_edge(ticker.symbol.base, ticker.symbol.quote, ticker=ticker)
            graph.add_edge(
                ticker.symbol.quote,
                ticker.symbol.base,
                ticker=ShortTicker(
                    Symbol(ticker.symbol.quote, ticker.symbol.base),  # Corrected here
                    1 / ticker.last_price,
                    reversed=True
                )
            )

    best_profit = 1.0
    best_cycle = None

    # Find all cycles in the graph with a length <= max_cycle.
    for cycle in nx.simple_cycles(graph):
        if len(cycle) > max_cycle:
            continue

        profit = 1.0
        tickers_in_cycle = []

        # Calculate the profit along the cycle.
        for i, base in enumerate(cycle):
            quote = cycle[(i + 1) % len(cycle)]  # Wrap around to complete the cycle.
            ticker = graph[base][quote]['ticker']
            tickers_in_cycle.append(ticker)
            profit *= ticker.last_price

        if profit > best_profit:
            best_profit = profit
            best_cycle = tickers_in_cycle

    # Adjust the best cycle to ensure consistent representation.
    if best_cycle is not None:
        best_cycle = [
            ShortTicker(
                Symbol(ticker.symbol.quote, ticker.symbol.base),  # Corrected here
                ticker.last_price,
                reversed=True
            ) if ticker.reversed else ticker
            for ticker in best_cycle
        ]

    return best_cycle, best_profit

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

    best_cycle, profit = get_best_opportunity(tickers)
    profit = round(profit, 3)

    if best_cycle:
        print("\nBest Arbitrage Opportunity:")
        for ticker in best_cycle:
            print(ticker)
        print(f"Total Profit: {profit}")
    else:
        print("No profitable arbitrage opportunity detected.")
