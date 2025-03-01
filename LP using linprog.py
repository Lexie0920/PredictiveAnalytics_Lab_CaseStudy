from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt

# Objective function coefficients (costs to minimize)
# Note: linprog minimizes, so we negate the profit
c = [-350, -475]  # Cost per serving of DL1 and DL2 (negative profit)

# Inequality constraints matrix (A_ub)
A = [
    [5, 8],      # Hardware constraint
    [3, 4],      # Software constraint
    [2, 2],      # Quality Control constraint
    [-1, 0],    # x >= 50 becomes -x <= -50
    [0, -1]      # y >= 30 becomes -y <= -30
]

# Inequality constraints bounds (b_ub)
b = [1200, 800, 400, -50, -30]  # Upper bounds for the constraints


# Variable bounds (non-negative servings)
x_bounds = (0, None)  # DL1 servings >= 0
y_bounds = (0, None)  # DL2 servings >= 0


# Solve the linear programming problem
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if result.success:
    optimal_x, optimal_y = result.x
    print(f"Optimal DL1: {optimal_x:.2f}")
    print(f"Optimal DL2: {optimal_y:.2f}")
    print(f"Maximum Profit: ${-result.fun:.2f}")
else:
    print("No solution was found.")


# Visualization

# Define the constraints
x = np.linspace(0, 300, 400) # Extend x from 50 to a higher range to cover all constraints
y1 = (1200 - 5 * x) / 8       # 5x + 8y <= 1200
y2 = (800 - 3 * x) / 4        # 3x + 4y <= 800
y3 = (400 - 2 * x) / 2        # 2x + 2y <= 400
y4 = np.full_like(x, 30)   # y >= 30


# Setting up the plot
plt.figure(figsize=(10, 8))
plt.xlim(0, 300)
plt.ylim(0, 300)
plt.xlabel('Servings of DL1 (x)')
plt.ylabel('Servings of DL2 (y)')


# Plot each line
plt.plot(x, y1, label=r'$5x + 8y \leq 1200$', linestyle='--')
plt.plot(x, y2, label=r'$3x + 4y \leq 800$', linestyle='--')
plt.plot(x, y3, label=r'$2x + 2y \leq 400$', linestyle='--')
plt.axhline(30, color='orange', label=r'$y \geq 30$', linestyle='--')
plt.axvline(50, color='red', label=r'$x \geq 50$', linestyle='--')

# Calculate the feasible region by considering all constraints
y = np.minimum(np.minimum(y1, y2), y3)
y = np.maximum(y, 30)

# Fill the feasible region
plt.fill_between(x, y, 30, where=(x >= 50) & (y >= 30) & (y <= y1) & (y <= y2) & (y <= y3), color='gray', alpha=0.5, label='Feasible Region')

# Plot the optimal solution
optimal_x, optimal_y = result.x
plt.plot(optimal_x, optimal_y, 'ro', markersize=10, label=f'Optimal Solution ({optimal_x:.2f}, {optimal_y:.2f})')

# Add legend
plt.legend()
plt.title('Feasible Region with Constraint Lines and Optimal Solution')
plt.show()
