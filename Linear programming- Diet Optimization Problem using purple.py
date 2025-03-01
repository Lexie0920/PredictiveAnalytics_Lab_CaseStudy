import pulp
# Create a problem variable:
prob = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable("x", lowBound=0, cat='Continuous')  # servings of Food 1
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')  # servings of Food 2

# Objective function
prob += 4 * x + 3 * y, "Total Cost of Food"

# Constraints
prob += 500 * x + 300 * y >= 2000, "Minimum Calories"
prob += 500 * x + 300 * y <= 4500, "Maximum Calories"

# Solve the problem
prob.solve()

# Print the results
print("Status:", pulp.LpStatus[prob.status])
print("Optimal servings of Food 1 (x):", pulp.value(x))
print("Optimal servings of Food 2 (y):", pulp.value(y))
print("Minimum Cost:", pulp.value(prob.objective))