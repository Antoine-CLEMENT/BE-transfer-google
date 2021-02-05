import facile
import numpy as np
import string

def solver(cost, OWA):
    assert OWA in ['utilitarism', 'egalitarism', 'gini']
    
    n_task = cost.shape[1]
    n_agent = cost.shape[0]
    
    boolean_variable = np.array([ facile.array([ facile.variable([0,1]) for i in range(n_task)]) for j in range(n_agent)])

    # Every task must be complete, by only one agent !
    for j in range(n_task):
        facile.constraint(sum(boolean_variable[:, j]) == 1)
    
    how_does_it_cost = facile.array(
        [ np.matmul(cost[i, :], facile.array(boolean_variable[i, :])) for i in range (n_agent)]
    )

    if OWA == 'utilitarism':
        weights = np.array([1 for i in range(n_agent)])
    elif OWA == 'egalitarism':
# as we only have the .sort() method for desutilities, weights must be in reverse order because the 'desutilities' should be sorted in descending order
        weights = np.array([0 for i in range(n_agent)])
        weights[-1] = 1
    else : 
# as we only have the .sort() method for desutilities, weights must be in reverse order because the 'desutilities' should be sorted in descending order
        weights = np.flip(np.array([ 2* (n_agent - i) + 1 for i in range(1, n_agent + 1)]))
        
    print(weights)
    to_minimize = np.matmul(weights, how_does_it_cost.sort())
    
    vars = []
    
    for i in range(n_agent):
        for j in range(n_task):
            vars.append(boolean_variable[i, j])

    res = np.array(facile.minimize(vars, to_minimize).solution)    
    boolean_res = res > 0
    
    tasks = np.array([list(string.ascii_lowercase)[0:n_task]])
    
    for i in range(n_agent):
        boolean_res[i:i+n_task]
        print(i + 1, ' does : ', tasks[:,boolean_res[n_task * i:n_task * (i + 1)]][0])
