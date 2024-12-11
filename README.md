# Defensive Rebalancing

## Armored AMMs: Capturing Arbitrage Opportunities with Defensive Rebalancing

### Overview
This thesis investigates the new paradigm of Defensive Rebalancing in the context of Automated Market Makers (AMMs) in decentralized finance (DeFi). With the prevalence of arbitrage whenever AMMs present different spot prices, there arises the question of how liquidity providers (LPs) can capture some of the arbitrageur’s would-be profit. One promising strategy is Defensive Rebalancing, where AMMs make trades with one another to eliminate an arbitrage opportunity between a given set of AMMs.

### Features
- **Optimal Rebalancing Problem**: Presents a modification of the Optimal Routing Problem with several nuances.
- **Mathematical Framework**: Analyzes self-rebalancing strategies in terms of optimality and relative welfare.
- **Convex Optimization**: Details a problem that can be efficiently solved to maximize LPs’ profits under fairness constraints.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/ruidazeng/defensive-rebalancing.git
   ```
2. Navigate to the project directory:
   ```bash
   cd defensive-rebalancing
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
To run the system, execute the main script:
```bash
python main.py
```

### Contributing
Contributions are welcome! Please submit pull requests or open issues to discuss potential improvements.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
