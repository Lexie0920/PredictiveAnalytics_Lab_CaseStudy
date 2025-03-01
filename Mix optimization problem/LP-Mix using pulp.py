from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

# Define the problem
model = LpProblem("Maximize_Profit", LpMaximize)

# Define the variables
x = LpVariable('x', lowBound=50)  # x ≥ 50
y = LpVariable('y', lowBound=50)  # y ≥ 50

# Add objective function
model += 350 * x + 475 * y, "Total Profit"

# Add constraints
model += 5 * x + 8 * y <= 1200, "Constraint_1"
model += 3 * x + 4 * y <= 800, "Constraint_2"
model += 2 * x + 2 * y <= 400, "Constraint_3"

# Solve the problem using PuLP's interface to CBC solver
model.solve(PULP_CBC_CMD(msg=True))

# Output solution and sensitivity analysis
for v in model.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Objective = {model.objective.value()}")

# Display sensitivity analysis (dual values)
#for name, c in model.constraints.items():
  #  print(f"{name}:")
 #   print(f"  Status: {c.pi} (shadow price/dual value)")
   # print(f"  Slack: {c.slack} (surplus for '<=' constraints)")
