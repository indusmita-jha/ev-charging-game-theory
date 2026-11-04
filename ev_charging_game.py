import os
import matplotlib
# 1. Force non-interactive backend to prevent window freezing/hanging
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def run_fast_ev_game():
    print("=== EV CHARGING GAME SIMULATION (ULTRA-FAST VERSION) ===")
    
    # Create plots directory if it doesn't exist
    os.makedirs("plots", exist_ok=True)

    # -------------------------------------------------------------
    # 1. Model Parameters
    # -------------------------------------------------------------
    a = 100.0   # Base demand
    b = 5.0     # Own-price elasticity
    c = 2.0     # Competitor cross-price elasticity
    mc = 0.15   # Wholesale electricity cost ($0.15/kWh)

    # -------------------------------------------------------------
    # 2. Closed-Form Analytical Nash Equilibrium (Instant Calculation)
    # -------------------------------------------------------------
    # Best Response Equation: p_i*(p_j) = (a + b*mc + c*p_j) / (2*b)
    intercept = (a + b * mc) / (2 * b)  # 10.075
    slope = c / (2 * b)                  # 0.20

    # Symmetric Nash Equilibrium Price: p* = (a + b*mc) / (2*b - c)
    p_eq = (a + b * mc) / (2 * b - c)    # $12.59375
    q_eq = a - b * p_eq + c * p_eq       # Demand
    profit_eq = (p_eq - mc) * q_eq       # Industry Profit

    print(f"\n[Analytical Nash Equilibrium Results]")
    print(f" Best Response Function : p1 = {intercept:.3f} + {slope:.2f} * p2")
    print(f" Equilibrium Price (p*) : ${p_eq:.2f} / kWh")
    print(f" Station Demand (Q*)   : {q_eq:.2f} kWh")
    print(f" Station Profit (π*)   : ${profit_eq:.2f}")

    # -------------------------------------------------------------
    # 3. Discrete 2x2 Prisoner's Dilemma Matrix
    # -------------------------------------------------------------
    pH, pL = 15.0, 10.0  # High vs Low Price
    
    def calc_profit(p_i, p_j):
        q = a - b * p_i + c * p_j
        return (p_i - mc) * q if q > 0 else 0

    print("\n[2x2 Discrete Matrix Game (Profits in $)]")
    print(f" (High, High) -> (${calc_profit(pH, pH):.0f}, ${calc_profit(pH, pH):.0f}) [Collusive]")
    print(f" (High, Low ) -> (${calc_profit(pH, pL):.0f}, ${calc_profit(pL, pH):.0f})")
    print(f" (Low,  High) -> (${calc_profit(pL, pH):.0f}, ${calc_profit(pH, pL):.0f})")
    print(f" (Low,  Low ) -> (${calc_profit(pL, pL):.0f}, ${calc_profit(pL, pL):.0f}) [NASH EQUILIBRIUM]")

    # -------------------------------------------------------------
    # 4. Plot 1: Best Response Curves & Nash Equilibrium Point
    # -------------------------------------------------------------
    p_vals = np.linspace(8, 18, 50)
    br1 = intercept + slope * p_vals  # Station 1 BR
    br2 = intercept + slope * p_vals  # Station 2 BR

    plt.figure(figsize=(6, 5))
    plt.plot(p_vals, br1, label='Station 1 Best Response', color='#1f77b4', linewidth=2)
    plt.plot(br2, p_vals, label='Station 2 Best Response', color='#ff7f0e', linewidth=2, linestyle='--')
    plt.plot(p_eq, p_eq, 'ro', markersize=8, label=f'Nash Equilibrium (${p_eq:.2f})')
    
    plt.title('EV Charging Price Competition: Best Response Curves', fontsize=11, fontweight='bold')
    plt.xlabel('Station 1 Price ($/kWh)')
    plt.ylabel('Station 2 Price ($/kWh)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig('plots/best_response_fast.png', dpi=150)
    plt.close()

    # -------------------------------------------------------------
    # 5. Plot 2: Subsidy Sensitivity Analysis
    # -------------------------------------------------------------
    subsidized_costs = np.linspace(0.05, 0.25, 10)
    eq_prices = (a + b * subsidized_costs) / (2 * b - c)

    plt.figure(figsize=(6, 4))
    plt.plot(subsidized_costs, eq_prices, marker='o', color='green', linewidth=2)
    plt.title('Effect of Grid Subsidy on Charging Price', fontsize=11, fontweight='bold')
    plt.xlabel('Wholesale Grid Electricity Cost ($/kWh)')
    plt.ylabel('Equilibrium Retail Price ($/kWh)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('plots/subsidy_sensitivity_fast.png', dpi=150)
    plt.close()

    print("\n✓ Success! Plots saved instantly in 'plots/' folder without hanging.")

if __name__ == "__main__":
    run_fast_ev_game()