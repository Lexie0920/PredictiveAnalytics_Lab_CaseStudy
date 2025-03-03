''' problem description:

minimize the total cost
solo cost$4, 2 player, 1 arena time; Team cost$6, 1 player, 3 arena time
player >=10, arena time >=12, x,y>=0

( Note: using linprog (change Max to Min), we need to negate the inequalities to <= )
'''

from scipy.optimize import linprog
import pandas as pd

#define the primal problem ( Max---Min)

# coefficients of objective function
c_primal = [4,6]
#constraints
A_primal = [[-2,-1],  #left-hand side coefficients
            [-1,-3]]
b_primal = [-10,-12]  #right-hand side
x_bounds = [(0,None),(0,None)]   #non-negativity for x1 and x2

#solve the primal problem
result_primal = linprog(c=c_primal,A_ub=A_primal,b_ub=b_primal,bounds=x_bounds,method='highs')


#derive and solve the dual problem, then interpret the shadow prices( y1 and y2)
#define the dual problem
c_dual=[10,12]
A_dual=[[2,1],
        [1,3]]
b_dual=[4,6]
y_bounds=[(0,None),(0,None)]
# Solve the dual problem
result_dual = linprog(c=c_dual, A_ub=A_dual, b_ub=b_dual, bounds=y_bounds, method='highs')

# Extract results
Z_primal = result_primal.fun  # Primal objective value
W_dual = -result_dual.fun  # Dual objective value
x_primal = result_primal.x  # Primal variable values
y_dual = result_dual.x  # Dual variable values
primal_slack = result_primal.slack if result_primal.slack is not None else []
dual_slack = result_dual.slack if result_dual.slack is not None else []


# Convert slack variables to lists to check lengths
primal_slack_list = list(primal_slack)
dual_slack_list = list(dual_slack)

# Ensure both lists are of equal length
max_length = max(len(primal_slack_list), len(dual_slack_list))
primal_slack_list += [None] * (max_length - len(primal_slack_list))
dual_slack_list += [None] * (max_length - len(dual_slack_list))

# Extract y1 and y2
y1, y2 = y_dual if len(y_dual) == 2 else (None, None)

# Create summaries for display
primal_summary = pd.DataFrame({
    'Variable': ['x1', 'x2'],
    'Optimal Value': x_primal
})

dual_summary = pd.DataFrame({
    'Constraint': ['Constraint 1 (≥10)', 'Constraint 2 (≥12)'],
    'Shadow Price (Dual Value)': y_dual
})

objective_values = pd.DataFrame({
    'Measure': ['Primal Objective (Z)', 'Dual Objective (W)', 'Difference'],
    'Value': [Z_primal, W_dual, abs(Z_primal - W_dual)]
})

slack_summary = pd.DataFrame({
    'Constraint': [f'Constraint {i+1}' for i in range(max_length)],
    'Primal Slack': primal_slack_list,
    'Dual Slack': dual_slack_list
})

# Display results
print("\nPrimal Solution:")
print(primal_summary)

print("\nDual Solution:")
print(dual_summary)

print("\nObjective Function Values:")
print(objective_values)

print("\nSlack Values:")
print(slack_summary)

print(f"\nShadow Prices: y1 = {y1}, y2 = {y2}")