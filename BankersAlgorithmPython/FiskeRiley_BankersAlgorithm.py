import numpy as np

# Write a program (in your favorite programming language) to implement the Banker’s algorithm for deadlock avoidance. Your program should accept as input the following set of matrices:
# • Allocation matrix describing the number of each resource type currently allocated to each process.
# • Maximum demand matrix describing the maximum number of each resource type that may be used by each process at any given time.
# • Available vector indicating the currently available number of each resource type.
# Your program should also accept a vector representing a set of resource requests by a process, i.e. the number of each resource type currently being requested by a given process.
# The program should then determine whether the request should be granted.
# Your program should display the “available” vector after each cycle, and display the final result of granting or denying the request.
# Design your own test data; you must have 2 data sets, one that will result in the request being granted and one that will result in the request being denied.

def request_safe_bankers_algorithm(allocation_matrix, maximum_matrix, available_vector, request_vector_process_number, request_vector_resources):
    is_safe = False
    # first check if request is less than or equal to available
    for a, r in zip(available_vector, request_vector_resources):
        if a < r:
            return is_safe
    
    # advance if initial request is okay
                
    for i in range(len(allocation_matrix[request_vector_process_number - 1])):
        allocation_matrix[request_vector_process_number - 1][i] += request_vector_resources[i]

    available_vector -= request_vector_resources
    print(available_vector) # show the available vector

    # create boolean vector to store if a row has been checked or not
    boolean_vector = np.zeros(len(allocation_matrix),dtype=bool)

    need_matrix = maximum_matrix - allocation_matrix
        
    # the main loop
    while(True):

        at_least_one_good = False # boolean to escape loop if complete one full cycle with no matches
    
        for n_row in range(len(need_matrix)): # cycle through the need matrix
            if not boolean_vector[n_row]: # if not already completed
                if all(need_matrix[n_row] <= available_vector): # if all slots in need are less than or equal to all slots in available
                    print("Row ", n_row + 1, " is good")
                    available_vector += allocation_matrix[n_row] # add allocation to available
                    boolean_vector[n_row] = True # set boolean cell to true
                    at_least_one_good = True # found one, so don't break the loop this time
                    print(available_vector) # show the available vector

        if not at_least_one_good: # break if no matches were found this cycle
            break

    if all(boolean_vector): # is safe if boolean vector is all true, aka all needs are fulfilled
        is_safe = True
    
    return is_safe

# From Test 1, safe process
allocation_1 = np.array([[2,0,1,1],[0,1,2,1],[0,0,0,3],[0,2,1,0],[1,0,3,0]])
max_1 = np.array([[3,2,1,4],[0,2,5,2],[5,1,0,5],[1,5,3,0],[3,0,3,3]])
available_1 = np.array([5,2,2,2])
request_1 = np.array([4,1,0,0])
requesting_process_1 = 3

if request_safe_bankers_algorithm(allocation_1,max_1,available_1,requesting_process_1,request_1) == True:
    print("Request 1 is a safe process.")
else:
    print("Request 1 is an unsafe process.")

# From Slides, unsafe process
allocation_2 = np.array([[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]])
max_2 = np.array([[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]])
available_2 = np.array([3,3,2])
request_2 = np.array([3,3,0])
requesting_process_2 = 5

if request_safe_bankers_algorithm(allocation_2,max_2,available_2,requesting_process_2,request_2) == True:
    print("Request 2 is a safe process.")
else:
    print("Request 2 is an unsafe process.")