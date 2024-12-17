import numpy as np
from arbitrage import solve_arbitrage

# Example: We have received pool data in a Python-friendly format that matches PoolDBData
# In practice, you might load this from JSON or an API
# Below is an example list. Each entry represents one pool from the DEX.
pooldb_data_list = [
    {
      "rpcData": "someData",
      "baseReserve": "10.0",
      "quoteReserve": "1.0",
      "mintAAmount": "1000",
      "mintBAmount": "100",
      "poolPrice": "10.0",
      "lastUpdated": 1234567890,
      "isValid": True,
      "accountId": "SomePublicKeyString1",
      "programId": "SomePublicKeyString2"
    },
    {
      "rpcData": "otherData",
      "baseReserve": "40.0",
      "quoteReserve": "50.0",
      "mintAAmount": "4000",
      "mintBAmount": "5000",
      "poolPrice": "0.8",
      "lastUpdated": 1234567890,
      "isValid": True,
      "accountId": "SomePublicKeyString3",
      "programId": "SomePublicKeyString4"
    },
    # Add as many pool entries as you have...
]

if __name__ == "__main__":
    # Suppose we have a global token list: token0, token1, token2, token3...
    # For simplicity, assume each pool is just between two tokens: 
    # e.g., first pool: token0 and token1; second: token1 and token2, etc.
    # You would define this according to your actual scenario.
    global_indices = [0, 1, 2, 3]

    # From the pool data, we need to construct local_indices, reserves, fees, and amm_types.
    # For demonstration, let's assume:
    # - Each pool is a Uniswap v2 style pool (constant product)
    # - Fee is a fixed 0.997 for all pools
    # - local_indices: each pool is between two consecutive tokens for demonstration
    #   In reality, you'd need a mapping from pool's tokens to global indices.
    #   If all pools are, say, base = token 0, quote = token 1, 
    #   you'd need logic to identify these token indices from pool info.
    #
    # Here, let's just assume:
    # first pool: (0,1)
    # second pool: (1,2)
    # If we had more pools, we'd map them accordingly.

    # Filter valid pools
    valid_pools = [p for p in pooldb_data_list if p["isValid"]]

    # Construct local_indices and reserves from valid pools
    # In a more complex scenario, you'd have a token mapping logic here.
    # For simplicity, we assign them in sequence:
    local_indices = []
    reserves = []
    amm_types = []
    fees = []
    for i, pool in enumerate(valid_pools):
        # Example token assignment logic:
        # Let's say the first pool is between tokens (0, 1)
        # the second between tokens (1, 2), and so forth.
        # This is just an example. In a real scenario, you'd determine
        # which tokens these "baseReserve" and "quoteReserve" correspond to.
        local_index = [i, i+1] if i+1 < len(global_indices) else [0, 1]
        local_indices.append(local_index)

        # Convert reserves from strings to floats
        base_res = float(pool["baseReserve"])
        quote_res = float(pool["quoteReserve"])
        reserves.append(np.array([base_res, quote_res]))

        # Assume a Uniswap v2 style AMM
        amm_types.append("uniswap_v2")

        # Assign a fixed fee for demonstration
        fees.append(0.997)

    # Market values for global tokens:
    # You must know the external reference price of each token
    market_values = [1.5, 10, 2, 3]  # Example values as before

    total_value, psi_solution, deltas_solution, lambdas_solution = solve_arbitrage(
        global_indices=global_indices,
        local_indices=local_indices,
        reserves=reserves,
        fees=fees,
        market_values=market_values,
        amm_types=amm_types,
        weights=None
    )

    print(f"Total output value: {total_value}")
    print("Net token flow (psi):", psi_solution)
    print("Deltas (buys):", deltas_solution)
    print("Lambdas (sells):", lambdas_solution)
