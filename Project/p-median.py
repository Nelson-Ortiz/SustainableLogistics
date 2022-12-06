from __future__ import print_function

import pandas as pd
from ortools.sat.python import cp_model as cp

# df = pd.read_excel('test.xlsx')
URL_path_dem = 'https://github.com/Nelson-Ortiz/SustainableLogistics/blob/0e7fec39e97c84cd9a01817347aa82e06b207121/test.xlsx?raw=true'
df_dem = pd.read_excel(URL_path_dem)
dem_stud = df_dem['Student'].values.tolist()
dem_stud = [int(elem) for elem in dem_stud]  # we transform the elements into integers

URL_path_dist = 'https://github.com/Nelson-Ortiz/SustainableLogistics/blob/master/test2.xlsx?raw=true'
df_dist = pd.read_excel(URL_path_dist)
dist_stud = df_dist.values.tolist()
# convert each distance into an integer
for n, i in enumerate(dist_stud):
    for k, j in enumerate(i):
        dist_stud[n][k] = int(j)


# dist_stud = [item for subl in dist_stud for item in subl]

def main():
    # Model
    model = cp.CpModel()

    # Data delcration
    p = 11

    num_customers = 17
    customers = list(range(num_customers))

    num_warehouses = 16
    warehouses = list(range(num_warehouses))

    demand = dem_stud
    distance = dist_stud

    # Variable delcaration
    open = [model.NewIntVar(0, num_warehouses, 'open[%i]% % i') for w in warehouses]
    x = {}
    for c in customers:
        for w in warehouses:
            x[c, w] = model.NewIntVar(0, 1, 'x[%i,%i]' % (c, w))

    z = model.NewIntVar(0, 1000, 'z')

    # Constraints
    model.Add(z == sum([
        demand[c] * distance[c][w] * x[c, w]
        for c in customers
        for w in warehouses
    ]))

    for c in customers:
        model.Add(sum([x[c, w] for w in warehouses]) == 1)

    model.Add(sum(open) == p)

    for c in customers:
        for w in warehouses:
            model.Add(x[c, w] <= open[w])

    # Objective function
    model.Minimize(z)

    # Model solution
    solver = cp.CpSolver()
    status = solver.Solve(model)

    if status == cp.OPTIMAL:
        print('z:', solver.Value(z))
        print('open:', [solver.Value(open[w]) for w in warehouses])
        for c in customers:
            for w in warehouses:
                print(solver.Value(x[c, w]), end=' ')
            print()
        print()

    print('WallTime:', solver.WallTime())


if __name__ == '__main__':
    main()
