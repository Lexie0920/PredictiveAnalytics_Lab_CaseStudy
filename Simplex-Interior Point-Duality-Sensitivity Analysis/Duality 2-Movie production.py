import cvxpy as cp
import numpy as np

# Primal Problem Definition
M1 = cp.Variable(nonneg=True)  # M1 >= 0
M2 = cp.Variable(nonneg=True)  # M2 >= 0

# Objective: Maximize Z = 70000M1 + 100000M2
primal_objective = cp.Maximize(70000 * M1 + 100000 * M2)

# Constraints
primal_constraints = [
    6 * M1 + 8 * M2 <= 300,  # Directors
    10 * M1 + 15 * M2 <= 500,  # Actors
    4 * M1 + 5 * M2 <= 200   # Studios
]

# Define and solve the primal problem
primal_problem = cp.Problem(primal_objective, primal_constraints)
primal_value = primal_problem.solve()
primal_solution = (M1.value, M2.value)

# Dual Problem Definition
Y1 = cp.Variable(nonneg=True)  # Dual variable for Directors
Y2 = cp.Variable(nonneg=True)  # Dual variable for Actors
Y3 = cp.Variable(nonneg=True)  # Dual variable for Studios

# Objective: Minimize W = 300Y1 + 500Y2 + 200Y3
dual_objective = cp.Minimize(300 * Y1 + 500 * Y2 + 200 * Y3)

# Dual constraints
dual_constraints = [
    6 * Y1 + 10 * Y2 + 4 * Y3 >= 70000,  # Coefficient of M1
    8 * Y1 + 15 * Y2 + 5 * Y3 >= 100000   # Coefficient of M2
]

# Define and solve the dual problem
dual_problem = cp.Problem(dual_objective, dual_constraints)
dual_value = dual_problem.solve()
dual_solution = (Y1.value, Y2.value, Y3.value)

# Output Results
print("=== PRIMAL PROBLEM RESULTS ===")
print(f"Optimal Value (Z): {primal_value}")
print(f"Optimal Solution: M1 = {M1.value}, M2 = {M2.value}")

print("\nPrimal Constraints:")
print(f"Directors: 6M1 + 8M2 <= 300 -> {6*M1.value + 8*M2.value} <= 300")
print(f"Actors: 10M1 + 15M2 <= 500 -> {10*M1.value + 15*M2.value} <= 500")
print(f"Studios: 4M1 + 5M2 <= 200 -> {4*M1.value + 5*M2.value} <= 200")

print("\n=== DUAL PROBLEM RESULTS ===")
print(f"Optimal Value (W): {dual_value}")
print(f"Optimal Solution: Y1 (Directors) = {Y1.value}, Y2 (Actors) = {Y2.value}, Y3 (Studios) = {Y3.value}")

print("\nDual Constraints:")
print(f"6Y1 + 10Y2 + 4Y3 >= 70000 -> {6*Y1.value + 10*Y2.value + 4*Y3.value} >= 70000")
print(f"8Y1 + 15Y2 + 5Y3 >= 100000 -> {8*Y1.value + 15*Y2.value + 5*Y3.value} >= 100000")

print("\n=== STRONG DUALITY CHECK ===")
if np.isclose(primal_value, dual_value):
    print(f"Strong Duality holds: Z (Primal) = W (Dual) = {primal_value}")
else:
    print("Duality gap detected!")
    print(f"Z (Primal Value): {primal_value}")
    print(f"W (Dual Value): {dual_value}")
