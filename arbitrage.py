import numpy as np
import cvxpy as cp

def solve_arbitrage(global_indices, local_indices, reserves, fees, market_values, amm_types, weights=None):
    n = len(global_indices)
    m = len(local_indices)

    # Build local-to-global mapping matrices
    A = []
    for l in local_indices:
        n_i = len(l)
        A_i = np.zeros((n, n_i))
        for i, idx in enumerate(l):
            A_i[idx, i] = 1
        A.append(A_i)

    # Decision variables
    deltas = [cp.Variable(len(l), nonneg=True) for l in local_indices]
    lambdas = [cp.Variable(len(l), nonneg=True) for l in local_indices]

    # Net token flow
    psi = cp.sum([A_i @ (D - L) for A_i, D, L in zip(A, deltas, lambdas)])

    # Objective
    obj = cp.Maximize(market_values @ psi)

    new_reserves = [R + gamma_i * D - L for R, gamma_i, D, L in zip(reserves, fees, deltas, lambdas)]

    cons = []
    for i, amm_type in enumerate(amm_types):
        R_old = reserves[i]
        R_new = new_reserves[i]
        if amm_type.lower() == "balancer":
            if weights is None or weights[i] is None:
                raise ValueError("Balancer pool requires weights.")
            cons.append(cp.geo_mean(R_new, p=weights[i]) >= cp.geo_mean(R_old, p=weights[i]))
        elif amm_type.lower() == "uniswap_v2":
            # Uniswap v2: constant product
            cons.append(cp.geo_mean(R_new) >= cp.geo_mean(R_old))
        elif amm_type.lower() == "constant_product":
            cons.append(cp.geo_mean(R_new) >= cp.geo_mean(R_old))
        elif amm_type.lower() == "constant_sum":
            cons.append(cp.sum(R_new) >= cp.sum(R_old))
            cons.append(R_new >= 0)
        else:
            raise ValueError(f"Unsupported AMM type: {amm_type}")

    cons.append(psi >= 0)

    prob = cp.Problem(obj, cons)
    prob.solve()

    return prob.value, psi.value, [d.value for d in deltas], [l.value for l in lambdas]
