"""
Enhanced implementation of DEX arbitrage optimization based on the work:

'Optimal Routing for Constant Function Market Makers'
by Guillermo Angeris, Tarun Chitra, Alex Evans, Stephen Boyd
Original code: https://github.com/angeris/cfmm-routing-code

This implementation extends their approach with additional features including:
- Enhanced error handling and validation
- Comprehensive trade analysis
- Object-oriented structure
- Type hints and documentation
"""

import numpy as np
import cvxpy as cp
from typing import List, Tuple
import logging

class DexArbitrage:
    def __init__(
        self,
        global_indices: List[int],
        local_indices: List[List[int]],
        reserves: List[np.ndarray],
        fees: List[float],
        market_value: List[float]
    ):
        """
        Initialize DEX arbitrage system.
        
        Args:
            global_indices: List of all token indices
            local_indices: List of token indices for each pool
            reserves: List of token reserves for each pool
            fees: List of fee multipliers for each pool
            market_value: Market prices for each token
        """
        self.global_indices = global_indices
        self.local_indices = local_indices
        self.reserves = reserves
        self.fees = fees
        self.market_value = market_value
        
        # Validate inputs
        self._validate_inputs()
        
        # Build local-global matrices
        self.A = self._build_matrices()
        
        # Initialize optimization variables
        self.deltas = None
        self.lambdas = None
        self.psi = None
        self.prob = None
        
    def _validate_inputs(self):
        """Validate input data consistency."""
        n_pools = len(self.local_indices)
        
        if not (len(self.fees) == n_pools and
                len(self.reserves) == n_pools):
            raise ValueError("Inconsistent number of pools across inputs")
            
        for i, (indices, reserves) in enumerate(zip(self.local_indices, self.reserves)):
            if len(indices) != len(reserves):
                raise ValueError(f"Mismatch between indices and reserves in pool {i}")
                
        if not all(0 < fee <= 1 for fee in self.fees):
            raise ValueError("Fees must be between 0 and 1")
            
    def _build_matrices(self) -> List[np.ndarray]:
        """Build local-global conversion matrices."""
        n = len(self.global_indices)
        A = []
        
        for l in self.local_indices:
            n_i = len(l)
            A_i = np.zeros((n, n_i))
            for i, idx in enumerate(l):
                A_i[idx, i] = 1
            A.append(A_i)
            
        return A
        
    def setup_optimization(self):
        """Set up the optimization problem."""
        # Build variables
        self.deltas = [cp.Variable(len(l), nonneg=True) for l in self.local_indices]
        self.lambdas = [cp.Variable(len(l), nonneg=True) for l in self.local_indices]
        
        # Net token flow
        self.psi = cp.sum([A_i @ (L - D) for A_i, D, L in zip(self.A, self.deltas, self.lambdas)])
        
        # Objective: maximize market value of output
        obj = cp.Maximize(self.market_value @ self.psi)
        
        # Calculate new reserves after trades
        new_reserves = [
            R + gamma_i*D - L 
            for R, gamma_i, D, L in zip(self.reserves, self.fees, self.deltas, self.lambdas)
        ]
        
        # Trading constraints
        cons = [
            # Balancer pool constraint
            cp.geo_mean(new_reserves[0], p=np.array([4, 3, 2, 1])) >= cp.geo_mean(self.reserves[0]),
            
            # Uniswap v2 constraints
            *[cp.geo_mean(new_reserves[i]) >= cp.geo_mean(self.reserves[i]) for i in range(1, 4)],
            
            # Constant sum pool constraints
            cp.sum(new_reserves[4]) >= cp.sum(self.reserves[4]),
            new_reserves[4] >= 0,
            
            # No negative token holdings
            self.psi >= 0
        ]
        
        self.prob = cp.Problem(obj, cons)
        
    def solve(self) -> Tuple[float, dict]:
        """
        Solve the optimization problem and return results.
        
        Returns:
            tuple: (optimal_value, detailed_results)
        """
        if self.prob is None:
            self.setup_optimization()
            
        try:
            optimal_value = self.prob.solve()
            
            if self.prob.status != 'optimal':
                raise RuntimeError(f"Problem not solved optimally. Status: {self.prob.status}")
                
            results = {
                'optimal_value': optimal_value,
                'deltas': [d.value for d in self.deltas],
                'lambdas': [l.value for l in self.lambdas],
                'net_flow': self.psi.value
            }
            
            return optimal_value, results
            
        except cp.error.SolverError as e:
            logging.error(f"Solver error: {e}")
            raise
            
    def analyze_trades(self, results: dict) -> dict:
        """
        Analyze the trading results.
        
        Args:
            results: Dictionary containing optimization results
            
        Returns:
            dict: Analysis metrics
        """
        analysis = {
            'total_value_traded': 0,
            'fees_paid': 0,
            'profit_by_token': np.zeros(len(self.global_indices)),
            'active_pools': set()
        }
        
        for pool_idx in range(len(self.local_indices)):
            deltas = results['deltas'][pool_idx]
            lambdas = results['lambdas'][pool_idx]
            
            # Skip inactive pools
            if np.all(deltas < 1e-6) and np.all(lambdas < 1e-6):
                continue
                
            analysis['active_pools'].add(pool_idx)
            
            # Calculate pool metrics
            pool_tokens = self.local_indices[pool_idx]
            
            for i, (delta, token_idx) in enumerate(zip(deltas, pool_tokens)):
                if delta > 1e-6:
                    value = delta * self.market_value[token_idx]
                    analysis['total_value_traded'] += value
                    analysis['profit_by_token'][token_idx] -= value
                    
            for i, (lambd, token_idx) in enumerate(zip(lambdas, pool_tokens)):
                if lambd > 1e-6:
                    value = lambd * self.market_value[token_idx]
                    analysis['profit_by_token'][token_idx] += value
                    
            # Calculate fees
            fees_paid = np.sum(deltas) * (1 - self.fees[pool_idx])
            analysis['fees_paid'] += fees_paid
            
        return analysis
