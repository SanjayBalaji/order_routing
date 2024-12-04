import pulp
import numpy as np
import pandas as pd

file_path = "C:/Users/rsanj/OneDrive/03_Trimester5/02_Operations_Analytics/14_Group_Project/Sample_data.xlsx"
distance_df = pd.read_excel(file_path, sheet_name="Distance Matrix", header=None)
deltime_df = pd.read_excel(file_path, sheet_name="Delivery Time Matrix", header=None)

minimum_time = 45
minimum_ser_lvl = 0.7
preparation_time = 7

distance_mat = distance_df.to_numpy()
# warehouse_nos, order_nos = distance_mat.shape
warehouse_nos, order_nos = (13, 35)

distance_mat = np.stack([distance_mat] * order_nos, axis=2)

deltime_mat = deltime_df.to_numpy()
deltime_mat = np.stack([deltime_mat] * order_nos, axis=2)

coktime_mat = np.zeros((warehouse_nos, order_nos, order_nos))

warehouses = range(warehouse_nos)
orders = range(order_nos)

# Fill the matrix with the required values
for k in orders:  # Iterate over each layer
    coktime_mat[:, :, k] = 7 * (k + 1)  # Increment by 7 for each layer

problem = pulp.LpProblem("Cloud_Kitchen_Optimization", pulp.LpMinimize)

x = pulp.LpVariable.dicts("x", (warehouses, orders, orders), cat=pulp.LpBinary)
fulfilled = pulp.LpVariable.dicts("fulfilled", orders, cat=pulp.LpBinary)

#Objective
problem += pulp.lpSum(
    x[i][j][k] * (distance_mat[i][j][k])
    for i in warehouses
    for j in orders
    for k in orders
), "Total_Distance"

#Constaint
for j in orders: 
    problem += pulp.lpSum(x[i][j][k] for i in warehouses for k in orders) == 1
    
for i in warehouses:
    for k in orders:
        problem += pulp.lpSum([x[i][j][k] for j in orders]) <= 1

# Link `fulfilled` to the total weighted time constraint
for j in orders:
    problem += pulp.lpSum(
        x[i][j][k] * (deltime_mat[i][j][k] + coktime_mat[i, j, k])
        for i in warehouses for k in orders
    ) <= minimum_time + (1 - fulfilled[j]) * 1000, f"Fulfillment_Constraint_{j}"

# Total number of fulfilled orders must be at least 90%
problem += pulp.lpSum(fulfilled[j] for j in orders) >= minimum_ser_lvl * order_nos, "Fulfillment_Threshold"

for k in range(len(orders)-1):
    for i in warehouses:
        problem += pulp.lpSum([x[i][j][k] - x[i][j][k+1] for j in orders]) >= 0
      
status = problem.solve(pulp.PULP_CBC_CMD())

for i in warehouses:
    for j in orders:
        flag = False
        for k in orders:
            if x[i][j][k].varValue == 1:
                print(k+1, end=" ")
                flag = True
        # if flag == False:
        #     print(0, end=" ")
    print('')
    
count = 0
for j in orders:
    if sum(x[i][j][k].varValue * (deltime_mat[i][j][k] + coktime_mat[i][j][k]) for i in warehouses for k in orders) <= minimum_time:
        count += 1

print(f'Service Level for {minimum_time} mins delivery:', count/len(orders))