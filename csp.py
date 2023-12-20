#
#  Constraint Statisfaction for map coloring!
#

class CSP():

    def __init__(self, graph, domains):
        """ Initialize a graph-coloring problem:

        Arguments:
          graph: a map from int -> set of integers
                that represents the graph in an
                adjacency set format.
                That is, each vertex in the graph
                has a integer index from 0...(nvertices-1)
                and the set stored at graph[i] represents
                all destination vertices from outgoing edges
                from vertex i.  In this representation, an
                undirected edge is represented as two directional
                edges: one from i to j and one from j to i.
                Further, it is not possible with this representation
                to have two distinct edges from i to j.

          domains: a map from int -> set where each element in
                the set stored at domain[i] indicates possible
                values that the vertex i may consider. e.g.,
                if domains[0] = { 'R', 'G', 'B' }, then vertex
                0 in the graph could be colored 'R', 'G', or 'B'

        """
        self.graph = graph
        self.domains = domains
        self.nvertices = len(self.graph)

        #self.solutions = [] 

    def solve(self, solutions=1, count=False, allstats=False, quiet=True):
        """_ Part 1: Implement this method _

        Arguments:
          solutions - the desired number of solutions to return.
                      it is possible that the search space will be
                      exhausted prior to finding the desired number
                      of solutions in which case all found solutions
                      will be returned.

          count - True if you should fully explore the state space
                  and return a count of legal solutions.  False if
                  you should terminate early, when the desired number
                  of solutions is found.

          allstats - True if you should return information about the
                  number of states that are pruned during search.
                  Supporting this argument is *optional*

          quiet - if True, don't print any output; there is no
                  need to do anything special if quiet == False,
                  but you should obey quiet == True by ensuring
                  no output is generated.


        Returns:
          a dictionary with keys dependent on the arguments:
          solutions, count and allstats:

          if solutions is > 0:
          'Solutions': should be a list of sequences; each sequence a
                       legal domain value for each vertex in the graph.
                       The length of the 'Solutions' list should be
                       == the solutions argument unless fewer solutions
                       actually exist in the search space. In that case,
                       all solutions should be included in the list.

          if count == True:
          'SolutionCount': the number of fully specified states that are valid
                           solutions

          if allstats == True:
          'Unexplored' : the number of fully specified states that have not
                         been deemed a solution or rejected
          'Rejected': the number of fully specified states that have been
                       eliminated as solutions
          'Enqueued': the number of *partial* states that have been put
                      on the queue

          Note that when count == True,
           The each state in the state space must either be a solution or rejected.
          when count == False,
           it is possible that a solution is returned while some fully specified
           states remain unexplored.
        """
        
        if not quiet:
            print("Calculating Solutions...")

        sol = []
        self.backTrackingSearch([], sol, quiet);

        if not quiet:
            print("All returned solutions: ", sol)
        
        cspDict = {}

        if (solutions > 0):
            if (solutions >= len(sol)):
                cspDict['Solutions'] = sol
            else:
                cspDict['Solutions'] = sol[:solutions]

        if count == True:
            cspDict['SolutionCount'] = len(sol)

        #if allstats == True:

        return cspDict

    """
    sudo code from slides (only performs DFS until finds a solution, not all solutions):

    if assignment is complete then return assigment
    var <- SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    for each value in ORDER-DOMAIN-VALUE(csp, var, assignment) do
        if value is consistent with assignment then
            add {var = value} to assignmeent
            inferences <- INFERENCE(csp, var, assignment)
            if inferences != failure then
                add inferences to csp
                result <- BACKTRACK(csp, assignment)
                if result != failure then return result
            remove {var = value} from assingment
    return failure
    """

    def backTrackingSearch(self, assignment, solutions, quiet):
        # check if assignment is complete (every node has only one color)
        # also is base case in our recusion
        if len(assignment) >= self.nvertices:
            if not quiet:
                print("found new possible solution: ", assignment)

            # need to do .copy() to avoid changing solutions when changing assignment later
            solutions.append(assignment.copy())
            return

        # get a node that has not been explored yet 
        var = len(assignment)
        
        # for each possible color...
        for col in self.domains[var]:
            # check if color is valid
            if self.valueConsistent(var, col, assignment):

                # since color is valid, add to assignment
                assignment.append(col)

                # recursive call
                self.backTrackingSearch(assignment, solutions, quiet)

                # remove color and continue searching
                assignment.pop(var)
        return

    def valueConsistent(self, node, col, assignment):
        """
        helper function for backTrackingSearch()

        checks if no adjacent node has the same color
        """
        for i in self.graph.get(node):
            if (i < node) and (col == assignment[i]):
                return False
        return True

def load_graph_file(fname):
    with open(fname, 'rt') as fin:
        graphstr = fin.read()
        return graphstr


def parse_graph_str(graphstr):
    lines = graphstr.splitlines()
    nv = int(lines[0].strip())
    graph = {i: {} for i in range(nv)}
    for line in lines[1:]:
        (v, e) = line.split(';')
        v = int(v.strip())
        e = [int(_) for _ in e.split()]
        graph[v] = e
    return graph


def parse_domains(domainstr):
    domains = {}
    for line in domainstr.splitlines():
        v, d = line.split(':')
        domains[int(v.strip())] = set(d.strip())
    return domains


if __name__ == "__main__":
    #
    # count the number of solutions to a simple problem:
    # when the graph in the file 'graph.g' is :
    # 4
    # 0; 1 2
    # 1; 0 2 3
    # 2; 0 1 3
    # 3; 1 2
    #
    # and each node is given 3 colors:
    # output (count=True) is (note that your Solution may be different!):
    #
    # Done in : 0.0005519390106201172
    # {'Solutions': [['B', 'G', 'R', 'B']], 'SolutionCount': 6}

    import time

    graph = parse_graph_str(load_graph_file('graph.g'))

    def makedomains(ncolors, graph):
        """Return map from vertex id -> set of color codes"""
        colors = 'RGBCMYKOPASDF'
        if ncolors > len(colors):
            print("That's too many colors ;)")
            return None
        return {k: set(colors[:ncolors]) for k in graph}

    domains = makedomains(3, graph)
    mycsp = CSP(graph, domains)

    start = time.time()
    r = mycsp.solve(count=True, quiet=True)
    stop = time.time()

    print("Done in :", (stop-start))

    print(r)

