import arbitrage
import numpy as np

# Example usage
if __name__ == "__main__":
    # Problem data
    global_indices = list(range(4))
    local_indices = [
        [0, 1, 2, 3],
        [0, 1],
        [1, 2],
        [2, 3],
        [2, 3]
    ]
    reserves = list(map(np.array, [
        [4, 4, 4, 4],
        [10, 1],
        [1, 5],
        [40, 50],
        [10, 10]
    ]))
    fees = [.998, .997, .997, .997, .999]
    market_value = [1.5, 10, 2, 3]
    
    # Initialize and run optimization
    arbitrage = arbitrage.DexArbitrage(global_indices, local_indices, reserves, fees, market_value)
    
    try:
        optimal_value, results = arbitrage.solve()
        analysis = arbitrage.analyze_trades(results)
        
        print(f"Optimal value: {optimal_value:.4f}")
        print(f"Total value traded: {analysis['total_value_traded']:.4f}")
        print(f"Total fees paid: {analysis['fees_paid']:.4f}")
        print(f"Active pools: {analysis['active_pools']}")
        print("Profit by token:")
        for i, profit in enumerate(analysis['profit_by_token']):
            print(f"  Token {i}: {profit:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")