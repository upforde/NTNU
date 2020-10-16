import copy
import itertools


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        # I added these numbers to serve as counters for the CSP
        self.backtrack_n = 0
        self.failure_n = 0

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = list(filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j]))

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """ 
        # The backtracking counter gets incremented for each time the backtracking
        # function is ran
        self.backtrack_n+=1

        # If the length of the lists is more than one, then the sum of the
        # lengths will be more than the amount of variables, meaning that 
        # if it is equal to the amount of variables, then the function is finished
        if sum(map(len, assignment.values())) == len(self.variables):
            # When finished, return the solution
            return assignment

        # Select an unassigned variable by using the selection function
        # This particular function uses MRV heuristics, because I felt
        # like it would be the most efficient for solving sudoku
        unassigned = self.select_unassigned_variable(assignment)
        
        # For each value from the variable domain
        for value in assignment[unassigned]:
            # create a copy of the domains for the purposes of
            # backtracking
            assignment_copy = copy.deepcopy(assignment)
            # assign the variable inside of the domain to the value
            assignment_copy[unassigned] = [value]
            # if the value assigned is consistent
            if self.inference(assignment_copy, self.get_all_neighboring_arcs(unassigned)):
                # the backtracking function gets called recursivelly
                result = self.backtrack(assignment_copy)
                # If the result is not a failure, the result is returned
                if result: return result
        # The failure counter is incremented for each time the function fails
        self.failure_n+=1
        # The function returns False if it fails
        return False

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """

        # I'm basing this unassigned variable retrieval method on the
        # minimum remaining values heuristic, because that is how humans
        # solve sudoku. By filling in the places with least possible 
        # answers first, the other places get even more constrained
        least = None
        # For each variable in the domains
        for variable in assignment:
            # if the variable has a a domain that is less than the previous smallest domain variable
            # and allso the domain has a length of more than 1
            if (least == None and len(assignment[variable]) > 1) or (len(assignment[variable]) > 1 and len(assignment[variable]) < len(assignment[least])):
                # make variable to least
                least = variable

        # The function returns least
        return least

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """

        # While the queue is not empty
        while queue:
            # pop the first element of queue
            current_i, current_j = queue.pop(0)
            # if the revise function returns true, meaning the assignment
            # has been revised
            if self.revise(assignment, current_i, current_j):
                # if the domain of the current_i element in the queue is empty
                # return False
                if not assignment[current_i]: return False
                # for each neighbouring arc
                for arc in self.get_all_neighboring_arcs(current_i):
                    # append the arc to the queue
                    queue.append(arc)
        
        # Function returns True
        return True

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """

        # Boolean variable that keeps track of wether
        # the assignment has been revised or not
        revised = False
        # For each value in the domain of i
        for x in assignment[i]:
            # a boolean variable used to check
            # wether the value is viable based on the
            # constraints betwixt i and j
            viable = False
            # for each value in the domain of j
            for y in assignment[j]:
                # if (x, y) is allowed by the constraints
                # betwixt i and j
                if (x, y) in self.constraints[i][j]:
                    # if (x, y) is viable, then the value x is viable,
                    # meaning that the rest of the constraints don't need
                    # to be checked. 
                    viable = True
                    break
            # if the value x is not viable
            if not viable:
                # remove the value from the domain of i
                assignment[i].remove(x)
                # set revised to true
                revised = True
        
        # The function returns revised
        return revised


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'], 'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
    colors = ['red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp

def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = list(map(lambda x: x.strip(), open(filename, 'r')))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), list(map(str, range(1, 10))))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print(solution['%d-%d' % (row, col)][0], end=" ")
            if col == 2 or col == 5:
                print('|', end=" ")
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')

easy = create_sudoku_csp('easy.txt')
medium = create_sudoku_csp('medium.txt')
hard = create_sudoku_csp('hard.txt')
veryhard = create_sudoku_csp('veryhard.txt')

print("Easy sudoku")
print_sudoku_solution(easy.backtracking_search())
print("Backtracking", end=": ")
print(easy.backtrack_n)
print("Failure", end=": ")
print(easy.failure_n)
print()
print("Medium sudoku")
print_sudoku_solution(medium.backtracking_search())
print("Backtracking", end=": ")
print(medium.backtrack_n)
print("Failure", end=": ")
print(medium.failure_n)
print()
print("Hard sudoku")
print_sudoku_solution(hard.backtracking_search())
print("Backtracking", end=": ")
print(hard.backtrack_n)
print("Failure", end=": ")
print(hard.failure_n)
print()
print("very hard sudoku")
print_sudoku_solution(veryhard.backtracking_search())
print("Backtracking", end=": ")
print(veryhard.backtrack_n)
print("Failure", end=": ")
print(veryhard.failure_n)
