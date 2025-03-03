from scipy.optimize import linprog
import pandas as pd

pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 100)
pd.set_option('display.max_columns', None)

# Define primal problem
# Minimize: Z = 3x1 + 5x2
# Subject to:
# x1 + 2x2 ≥ 8  -> -x1 - 2x2 ≤ -8
# 2x1 + x2 ≥ 6  -> -2x1 - x2 ≤ -6
# x1, x2 ≥ 0

# Coefficients for the objective function (minimization)
c = [3, 5]

# Coefficients for the inequality constraints
A = [
    [-1, -2],  # Converted constraint: x1 + 2x2 ≥ 8 -> -x1 - 2x2 ≤ -8
    [-2, -1]   # Converted constraint: 2x1 + x2 ≥ 6 -> -2x1 - x2 ≤ -6
]
b = [-8, -6]  # Right-hand side of inequalities

# Solve primal problem
primal_solution = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method="highs")

# Dual problem
# Maximize: W = 8y1 + 6y2
# Subject to:
# y1 + 2y2 ≤ 3
# 2y1 + y2 ≤ 5
# y1, y2 ≥ 0

# Coefficients for the objective function (maximization)
c_dual = [-8, -6]  # Negative of the coefficients because linprog minimizes by default

# Coefficients for the inequality constraints (dual)
A_dual = [
    [1, 2],  # Dual constraint for x1
    [2, 1]   # Dual constraint for x2
]
b_dual = [3, 5]  # Right-hand side of inequalities

# Solve dual problem
dual_solution = linprog(c_dual, A_ub=A_dual, b_ub=b_dual, bounds=(0, None), method="highs")

# Extract results
primal_results = {
    "Z (Optimal Value)": [primal_solution.fun],
    "x1 (Optimal)": [primal_solution.x[0]],
    "x2 (Optimal)": [primal_solution.x[1]],
    "y1 (Shadow Price)": [dual_solution.x[0]],
    "y2 (Shadow Price)": [dual_solution.x[1]],
    "W (Optimal Value)": [-dual_solution.fun]  # Convert back to maximization
}

# Convert to DataFrame
df_results = pd.DataFrame(primal_results)

# Print results
print("\nPrimal and Dual Optimization Results:")
print(df_results)

print(f"\nOptimal Value (Z): {primal_solution.fun}")
print(f"Optimal Variables: x1 = {primal_solution.x[0]}, x2 = {primal_solution.x[1]}")
print(f"Shadow Prices: y1 = {dual_solution.x[0]}, y2 = {dual_solution.x[1]}")
print(f"Optimal Value (W): {-dual_solution.fun}")  # Convert back to maximization
