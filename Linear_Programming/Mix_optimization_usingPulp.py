from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

#define the problem
model= LpProblem('Maximize_Profit', LpMaximize)

#define the variables
x= LpVariable('x',lowBound=50)
y= LpVariable('y', lowBound=30)

#add objective function and constraints into the problem
model += 350 * x + 475 * y, "Total Profit"
model += 5 * x + 8 * y <= 1200, "Constraint_1"
model += 3 * x + 4 * y <= 800, "Constraint_2"
model += 2 * x + 2 * y <= 400, "Constraint_3"

# Solve the problem using PuLP's interface to CBC solver
model.solve(PULP_CBC_CMD(msg=True))

# Output solution
for v in model.variables():
    print(f"{v.name} = {v.varValue}")
print(f"Objective = {model.objective.value()}")


#sensitivity analysis （Dual Values）
for name, c in model.constraints.items():
  print(f"{name}:")
  print(f"  Status: {c.pi} (shadow price/dual value)")
  print(f"  Slack: {c.slack} (surplus for '<=' constraints)")

'''
print_result:

Constraint_1:
  Status: 10.0 (shadow price/dual value)
  Slack: 0.0 (surplus for '<=' constraints)
Constraint_2:
  Status: 5.0 (shadow price/dual value)
  Slack: 20.0 (surplus for '<=' constraints)
Constraint_3:
  Status: 0.0 (shadow price/dual value)
  Slack: 50.0 (surplus for '<=' constraints)
  
  interpret:
a shadow price of 10.0 indicates that if the right-hand side value (RHS) of 
constraint_1 increases by 1 unit, the objective function value (profit) will 
increase by 10.0 unites.
this shows that constraint_1 is a critical constraint with !!! a significant 
marginal contribution to the objective function value!!!
slack=0 indicates that the constraint_1 is a binding constraint, meaning
the resource has been fully utilized with no surplus remaining.


- practical Application in decision making


Resource Optimization: Allocate more resources to Constraint_1 to increase the objective function value.  
Cost Savings: Reduce resource allocation to Constraint_3 to lower costs.  
Model Improvement: If Constraint_3 has no practical impact on the problem, consider removing it from the model to simplify the problem.  

Through sensitivity analysis, we can better understand the optimization results of the model and provide a basis for resource allocation and model improvement.
  
  
  
  '''