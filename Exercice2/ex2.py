from __future__ import print_function

import time

from ortools.sat.python import cp_model


def main():
    # define model: you can use CpModel()

    start = time.time()
    impact = [
        [30, 45, 40, 50, 70, 90, 110, 100],
        [35, 50, 45, 66, 79, 100, 130, 90],
        [40, 60, 50, 70, 80, 90, 100, 90],
        [55, 65, 60, 80, 90, 110, 60, 80],
        [79, 80, 60, 90, 105, 120, 80, 97],
        [86, 90, 80, 95, 110, 130, 90, 100],
        [90, 100, 90, 148, 103, 140, 95, 110],
        [180, 190, 110, 159, 116, 190, 140, 130],
        [200, 260, 180, 170, 150, 200, 180, 190],
        [200, 270, 260, 200, 170, 210, 200, 190]]
    num_vehicles = len(impact)
    num_jobs = len(impact[0])
    num_group = 3

    group1 = [0, 1, 2, 3]
    group2 = [4, 5, 6]
    group3 = [7, 8, 9]
    group = [group1, group2, group3]

    max_aut = [150, 300, 500]  # max autonomy for group 1

    distances = [130, 80, 230, 100, 150, 440, 110, 250]

    model = cp_model.CpModel()

    # Variables
    x = {}
    '''
    for i in range(num_vehicles):
        for j in range(num_jobs):
            x[i, j] = model.NewIntVar(0, 1, '')
    '''
    for vehicle in range(num_vehicles):
        for job in range(num_jobs):
            x[vehicle, job] = model.NewBoolVar(f'x[{vehicle},{job}]')

    # Constraints

    # Each vehicle is assigned to at most one job.
    for vehicle in range(num_vehicles):
        model.AddAtMostOne(x[vehicle, job] for job in range(num_jobs))

    # Each job is assigned to exactly one vehicle.
    for job in range(num_jobs):
        model.AddExactlyOne(x[vehicle, job] for vehicle in range(num_vehicles))

    '''
    # each job has only one vehicle
    for j in range(num_jobs):
        model.Add(model.Sum(x[i, j] for i in range(num_vehicles)) == 1)

    # each vehicle is assigned to at most 1 job
    for i in range(num_vehicles):
        model.Add(solver.Sum(x[i, j] for j in range(num_jobs)) <= 1)
    '''

    # Max autonomy constraint
    for t in range(num_group):
        max_dist = max_aut[t]
        for i in group[t]:
            for j in range(num_jobs):
                model.Add(x[i, j] * distances[j] <= max_dist)

    # define objective function and solve the model
    objective_terms = []
    for i in range(num_vehicles):
        for j in range(num_jobs):
            objective_terms.append(impact[i][j] * x[i, j])
    model.Minimize(sum(objective_terms))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print('Minimum impact = %i' % solver.ObjectiveValue())
        print()

        for i in range(num_vehicles):

            for j in range(num_jobs):

                if solver.Value(x[i,j]) == 1:
                    print('Vehicle ', i, ' performs delivery ', j, '  Km = ', impact[i][j])
        print()
        end = time.time()
        print("Time = ", round(end - start, 4), "seconds")


if __name__ == '__main__':
    main()
