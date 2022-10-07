from ortools.sat.python import cp_model


def ConstraintOptimization():
    """Linear programming sample."""
    # Instantiate a Glop solver, naming it LinearExample.
    model= cp_model.CpModel()

    #Create the variables
    num_vals= 3 #number of values that the variables can take
    x = model.NewIntVar(0, num_vals-1,'x') # num_vals-1 is the upper bound. It is not mandatory to name the variables.
    y = model.NewIntVar(0, num_vals-1,'y')
    z = model.NewIntVar(0, num_vals-1,'z')

    #create the constraint
    model.Add(x != y )
    model.Add(x > y )

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)


    #print results

    """print("done! 🥇🥇")
    print('x=%i' % solver.Value(x))
    print('y=%i' % solver.Value(y))
    print('z=%i' % solver.Value(z))
    """
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Maximum of objective function: {solver.ObjectiveValue()}\n')
        print(f'x = {solver.Value(x)}')
        print(f'y = {solver.Value(y)}')
        print(f'z = {solver.Value(z)}')
    else:
        print('No solution found.')

        # Statistics.
    print('\nStatistics')
    print(f'  status   : {solver.StatusName(status)}')
    print(f'  conflicts: {solver.NumConflicts()}')
    print(f'  branches : {solver.NumBranches()}')
    print(f'  wall time: {solver.WallTime()} s')

if __name__ == '__main__':
    ConstraintOptimization()

    #print the results

