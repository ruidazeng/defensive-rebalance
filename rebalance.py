import numpy as np
import cvxpy as cp

def defensive_rebalance(global_indices, local_indices, reserves, fees, current_assets):
    """
    Rebalance the portfolio by liquidating assets into a target token.

    Args:
        global_indices (list): List of global token indices.
        local_indices (list): List of local token index pairs for each trading pool.
        reserves (list): List of reserve arrays for each trading pool.
        fees (list): List of fee multipliers for each trading pool.
        current_assets (list): Current asset amounts for each token.

    Returns:
        float: The total liquidated value in the target token.
    """
    # Build local-global matrices
    n = len(global_indices)

    A = []
    for l in local_indices:
        n_i = len(l)
        A_i = np.zeros((n, n_i))
        for i, idx in enumerate(l):
            A_i[idx, i] = 1
        A.append(A_i)

    # Build variables
    deltas = [cp.Variable(len(l), nonneg=True) for l in local_indices]
    lambdas = [cp.Variable(len(l), nonneg=True) for l in local_indices]

    psi = cp.sum([A_i @ (L - D) for A_i, D, L in zip(A, deltas, lambdas)])

    # Objective is to liquidate everything into token 4
    obj = cp.Maximize(psi[4])

    # Reserves after trade
    new_reserves = [R + gamma_i * D - L for R, gamma_i, D, L in zip(reserves, fees, deltas, lambdas)]

    # Trading function constraints
    cons = [
        # Balancer pool with weights adjusted to match reserves[0] size
        cp.geo_mean(new_reserves[0], p=np.array([5, 4, 3, 2, 1])) >= cp.geo_mean(reserves[0]),

        # Uniswap v2 pools
        cp.geo_mean(new_reserves[1]) >= cp.geo_mean(reserves[1]),
        cp.geo_mean(new_reserves[2]) >= cp.geo_mean(reserves[2]),
        cp.geo_mean(new_reserves[3]) >= cp.geo_mean(reserves[3]),

        # Constant sum pool
        cp.sum(new_reserves[4]) >= cp.sum(reserves[4]),
        new_reserves[4] >= 0,

        # Liquidate all assets, except 4
        psi[0] + current_assets[0] == 0,
        psi[1] + current_assets[1] == 0,
        psi[2] + current_assets[2] == 0,
        psi[3] + current_assets[3] == 0
    ]

    # Set up and solve problem
    prob = cp.Problem(obj, cons)
    prob.solve()

    return psi.value[4]
