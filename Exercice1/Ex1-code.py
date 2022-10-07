from ortools.linear_solver import pywraplp

#1 Import the solver

solver=pywraplp.Solver_CreateSolver('CP_SAT')




#2 create the variables

x= solver.IntVar(0.0 ,solver.infinity(), 'x')
y= solver.IntVar(0.0 ,solver.infinity(), 'y')

#3 create the constraint

solver.Add(x+y<=128)
solver.Add(x*240+y*144<=24000)


#4 define the objective function

solver.Maximize(x*300+y*240)


#5 Invoke the solver and display the results

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    print('x =', x.solution_value())
    print('y =', y.solution_value())
else:
    print('The problem does not have an optimal solution.')