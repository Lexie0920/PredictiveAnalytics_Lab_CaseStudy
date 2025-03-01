from scipy.optimize import linprog

from scipy.optimize import linprog

# Objective function coefficients (costs to minimize)
c = [4, 3]  # Cost per serving of Food 1 and Food 2

# Inequality constraints matrix (caloric intake)
A = [
    [-500, -300],  # Min caloric intake (negative for ≥ constraint)
    [500, 300]    # Max caloric intake
]

# Inequality constraints bounds
b = [-2000, 4500]  # Minimum and maximum calories

# Variable bounds (non-negative servings)
x_bounds = (0, None)  # Food 1 servings ≥ 0
y_bounds = (0, None)  # Food 2 servings ≥ 0

# Solve the linear programming problem
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if result.success:
    optimal_food1, optimal_food2 = result.x
    print(f"Optimal servings of Food 1: {optimal_food1:.2f}")
    print(f"Optimal servings of Food 2: {optimal_food2:.2f}")
    print(f"Minimum Cost: ${result.fun:.2f}")
else:
    print("No solution was found.")